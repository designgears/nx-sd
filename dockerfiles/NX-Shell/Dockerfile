FROM devkitpro/devkita64:20190329

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM
ENV DEVKITA64=${DEVKITPRO}/devkitA64

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard bc1786b

RUN make -j5 install

WORKDIR /developer/components/NX-Shell

ENTRYPOINT ["make", "-j5"]
