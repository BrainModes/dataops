import pytest
import json
from models.project_creation_models import ProjectCreatePost
import uuid
from tests.prepare_test import SetUpTest
from tests.logger import Logger

log = Logger(name='test_project.log')
client = SetUpTest(log).create_test_client()

zone_bucket = [
    ({"zone": "core"}, "core-"),
    ({"zone": "greenroom"}, "gr-"),
]


@pytest.mark.parametrize("payload, expected", zone_bucket)
def test_check_bucket_prefix_matched_zone(payload, expected):
    """
    project_creation_models returns "core-" minio bucket prefix for "core" zone or "gr-" for "greenroom".
    """
    model = ProjectCreatePost(project_code="testproject", zone=payload["zone"])
    assert model.zone == expected


def test_check_incorrect_zone_doesnt_return_200_status():
    """
    Incorrect zone provided in payload should trigger pydantic validator.
    """
    payload = {"project_code": "test45z64d5af7", "zone": "other"}
    response = client.post("/v1/projects", json.dumps(payload))
    assert response.status_code != 200


def test_check_bucket_already_exists():
    """
    If bucket already exists, termination should occur and bucket is not created.
    """
    payload = {"project_code": "test123", "zone": "greenroom"}
    response = client.post("/v1/projects", json.dumps(payload))
    assert response.status_code != 200


@pytest.mark.parametrize("payload, prefix", zone_bucket)
def test_check_bucket_successfully_created_in_minio(payload, prefix):
    """
    Check if bucket successfully created in minio with "core-" or "gr-" prefix
    """
    project_name = uuid.uuid4().hex[0:10]
    payload["project_code"] = project_name
    response = client.post("/v1/projects", json.dumps(payload))
    mc = SetUpTest(log).create_minio_client()
    bucket_name = f"{prefix}{project_name}"
    mc.client.remove_bucket(bucket_name)
    assert response.status_code == 200
