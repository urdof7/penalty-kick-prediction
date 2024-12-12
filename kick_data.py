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
       "video_name": "converted_Argentina v France： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup Final [MCWJNOfJoSM].mp4",
       "timestamp": "00:28",
       "direction": 1,
       "player_name": "Kylian Mbappé",
       "player_team": "France",
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina v France： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup Final [MCWJNOfJoSM].mp4",
       "timestamp": "01:15",
       "direction": 4,
       "player_name": "Lionel Messi",
       "player_team": "Argentina",
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina v France： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup Final [MCWJNOfJoSM].mp4",
       "timestamp": "01:52",
       "direction": 4,
       "player_name": "Kingsley Coman",
       "player_team": "France",
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina v France： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup Final [MCWJNOfJoSM].mp4",
       "timestamp": "02:32",
       "direction": 5,
       "player_name": "Paulo Dybala",
       "player_team": "Argentina",
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina v France： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup Final [MCWJNOfJoSM].mp4",
       "timestamp": "04:15.5",
       "direction": 4,
       "player_name": None,
       "player_team": "Argentina",
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina v France： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup Final [MCWJNOfJoSM].mp4",
       "timestamp": "05:05.5",
       "direction": 2,
       "player_name": None,
       "player_team": "France",
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina v France： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup Final [MCWJNOfJoSM].mp4",
       "timestamp": "05:51.5",
       "direction": 4,
       "player_name": None,
       "player_team": "Argentina",
       "goal_scored": True,
       "num_frames": 10
   },


   #next video


   {
       "video_name": "converted_Brazil v Croatia： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup [uR9vgLLDhE0].mp4",
       "timestamp": "00:15.4",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Brazil v Croatia： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup [uR9vgLLDhE0].mp4",
       "timestamp": "01:00.0",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Brazil v Croatia： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup [uR9vgLLDhE0].mp4",
       "timestamp": "01:51.0",
       "direction": 5,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Brazil v Croatia： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup [uR9vgLLDhE0].mp4",
       "timestamp": "02:29.8",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Brazil v Croatia： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup [uR9vgLLDhE0].mp4",
       "timestamp": "03:18.4",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Brazil v Croatia： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup [uR9vgLLDhE0].mp4",
       "timestamp": "04:01.7",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Brazil v Croatia： Full Penalty Shoot-out ｜ 2022 #FIFAWorldCup [uR9vgLLDhE0].mp4",
       "timestamp": "04:46.4",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },


   #next video


  
    {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "00:54.4",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "01:38.1",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "02:22.0",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "02:22.0",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
        {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "03:02.6",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "03:56.6",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "04:27.6 ",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "05:16.1 ",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "06:13.7  ",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "07:33.5 ",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Colombia v England： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [NtvUzy00DuU].mp4",
       "timestamp": "07:33.5 ",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },


   #next video


   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "01:12.08",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "01:45.64",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "02:40.92",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "03:24.84",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "04:18.16",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "05:05.16",
       "direction": 5,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "05:55.68",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "07:04.24",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "07:56.24",
       "direction": 5,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Croatia v Denmark： Full Penalty Shoot-out ｜ 2018 #FIFAWorldCup Round of 16 [lO36Q8Uj2bE].mp4",
       "timestamp": "08:53.32",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },

    
    # next video


   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "00:16.20",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "00:41.15",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "01:02.01",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "01:24.19",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "01:46.18",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "02:03.01",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "02:24.25",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "02:54.26",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "03:03.23",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Argentina's EPIC penalty shootout with the Netherlands ｜ Every Angle [KoiXYX7tui4].mp4",
       "timestamp": "03:25.24",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },


   # next video


   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "00:37.11",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "01:22.13",
       "direction": 5,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "02:08.24",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "02:54.11",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "03:38.06",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "04:21.20",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "05:06.23",
       "direction": 5,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "06:05.11",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "07:02.02",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_BRAZIL VS CHILE： 2014 FIFA World Cup Penalty Shootout [RE1MtSIXKr0].mp4",
       "timestamp": "07:52.17",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },


   # next video


   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "00:07.05",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "00:22.06",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "00:37.15",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "00:47.00",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "01:00.18",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "01:12.01",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "01:32.23",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "01:40.10",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "01:44.09",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "01:54.23",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "02:10.15",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "02:23.07",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "02:36.08",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "02:46.09",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "03:01.17",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "03:09.05",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "03:24.20",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "03:37.03",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "03:46.10",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "04:13.11",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "04:26.24",
       "direction": 5,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "04:41.02",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "04:52.20",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "05:03.06",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "05:19.08",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "05:33.09",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "05:42.04",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "05:53.02",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "06:17.05",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "06:38.22",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "06:47.04",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "07:01.18",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "07:13.08",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "07:27.16",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "07:38.04",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "07:52.17",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "08:22.02",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Dramatic Penalty Shootout #1 [XvDNH2b3QZQ].mp4",
       "timestamp": "08:48.04",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },

   # next video

   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "00:27.14",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "00:52.24",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "01:35.03",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "02:12.15",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "02:55.20",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "03:32.01",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "04:17.06",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "04:55.25",
       "direction": 5,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "05:39.17",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_England vs. Switzerland Full Penalty Shootout ｜ UEFA Euro 2024 ｜ Quarterfinals [ScjLXWPJfSc].mp4",
       "timestamp": "00:27.14",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },

    # next video

    {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "03:33.23",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "03:57.01",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "04:14.23",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "04:28.20",
       "direction": 5,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "04:50.16",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "05:07.02",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "05:32.19",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "06:03.27",
       "direction": 4,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "07:01.08",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "07:22.18",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "07:35.01",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "07:55.29",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "09:05.16",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "09:34.12",
       "direction": 3,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_Epic Penalty Shootout [LoolI4MQgns].mp4",
       "timestamp": "10:06.12",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },

    #next video

   {
       "video_name": "converted_France v Italy： Full Penalty Shoot-out ｜ 2006 #FIFAWorldCup Final [0Y2Z7vCcLec].mp4",
       "timestamp": "00:25.22",
       "direction": 2,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },
   {
       "video_name": "converted_France v Italy： Full Penalty Shoot-out ｜ 2006 #FIFAWorldCup Final [0Y2Z7vCcLec].mp4",
       "timestamp": "02:25.13",
       "direction": 1,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },

   #next video

   {
       "video_name": "converted_Germany v Argentina： Full Penalty Shoot-out ｜ 2006 FIFA World Cup [AU9yfAXU09k].mp4",
       "timestamp": "02:38.15",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": False,
       "num_frames": 10
   },
   {
       "video_name": "converted_Germany v Argentina： Full Penalty Shoot-out ｜ 2006 FIFA World Cup [AU9yfAXU09k].mp4",
       "timestamp": "04:38.21",
       "direction": 6,
       "player_name": None,
       "player_team": None,
       "goal_scored": True,
       "num_frames": 10
   },

   #next video 

#    {
#        "video_name": "converted_Germany v Argentina： Full Penalty Shoot-out ｜ 2006 FIFA World Cup [AU9yfAXU09k].mp4",
#        "timestamp": "02:38.15",
#        "direction": 6,
#        "player_name": None,
#        "player_team": None,
#        "goal_scored": False,
#        "num_frames": 10
#    },






]





