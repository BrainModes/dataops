from pydantic import BaseModel, Field
from models.base_models import APIResponse

class TaskModel(BaseModel):
    key: str = ""
    session_id: str = ""
    task_id: str = ""
    start_timestamp: str = ""
    end_timestamp: str = ""
    frontend_state: str = "uploading"
    state: str = "init"
    progress: float = 0.0
    file_name: str = ""
    project_code: str = ""
    project_id: str = ""

class StatusUploadResponse(APIResponse):
    """
    Delete file upload response class
    """
    result: dict = Field({}, example={
        "code": 200,
        "error_msg": "",
        "result": {"Session id deleted:" "admin-a183jcalt13"}
    })
