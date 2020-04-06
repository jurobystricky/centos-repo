#!/bin/bash

curr_dir=$(readlink -f $(dirname ${0}))

sudo docker build \
    --build-arg http_proxy=$http_proxy \
    --build-arg https_proxy=$https_proxy \
    --build-arg no_proxy=$no_proxy \
    -f mock-build-docker/Dockerfile \
    -t intel-linux-mock-build \
    .
