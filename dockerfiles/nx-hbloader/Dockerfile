FROM devkitpro/devkita64

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkitA64 \
    devkitARM \
    devkitarm-rules && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/nx-hbloader

ENTRYPOINT ["make", "-j5"]
