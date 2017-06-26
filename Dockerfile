FROM python:2.7
MAINTAINER Anton Iskov <aiskov@jiss-software.com>

ENV SERVICE_DIR /usr/lib/file-service

# Install app
ADD . ${SERVICE_DIR}
WORKDIR ${SERVICE_DIR}

RUN python setup.py install

# Run
CMD python server.py --db_address="mongodb://${MONGO_HOSTS:-localhost}:${MONGO_PORT:-27017}?replicaSet=${MONGO_REPLICA:main}?serverSelectionTimeoutMS=${MONGO_TIMEOUT:-2000}&socketTimeoutMS=${MONGO_TIMEOUT:-2000}&connectTimeoutMS=${MONGO_TIMEOUT:-2000}"
