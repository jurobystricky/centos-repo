#!/bin/bash

curr_dir=$(readlink -f $(dirname ${0}))
top_dir=$curr_dir
repo_dir=$top_dir/repo
build_dir=$top_dir/build
cache_dir=$top_dir/cache
package_category_dirs=(BaseOS AppStream)
package_build=""
mock_docker_image="intel-linux-mock-build"
build_in_docker=1

usage() {
    echo "Usage: $0 <list|build|init-mock> [-r <repo_dir>] [-p package_name]"
    exit 1
}

#
# Command: List all package from repo
# Params: -r <repo path>
#
cmd_list_packages() {
    echo "Repo dir: $repo_dir"
    echo "List all packages:"

    cd $repo_dir

    packages=()
    for i in ${package_category_dirs[@]}; do
        if [ -d $repo_dir/$i ]; then
            folders=$(ls $repo_dir/$i)
            for f in ${folders[@]}; do
                packages+=( $f-\($i\) )
            done
        fi
    done

    for p in ${packages[@]}; do
        echo "  => $p"
    done
}

#
# Command: Build given package
# Params: -p <package Name>
#         -r <repo path>
#
cmd_build_package() {
    mkdir -p $build_dir
    mkdir -p $cache_dir

    if ((build_in_docker)); then
        # check whether docker service installed
        if ! command -v docker >/dev/null 2>&1; then
            echo "Please install docker environment for build"
            exit 1
        fi

        # check whether mock docker image exist
        if [[ "$(sudo docker images -q $mock_docker_image 2> /dev/null)" == "" ]]; then
            echo "Build intel-linux-mock-docker container..."
            cd $top_dir/tools/ && ./build-container.sh
        fi
    else
        distro=$(cat /etc/*-release | grep "CentOS Linux 8")
        if [[ -z $distro ]]; then
            echo "Native build can only be taken on CentOS Linux 8."
            exit 1
        fi
        sudo mkdir -p /opt/cache
        sudo mkdir -p /intel-linux

        if [[ ! -d /intel-linux/repo ]]; then
            sudo ln -s $top_dir/repo /intel-linux/repo
        fi
        if [[ ! -d /intel-linux/build ]]; then
            sudo ln -s $top_dir/build /intel-linux/build
        fi
    fi

    echo "Repo dir: $repo_dir"
    echo "Build Package: $package_build"

    if [ -z $package_build ]; then
        echo "ERROR: Please input correct package name via -p, or explore" \
             "existing packages via \"pkg.sh list\""
        exit 1
    fi

    package_path=""
    for i in ${package_category_dirs[@]}; do 
        if [ -d ${repo_dir}/$i/$package_build ]; then
            package_path=$i/$package_build
            break
        fi
    done

    if [ -z $package_path ]; then
        echo "ERROR: Package $package_build does not exist."
        exit 1
    fi

    if ((build_in_docker)); then
        trap stop_build 1 2 3 6
        sudo docker run \
            --cap-add=SYS_ADMIN \
            -e http_proxy=$http_proxy \
            -e https_proxy=$http_proxy \
            -e PACKAGE=$package_build \
            -v $repo_dir:/intel-linux/repo \
            -v $build_dir:/intel-linux/build \
            -v $cache_dir:/opt/cache \
            $mock_docker_image \
            /usr/bin/mock-build.sh &

        while [ : ]
        do
            sleep 5
            mock_pid=$(pgrep mock-build.sh)
            if [[ -z "$mock_pid" ]]; then
                break
            fi
        done
    else
        export PACKAGE=$package_build
        sudo $top_dir/tools/prepare-local-mock-repo.sh
        sudo cp $top_dir/tools/intel-linux-centos.cfg /etc/mock/
        $top_dir/tools/mock-build.sh
    fi

    echo "Done~"
}

#
# Stop current build when CTRL+C
#
stop_build() {
    mock_pid=$(pgrep mock-build.sh)
    echo -e "\n===> Kill current package build, PID: $mock_pid <==="
    if [ ! -z $mock_pid ]; then
        kill -9 $mock_pid
    fi    
}

parse_cmd() {
    if [ -z $1 ]; then
        usage
    fi

    case $1 in
        list)
            shift
            while getopts ":r:" opt; do
                case $opt in
                    r)
                        repo_dir=$(readlink -f $OPTARG)
                        ;;
                    *)
                        echo "Invalid Options - $opt"
                        usage
                        ;;
                esac
            done
            cmd_list_packages
            ;;
        build)
            distro=$(cat /etc/*-release | grep "CentOS Linux 8")
            if [[ ! -z $distro ]]; then
                echo "Current system is CentOS, so use native build by default"
                build_in_docker=0
            else
                echo "Current system is not CentOS, so use docker build by default"
                build_in_docker=1
            fi

            shift
            while getopts ":rp:nd" opt; do
                case $opt in
                    r)
                        repo_dir=$(readlink -f $OPTARG)
                        ;;
                    p)
                        package_build=$OPTARG
                        ;;
                    n)
                        echo "Force Native build"
                        build_in_docker=0
                        ;;
                    d)
                        echo "Force Docker build"
                        build_in_docker=1
                        ;;
                    *)
                        echo "Invalid Options - $opt"
                        usage
                        ;;
                esac
            done
            cmd_build_package
            ;;
        init-mock-docker)
            $top_dir/tools/build-container.sh
            ;;
        *)
            usage
            ;;
    esac
}

parse_cmd $@
