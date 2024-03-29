from pydantic import BaseModel, Field
from models.base_models import APIResponse
from config import ConfigClass

### FiledataMeta ###


class FiledataMetaPOST(BaseModel):
    uploader: str
    file_name: str
    path: str
    file_size: int
    description: str
    namespace: str
    labels: list
    project_code: str
    dcm_id: str = ""
    process_pipeline: str = ""
    operator: str = ""
    parent_query: dict = {}
    parent_folder_geid: str = ""
    original_geid: str = None
    # Minio attribute
    bucket: str = ""
    minio_object_path: str = ""
    version_id: str = ""


class FiledataMetaPOSTResponse(APIResponse):
    result: dict = Field({}, example={
        'archived': False,
        'file_size': 1024,
        'full_path': '/data/storage/dcm/raw/BCD-1234_file_2.aacn',
        'dcm_id': 'BCD-1234_2',
        'guid': '5321880a-1a41-4bc8-a5d5-9767323205792',
        'id': 478,
        'labels': [ConfigClass.CORE_ZONE_LABEL, 'File', 'Processed'],
        'name': 'BCD-1234_file_2.aacn',
        'namespace': 'core',
        'path': '/data/storage/dcm/raw',
        'process_pipeline': 'greg_testing',
        'time_created': '2021-01-06T18:02:55',
        'time_lastmodified': '2021-01-06T18:02:55',
        'type': 'processed',
        'uploader': 'admin',
        'operator': 'admin'
    }
    )
