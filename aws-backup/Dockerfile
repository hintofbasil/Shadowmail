FROM cgswong/aws

ENV AWS_ACCESS_KEY_ID ""
ENV AWS_SECRET_ACCESS_KEY ""
ENV AWS_REGION ""

RUN apk update && apk add mysql-client

COPY entrypoint.sh /entrypoint.sh

CMD /entrypoint.sh
