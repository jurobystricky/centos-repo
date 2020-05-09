#!/bin/bash

curr_dir=$(readlink -f $(dirname ${0}))
top_dir=$curr_dir
repo_dir=$top_dir/repo
build_dir=$top_dir/build
rpms_dir=$build_dir/rpms
pkg_build_url="https://github.com/kenplusplus/base-repo-tools.git"
base_repo_tools_dir=$top_dir/base-repo-tools
package_category_dirs=(BaseOS AppStream)
package_build=""
pkg_build_docker="il-pkg-build"
docker_registry="library"
build_in_docker=1
verbose=0

usage() {
    echo "Usage: $0 <list|build|init-build-docker> [-r <repo_dir>] [-p package_name] [-b <build_dir>]"
    exit 1
}

check_cmd() {
    command -v $1 >/dev/null && : || { echo "$1 command not found. please install."; exit 1; }
}

check_pkg_build_tool() {
    if [[ ! -d $curr_dir/base-repo-tools ]]; then
        echo "Does not find the base-repo-tools, download it now"
        check_cmd git
        git clone $pkg_build_url
    fi
}

#
# Command: List all package from repo
# Params: -r <repo path>
#
cmd_list_packages() {
    echo "Repo dir: $repo_dir"
    echo "List all packages:"

    cd $repo_dir
    for i in ${package_category_dirs[@]}; do
        if [ -d $repo_dir/$i ]; then
            folders=$(ls $repo_dir/$i)
            for f in ${folders[@]}; do
                if ((verbose)); then
                    echo -e "  $f \t\t($i)"
                else
                    echo "  $f"
                fi
            done
        fi
    done
}

#
# Command: Build given package
# Params: -p <package Name>
#         -r <repo path>
#
cmd_build_package() {
    mkdir -p $build_dir

    # check whether docker service installed
    check_cmd docker
    # check whether mock docker image exist
    if [[ "$(sudo docker images -q $pkg_build_docker 2> /dev/null)" == "" ]]; then
        cmd_init_build_docker
    fi

    echo "Repo dir          : $repo_dir"
    echo "Build dir         : $build_dir"
    echo "Build Package     : $package_build"

    if [ -z $package_build ]; then
        echo "ERROR: Please input correct package name via -p, or explore" \
             "existing packages via \"pkg.sh list\""
        exit 1
    fi

    # Check whether package exist
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

    #
    # To stop build in docker, press Ctrl + C
    #
    ID=$(sudo docker run \
        -e http_proxy=$http_proxy \
        -e https_proxy=$http_proxy \
        -e PACKAGE=$package_build \
        -v $repo_dir:/repo \
        -v $build_dir:/build \
        -t -i -d \
        $docker_registry/$pkg_build_docker)
    sudo docker attach $ID

    echo "Done~"
}

#
# Initialize build docker
#
cmd_init_build_docker() {
    echo "Build $pkg_build_docker container..."
    check_pkg_build_tool
    cd $base_repo_tools_dir
    git pull origin master
    check_cmd docker
    ./build-container.sh -a build -r $docker_registry -c $pkg_build_docker
    echo "Done~"
}

#
# Build all packages in repo directory.
#
cmd_build_all() {
    mkdir -p $rpms_dir

    cd $repo_dir
    for i in ${package_category_dirs[@]}; do
        if [ -d $repo_dir/$i ]; then
            folders=$(ls $repo_dir/$i)
            for f in ${folders[@]}; do
                package_build=$f
                cmd_build_package
                echo "Copy results RPMs to rpm repo directory..."
                cp $build_dir/$f/result/*.rpm $rpms_dir
                echo "========================================="
            done
        fi
    done
}

parse_cmd() {
    if [ -z $1 ]; then
        usage
    fi

    case $1 in
        list)
            shift
            while getopts ":r:v" opt; do
                case $opt in
                    r)
                        repo_dir=$(readlink -f $OPTARG)
                        ;;
                    v)
                        verbose=1
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
            while getopts ":rbp:nd" opt; do
                case $opt in
                    r)
                        repo_dir=$(readlink -f $OPTARG)
                        ;;
                    b)
                        build_dir=$(readlink -f $OPTARG)
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
        init-build-docker)
            cmd_init_build_docker
            ;;
        build-all)
            cmd_build_all
            ;;
        *)
            usage
            ;;
    esac
}


check_pkg_build_tool
parse_cmd $@
