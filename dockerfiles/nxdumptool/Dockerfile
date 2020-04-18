FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard 2c19f13
RUN make -j8 install

WORKDIR /developer/components/nxdumptool

ENTRYPOINT ["make", "-j8"]
