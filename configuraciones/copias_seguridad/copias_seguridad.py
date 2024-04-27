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
APPLICATIONS = ['filebrowser', 'jenkins', 'bitwarden']


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
        key_file_path = 'key_account_service.json'
        # key_file_path = '/home/proyectos/config-servidores/configuraciones/copias_seguridad/key_account_service.json'
        creds = service_account.Credentials.from_service_account_file(
            filename=key_file_path,
            scopes=SCOPES)
        return creds

    def list_files(self, query, pageSize=100):
        """List files in Google Drive"""
        try:
            results = self.service.files().list(
                pageSize=pageSize, fields="nextPageToken, files(id, name)",
                q=query).execute()
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
        folder_id = ""
        query = "mimeType = 'application/vnd.google-apps.folder'"
        items = drive_api.list_files(query)
        for item in items:
            if item['name'] == 'copias_seguridad':
                folder_id = item['id']
                print(u'{0} ({1})'.format(item['name'], item['id']))
        return folder_id

    def download_backup(self, volume_name):

        self.keep_last_five()
        folder_id = drive_api.devuelve_id_folder()
        print("Listing files...")
        query = "'" + folder_id + "' in parents"
        # query = ""
        items = drive_api.list_files(query)
        if not items:
            print('No files found.')
        else:
            matches = [i for i in items if volume_name in i['name']]
            print('Backups de ' + volume_name + ':')
            for m in matches:
                print(u'{0} ({1})'.format(m['name'], m['id']))

        # Download a file
        print("Descargando Backup de " + volume_name)
        path_to_download = "/tmp/" + volume_name + "_volume.tar.gz"
        try:
            os.remove(path_to_download)
        except OSError:
            pass
        success = drive_api.download_file(matches[0]['id'], path_to_download)
        if success:
            print("Descargado correctamente")
        else:
            print("Fallo al descargar el backup")

    def backup(self, volume_name):
        if volume_name == "jenkins":
            path = "/home/jenkins/jenkins_compose/jenkins_configuration"
        elif volume_name == "filebrowser":
            path = "/home/filebrowser/filebrowser_configuration"
        elif volume_name == "bitwarden":
            path = "/opt/bitwarden"
        else:
            print("Error al elegir el backup. Los valores validos son " + ', '.join(APPLICATIONS))
            return

        date = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')

        file_name = date + "_" + volume_name + ".tar.gz"

        tar = Tar()
        print("Creando copia de " + volume_name)
        tar.tardirectory(path, file_name)

        folder_id = drive_api.devuelve_id_folder()

        print("Subiendo copia de " + volume_name)
        file_metadata = drive_api.upload_file(file_name, file_name, "application/tar+gzip", folder_id)
        print(f"Uploaded file with ID {file_metadata['id']}")

        print("Listing files...")
        query = "'" + folder_id + "' in parents"
        # query = ""
        items = drive_api.list_files(query)
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))

        self.keep_last_five()

    def keep_last_five(self):
        print("Listing files...")
        folder_id = drive_api.devuelve_id_folder()
        query = "'" + folder_id + "' in parents"
        # query = ""
        items = drive_api.list_files(query)
        for a in APPLICATIONS:
            matches = [i for i in items if a in i['name']]
            cont = 0
            for m in matches:
                if cont >= 5:
                    self.delete_file(m['id'])
                    print(u'Eliminado fichero {0} ({1})'.format(m['name'], m['id']))
                cont += 1


class Tar:
    def tardirectory(self, path, name):
        with tarfile.open(name, "w:gz") as tarhandle:
            for root, dirs, files in os.walk(path):
                for f in files:
                    tarhandle.add(os.path.join(root, f))


# Example usage
if __name__ == '__main__':

    parameter, parameter2 = "", ""
    try:
        parameter = sys.argv[1]
        parameter2 = sys.argv[2]
    except:
        pass
    if parameter != "":

        drive_api = GoogleDriveAPI()

        if parameter == "backup":
            drive_api.backup(parameter2)

        elif parameter == "download":
            drive_api.download_backup(parameter2)
        else:
            print("No se ha pasado ninguna variable para ejecutar el script.")
