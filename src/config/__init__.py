from __future__ import annotations

import os
import json
import boto3

from dataclasses import dataclass
from typing import Dict, List

from dotenv import load_dotenv

try:
    load_dotenv(".env")
except:
    pass


@dataclass()
class Config:
    autoscaling_env_tags: List[str]
    autoscaling_name_tags: List[str]

    ec2_name_tags: List[str]
    ec2_env_tags: List[str]

    rds_identifier: str

    @classmethod
    def of(cls, params: Dict) -> Config:
        return cls(
            autoscaling_env_tags=params["AUTOSCALING_ENV_TAGS"].split(","),
            autoscaling_name_tags=params["AUTOSCALING_NAME_TAGS"].split(","),
            ec2_name_tags=params["EC2_NAME_TAGS"].split(","),
            ec2_env_tags=params["EC2_ENV_TAGS"].split(","),
            rds_identifier=params["RDS_IDENTIFIER"],
        )


def load_from_env(secret_id: str, region: str) -> Config:
    if os.getenv("ENV") == "local":
        return Config.of({k: v for k, v in os.environ.items()})

    _client = boto3.client("secretmanager", region_name=region)
    res = _client.get_secret_value(SecretId=secret_id)
    values = json.loads(res["SecretString"])

    return Config.of(values)
