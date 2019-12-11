FROM devkitpro/devkita64:20190720

#RUN dkp-pacman -Syu libnx --noconfirm
RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard 26876ce
RUN make -j8 install

WORKDIR /developer/components/sys-ftpd-light

ENTRYPOINT ["make", "-j8"]
