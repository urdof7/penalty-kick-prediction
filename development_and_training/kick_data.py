'''
Descrption: This program inserts new data, which is manually hard coded here, into the kick_data.db.
'''



# Directions:
# 1 - Top left
# 2 - Middle top
# 3 - Top right
# 4 - Bottom left
# 5 - Middle bottom
# 6 - Bottom right


# NOTE: for this program, manually write the following information: video_name, timestamp, direction (quadrant in which the ball is scored);
# every other attributes can be null.



kick_data = [ # video_name, timestamp, direction attributes are required; the rest are not
 { # each entry is a kick
 "video_name": "Argentina_v_France_Full_2022.mp4",
 "timestamp": "00:28",
 "direction": 1,
 "player_name": "Kylian Mbappé",
 "player_team": "France",
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Argentina_v_France_Full_2022.mp4",
 "timestamp": "01:15",
 "direction": 4,
 "player_name": "Lionel Messi",
 "player_team": "Argentina",
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Argentina_v_France_Full_2022.mp4",
 "timestamp": "01:52",
 "direction": 4,
 "player_name": "Kingsley Coman",
 "player_team": "France",
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Argentina_v_France_Full_2022.mp4",
 "timestamp": "02:32",
 "direction": 5,
 "player_name": "Paulo Dybala",
 "player_team": "Argentina",
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Argentina_v_France_Full_2022.mp4",
 "timestamp": "04:15.5",
 "direction": 4,
 "player_name": None,
 "player_team": "Argentina",
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Argentina_v_France_Full_2022.mp4",
 "timestamp": "05:05.5",
 "direction": 2,
 "player_name": None,
 "player_team": "France",
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Argentina_v_France_Full_2022.mp4",
 "timestamp": "05:51.5",
 "direction": 4,
 "player_name": None,
 "player_team": "Argentina",
 "goal_scored": True,
 "num_frames": 10
 },


 #next video

 #next video


 {
 "video_name": "Brazil_v_Croatia_Full_2022.mp4",
 "timestamp": "00:15.4",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Croatia_Full_2022.mp4",
 "timestamp": "01:00.0",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Croatia_Full_2022.mp4",
 "timestamp": "01:51.0",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Croatia_Full_2022.mp4",
 "timestamp": "02:29.8",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Croatia_Full_2022.mp4",
 "timestamp": "03:18.4",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Croatia_Full_2022.mp4",
 "timestamp": "04:01.7",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Croatia_Full_2022.mp4",
 "timestamp": "04:46.4",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },


 #next video

 #next video


 
 {
 "video_name": "Columbia_v_England_Full_2018.mp4",
 "timestamp": "00:54.4",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Columbia_v_England_Full_2018.mp4",
 "timestamp": "01:38.1",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Columbia_v_England_Full_2018.mp4",
 "timestamp": "02:22.0",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Columbia_v_England_Full_2018.mp4",
 "timestamp": "03:02.6",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Columbia_v_England_Full_2018.mp4",
 "timestamp": "03:56.6",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Columbia_v_England_Full_2018.mp4",
 "timestamp": "04:27.6 ",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Columbia_v_England_Full_2018.mp4",
 "timestamp": "05:16.1 ",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Columbia_v_England_Full_2018.mp4",
 "timestamp": "06:13.7 ",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Columbia_v_England_Full_2018.mp4",
 "timestamp": "07:33.5 ",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },


 #next video

 #next video


 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "01:12.08",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "01:45.64",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "02:40.92",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "03:24.84",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "04:18.16",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "05:05.16",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "05:55.68",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "07:04.24",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "07:56.24",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Croatia_v_Denmark_Full_2018.mp4",
 "timestamp": "08:53.32",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

 
 # next video


#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "00:16.20",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "00:41.15",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "01:02.01",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "01:24.19",
#  "direction": 1,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "01:46.18",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "02:03.01",
#  "direction": 3,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "02:24.25",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "02:54.26",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "03:03.23",
#  "direction": 3,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
#  "timestamp": "03:25.24",
#  "direction": 1,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },


 # next video


 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "00:37.11",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "01:22.13",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "02:08.24",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "02:54.11",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "03:38.06",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "04:21.20",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "05:06.23",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "06:05.11",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "07:02.02",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Brazil_v_Chile_WC_2014.mp4",
 "timestamp": "07:52.17",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },


 # next video


#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "00:07.05",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "00:22.06",
#  "direction": 1,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "00:37.15",
#  "direction": 3,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "00:47.00",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "01:00.18",
#  "direction": 2,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "01:12.01",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "01:32.23",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "01:40.10",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "01:44.09",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "01:54.23",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "02:10.15",
#  "direction": 1,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "02:23.07",
#  "direction": 2,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "02:36.08",
#  "direction": 3,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "02:46.09",
#  "direction": 2,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "03:01.17",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "03:09.05",
#  "direction": 1,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "03:24.20",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "03:37.03",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "03:46.10",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "04:13.11",
#  "direction": 3,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "04:26.24",
#  "direction": 5,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "04:41.02",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "04:52.20",
#  "direction": 2,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "05:03.06",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "05:19.08",
#  "direction": 2,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "05:33.09",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "05:42.04",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "05:53.02",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "06:17.05",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "06:38.22",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "06:47.04",
#  "direction": 1,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "07:01.18",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "07:13.08",
#  "direction": 3,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "07:27.16",
#  "direction": 3,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "07:38.04",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "07:52.17",
#  "direction": 4,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "08:22.02",
#  "direction": 6,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": False,
#  "num_frames": 10
#  },
#  {
#  "video_name": "Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
#  "timestamp": "08:48.04",
#  "direction": 3,
#  "player_name": None,
#  "player_team": None,
#  "goal_scored": True,
#  "num_frames": 10
#  },

 # next video

 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "03:33.23",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "03:57.01",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "04:14.23",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "04:28.20",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "04:50.16",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "05:07.02",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "05:32.19",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "06:03.27",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "07:01.08",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "07:22.18",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "07:35.01",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "07:55.29",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "09:05.16",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "09:34.12",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Epic_Penalty_Shootout.mp4",
 "timestamp": "10:06.12",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },

 #next video

 {
 "video_name": "France_v_Italy_Full_2006.mp4",
 "timestamp": "00:25.22",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "France_v_Italy_Full_2006.mp4",
 "timestamp": "02:25.13",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },

 #next video

 {
 "video_name": "Germany_v_Argentina_Full_2006.mp4",
 "timestamp": "02:38.15",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Germany_v_Argentina_Full_2006.mp4",
 "timestamp": "04:38.21",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

 #next video 

 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "00:26.25",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "00:43.28",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "01:01.08",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "01:19.00",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "01:46.05",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "02:05.07",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "02:25.10",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "02:44.17",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "02:57.26",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "03:20.26",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "04:10.05",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "04:36.07",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "04:58.17",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "05:29.27",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "05:58.04",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "06:20.25",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "06:44.15",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "07:43.23",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Heartbreaking_Penalty_Shootout.mp4",
 "timestamp": "08:01.27",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

#  #next video

 {
 "video_name": "Legendary_Penalty_Kicks.mp4",
 "timestamp": "02:06.02",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Legendary_Penalty_Kicks.mp4",
 "timestamp": "03:13.13",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Legendary_Penalty_Kicks.mp4",
 "timestamp": "04:43.00",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Legendary_Penalty_Kicks.mp4",
 "timestamp": "05:50.04",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },

 #next video

 {
 "video_name": "Netherlands_v_Costa_Rica_Full_2014.mp4",
 "timestamp": "01:46.10",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Netherlands_v_Costa_Rica_Full_2014.mp4",
 "timestamp": "03:09.06",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Netherlands_v_Costa_Rica_Full_2014.mp4",
 "timestamp": "04:04.13",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Netherlands_v_Costa_Rica_Full_2014.mp4",
 "timestamp": "05:38.03",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Netherlands_v_Costa_Rica_Full_2014.mp4",
 "timestamp": "06:06.05",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

 #next video

 {
 "video_name": "Paraguay_v_Japan_Full_2010.mp4",
 "timestamp": "01:04.21",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Paraguay_v_Japan_Full_2010.mp4",
 "timestamp": "01:45.11",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Paraguay_v_Japan_Full_2010.mp4",
 "timestamp": "03:16.11",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Paraguay_v_Japan_Full_2010.mp4",
 "timestamp": "04:45.11",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Paraguay_v_Japan_Full_2010.mp4",
 "timestamp": "05:20.02",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },




 #next video

 {
 "video_name": "Portugal_v_Slovenia_Full_2024.mp4",
 "timestamp": "00:06.36",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Portugal_v_Slovenia_Full_2024.mp4",
 "timestamp": "00:56.21",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Portugal_v_Slovenia_Full_2024.mp4",
 "timestamp": "02:44.19",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Portugal_v_Slovenia_Full_2024.mp4",
 "timestamp": "03:19.45",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Portugal_v_Slovenia_Full_2024.mp4",
 "timestamp": "04:11.40",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

#  # next video

 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "01:53.02",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "02:14.26",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "07:45.09",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "08:34.17",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "08:56.16",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "09:15.13",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "09:30.02",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "09:41.08",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "09:57.14",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "10:33.10",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "10:43.01",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "10:58.07",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "11:15.12",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "11:29.19",
 "direction": 5,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Unforgettable_Penalty_Shootout.mp4",
 "timestamp": "12:01.14",
 "direction": 1,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

#  #next video

 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "00:25.06",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "01:12.00",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "01:53.21",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "02:34.11",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "03:20.11",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "04:32.17",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "05:24.27",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "06:18.11",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "07:20.20",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "08:14.27",
 "direction": 3,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "08:58.18",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": False,
 "num_frames": 10
 },
 {
 "video_name": "Venezuela_v_Canada_Entire_2024.mp4",
 "timestamp": "09:53.27",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

# next video


{
 "video_name": "brayden_kicks.mp4",
 "timestamp": "00:46.30",
 "direction": 2,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

 {
 "video_name": "brayden_kicks.mp4",
 "timestamp": "01:00.03",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

{
 "video_name": "brayden_kicks.mp4",
 "timestamp": "01:19.18",
 "direction": 4,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 },

   {
 "video_name": "brayden_kicks.mp4",
 "timestamp": "01:29.24",
 "direction": 6,
 "player_name": None,
 "player_team": None,
 "goal_scored": True,
 "num_frames": 10
 }


]
#  ## END