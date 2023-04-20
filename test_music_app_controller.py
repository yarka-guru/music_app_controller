import unittest
from unittest.mock import patch
from music_app_controller import MusicAppController, MusicScheduler

class TestMusicAppController(unittest.TestCase):

    def setUp(self):
        self.controller = MusicAppController()

    @patch("subprocess.run")
    def test_pause(self, mock_run):
        self.controller.pause()
        mock_run.assert_called()

    @patch("subprocess.run")
    def test_resume(self, mock_run):
        self.controller.resume()
        mock_run.assert_called()

    @patch("subprocess.run")
    def test_play_stop_music(self, mock_run):
        self.controller.play("stop_music")
        mock_run.assert_called()

class TestMusicScheduler(unittest.TestCase):

    @patch.object(MusicAppController, "play")
    def setUp(self, mock_play):
        self.mock_play = mock_play
        self.scheduler = MusicScheduler(MusicAppController())

    def test_set_activities(self):
        activities = [("08:00", "morning_music"), ("12:00", "lunch_music")]
        self.scheduler.set_activities(activities)
        self.assertEqual(self.scheduler.get_activities(), activities)

    def test_get_current_activity(self):
        activities = [("08:00", "morning_music"), ("12:00", "lunch_music")]
        self.scheduler.set_activities(activities)
        self.scheduler.current_activity = "morning_music"
        self.assertEqual(self.scheduler.get_current_activity(), "morning_music")

if __name__ == "__main__":
    unittest.main()
