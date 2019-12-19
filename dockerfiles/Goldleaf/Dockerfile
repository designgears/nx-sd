FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard ce39433
RUN make -j8 install

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/Goldleaf

ENTRYPOINT ["make", "-j8"]
