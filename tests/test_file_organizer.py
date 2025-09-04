import tempfile
import unittest
from pathlib import Path

from photo_organizer.file_handler import FileHandler
from photo_organizer.file_organizer import FileOrganizer


class TestFileOrganizer(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = Path(self.temp_dir)

        self.test_files = [
            self.base_path / "foto.jpg",
            self.base_path / "video.mp4",
            self.base_path / "documento.txt",
            self.base_path / "planilha.xlsx",
        ]

        for file_path in self.test_files:
            file_path.touch()

    def test_organize_files_creates_necessary_folders(self):
        files = [FileHandler(path) for path in self.test_files]
        organizer = FileOrganizer(self.base_path)

        organizer.organize_files(files)

        self.assertTrue((self.base_path / "Videos").exists())
        self.assertTrue((self.base_path / "Textos").exists())
        self.assertTrue((self.base_path / "Outros").exists())

        self.assertFalse((self.base_path / "Imagens").exists())

    def test_organize_files_moves_correct_files(self):
        files = [FileHandler(path) for path in self.test_files]
        organizer = FileOrganizer(self.base_path)

        moved_files = organizer.organize_files(files)

        self.assertTrue((self.base_path / "Videos" / "video.mp4").exists())
        self.assertTrue((self.base_path / "Textos" / "documento.txt").exists())
        self.assertTrue((self.base_path / "Outros" / "planilha.xlsx").exists())

        self.assertTrue((self.base_path / "foto.jpg").exists())

        self.assertEqual(moved_files["Vídeo"], 1)
        self.assertEqual(moved_files["Texto"], 1)
        self.assertEqual(moved_files["Outro"], 1)

    def test_organize_files_with_only_images(self):
        for file_path in self.test_files[1:]:
            file_path.unlink()

        files = [FileHandler(self.test_files[0])]  # Apenas foto.jpg
        organizer = FileOrganizer(self.base_path)

        moved_files = organizer.organize_files(files)

        self.assertFalse((self.base_path / "Videos").exists())
        self.assertFalse((self.base_path / "Textos").exists())
        self.assertFalse((self.base_path / "Outros").exists())

        self.assertEqual(len(moved_files), 0)

        self.assertTrue(self.test_files[0].exists())

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    unittest.main()
