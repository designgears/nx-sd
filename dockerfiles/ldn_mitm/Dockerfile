FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Syu --noconfirm
RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard 8cbac97
RUN make -j8 install

WORKDIR /developer/components/ldn_mitm

ENTRYPOINT ["make", "-j8"]
