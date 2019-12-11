FROM ubuntu

EXPOSE 25/tcp 465/tcp 587/tcp

VOLUME /var/log/postfix
VOLUME /var/spool/postfix
VOLUME /ssl

# Ignore apt-get prompts
ENV  DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install --yes postfix postfix-pgsql
RUN echo "mail.shadowmail.co.uk" > /etc/mailname
RUN apt-get install -y syslog-ng

COPY ./etc /etc

COPY ./entrypoint.sh /entrypoint.sh

CMD /entrypoint.sh
