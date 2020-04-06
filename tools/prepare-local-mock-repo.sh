#!/bin/sh

if [ ! -d /opt/local-mock-repo ]; then
    mkdir -p /opt/local-mock-repo
    cd /opt/local-mock-repo
    wget https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/c/ccache-3.7.7-1.el8.x86_64.rpm
    wget https://download-ib01.fedoraproject.org/pub/epel/8/Everything/x86_64/Packages/k/kmodtool-1-37.el8.noarch.rpm
    createrepo /opt/local-mock-repo
fi

echo -e " \n\
config_opts['cache_topdir'] = '/opt/cache/mock' \n\
config_opts['docker_unshare_warning'] = False \n\
config_opts['plugin_conf']['ccache_enable'] = True \n\
config_opts['plugin_conf']['ccache_opts']['max_cache_size'] = '8G' \n\
config_opts['plugin_conf']['ccache_opts']['compress'] = None \n\
config_opts['plugin_conf']['ccache_opts']['dir'] = '/opt/cache/ccache' " >> /etc/mock/site-defaults.cfg