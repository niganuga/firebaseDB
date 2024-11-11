import os
import dropbox

# Retrieve secrets from environment variables
DROPBOX_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
FIREBASE_TOKEN = os.getenv("FIREBASE_TOKEN")

# Check if the secrets are retrieved correctly (for debugging purposes)
if not DROPBOX_TOKEN:
    print("Error: DROPBOX_ACCESS_TOKEN is not set.")
if not FIREBASE_TOKEN:
    print("Error: FIREBASE_TOKEN is not set.")

# Local and Dropbox base paths
LOCAL_BASE_PATH = '/Users/makko/Documents/firebaseDB'
DROPBOX_BASE_PATH = '/Database_Prep'

# Function to upload files and create folders
def upload_to_dropbox(local_path, dropbox_path):
    for root, dirs, files in os.walk(local_path):
        # Create corresponding Dropbox folder
        relative_path = os.path.relpath(root, local_path)
        dropbox_folder_path = os.path.join(dropbox_path, relative_path).replace("\\", "/")

        try:
            dbx.files_create_folder_v2(dropbox_folder_path)
            print(f"Created folder: {dropbox_folder_path}")
        except dropbox.exceptions.ApiError as e:
            if "conflict" in str(e):
                print(f"Folder already exists: {dropbox_folder_path}")
            else:
                print(f"Error creating folder {dropbox_folder_path}: {e}")

        # Upload files in the current directory
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            dropbox_file_path = os.path.join(dropbox_folder_path, file_name).replace("\\", "/")

            with open(local_file_path, "rb") as f:
                try:
                    dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))
                    print(f"Uploaded file: {dropbox_file_path}")
                except Exception as e:
                    print(f"Error uploading file {dropbox_file_path}: {e}")

# Run the sync process
if __name__ == "__main__":
    upload_to_dropbox(LOCAL_BASE_PATH, DROPBOX_BASE_PATH)
    print("Sync to Dropbox completed successfully!")