from fastapi import APIRouter
from fastapi_utils.cbv import cbv
from models.project_creation_models import ProjectCreatePost, ProjectCreateResponse
from commons.logger_services.logger_factory_service import SrvLoggerFactory
from resources.error_handler import catch_internal
from models.base_models import EAPIResponseCode
import json
from minio.versioningconfig import VersioningConfig, ENABLED
from minio.sseconfig import Rule, SSEConfig
from resources.minio import Minio_Client

router = APIRouter()
_API_TAG = 'project'
_API_NAMESPACE = "api_project_create"


@cbv(router)
class ProjectCreate:

    def __init__(self):
        self._logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()

    @router.post("/projects", tags=[_API_TAG],
                 response_model=ProjectCreateResponse,
                 summary="Create new project via MinIO")
    @catch_internal(_API_NAMESPACE)
    async def project_create(self, request: ProjectCreatePost):
        '''
        Create new greenroom or core project through MinIO bucket creation
        '''
        self._logger.info("API create_project".center(80, '-'))
        api_response = ProjectCreateResponse()

        try:
            # establish minio bucket prefix (gr- or core-) based on zone parameter in payload
            req = request.json()
            payload = json.loads(req)

            # establish bucket name
            bucket_name = payload["zone"] + payload["project_code"]

            # initialize minio client
            mc = Minio_Client()

            # if project/bucket name does not already exist, create it in minio
            if not mc.client.bucket_exists(bucket_name):
                mc.client.make_bucket(bucket_name)
                mc.client.set_bucket_versioning(bucket_name, VersioningConfig(ENABLED))
                mc.client.set_bucket_encryption(
                    bucket_name, SSEConfig(Rule.new_sse_s3_rule()),
                )
            else:
                raise ValueError("Project already exists")

            response_info = {"project_code": bucket_name}
            self._logger.info(f"Project created: {response_info}: Status code: {EAPIResponseCode.success}")
            api_response.result = response_info
            api_response.error_msg = ""
            api_response.code = EAPIResponseCode.success
            return api_response.json_response()
        except Exception as e:
            api_response.result = []
            error_msg = str(e)
            error = f"Cannot create new project: {error_msg}"
            api_response.error_msg = error
            self._logger.error(error)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
