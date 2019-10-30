FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git log
RUN git reset --hard 01133f7
RUN make -j8 install

WORKDIR /developer/components/nx-hbloader

ENTRYPOINT ["make", "-j8"]
