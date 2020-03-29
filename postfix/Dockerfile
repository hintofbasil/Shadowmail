FROM ubuntu

EXPOSE 25/tcp 465/tcp 587/tcp

VOLUME /var/spool/postfix
VOLUME /ssl

# Ignore apt-get prompts
ENV  DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install --yes postfix postfix-pgsql syslog-ng
RUN echo "mail.shadowmail.co.uk" > /etc/mailname
COPY ./etc /etc
COPY ./scripts /scripts

COPY ./entrypoint.sh /entrypoint.sh

CMD service syslog-ng enable
CMD /entrypoint.sh
