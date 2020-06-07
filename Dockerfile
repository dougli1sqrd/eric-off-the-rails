FROM httpd:latest
COPY ./config/my-httpd.conf /usr/local/apache2/conf/httpd.conf

RUN apt-get update -y
RUN apt-get install -y apt-utils python3.7 python3-pip python3-venv

RUN useradd -ms /bin/bash ericoff
USER ericoff
WORKDIR /home/ericoff

RUN python3.7 -m venv env

USER root
