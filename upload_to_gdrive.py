from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def upload_csv_to_drive(folder_id):
    # Authenticate using the service account config file
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
            gfile = drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})
            gfile.SetContentFile(file_path)
            gfile.Upload()
            print(f"Uploaded: {filename}")

if __name__ == "__main__":
    folder_id = os.environ.get('FOLDER_ID')
    if not folder_id:
        print("Error: FOLDER_ID environment variable is not set.")
    else:
        upload_csv_to_drive(folder_id)
