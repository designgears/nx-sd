FROM devkitpro/devkita64:20190502

RUN apt update -y && \
    apt install -y zip

RUN dkp-pacman -Syyu --noconfirm --needed && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard 75c79e8

RUN make -j8 install

WORKDIR /developer/components/nx-hbmenu

ENTRYPOINT ["make", "-j8", "nx"]
