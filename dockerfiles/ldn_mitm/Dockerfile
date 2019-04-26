FROM devkitpro/devkita64:latest

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard bc1786b

RUN make -j5 install

WORKDIR /developer/components/ldn_mitm

ENTRYPOINT ["make", "-j5"]
