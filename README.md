Introduction
------------

The Music App Controller for Mac OS is a Python script that allows users to schedule and play music based on a list of activities. This project is open-source and provides automatic music playback control based on daily schedules.

Features
--------

* Pause and resume the music app automatically
* Play music for specific activities based on schedule
* Schedule activities for specific times of the day
* Notifications for when music starts and stops
* Multi-language support for activity audio files

Installation
------------

1. Install Python 3.13+ if it's not already installed on your system.
2. Clone the repository from GitHub: `git clone https://github.com/yarka-guru/music_app_controller.git`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Set up environment variables by creating a `.env` file and adding the following variables:

```bash
MUSIC_APP_NAME=Music
MUSIC_DIR=/path/to/dir/with/music
SCHEDULE_DIR=/path/to/dir/with/schedule
LOG_FILE=/path/to/dir/with/logs/music_app_controller.log
ACTIVITY_FILES='{"0": "monday.txt", "1": "tuesday.txt", "2": "wednesday.txt", "3": "thursday.txt", "4": "friday.txt", "5": "saturday.txt", "6": "sunday.txt"}'
LANGUAGES=en,de,es,fr
```

Usage
-----

### Schedule activities

Create a text file for each day of the week in the `SCHEDULE_DIR` directory. The name of the file should match the configuration in `ACTIVITY_FILES` (e.g., `monday.txt`, `tuesday.txt`, etc.).

In each file, add a list of activities in the following format:

```text
HH:MM - activity_name
```

Replace `HH:MM` with the time you want the activity to start (in 24-hour format), and `activity_name` with the name of the activity.

For example:

```text
09:00 - exercise
12:00 - lunch
15:00 - tea_break
18:00 - dinner
20:00 - relax
22:00 - stop_music
```

Use `stop_music` as the activity name to pause playback at a specific time.

### Music files

Place your music files in the `MUSIC_DIR` directory, organized by language:

```text
music/
├── en/
│   ├── exercise.mp3
│   ├── lunch.mp3
│   └── ...
├── de/
│   ├── exercise.mp3
│   └── ...
└── ...
```

Each activity should have a corresponding `.mp3` file named `{activity_name}.mp3`.

### Run the music scheduler

To run the music scheduler:

```bash
python music_app_controller.py
```

This will start the scheduler, and music will be played automatically for the scheduled activities. The scheduler checks for activities every 30 seconds and reloads schedule files on each iteration.

Setting up Autoloader
---------------------

To run the script automatically every time the system starts, set up a Launch Agent:

1. Create a new property list file:

```bash
nano ~/Library/LaunchAgents/com.music-app-controller.plist
```

2. Add the following configuration:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.music-app-controller</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/music_app_controller.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>/path/to/music_app_controller</string>
</dict>
</plist>
```

3. Load the Launch Agent:

```bash
launchctl load ~/Library/LaunchAgents/com.music-app-controller.plist
```

Contributing
------------

We welcome contributions from the community. To contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/your_feature_name`
3. Make your changes and commit them: `git commit -m "Your commit message"`
4. Push your changes to your fork: `git push origin feature/your_feature_name`
5. Submit a pull request to the main repository.

License
-------

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
