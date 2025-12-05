import unittest
from src.player import VideoPlayer

class TestVideoPlayer(unittest.TestCase):

    def setUp(self):
        self.player = VideoPlayer()

    def test_play(self):
        self.player.play()
        self.assertTrue(self.player.is_playing)

    def test_pause(self):
        self.player.play()
        self.player.pause()
        self.assertFalse(self.player.is_playing)

    def test_stop(self):
        self.player.play()
        self.player.stop()
        self.assertFalse(self.player.is_playing)

    def test_set_volume(self):
        self.player.set_volume(50)
        self.assertEqual(self.player.volume, 50)

    def test_set_volume_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.player.set_volume(150)
        with self.assertRaises(ValueError):
            self.player.set_volume(-10)

if __name__ == '__main__':
    unittest.main()