from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


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


def load_from_env() -> Config:
    params = {}

    return Config.of(params)
