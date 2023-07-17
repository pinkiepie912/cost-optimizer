#!/bin/bash

# For local

export ROLE=
export ECR_URL=
export REPO=
export TAG=
export ECR_URI=${ECR_URL}/${REPO}:${TAG}
export SUBNET_GROUP_ID=
export SUBNET_ID=

export AUTOSCALING_ENV_TAGS=
export AUTOSCALING_NAME_TAGS=
export EC2_NAME_TAGS=
export EC2_ENV_TAGS=
export RDS_IDENTIFIER=
export ECS_CLUSTER_ARN=
export ECS_SERVICE_ARNS=

# Build image
docker build -t ${REPO}:${TAG} .

# Login to ECR
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin ${ECR_URL} 

# Tag
docker tag ${REPO}:${TAG} ${ECR_URI}

# Push to ECR
docker push ${ECR_URI}

# Deploy lambda
sls deploy
