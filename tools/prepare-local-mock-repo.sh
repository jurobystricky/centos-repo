#!/bin/sh

if [ ! -d /opt/local-mock-repo ]; then
    mkdir -p /opt/local-mock-repo
    cd /opt/local-mock-repo
    wget https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/c/ccache-3.7.7-1.el8.x86_64.rpm
    wget https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
    wget https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-8.noarch.rpm
    wget https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/k/kmodtool-1-37.el8.noarch.rpm
    createrepo /opt/local-mock-repo
fi