'''
Description: This program runs multiple classic supervised ML models on a given the transformed dataset. There is one train/test split of the data per iteration which all models utilize;
every iteration generates a new split. During each cycle, there are metrics being collected for each model individually. When all iterations are completed, such metrics are then averaged and printed.
Moreover, a plot of the most influential input features based on ANOVA F-test is displayed.
Dependencies: numpy, pandas, argparse, matplotlib.pyplot, sklearn.model_selection, sklearn.preprocessing, sklearn.feature_selection, sklearn.metrics, 
sklearn.dummy, sklearn.linear_model, sklearn.svm, sklearn.tree, sklearn.neighbors, sklearn.naive_bayes
'''

import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import (
    confusion_matrix, # grid of T/FP and T/FN
    accuracy_score, # the proportion of correction predictions
    precision_score, # the proportion of correct positive predictions
    recall_score, # the proportion of correctly predicted positive instances/outcomes/observations
    f1_score, # harmonic mean of precision and recall (used to evaluate a model's accuracy)
)

from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

def anova_feature_selection_with_graph(X: pd.DataFrame, y: pd.Series, k: int = 10):
    """
    Selects features using ANOVA F-test, outputs a graph of feature scores, 
    and returns the selected feature matrix and feature labels.

    Arguments:
        X (pd.DataFrame): Input feature dataset.
        y (pd.Series): Target dataset.
        k (int): Number of top features to select.

    Returns:
        tuple: (Selected feature matrix, Selected feature labels)
    """
    # Normalize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform ANOVA F-test
    selector = SelectKBest(score_func=f_classif, k=k)
    X_selected = selector.fit_transform(X_scaled, y)
    selected_features = np.array(X.columns)[selector.get_support()]

    # Prepare data for visualization
    feature_scores = pd.DataFrame({
        'Feature': selected_features,
        'Score': selector.scores_[selector.get_support()]
    }).sort_values(by='Score', ascending=False)

    # Plot the scores of selected features
    plt.figure(figsize=(10, 6))
    plt.barh(feature_scores['Feature'], feature_scores['Score'], color='skyblue')
    plt.xlabel('Score')
    plt.ylabel('Feature')
    plt.title('Feature Scores (ANOVA F-test)')
    plt.gca().invert_yaxis()  # Highest score on top
    plt.show()

    # Return selected feature matrix and feature labels
    return X_selected, selected_features.tolist()

def initialize_features(data: pd.DataFrame) -> tuple[np.ndarray, pd.Series]:
    """
    Initializes features X and y from the dataset.

    Arguments:
        data (pd.DataFrame): Input dataset.

    Returns:
        tuple[np.ndarray, pd.Series]: Feature matrix X and target vector y.
    """
    # drop all unnecessary input features
    X_init = data.drop(columns=['kick_direction', 'frame_id', 'kick_id'])
    X_init = X_init.loc[:, ~X_init.columns.str.contains('visibility_')]
    y = data['kick_direction']

    # Get selected features and reduced feature matrix
    X_selected, selected_features = anova_feature_selection_with_graph(X_init, y, k=30)
    # print(f"Selected Features for Training: {selected_features}")
    return X_selected, y

def aggregate_results(results: pd.DataFrame, models: dict)-> pd.DataFrame:
    '''
    Aggregates the results of each model respectively, thus providing the average of each metric.

    Arguments: 
        results (pd.DataFrame): the results of all models.
        models (dict): dictionary of models to be trained and tested.

    Returns:
        aggregated_results (pd.DataFrame): the aggregated results of each model respectively.
    '''
    aggregated_results = {}
    for model_name in models:
        model_metrics = [res for iteration in results for res in iteration if res["Model"] == model_name[0]]

        # Sum confusion matrices
        total_conf_matrix = np.sum([m["Confusion Matrix"] for m in model_metrics], axis=0)

        # Compute average metrics
        avg_metrics = {
            "Model": model_name[0],
            "Confusion Matrix": total_conf_matrix,
            "Accuracy": round(np.mean([m["Accuracy"] for m in model_metrics]), 3),
            "Precision": round(np.mean([m["Precision"] for m in model_metrics]), 3),
            "Recall": round(np.mean([m["Recall"] for m in model_metrics]), 3),
            "F1 Score": round(np.mean([m["F1 Score"] for m in model_metrics]), 3)
        }

        # Add to aggregated results
        aggregated_results[model_name[0]] = avg_metrics
    return aggregated_results

def run_models(data: pd.DataFrame, models: dict, iterations: int = 100) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Runs models on the dataset and computes metrics.

    Arguments:
        data (pd.DataFrame): Input dataset.
        models (dict): Dictionary of models to train and test.
        iterations (int): Number of iterations.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: Results dataframes.
    """
    X, y = initialize_features(data)
    results = []

    for _ in range(iterations):
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        iteration_results = []
        for name, model in models:
            model.fit(X_train, y_train)
            y_prediction = model.predict(X_test)

            # Metric calculations with multiclass averaging
            conf_matrix = confusion_matrix(y_true=y_test, y_pred=y_prediction)
            accuracy = accuracy_score(y_true=y_test, y_pred=y_prediction)
            precision = precision_score(y_true=y_test, y_pred=y_prediction, average='macro', zero_division=0)
            recall = recall_score(y_true=y_test, y_pred=y_prediction, average='macro', zero_division=0)
            F1 = f1_score(y_true=y_test, y_pred=y_prediction, average='macro', zero_division=0)

            iteration_results.append({
                "Model": name,
                "Confusion Matrix": conf_matrix,
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall": recall,
                "F1 Score": F1
            })

        results.append(iteration_results)

    aggregated_results = aggregate_results(results, models)

    # get results dataframe without confusion matrix per model and results of confusion matrix per model
    results_df = pd.DataFrame([{k: v for k, v in res.items() if k != "Confusion Matrix"} for res in aggregated_results.values()])
    results_conf_matrix = pd.DataFrame([{k: v for k, v in res.items() if k in ["Model", "Confusion Matrix"]} for res in aggregated_results.values()])

    return results_df, results_conf_matrix

def get_data(data_file: str)-> pd.DataFrame:
    '''
    Gets the data from the CSV file given a file location from the CLI. 
    Terminates the program if it fails to read file.

    Arguments: 
        data_file (str): CSV data location.

    Returns: 
        data (pd.DataFrame): data from the CSV file.
    '''
    try:
        return pd.read_csv(data_file)
    except:
        print(f"There was an issue accessing {data_file}")
        exit(0)

def main() -> None:
    # get CLI arguments
    parser = argparse.ArgumentParser(description="Load data from CSV files for ML models.")
    parser.add_argument('--data', required=True, type=str, help="Path to transformed data CSV file.")
    parser.add_argument('--iter', required=False, type=int, help="Number of iterations to run the models.")

    # parse arguments
    args = parser.parse_args()

    # get data
    data = get_data(args.data)
    
    # create dict for models
    models = [
    ("Dummy Classifier", DummyClassifier(strategy="most_frequent")),
    ("Logistic Regression", LogisticRegression(max_iter=1000)),
    ("Support Vector Classifier", SVC()),
    ("Decision Tree", DecisionTreeClassifier()),
    ("K-Nearest Neighbors", KNeighborsClassifier()),
    ("Naive Bayes", GaussianNB())]

    # run models
    iterations = args.iter if args.iter is not None else 100
    results_df, results_conf_matrix = run_models(data, models, iterations) # ignore confusion matrix

    # print average results of all models
    print(f"\nModel performance metrics averages, over {iterations} iterations:")
    print(results_df)

    exit(0)

if __name__ == "__main__":
    main()
