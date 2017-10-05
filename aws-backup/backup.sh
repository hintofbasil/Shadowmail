#!/bin/bash

mysqldump --databases $DB_NAME -h db -u backup -p$DB_PASSWORD \
	| gzip \
	| openssl smime -encrypt -binary -text -aes256 -outform DER /openssl/public.pem \
	| aws s3 cp - s3://$AWS_BUCKET_NAME/$(date "+%Y/%m_%b/%F-%R").gz.enc
