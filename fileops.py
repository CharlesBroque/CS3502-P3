import os
import shutil
from pathlib import Path

class FileManager:
    # override this
    def update_display():
        pass
    def show_error(self, message, title="Error"):
        print(title + ": " + message + '\n')
    def confirm_dialog(self, string):
        print(string + ' (y for yes)\n')
        reply = input()
        if (reply.startswith('y')): return True
        else: return False

    # actual functions

    def create_file(self, path, content):
        """Create a new file with content"""
        if os.path.exists(path):
            self.show_error("File already exists.")
            return False
        try:
            # opens file, gets file descriptor from OS
            with open(path, 'w') as f:
                f.write(content)
            self.update_display()
            return True
        except PermissionError:
            self.show_error("Permission denied: cannot create file in this directory.")
            return False
        except Exception as e:
            self.show_error(f"Error creating file: {str(e)}")
            return False
        
    def read_file(self, path):
        """Read and return file contents"""
        if not Path.exists(path):
            self.show_error("File not found.")
            return None
        try:
            # OS opens file, allocates file descriptor
            with open(path, 'r') as f:
                # OS checks permissions
                if not os.access(path, os.R_OK): raise PermissionError
                content = f.read()
            # OS closes file descriptor when done
            return content
        except PermissionError:
            self.show_error("Permission denied: cannot read this file.")
            return None
        except Exception as e:
            self.show_error(f"Error reading file: {str(e)}")
            return None
        
    def update_file(self, path, new_content):
        """Update existing file with new content"""
        # check if file is writable
        if not os.access(path, os.W_OK):
            self.show_error("File is read-only.")
            return False
        # similar pattern to create_file...
        try:
            # OS opens file, allocates file descriptor
            with open(path, 'w') as f:
                # permissions are already checked
                f.write(new_content)
            return True
        except Exception as e:
            self.show_error(f"Error writing file: {str(e)}")
            return False

    def delete_file(self, path):
        """Delete a file after confirmation"""
        if self.confirm_dialog(f"Delete {path}?"):
            try:
                # OS unliks file (decrements inode reference count)
                os.remove(path)
                self.update_display()
                return True
            except PermissionError:
                self.show_error("Permission denied: cannot delete this file.")
                return False
            except Exception as e:
                self.show_error(f"Error deleting file: {str(e)}")
                return False
            
    def rename_file(self, path, new_filename):
        if not Path.exists(path):
            self.show_error("No such path.")
            return False
        try:
            new_path = Path.with_stem(path, new_filename)
            Path.rename(path, new_path)
            return True
        except PermissionError:
            self.show_error("Permission denied.")
            return False
        except Exception as e:
            self.show_error(f"Error renaming file: {str(e)}")