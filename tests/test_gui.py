import unittest
import tkinter as tk
from src.main import App

class TestApp(unittest.TestCase):
    def setUp(self):
        # Suppress the GUI window from appearing
        self.app = App()
        #self.app.withdraw()  # Hide the main window

    def tearDown(self):
        self.app.destroy()  # Clean up the instance

    def test_title(self):
        self.assertEqual(self.app.title(), "TVDB GUI")

    def test_labels(self):
        self.assertEqual(self.app.widgets['title'].cget('text'), "TVDB Renaming Tool")

    def test_treeview(self):
        self.assertEqual(self.app.widgets['table']['columns'], ('Filename','Location'))

    def test_button(self):
        self.assertEqual(self.app.widgets['select_files'].cget('text'), "Select Files")
        self.assertEqual(str(self.app.widgets["search_by_id"].cget('state')), 'disabled')

    def test_dropdown(self):
        self.assertEqual(self.app.widgets['season_select_menu'].cget('text'), "Select a Season")

    def test_image(self):
        self.assertIn("tvdb_logo", self.app.widgets)

if __name__ == "__main__":
    unittest.main()
