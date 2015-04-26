# packages required for application build are listed in yum_install.sh
# yum_install.sh can be added to RUN to prepare a raw image
FROM 192.168.0.5:5000/lalmeras/homezwaverest-base-i386

COPY scripts /root/
RUN /root/homezwaverest_build.sh 

