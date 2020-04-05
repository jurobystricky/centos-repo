#!/bin/bash

curr_dir=$(readlink -f $(dirname ${0}))

cd $curr_dir
sudo docker build \
    --build-arg http_proxy=$http_proxy \
    --build-arg https_proxy=$https_proxy \
    --build-arg no_proxy=$no_proxy \
    -t intel-linux-mock-build .
