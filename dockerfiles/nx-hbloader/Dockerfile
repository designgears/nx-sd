FROM devkitpro/devkita64:20190502

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN make -j8 install

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/nx-hbloader

ENTRYPOINT ["make", "-j8"]
