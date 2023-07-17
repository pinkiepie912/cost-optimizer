from __future__ import annotations

import boto3

__all__ = ["ECSHandler"]


class ECSHandler:
    def __init__(self, region: str):
        self._client = boto3.client("ecs", region_name=region)

    def change_desired_cnt(self, cluster_arn: str, service_arn: str, cnt: int) -> None:
        self._client.update_service(
            cluster=cluster_arn, service=service_arn, desiredCount=cnt
        )
