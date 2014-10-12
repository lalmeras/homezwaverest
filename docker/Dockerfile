FROM imcsk8/fedora-20-i386

COPY scripts /root/
RUN /root/yum_proxy.sh \
	&& /root/yum_install.sh \
	&& /root/homezwaverest_build.sh \
	&& yum clean all

