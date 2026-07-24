# Declare keys outside of build stage, with their values defined in docker-compose.yml
ARG DATA_GROUP
ARG DATA_DIR
ARG APP_DIR
ARG REMOTE_USER
ARG REMOTE_PASS

# Choose one suitable image from Docker Hub and declare it here
FROM python:3.13-slim AS builder
# FROM python:3.13-slim
# FROM pytorch/pytorch:2.9.0-cuda12.6-cudnn9-runtime

# We need sudo and zip so we can work with volume and data for training
RUN apt-get update && apt-get install -y sudo unzip \
    build-essential cmake ninja-build \
    libfftw3-dev libopencv-dev libsuitesparse-dev liblapack-dev libopenblas-dev gfortran

# Declare keys again here after FROM above so they are accessible below (in the container)
ARG DATA_GROUP
ARG DATA_DIR
ARG APP_DIR
ARG REMOTE_USER
ARG REMOTE_PASS

ENV ENV_DATA_DIR=${DATA_DIR}
ENV ENV_APP_DIR=${APP_DIR}

# RUN python3 -m pip install 'ansible-core<2.14' ansible-lint fqdn
COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /tmp/requirements.txt

# Create the REMOTE_USER with bash shell and home dir with password REMOTE_PASS and add to sudo group
# RUN useradd -m -s /bin/bash ${REMOTE_USER}
RUN useradd -p $(openssl passwd -1 ${REMOTE_PASS}) -m -s /bin/bash ${REMOTE_USER}
RUN usermod -aG sudo ${REMOTE_USER}

# Create DATA_GROUP and add REMOTE_USER to it, which is volume group so anyone belongs to this DATA_GROUP can rwx it
RUN groupadd ${DATA_GROUP}
RUN usermod -aG ${DATA_GROUP} ${REMOTE_USER}

# Create DATA_DIR if it does not exist and change its group to DATA_GROUP
# RUN mkdir ${DATA_DIR} && chmod 775 ${DATA_DIR}
# RUN chgrp -R ${DATA_GROUP} ${DATA_DIR}
RUN [ ! -d ${DATA_DIR} ] && mkdir -m=775 -p ${DATA_DIR} && chgrp -R ${DATA_GROUP} ${DATA_DIR}
