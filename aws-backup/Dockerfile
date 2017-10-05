FROM cgswong/aws

ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""
ENV AWS_REGION ""
ENV AWS_BUCKET_NAME ""
ENV DB_PASSWORD ""

RUN apk update && apk add mysql-client

COPY entrypoint.sh /entrypoint.sh
COPY backup.sh /backup.sh

CMD /entrypoint.sh
