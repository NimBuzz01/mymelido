import os
from werkzeug.utils import secure_filename
from config import Config
import tempfile

class FileHandler:
    def __init__(self):
        self.config = Config()
        # Create a dedicated temp directory if it doesn't exist
        self.temp_dir = os.path.join(tempfile.gettempdir(), "uploads")
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def is_allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.config.ALLOWED_EXTENSIONS
    
    def save_temp_file(self, file):
        """Save uploaded file to temporary location"""
        if not file or not self.is_allowed_file(file.filename):
            return None
            
        try:
            filename = secure_filename(file.filename)
            temp_path = os.path.join(self.temp_dir, filename)
            
            # Ensure unique filename to prevent collisions
            counter = 1
            while os.path.exists(temp_path):
                name, ext = os.path.splitext(filename)
                temp_path = os.path.join(self.temp_dir, f"{name}_{counter}{ext}")
                counter += 1
                
            file.save(temp_path)
            return temp_path
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    
    def cleanup_file(self, file_path):
        """Remove temporary file"""
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")