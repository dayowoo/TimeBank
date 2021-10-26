# BEGIN PROVISIONER ADDED ENVIRONMENT SETTINGS

PATH=/opt/bitnami/apache/bin:/opt/bitnami/apache2/bin:/opt/bitnami/common/bin:/opt/bitnami/git/bin:/opt/bitnami/gonit/bin:/opt/bitnami/mariadb/bin:/opt/bitnami/mariadb/sbin:/opt/bitnami/node/bin:/opt/bitnami/postgresql/bin:/opt/bitnami/python/bin:/opt/bitnami/nami/bin:$PATH
export PATH

# END PROVISIONER ADDED ENVIRONMENT SETTINGS
# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

# BEGIN BITNAMI IMAGE METADATA SETTINGS
export OS_ARCH=amd64
export OS_FLAVOUR=debian-10
export OS_NAME=linux
export BITNAMI_APP_NAME=django
export BITNAMI_IMAGE_VERSION=3.1.6
# END BITNAMI IMAGE METADATA SETTINGS
