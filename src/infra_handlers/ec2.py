from __future__ import annotations

import boto3

from typing import Dict, List
from dataclasses import dataclass

__all__ = ["EC2Handler"]


@dataclass()
class Tag:
    key: str
    value: str

    @classmethod
    def of(cls, params: Dict) -> Tag:
        return cls(key=params["Key"], value=params["Value"])


@dataclass()
class Instance:
    instance_id: str
    tags: List[Tag]

    @classmethod
    def of(cls, params: Dict) -> Instance:
        return cls(
            instance_id=params["InstanceId"],
            tags=[Tag.of(row) for row in params["Tags"]],
        )


@dataclass()
class DescribeRes:
    instances: List[Instance]

    @classmethod
    def of(cls, params: Dict) -> DescribeRes:
        instances = []
        for reservation in params["Reservations"]:
            instances += [Instance.of(row) for row in reservation["Instances"]]
        return cls(instances=instances)


class EC2Handler:
    def __init__(self, region: str):
        self._client = boto3.client("ec2", region_name=region)

    def start_instances(self, name_tags: List[str], env_tags: List[str]) -> None:
        instances = self._get_ec2_instances(env_tags=env_tags, name_tags=name_tags)
        self._client.start_instances(InstanceIds=[row.instance_id for row in instances])

    def stop_instances(self, name_tags: List[str], env_tags: List[str]) -> None:
        instances = self._get_ec2_instances(env_tags=env_tags, name_tags=name_tags)
        self._client.stop_instances(InstanceIds=[row.instance_id for row in instances])

    def _get_ec2_instances(
        self, name_tags: List[str], env_tags: List[str]
    ) -> List[Instance]:
        res = self._client.describe_instances(
            Filters=[
                {"Name": "tag:Name", "Values": name_tags},
                {"Name": "tag:ENV", "Values": env_tags},
            ]
        )

        describe_res = DescribeRes.of(res)
        return describe_res.instances
