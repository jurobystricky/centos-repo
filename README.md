# Intel Linux CentOS Repository

This repository includes all Intel optimized packages on CentOS Stream. These optimizes are collected from ClearLinux, OneAPI or other COE projects.

![](doc/intel-repo-arch.png)

## How To Use

### List Packages
```
./pkg2.sh list [-r <repo_dir> ]
```
* `-r <repo_dir>` is optional, by default the repository directory is the "repo" folder under this projects

### Build Packages

#### Prerequisites:

By default, build will be executed in docker environment on non-CentOS 8 OS and will be executed in native environment on CentOS OS.
So on non-CentOS8 OS, please install docker engine.

_NOTE: Since the data folders like `build`, `result` was seperated customizable and stateless, so whole build can be easily deployed on kubernetes based cloud native build framework._

#### Initialize mock build container
```
./pkg.sh init-build-docker
```

_NOTE: On CentOS, you might need install docker as:
```
dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
dnf remove podman
dnf install docker-ce --nobest -y

systemctl enable docker
systemctl start docker

# disable selinux temporary
setenforce 0

# disable selinux permenary, need reboot
sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux
```
#### Build a package
```
./pkg2.sh build -p <package_name> [ -r <repo_dir>] [-n|-d]
```
* `-p <package_name>` Specify the package name for build, please use `./pkg2.sh list` to find the package for build
* `-r <repo_dir>` is optional, by default the repository directory is the "repo" folder under this projects
* `-d` Force build in docker environment
* `-n` Force build in native environment

For example:
```
./pkg2.sh build -p glibc-intel-avx
```

After build,
- Original upstream rpm at `./build/<package_name>`
- Optimized srpm and rpms at `./build/<package_name>/result/`
