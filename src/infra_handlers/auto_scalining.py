from __future__ import annotations

import boto3
from pprint import pprint

from typing import Dict, List
from dataclasses import dataclass

__all__ = ["AutoScalingGroupHandler"]


@dataclass()
class Tag:
    key: str
    value: str

    @classmethod
    def of(cls, params: Dict) -> Tag:
        return cls(key=params["Key"], value=params["Value"])


@dataclass()
class Groups:
    name: str
    tags: List[Tag]

    @classmethod
    def of(cls, params: Dict) -> Groups:
        return cls(
            name=params["AutoScalingGroupName"],
            tags=[Tag.of(row) for row in params["Tags"]],
        )


@dataclass()
class DescribeRes:
    groups: List[Groups]

    @classmethod
    def of(cls, params: Dict) -> DescribeRes:
        groups = [Groups.of(row) for row in params["AutoScalingGroups"]]
        return cls(groups=groups)


class AutoScalingGroupHandler:
    def __init__(self, region: str):
        self._client = boto3.client("autoscaling", region_name=region)

    def change_scale(
        self, name_tags: List[str], env_tags: List[str], target_cnt: int
    ) -> None:
        groups = self._get_autoscaling_groups(env_tags=env_tags, name_tags=name_tags)
        pprint(groups)

        for group in groups:
            self._client.set_desired_capacity(
                AutoScalingGroupName=group.name,
                DesiredCapacity=target_cnt,
                HonorCooldown=True,
            )

    def _get_autoscaling_groups(
        self, env_tags: List[str], name_tags: List[str]
    ) -> List[Groups]:
        desc_filters = [
            {"Name": "tag:ENV", "Values": env_tags},
            {"Name": "tag:Name", "Values": name_tags},
        ]
        res = self._client.describe_auto_scaling_groups(Filters=desc_filters)
        describe_res = DescribeRes.of(res)

        return describe_res.groups
