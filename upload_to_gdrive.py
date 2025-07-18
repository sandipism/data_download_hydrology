from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def upload_csv_to_drive(folder_id):
    print(f"Using folder ID: {folder_id}")

    gauth = GoogleAuth(settings_file='gdrive-config/settings.yaml')
    gauth.ServiceAuth()
    drive = GoogleDrive(gauth)

    data_dir = "data"
    if not os.path.exists(data_dir):
        print(f"Data directory '{data_dir}' does not exist.")
        return

    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(data_dir, filename)
            try:
                print(f"Trying to upload {filename} to folder {folder_id}...")
                gfile = drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})
                gfile.SetContentFile(file_path)
                gfile.Upload()
                print(f"Uploaded {filename} to folder {folder_id}")
            except Exception as e:
                print(f"Upload to folder failed: {e}")
                print(f"Trying to upload {filename} to root folder instead...")
                try:
                    gfile = drive.CreateFile({'title': filename})
                    gfile.SetContentFile(file_path)
                    gfile.Upload()
                    print(f"Uploaded {filename} to root folder successfully")
                except Exception as e2:
                    print(f"Upload to root folder also failed: {e2}")

if __name__ == "__main__":
    folder_id = os.environ.get('FOLDER_ID')
    if not folder_id:
        print("Error: FOLDER_ID environment variable is not set.")
    else:
        upload_csv_to_drive(folder_id)
