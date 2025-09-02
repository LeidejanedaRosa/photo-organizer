from .duplicate_manager import DuplicateManager
from .file_renamer import FilenameGenerator
from .image_analyzer import ImageAnalyzer


class ImageProcessor:

    def __init__(self):
        self.analyzer = ImageAnalyzer()
        self.duplicate_manager = DuplicateManager()
        self.filename_generator = FilenameGenerator()

    def calculate_image_hash(self, image_path):

        return self.analyzer._calculate_image_hash(image_path)

    def is_duplicate_image(self, hash1, hash2):

        return hash1 == hash2

    def generate_new_filename(self, base_name, extension):

        import os

        counter = 1
        new_name = f"{base_name}{extension}"

        while os.path.exists(new_name):
            counter += 1
            new_name = f"{base_name}_{counter}{extension}"

        return new_name
