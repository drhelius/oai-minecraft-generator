from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

class BlobStorageClient:
    def __init__(self, container_name):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = container_name
        
        # Ensure container exists
        container_client = self.blob_service_client.get_container_client(self.container_name)
        if not container_client.exists():
            container_client.create_container()

    def upload_file(self, local_file_path, blob_name=None):
        try:
            blob_name = blob_name or os.path.basename(local_file_path)
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
                print(f"Uploaded {blob_name} to Azure Blob Storage.")
        except Exception as e:
            print(f"Failed to upload {local_file_path} to Azure Blob Storage: {e}")
            raise e
    
    def upload_bytes(self, bytes_data, blob_name):
        """Upload bytes directly to blob storage without local file."""
        try:
            blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
            # Reset pointer to start of stream
            bytes_data.seek(0)
            blob_client.upload_blob(bytes_data, overwrite=True)
            print(f"Uploaded {blob_name} to Azure Blob Storage.")
        except Exception as e:
            print(f"Failed to upload bytes to Azure Blob Storage: {e}")
            raise e

    def download_file(self, blob_name, download_file_path):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
        with open(download_file_path, "wb") as file:
            download_stream = blob_client.download_blob()
            file.write(download_stream.readall())
            print(f"Downloaded {blob_name} to {download_file_path}.")

    def get_blob_url(self, blob_name):
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
        return blob_client.url
