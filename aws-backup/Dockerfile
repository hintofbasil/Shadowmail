FROM cgswong/aws

ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""
ENV AWS_REGION ""
ENV AWS_BUCKET_NAME ""
ENV DB_PASSWORD ""

RUN apk --no-cache add mysql-client openssl

COPY entrypoint.sh /entrypoint.sh
COPY backup.sh /backup.sh

RUN (crontab -u $(whoami) -l; echo "0 1 * * * /backup.sh") \
	| crontab -u $(whoami) -

CMD /entrypoint.sh
