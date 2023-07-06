from __future__ import annotations

import os

from dataclasses import dataclass
from typing import Dict, List

from dotenv import load_dotenv

__all__ = ["Config", "load_from_env"]

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

    region: str

    @classmethod
    def of(cls, params: Dict) -> Config:
        return cls(
            autoscaling_env_tags=params["AUTOSCALING_ENV_TAGS"].split(","),
            autoscaling_name_tags=params["AUTOSCALING_NAME_TAGS"].split(","),
            ec2_name_tags=params["EC2_NAME_TAGS"].split(","),
            ec2_env_tags=params["EC2_ENV_TAGS"].split(","),
            rds_identifier=params["RDS_IDENTIFIER"],
            region=params["REGION"],
        )


def load_from_env() -> Config:
    return Config.of({k: v for k, v in os.environ.items()})
