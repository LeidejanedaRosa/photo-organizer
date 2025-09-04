import tempfile
import unittest
from pathlib import Path

from photo_organizer.controller import PhotoOrganizerController
from photo_organizer.models import OrganizationRequest
from photo_organizer.service import PhotoOrganizerService


class TestPhotoOrganizerService(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = Path(self.temp_dir)
        self.service = PhotoOrganizerService()

        self.test_files = [
            self.base_path / "foto.jpg",
            self.base_path / "video.mp4",
            self.base_path / "documento.txt",
            self.base_path / "planilha.xlsx",
        ]

        for file_path in self.test_files:
            file_path.touch()

    def test_analyze_folder_success(self):
        result = self.service.analyze_folder(str(self.base_path))

        self.assertTrue(result.success)
        self.assertEqual(result.total_files, 4)
        self.assertIn("Imagem", result.files_by_type)
        self.assertIn("Vídeo", result.files_by_type)
        self.assertIn("Texto", result.files_by_type)
        self.assertIn("Outro", result.files_by_type)
        self.assertEqual(len(result.errors), 0)

    def test_analyze_nonexistent_folder(self):
        result = self.service.analyze_folder("/pasta/inexistente")

        self.assertFalse(result.success)
        self.assertEqual(result.total_files, 0)
        self.assertGreater(len(result.errors), 0)

    def test_organize_files_without_organize_flag(self):
        request = OrganizationRequest(source_folder=str(self.base_path), organize=False)

        result = self.service.organize_files(request)

        self.assertTrue(result.success)
        self.assertEqual(len(result.moved_files), 0)
        self.assertEqual(len(result.folders_created), 0)

    def test_organize_files_with_organize_flag(self):
        request = OrganizationRequest(source_folder=str(self.base_path), organize=True)

        result = self.service.organize_files(request)

        self.assertTrue(result.success)
        self.assertGreater(len(result.moved_files), 0)
        self.assertGreater(len(result.folders_created), 0)

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir)


class TestPhotoOrganizerController(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.base_path = Path(self.temp_dir)
        self.controller = PhotoOrganizerController()

        test_files = [self.base_path / "foto.jpg", self.base_path / "video.mp4"]

        for file_path in test_files:
            file_path.touch()

    def test_analyze_folder_endpoint(self):
        result = self.controller.analyze_folder_endpoint(str(self.base_path))

        self.assertTrue(result["success"])
        self.assertIn("data", result)
        self.assertIn("total_files", result["data"])
        self.assertIn("files", result["data"])
        self.assertEqual(len(result["errors"]), 0)

    def test_organize_files_endpoint(self):
        result = self.controller.organize_files_endpoint(
            folder_path=str(self.base_path), organize=True
        )

        self.assertTrue(result["success"])
        self.assertIn("data", result)
        self.assertIn("organization_summary", result["data"])

    def test_get_supported_file_types_endpoint(self):
        result = self.controller.get_supported_file_types_endpoint()

        self.assertTrue(result["success"])
        self.assertIn("data", result)
        self.assertIn("image_extensions", result["data"])
        self.assertIn("video_extensions", result["data"])
        self.assertIn("text_extensions", result["data"])
        self.assertIn("folder_mapping", result["data"])

    def tearDown(self):
        import shutil

        shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    unittest.main()
