FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Syu libnx --noconfirm
RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard 7e581f6
RUN make -j8 install

WORKDIR /developer/components/Status-Monitor-Overlay

ENTRYPOINT ["make", "-j8"]
