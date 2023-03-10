Introduction
------------

The Music App Controller for Mac OS is a Python script that allows users to control their music app from the command line. This project is open-source and aims to provide a simple way to schedule and play music based on a list of activities.

Features
--------

* Pause and resume the music app
* Play music for specific activities
* Schedule activities for specific times of the day
* Notifications for when music starts and stops

Installation
------------

1. Install Python 3 if it's not already installed on your system.
2. Clone the repository from GitHub: `git clone https://github.com/yarka-guru/music_app_controller.git`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Set up environment variables by creating a `.env` file and adding the following variables:

```makefile
MUSIC_APP_NAME=Music
MUSIC_DIR=/path/to/dir/with/music
SCHEDULE_DIR=/path/to/dir/with/schedule
LOG_FILE=/path/to/dir/with/logs/music_app_controller.log
VOLUME=100%
ACTIVITY_FILES='{"0": "monday.txt", "1": "tuesday.txt", "2": "wednesday.txt", "3": "thursday.txt", "4": "friday.txt", "5": "saturday.txt", "6": "sunday.txt"}'
LANGUAGES=en,de,es,fr
```

Usage
-----

### Pause and resume music

To pause the music, run the following command:

```css
python music_app_controller.py pause
```

To resume the music, run the following command:

```lua
python music_app_controller.py resume
```

### Play music for an activity

To play music for a specific activity, run the following command:

`python music_app_controller.py play activity_name`

Replace `activity_name` with the name of the activity you want to play music for. For example:

`python music_app_controller.py play exercise`

### Schedule activities

To schedule activities, create a text file for each day of the week in the `SCHEDULE_DIR` directory. The name of the file should be the name of the day (e.g., `monday.txt`, `tuesday.txt`, etc.).

In each file, add a list of activities in the following format:

```makefile
HH:MM - activity_name
```

Replace `HH:MM` with the time you want the activity to start (in 24-hour format), and `activity_name` with the name of the activity.

For example:

```makefile
09:00 - exercise
12:00 - lunch
15:00 - tea_break
18:00 - dinner
20:00 - relax
22:00 - sleep
```

### Run the music scheduler

To run the music scheduler, run the following command:

`python music_app_controller.py`

This will start the scheduler, and music will be played automatically for the scheduled activities.

# Setting up Autoloader

In order to run the script automatically every time the system starts, you can set up a Launch Agent.

1. Create a new property list file named startup.plist in the ~/Library/LaunchAgents directory using the command nano ~/Library/LaunchAgents/startup.plist
2. Copy the following code and paste it into the startup.plist file:

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.startup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/your/script.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Contributing
------------

We welcome contributions from the community. To contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/your_feature_name`
3. Make your changes and commit them: `git commit -m "Your commit message"`
4. Push your changes to your fork: `git push origin feature/your_feature_name`
5. Submit a pull request to the main repository.

Conclusion
----------

We hope this documentation helps you get started with the Music App Controller for Mac
