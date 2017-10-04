#!/bin/bash

echo -e "[default]\n\
aws_access_key_id = $AWS_ACCESS_KEY_ID\n\
aws_secret_access_key = $AWS_SECRET_ACCESS_KEY" > /root/.aws/credentials

echo -e "[default]\n\
region = $AWS_REGION" > /root/.aws/config

crond -f
