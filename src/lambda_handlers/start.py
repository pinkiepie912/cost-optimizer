from ..config import load_from_env
from ..infra_handlers.auto_scalining import AutoScalingGroupHandler
from ..infra_handlers.ec2 import EC2Handler
from ..infra_handlers.rds import RdsHandler
from ..infra_handlers.ecs import ECSHandler


def start_handler(event, context):
    conf = load_from_env()

    auto_scalining_handler = AutoScalingGroupHandler(conf.region)
    ec2_handler = EC2Handler(conf.region)
    rds_handler = RdsHandler(conf.region)
    ecs_handler = ECSHandler(conf.region)

    auto_scalining_handler.change_scale(
        name_tags=conf.autoscaling_name_tags,
        env_tags=conf.autoscaling_env_tags,
        target_cnt=1,
    )
    ec2_handler.start_instances(
        name_tags=conf.ec2_name_tags, env_tags=conf.ec2_env_tags
    )

    rds_handler.start(rds_identifier=conf.rds_identifier)

    for service_arn in conf.ecs_service_arns:
        ecs_handler.change_desired_cnt(
            cluster_arn=conf.ecs_cluster_arn, service_arn=service_arn, cnt=1
        )
