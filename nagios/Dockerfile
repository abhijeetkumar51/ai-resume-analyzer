FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      apache2 \
      apache2-utils \
      nagios4 \
      nagios4-cgi \
      python3 \
      ruby \
      ca-certificates \
    && gem install puppet --no-document \
    && a2enmod cgi \
    && a2enconf nagios4-cgi \
    && htpasswd -bc /etc/nagios4/htpasswd.users nagiosadmin devops-demo \
    && sed -i 's/^use_authentication=0/use_authentication=1/' /etc/nagios4/cgi.cfg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY puppet/modules/resume_analyzer_monitoring/ /etc/puppetlabs/code/modules/resume_analyzer_monitoring/

EXPOSE 80

CMD ["sleep", "infinity"]
