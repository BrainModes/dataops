from fastapi import APIRouter, Header
from fastapi_utils.cbv import cbv
from models.upload_models import StatusUploadResponse
from resources.redis import SrvRedisSingleton
from commons.logger_services.logger_factory_service import SrvLoggerFactory
from resources.error_handler import catch_internal
from models.base_models import EAPIResponseCode

router = APIRouter()
_API_TAG = 'file-operations'
_API_NAMESPACE = "api_delete_file_status"


@cbv(router)
class DeleteFileStatus:

    def __init__(self):
        self._logger = SrvLoggerFactory(_API_NAMESPACE).get_logger()

    @router.delete("/files/upload-state", tags=[_API_TAG],
                   response_model=StatusUploadResponse,
                   summary="Delete file upload status for given session_id")
    @catch_internal(_API_NAMESPACE)
    async def delete_status(self, session_id: str = Header(...)):
        '''
        Delete file upload status based on session_id in Neo4J
        '''
        self._logger.info("API delete_file_upload_status".center(80, '-'))
        api_response = StatusUploadResponse()

        try:
            # initialize redis session
            srv_redis = SrvRedisSingleton()

            # retrieve all keys with respective session_id
            key_results = srv_redis.get_by_prefix(session_id)

            # if no keys are retrieved for session_id
            if not key_results:
                raise Exception("session_id does not exist")

            # delete records by key
            for key in key_results:
                record = key.decode()
                srv_redis.delete_by_key(record)

            response_info = {"session_id": session_id}
            self._logger.info(f"File upload status deleted for: {response_info}: Status code: {EAPIResponseCode.success}")
            api_response.result = response_info
            api_response.error_msg = ""
            api_response.code = EAPIResponseCode.success
            return api_response.json_response()
        except Exception as e:
            api_response.result = []
            error_msg = str(e)
            error = f"Deletion of file upload status failed: {error_msg}"
            api_response.error_msg = error
            self._logger.error(error)
            api_response.code = EAPIResponseCode.internal_error
            return api_response.json_response()
