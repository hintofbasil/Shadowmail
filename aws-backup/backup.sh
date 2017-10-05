#!/bin/bash

mysqldump --databases $DB_NAME -h db -u backup -p$DB_PASSWORD \
	| gzip \
	| aws s3 cp - s3://$AWS_BUCKET_NAME/$(date "+%Y/%m_%b/%F-%R").gz
