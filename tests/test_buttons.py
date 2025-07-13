import unittest
from unittest.mock import MagicMock
import os
import tkinter as tk

from src.main import App


class TestButtons(unittest.TestCase):
    def setUp(self):
        # Suppress the GUI window from appearing
        self.app = App()
        self.app.withdraw()

    def tearDown(self):
        self.app.destroy()  # Clean up the instance

    def test_table_population(self):
        mock_video1 = MagicMock()
        mock_video2 = MagicMock()
        mock_video1.name = 'path/to/video/test1.mp4'
        mock_video2.name = 'path/to/video/test2.mp4'
        videos = [mock_video1, mock_video2]
        self.app.populate_table(videos)
        self.assertEqual(len(self.app.widgets['table'].get_children()), 2)


if __name__ == "__main__":
    unittest.main()
