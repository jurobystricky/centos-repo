#!/bin/bash

curr_dir=$(readlink -f $(dirname ${0}))

cd $curr_dir
sudo docker build \
    --no-cache \
    --build-arg http_proxy=$http_proxy \
    --build-arg https_proxy=$https_proxy \
    --build-arg no_proxy=$no_proxy \
    -f $curr_dir/mock-build-docker/Dockerfile \
    -t intel-linux-mock-build \
    .
