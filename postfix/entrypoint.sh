#!/bin/bash

echo "user = $DB_USERNAME" >> /etc/postfix/pgsql-aliases.cf
echo "password = $DB_PASSWORD" >> /etc/postfix/pgsql-aliases.cf
echo "hosts = $DB_HOSTS" >> /etc/postfix/pgsql-aliases.cf

echo "mail.$MAILNAME	OK" >> /etc/postfix/virtual_mailbox_domains
postmap /etc/postfix/virtual_mailbox_domains

useradd -r -d /var/spool/filter filter
mkdir /var/spool/filter
chown filter:filter /var/spool/filter
chmod 750 /var/spool/filter

service syslog-ng start
postfix start-fg
