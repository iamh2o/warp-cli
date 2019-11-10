#! /usr/bin/python
#### WDT Wrapper for Uni-Cast - https://github.com/facebook/wdt
## Version 2.0
from global_defuns import *

############
## Setup WDT
########
def build_wdt(base_dir):
    import re
    ## build and setup wdt dependencies depending on linux distro
    os_name = os_distro()
    #############
    if re.search(r'arch', os_name.lower()):
        aur_tool = input('Do you use a AUR Tool? If so enter the install command for your Tool. /n I.E. "pacaur -S": ')
        if len(aur_tool) > 0:
            os.system(aur_tool + " wdt-git")
            sys.exit('Done!')
        else:
            sys.exit('Refer to the manual build guide OR don\'t be stupid and use a AUR manager. :P')
    #############
    elif re.search(r'(fedora 30|fedora 29|fedora 28)', os_name.lower()):
        yum('cmake boost-devel openssl jemalloc glog-devel double-conversion-devel make automake gcc gcc-c++ kernel-devel gtest-devel openssl-devel libevent-devel')
    #############
    elif re.search(r'(ubuntu 19|ubuntu 18|debian gnu/linux 9|debian gnu/linux 10)', os_name.lower()):
        apt('cmake libjemalloc-dev libgoogle-glog-dev libboost-system-dev libdouble-conversion-dev openssl build-essential libboost-all-dev libssl-dev libgtest-dev libevent-dev')
    #############
    else:
        sys.exit('Automated package installs for ' + os_name + ' are not supported.')
    
    ## download and build wdt from github source
    mkdir(base_dir + '/build', 'u')
    os.system('cd ' + base_dir + '/build && git clone https://github.com/facebook/folly.git')
    #  os.system('cd ' + base_dir + '/build/folly && git checkout "$(git describe --abbrev=0 --always)"')
    os.system('cd ' + base_dir + '/build/folly && git checkout v2019.09.02.00')
    os.system('cd ' + base_dir + '/build && git clone https://github.com/facebook/wdt.git')
    mkdir(base_dir + '/build/wdt/_build', 'u')
    os.system('cd ' + base_dir + '/build/wdt/_build && cmake -DCMAKE_INSTALL_PREFIX="/usr" -DCMAKE_BUILD_TYPE=Release ../ && make -j && sudo make install')

############
## Setup Warp-CLI
########
def setup_warp():
    ## setup warp-cli dirs
    base_dir = os.getcwd[:-5]
    mkdir(base_dir + '/pool', 'u')
    mkdir(base_dir + '/macros', 'u')
    open_permissions(base_dir)
    ## link warp in bash to warp.py
    os.system('sudo ln -s ' + base_dir + '/core/warp.py /usr/bin/warp')
    build_wdt(base_dir)

def setup_warp_remote(ssh_alias, base_dir):
    ## tunnel to a remote machine and install warp-cli minimal
    git_clone = ' cd ' + base_dir + ' && git clone https://github.com/JustinTimperio/warp-cli.git &&'
    build = ' python3 ' + base_dir + '/warp-cli/core/warp.py --install' 
    os.system('ssh ' + ssh_alias + git_clone + build)

def uninstall_warp(base_dir):
    rm_dir(base_dir, 'r')
    rm_file('/usr/bin/warp', 'r')
