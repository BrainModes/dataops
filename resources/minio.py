from minio import Minio
from config import ConfigClass


class Minio_Client():
    '''
    Connect to MinIO
    '''
    def __init__(self):
        self.client = Minio(
            ConfigClass.MINIO_ENDPOINT,
            access_key=ConfigClass.MINIO_ACCESS_KEY,
            secret_key=ConfigClass.MINIO_SECRET_KEY,
            secure=ConfigClass.MINIO_HTTPS
        )
