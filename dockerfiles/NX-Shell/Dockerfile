FROM devkitpro/devkita64

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkitA64 \
    devkitARM \
    switch-portlibs \
    libnx \
    switch-sdl2 \
    switch-dev \
    devkitarm-rules && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM
ENV DEVKITA64=${DEVKITPRO}/devkitA64

WORKDIR /developer/components/NX-Shell

ENTRYPOINT ["make", "-j5"]
