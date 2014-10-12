#! /bin/bash

sed -i '/^metalink/ s@^@#@#' /etc/yum.repos.d/*.repo
sed -i '/^#baseurl/ s@^#@@#' /etc/yum.repos.d/*.repo
sed -i 's@http://download.fedoraproject.org/pub/fedora/linux/@http://ftp.free.fr/mirrors/fedora.redhat.com/fedora/linux/@' /etc/yum.repos.d/*.repo
echo -e "\nproxy=http://192.168.0.42:8123" >> /etc/yum.conf
