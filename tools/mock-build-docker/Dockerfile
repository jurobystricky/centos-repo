From centos:8.1.1911

RUN yum -y --setopt="tsflags=nodocs" update
RUN yum -y --setopt="tsflags=nodocs" install epel-release && \
    yum -y --setopt="tsflags=nodocs" install mock rpmdevtools wget
RUN yum clean all && \
	rm -rf /var/cache/yum/

COPY intel-linux-centos.cfg /etc/mock
COPY prepare-local-mock-repo.sh /usr/bin/
COPY mock-build.sh /usr/bin/
COPY logging.ini /etc/mock/

# Prepare mock local repo and configurations. ccache will be used to accelerate
# build speed, but ccache is not provided by CentOS8 or CentOS8 stream repo.
# So the "prepare-local-mock-repo.sh" will download ccache rpm from Fedora repo
# and establish a local mock repo for mock use.
RUN [ "/usr/bin/prepare-local-mock-repo.sh" ]
RUN echo "config_opts['cache_topdir'] = '/opt/cache/mock'" >> /etc/mock/site-defaults.cfg
RUN echo "config_opts['docker_unshare_warning'] = False" >> /etc/mock/site-defaults.cfg
RUN echo "config_opts['plugin_conf']['ccache_enable'] = True " >> /etc/mock/site-defaults.cfg
RUN echo "config_opts['plugin_conf']['ccache_opts']['max_cache_size'] = '8G' " >> /etc/mock/site-defaults.cfg
RUN echo "config_opts['plugin_conf']['ccache_opts']['compress'] = None " >> /etc/mock/site-defaults.cfg
RUN echo "config_opts['plugin_conf']['ccache_opts']['dir'] = '/opt/cache/ccache' " >> /etc/mock/site-defaults.cfg

RUN useradd -u 1000 builder && usermod -a -G mock builder

VOLUME [ "/repo" ]
VOLUME [ "/build" ]
VOLUME [ "/opt/cache" ]

RUN chown -R builder:mock /repo
RUN chown -R builder:mock /build && chmod g+w /build
RUN chown -R builder:mock /opt/cache && chmod g+w /opt/cache

ENV PACKAGE=""

USER builder
ENV HOME /home/builder
