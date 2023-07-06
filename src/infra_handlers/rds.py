from __future__ import annotations

import boto3

__all__ = ["RdsHandler"]


class RdsHandler:
    def __init__(self, region: str):
        self._client = boto3.client("rds", region_name=region)

    def start(self, rds_identifier: str) -> None:
        self._client.start_db_instance(DBInstanceIdentifier=rds_identifier)

    def stop(self, rds_identifier: str) -> None:
        self._client.stop_db_instance(DBInstanceIdentifier=rds_identifier)
