FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard afaa33d

RUN make -j8 install

WORKDIR /developer/components/hid-mitm

ENTRYPOINT ["make", "-j8"]
