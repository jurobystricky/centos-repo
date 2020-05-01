#!/bin/bash



curr_dir=$(readlink -f $(dirname ${0}))
top_dir=$curr_dir
repo_dir=$top_dir/repo
build_dir=$top_dir/build
rpms_dir=$build_dir/rpms
cache_dir=$top_dir/cache
package_category_dirs=(BaseOS AppStream)
package_build=""
mock_docker_image="intel-linux-mock-build"
build_in_docker=1
verbose=0

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
        #
        # To stop build in docker, press Ctrl + C
        #
        ID=$(sudo docker run \
            --cap-add=SYS_ADMIN \
            -e http_proxy=$http_proxy \
            -e https_proxy=$http_proxy \
            -e PACKAGE=$package_build \
            -v $repo_dir:/intel-linux/repo \
            -v $build_dir:/intel-linux/build \
            -v $cache_dir:/opt/cache \
            -t -i -d \
            $mock_docker_image \
            /usr/bin/mock-build.sh)
        sudo docker attach $ID
    else
        export PACKAGE=$package_build
        if [[ ! -f /etc/mock/intel-linux-centos.cfg ]]; then
            sudo cp $top_dir/tools/intel-linux-centos.cfg /etc/mock/
        fi
        $top_dir/tools/mock-build.sh
    fi

    echo "Done~"
}

#
# Initialize mock docker. On non-CentOS system, the package build is via mock
# container; while on CentOS system, it is native.
#
cmd_init_mock_docker() {
    echo "Build mock build docker image..."
    $top_dir/tools/build-container.sh
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

#
# Judge whether current OS is CentOS
#
is_centos() {
    distro=$(cat /etc/*-release | grep "CentOS Linux 8")
    if [[ -z $distro ]]; then
        echo 0
    else
        echo 1
    fi
}

parse_cmd() {
    build_in_docker=$((1-$(is_centos)))

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
            cmd_init_mock_docker
            ;;
        build-all)
            cmd_build_all
            ;;
        *)
            usage
            ;;
    esac
}

parse_cmd $@
