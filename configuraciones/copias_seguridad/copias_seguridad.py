import os.path
import io
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import tarfile
from datetime import datetime
import sys

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveAPI:
    """Google Drive API class"""
    def __init__(self):
        creds = self.get_credentials()
        try:
            self.service = build('drive', 'v3', credentials=creds)
        except Exception as e:
            print(f"Failed to build service: {e}")

    def get_credentials(self):
        """Get user credentials"""
        creds = service_account.Credentials.from_service_account_file(
                        filename='key_account_service.json', 
                        scopes=SCOPES)
        return creds

    def list_files(self, query ,pageSize=10):
        """List files in Google Drive"""
        try:
            results = self.service.files().list(
                pageSize=pageSize, fields="nextPageToken, files(id, name)",
                q=query ).execute()
            items = results.get('files', [])
            return items
        except HttpError as error:
            print(f"An error occurred: {error}")

    def upload_file(self, filename, filepath, mimetype, folder):
        """Upload file to Google Drive"""
        file_metadata = {'name': filename,
                         'parents': [folder]}
        media = MediaFileUpload(filepath, mimetype=mimetype)
        try:
            file = self.service.files().create(body=file_metadata,
                                               media_body=media,
                                               fields='id').execute()
            return file
        except HttpError as error:
            print(f"An error occurred: {error}")

    def download_file(self, file_id, filepath):
        """Download file from Google Drive"""
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(filepath, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        try:
            while done is False:
                status, done = downloader.next_chunk()
            return True if done else False
        except HttpError as error:
            print(f"An error occurred: {error}")

    def delete_file(self, file_id):
        """Delete file from Google Drive"""
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        except HttpError as error:
            print(f"An error occurred: {error}")
    def devuelve_id_folder(self):
        print("Getting id Folders")
        folder_id=""
        query = "mimeType = 'application/vnd.google-apps.folder'"
        items = drive_api.list_files(query)
        for item in items:
            if item['name']=='copias_seguridad':
                folder_id = item['id']
                print(u'{0} ({1})'.format(item['name'], item['id']))
        return folder_id
class Tar:
    def tardirectory(self, path,name):
        with tarfile.open(name, "w:gz") as tarhandle:
            for root, dirs, files in os.walk(path):
                for f in files:
                    tarhandle.add(os.path.join(root, f))
# Example usage
if __name__ == '__main__':

    parameter = sys.argv[1]
    if parameter is not None:

        drive_api = GoogleDriveAPI()

    
        if parameter == "backup":
        
            date = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')

            file_name_jenkins = date+"_jenkins.tar.gz"
            file_name_filebrowser = date+"_filebrowser.tar.gz"

            path_jenkins = "/home/jenkins/jenkins_compose/jenkins_configuration"
            path_filebrowser = "/home/filebrowser/filebrowser_configuration"

            "./config/.filebrowser.json"
            "./database/filebrowser.db:"

            tar = Tar()
            print("Creando copia de Jenkins")
            tar.tardirectory(path_jenkins, file_name_jenkins)
            print("Creando copia de Filebrowser")
            tar.tardirectory(path_filebrowser, file_name_filebrowser)

            folder_id = drive_api.devuelve_id_folder()


            print("Subiendo copia de Jenkins")
            file_metadata = drive_api.upload_file(file_name_jenkins, file_name_jenkins, "application/tar+gzip",folder_id)
            print(f"Uploaded file with ID {file_metadata['id']}")

            print("Subiendo copia de Filebrowser")
            file_metadata = drive_api.upload_file(file_name_filebrowser, file_name_filebrowser, "application/tar+gzip",folder_id)
            print(f"Uploaded file with ID {file_metadata['id']}")



            print("Listing files...")
            query = "'"+folder_id+"' in parents"
            # query = ""
            items = drive_api.list_files(query)
            if not items:
                print('No files found.')
            else:
                print('Files:')
                for item in items:
                    print(u'{0} ({1})'.format(item['name'], item['id']))


        elif parameter == "download_jenkins":

            folder_id = drive_api.devuelve_id_folder()
            print("Listing files...")
            query = "'"+folder_id+"' in parents"
            # query = ""
            items = drive_api.list_files(query)
            if not items:
                print('No files found.')
            else:
                matches = [i for i in items if "jenkins" in i['name']]
                print('Backups de jenkins:')
                for m in matches:
                    print(m)
                    # print(u'{0} ({1})'.format(item['name'], item['id']))


            # # Download a file
            # print("Downloading a file...")
            # success = drive_api.download_file(file_metadata['id'], "/path/to/download/test.txt")
            # if success:
            #     print("File downloaded successfully")
            # else:
            #     print("Failed to download file")

        elif parameter == "download_filebrowser":
            pass
        else:
            print("No se ha pasado ninguna variable para ejecutar el script.")
    # # Download a file
    # print("Downloading a file...")
    # success = drive_api.download_file(file_metadata['id'], "/path/to/download/test.txt")
    # if success:
    #     print("File downloaded successfully")
    # else:
    #     print("Failed to download file")

    # # Delete a file
    # print("Deleting a file...")
    # drive_api.delete_file(file_metadata['id'])
    # print("File deleted")