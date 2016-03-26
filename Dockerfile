FROM jiss/python2
MAINTAINER Anton Iskov <aiskov@jiss-software.com>

ENV SERVICE_DIR /usr/lib/file-service

# Install app
ADD . ${SERVICE_DIR}
WORKDIR ${SERVICE_DIR}

RUN python setup.py install

# Run
EXPOSE 33005

ENV SHELL /bin/bash

ENTRYPOINT ["python", "server.py"]
CMD []
