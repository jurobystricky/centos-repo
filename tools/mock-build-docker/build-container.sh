#!/bin/bash

curr_dir=$(readlink -f $(dirname ${0}))

cd $curr_dir
sudo docker build -t intel-linux-mock-build .