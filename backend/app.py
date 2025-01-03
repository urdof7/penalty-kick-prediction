from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/uploads')

app = Flask(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "flask is running"

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file found"}), 400
    
    # Create the uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Save the file with its original filename, or generate a unique name
    filename = file.filename
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    
    # Return the filename (or a unique ID) so the frontend knows how to access it
    return jsonify({
        "message": "File received successfully",
        "filename": filename
    })

@app.route('/videos/<path:filename>', methods=['GET'])
def serve_video(filename):
    """
    Serves a video file from the uploads folder.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)