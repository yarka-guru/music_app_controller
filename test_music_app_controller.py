import datetime
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock, call
from music_app_controller import (
    MusicAppController, MusicScheduler, CONFIG,
    _validate_app_name, _parse_activity_files
)


class TestMusicAppController(unittest.TestCase):

    def setUp(self):
        self.controller = MusicAppController(music_app_name="TestMusic")

    @patch("music_app_controller.MusicAppController._is_running")
    @patch("subprocess.run")
    def test_pause_when_running(self, mock_run, mock_is_running):
        """Test pause calls osascript when app is running"""
        mock_is_running.return_value = True
        self.controller.pause()
        mock_run.assert_called_once_with(
            ["osascript", "-e", 'tell application "TestMusic" to pause'],
            check=True
        )

    @patch("music_app_controller.MusicAppController._is_running")
    @patch("subprocess.run")
    def test_pause_when_not_running(self, mock_run, mock_is_running):
        """Test pause does nothing when app is not running"""
        mock_is_running.return_value = False
        self.controller.pause()
        mock_run.assert_not_called()

    @patch("music_app_controller.MusicAppController._is_running")
    @patch("subprocess.run")
    def test_resume_when_running(self, mock_run, mock_is_running):
        """Test resume calls play when app is running"""
        mock_is_running.return_value = True
        self.controller.resume()
        mock_run.assert_called_once_with(
            ["osascript", "-e", 'tell application "TestMusic" to play'],
            check=True
        )

    @patch("music_app_controller.MusicAppController._is_running")
    @patch("subprocess.run")
    def test_resume_when_not_running(self, mock_run, mock_is_running):
        """Test resume opens app when not running"""
        mock_is_running.return_value = False
        self.controller.resume()
        mock_run.assert_called_once_with(
            ["open", "-a", "TestMusic"],
            check=True
        )

    @patch("music_app_controller.MusicAppController._is_running")
    @patch("subprocess.run")
    def test_play_stop_music(self, mock_run, mock_is_running):
        """Test play with stop_music activity pauses and returns"""
        mock_is_running.return_value = True
        self.controller.play("stop_music")
        mock_run.assert_called_once_with(
            ["osascript", "-e", 'tell application "TestMusic" to pause'],
            check=True
        )

    @patch("subprocess.run")
    def test_is_running_returns_true(self, mock_run):
        """Test _is_running returns True when process exists"""
        mock_run.return_value = MagicMock(returncode=0)
        result = self.controller._is_running()
        self.assertTrue(result)
        mock_run.assert_called_once_with(
            ["pgrep", "-x", "TestMusic"],
            stdout=-1,
            encoding="utf-8",
            check=False
        )

    @patch("subprocess.run")
    def test_is_running_returns_false(self, mock_run):
        """Test _is_running returns False when process doesn't exist"""
        mock_run.return_value = MagicMock(returncode=1)
        result = self.controller._is_running()
        self.assertFalse(result)


class TestMusicScheduler(unittest.TestCase):

    @patch("music_app_controller.MusicScheduler._read_activities")
    def setUp(self, mock_read_activities):
        mock_read_activities.return_value = []
        self.controller = MusicAppController(music_app_name="TestMusic")
        self.scheduler = MusicScheduler(self.controller)

    def test_set_activities(self):
        """Test setting activities with correct datetime format"""
        activities = [
            (datetime.datetime.strptime("08:00", "%H:%M"), "morning_music"),
            (datetime.datetime.strptime("12:00", "%H:%M"), "lunch_music")
        ]
        self.scheduler.set_activities(activities)
        self.assertEqual(self.scheduler.get_activities(), activities)

    def test_get_current_activity(self):
        """Test getting current activity"""
        self.scheduler.current_activity = "morning_music"
        self.assertEqual(self.scheduler.get_current_activity(), "morning_music")

    def test_get_current_activity_empty(self):
        """Test current activity is empty initially"""
        self.assertEqual(self.scheduler.get_current_activity(), "")


class TestMusicSchedulerReadActivities(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.controller = MusicAppController(music_app_name="TestMusic")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch.object(MusicScheduler, "_get_filename")
    def test_read_activities_valid_file(self, mock_get_filename):
        """Test reading activities from a valid schedule file"""
        schedule_file = os.path.join(self.temp_dir, "test_schedule.txt")
        with open(schedule_file, "w") as f:
            f.write("08:00 - morning_music\n")
            f.write("12:00 - lunch_music\n")
            f.write("18:00 - evening_music\n")

        mock_get_filename.return_value = schedule_file
        scheduler = MusicScheduler(self.controller, schedule_dir=self.temp_dir)

        activities = scheduler.get_activities()
        self.assertEqual(len(activities), 3)
        self.assertEqual(activities[0][0].hour, 8)
        self.assertEqual(activities[0][0].minute, 0)
        self.assertEqual(activities[0][1], "morning_music")
        self.assertEqual(activities[1][1], "lunch_music")
        self.assertEqual(activities[2][1], "evening_music")

    @patch.object(MusicScheduler, "_get_filename")
    def test_read_activities_file_not_found(self, mock_get_filename):
        """Test reading activities when file doesn't exist"""
        mock_get_filename.return_value = "/nonexistent/file.txt"
        scheduler = MusicScheduler(self.controller, schedule_dir=self.temp_dir)
        activities = scheduler.get_activities()
        self.assertEqual(activities, [])

    @patch.object(MusicScheduler, "_get_filename")
    def test_read_activities_invalid_format(self, mock_get_filename):
        """Test reading activities with invalid line format"""
        schedule_file = os.path.join(self.temp_dir, "test_schedule.txt")
        with open(schedule_file, "w") as f:
            f.write("08:00 - valid_activity\n")
            f.write("invalid line without separator\n")
            f.write("12:00 - another_valid\n")

        mock_get_filename.return_value = schedule_file
        scheduler = MusicScheduler(self.controller, schedule_dir=self.temp_dir)

        activities = scheduler.get_activities()
        self.assertEqual(len(activities), 2)


class TestMusicSchedulerGetFilename(unittest.TestCase):

    @patch.object(MusicScheduler, "_read_activities")
    def test_get_filename_valid_weekday(self, mock_read_activities):
        """Test _get_filename returns correct path for valid weekday"""
        mock_read_activities.return_value = []
        controller = MusicAppController(music_app_name="TestMusic")
        scheduler = MusicScheduler(controller, schedule_dir="/test/schedule")

        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.today.return_value.weekday.return_value = 0
            mock_datetime.now = datetime.datetime.now
            mock_datetime.strptime = datetime.datetime.strptime

            filename = scheduler._get_filename()
            self.assertEqual(filename, "/test/schedule/monday.txt")

    @patch.object(MusicScheduler, "_read_activities")
    @patch("music_app_controller.CONFIG", {"ACTIVITY_FILES": {}})
    def test_get_filename_missing_weekday(self, mock_read_activities):
        """Test _get_filename returns empty string for missing weekday"""
        mock_read_activities.return_value = []
        controller = MusicAppController(music_app_name="TestMusic")
        scheduler = MusicScheduler(controller, schedule_dir="/test/schedule")

        filename = scheduler._get_filename()
        self.assertEqual(filename, "")


class TestMusicSchedulerLifecycle(unittest.TestCase):
    """Tests for scheduler start/stop lifecycle"""

    @patch("music_app_controller.MusicScheduler._read_activities")
    def test_scheduler_stop(self, mock_read_activities):
        """Test scheduler stop method sets running to False"""
        mock_read_activities.return_value = []
        controller = MusicAppController(music_app_name="TestMusic")
        scheduler = MusicScheduler(controller)

        scheduler._running = True
        with patch("pync.notify"):
            scheduler.stop()

        self.assertFalse(scheduler._running)

    @patch("music_app_controller.MusicScheduler._read_activities")
    def test_scheduler_initial_state(self, mock_read_activities):
        """Test scheduler starts with _running=False"""
        mock_read_activities.return_value = []
        controller = MusicAppController(music_app_name="TestMusic")
        scheduler = MusicScheduler(controller)

        self.assertFalse(scheduler._running)


class TestMusicAppControllerAudio(unittest.TestCase):
    """Tests for audio playback functionality"""

    def setUp(self):
        self.controller = MusicAppController(music_app_name="TestMusic")

    def test_stop_current_audio_no_process(self):
        """Test _stop_current_audio does nothing when no process running"""
        self.controller._audio_process = None
        self.controller._stop_current_audio()
        self.assertIsNone(self.controller._audio_process)

    def test_stop_current_audio_with_process(self):
        """Test _stop_current_audio terminates running process"""
        mock_process = MagicMock()
        self.controller._audio_process = mock_process

        self.controller._stop_current_audio()

        mock_process.terminate.assert_called_once()
        self.assertIsNone(self.controller._audio_process)

    def test_controller_initializes_audio_state(self):
        """Test controller initializes audio process and thread as None"""
        self.assertIsNone(self.controller._audio_process)
        self.assertIsNone(self.controller._audio_thread)


class TestSecurityValidation(unittest.TestCase):
    """Tests for security validation functions"""

    def test_validate_app_name_valid(self):
        """Test valid app names pass validation"""
        self.assertEqual(_validate_app_name("Music"), "Music")
        self.assertEqual(_validate_app_name("Spotify"), "Spotify")
        self.assertEqual(_validate_app_name("Apple Music"), "Apple Music")
        self.assertEqual(_validate_app_name("VLC-Player"), "VLC-Player")
        self.assertEqual(_validate_app_name("App.Name"), "App.Name")

    def test_validate_app_name_empty(self):
        """Test empty app name returns default"""
        self.assertEqual(_validate_app_name(""), "Music")
        self.assertEqual(_validate_app_name(None), "Music")

    def test_validate_app_name_injection_attempt(self):
        """Test command injection attempts are rejected"""
        with self.assertRaises(ValueError):
            _validate_app_name('Music"; rm -rf /')
        with self.assertRaises(ValueError):
            _validate_app_name("Music' && malicious")
        with self.assertRaises(ValueError):
            _validate_app_name("Music$(whoami)")
        with self.assertRaises(ValueError):
            _validate_app_name("Music`id`")
        with self.assertRaises(ValueError):
            _validate_app_name("Music|cat /etc/passwd")

    @patch("os.getenv")
    def test_parse_activity_files_valid_json(self, mock_getenv):
        """Test valid JSON is parsed correctly"""
        mock_getenv.return_value = '{"0": "monday.txt", "1": "tuesday.txt"}'
        result = _parse_activity_files()
        self.assertEqual(result, {"0": "monday.txt", "1": "tuesday.txt"})

    @patch("os.getenv")
    def test_parse_activity_files_invalid_json(self, mock_getenv):
        """Test invalid JSON returns empty dict"""
        mock_getenv.return_value = "not valid json {"
        result = _parse_activity_files()
        self.assertEqual(result, {})

    @patch("os.getenv")
    def test_parse_activity_files_empty(self, mock_getenv):
        """Test missing env var returns empty dict"""
        mock_getenv.return_value = "{}"
        result = _parse_activity_files()
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
