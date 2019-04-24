FROM devkitpro/devkita64:20190329

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN make -j5 install

WORKDIR /developer/components/EdiZon

ENTRYPOINT ["make", "-j5"]
