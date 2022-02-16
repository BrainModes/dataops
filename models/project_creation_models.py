from pydantic import Field, validator, constr
from models.base_models import APIResponse, BaseModel


class ProjectCreatePost(BaseModel):
    """
    Project creation class
    """
    project_code: constr(to_lower=True)
    zone: constr(to_lower=True)

    @validator("zone", allow_reuse=True)
    def must_choose_valid_zone(cls, zone):
        valid_zone = ["greenroom", "core"]
        if zone not in valid_zone:
            raise ValueError('Invalid zone selected')
        if zone == "greenroom":
            bucket_prefix = "gr-"
        else:
            bucket_prefix = "core-"
        return bucket_prefix


class ProjectCreateResponse(APIResponse):
    """
    Project creation response class
    """
    result: dict = Field({}, example={
        "code": 200,
        "error_msg": "",
        "result": {"project_code": "gr-testproject"}
    })
