FROM devkitpro/devkita64

RUN apt install -y zip

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkitA64 \
    devkitARM \
    libnx \
    devkitarm-rules && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/nx-hbmenu

ENTRYPOINT ["make", "nx"]
