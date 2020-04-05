#!/bin/bash

curr_dir=$(readlink -f $(dirname ${0}))
top_dir=$curr_dir
repo_dir=$top_dir/repo
build_dir=$top_dir/build
cache_dir=$top_dir/cache
package_category_dirs=(BaseOS AppStream)
package_build=""
mock_docker_image="intel-linux-mock-build"

usage() {
    echo "Usage: $0 <list|build> [-r <repo_dir>] [-p package_name]"
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
            folders+=$(ls $repo_dir/$i)
            for f in ${folders[@]}; do
                packages+=($f-\($i\))
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
    # check whether docker service installed
    if ! command -v docker >/dev/null 2>&1; then
        echo "Please install docker environment for build"
        exit 1
    fi

    # check whether mock docker image exist
    if [[ "$(docker images -q $mock_docker_image 2> /dev/null)" == "" ]]; then
        echo "Build intel-linux-mock-docker container..."
        cd $top_dir/tools/mock-build-docker && ./build-container.sh
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

    mkdir -p $build_dir
    mkdir -p $cache_dir
    sudo docker run \
        --cap-add=SYS_ADMIN \
        -e http_proxy=$http_proxy \
        -e https_proxy=$http_proxy \
        -e PACKAGE=$package_build \
        -v $repo_dir:/repo \
        -v $build_dir:/build \
        -v $cache_dir:/opt/cache \
        $mock_docker_image \
        /usr/bin/mock-build.sh &

    while [ : ]
    do
        sleep 1
        mock_pid=$(pgrep mock-build.sh)
        if [ -z $mock_pid ]; then
            break
        fi
    done
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
            shift
            while getopts ":rp:" opt; do
                case $opt in
                    r)
                        repo_dir=$(readlink -f $OPTARG)
                        ;;
                    p)
                        package_build=$OPTARG
                        ;;
                    *)
                        echo "Invalid Options - $opt"
                        usage
                        ;;
                esac
            done
            cmd_build_package
            ;;
        *)
            usage
            ;;
    esac
}

trap stop_build 1 2 3 6
parse_cmd $@