FROM python:2.7-stretch

LABEL version="1.0"
LABEL maintainer="Ken Moini <ken@kenmoini.com>"
LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.url="https://github.com/kenmoini/iodineServer"
LABEL org.label-schema.vcs-url="https://github.com/kenmoini/iodineServer"
LABEL org.label-schema.name="kenmoini/iodineServer"

USER root

RUN groupadd -r iodine && useradd --no-log-init -r -g iodine iodine

WORKDIR /opt
RUN git clone https://github.com/kenmoini/iodineServer.git

WORKDIR /opt/iodineServer
RUN ./install.sh

USER iodine

EXPOSE 2082

CMD ["python" "/opt/iodineServer/xmlrpc-server.py -s"]
