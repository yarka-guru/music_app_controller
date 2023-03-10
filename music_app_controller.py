'''Music app controller for Mac OS'''
import datetime
import logging
import os
import subprocess
import time
import json
import pync
from dotenv import load_dotenv

load_dotenv()

MUSIC_DIR = os.getenv("MUSIC_DIR")
SCHEDULE_DIR = os.getenv("SCHEDULE_DIR")
LOG_FILE = os.getenv("LOG_FILE")
MUSIC_APP_NAME = os.getenv("MUSIC_APP_NAME")
VOLUME = os.getenv("VOLUME")
ACTIVITY_FILES = json.loads(os.getenv("ACTIVITY_FILES"))
LANGUAGES = os.environ.get("LANGUAGES", "").split(",")

class MusicAppController:
    """Class for controlling music app on Mac OS"""
    def __init__(self, music_app_name=MUSIC_APP_NAME):
        self.music_app_name = music_app_name

    def pause(self):
        """Pause music app if it is running"""
        if self._is_running():
            subprocess.run(
                ["osascript", "-e", f'tell application "{self.music_app_name}" to pause'],
                check=True,
            )

    def resume(self):
        """Resume music app if it is running, otherwise open it"""
        if self._is_running():
            subprocess.run(
                ["osascript", "-e", f'tell application "{self.music_app_name}" to play'],
                check=True,
            )
        else:
            subprocess.run(["open", "-a", self.music_app_name], check=True)

    def play(self, activity):
        """Play music for activity"""
        if activity == "stop_music":
            self.pause()
            return

        for language in LANGUAGES:
            music_file = os.path.join(MUSIC_DIR, language, f"{activity}.mp3")
            try:
                self.pause()
                subprocess.run(["afplay", music_file], check=True)
            except FileNotFoundError:
                logging.error("Music file not found: %s", music_file)
            if activity != "stop_music":
                self.resume()


    def _is_running(self):
        """Check if the music app is running"""
        check_app = subprocess.run(
            ["pgrep", "-x", self.music_app_name],
            stdout=subprocess.PIPE,
            encoding="utf-8",
            check=False,
        )
        return check_app.returncode == 0


class MusicScheduler:
    """Class for scheduling music"""
    def __init__(self, music_app_controller, schedule_dir=SCHEDULE_DIR):
        self.music_app_controller = music_app_controller
        self.schedule_dir = schedule_dir
        self.activities = self._read_activities()
        self.current_activity = ""

    def run(self):
        """Run the music scheduler"""
        self._setup_logging()
        self._setup_notifications()
        self._run()

    def _setup_logging(self):
        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logging.info("Music app controller started")

    def _setup_notifications(self):
        pync.notify("Music app controller started", title="Music App")

    def _run(self):
        while True:
            now = datetime.datetime.now()
            current_hour, current_minute = now.hour, now.minute

            for activity_time, activity in self.activities:
                if (
                    activity_time.hour == current_hour
                    and activity_time.minute == current_minute
                ):
                    if self.current_activity == "stop_music":
                        self.music_app_controller.pause()
                        logging.info(
                            "Music stopped at %s", activity_time.strftime("%H:%M")
                        )
                        pync.notify("Music stopped", title="Music App")
                    elif self.current_activity != activity:
                        self.current_activity = activity
                        logging.info(
                            "Playing music for activity %s at %s",
                            activity,
                            activity_time.strftime("%H:%M"),
                        )
                        pync.notify(activity, title="Music App")
                        self.music_app_controller.play(activity)

            # Sleep for 30 seconds
            time.sleep(30)

    def _read_activities(self):
        filename = self._get_filename()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            logging.error("Activity list file not found: %s", filename)
            return []

        activities = []
        for line in lines:
            try:
                time_str, activity = line.split(" - ", 1)
                activity_time = datetime.datetime.strptime(time_str, "%H:%M")
                activities.append((activity_time, activity.strip()))
            except ValueError:
                logging.error(
                    "Incorrect format in activity list file: %s", line.strip()
                )

        return activities

    def _get_filename(self):
        activity_files_json = os.getenv("ACTIVITY_FILES")
        activity_files_dict = json.loads(activity_files_json)
        today = datetime.datetime.today()
        filename = activity_files_dict.get(str(today.weekday()))
        return os.path.join(self.schedule_dir, filename)

    def get_current_activity(self):
        '''Get current activity'''
        return self.current_activity

    def get_activities(self):
        '''Get activities'''
        return self.activities

    def set_activities(self, activities):
        '''Set activities'''
        self.activities = activities

def main():
    """Main function"""
    music_app_controller = MusicAppController()
    music_scheduler = MusicScheduler(music_app_controller)
    music_scheduler.run()

if __name__ == "__main__":
    main()
