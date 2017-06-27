FROM python:2.7
MAINTAINER Anton Iskov <aiskov@jiss-software.com>

ENV SERVICE_DIR /usr/lib/file-service

# Install app
ADD . ${SERVICE_DIR}
WORKDIR ${SERVICE_DIR}

RUN python setup.py install

# Run
CMD /bin/bash -c \
    'python server.py \
        --files_dir="/var/file_service" \
        --log_dir="/var/logs" \
        --db_address="mongodb://${MONGO_HOSTS:-localhost:27017}/?replicaSet=${MONGO_REPLICA:main}&serverSelectionTimeoutMS=${MONGO_TIMEOUT:-2000}&socketTimeoutMS=${MONGO_TIMEOUT:-2000}&connectTimeoutMS=${MONGO_TIMEOUT:-2000}"'
