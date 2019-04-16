FROM devkitpro/devkita64

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkitA64 \
    devkitARM \
    libnx \
    switch-portlibs \
    devkitarm-rules && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/ldn_mitm

ENTRYPOINT ["make", "-j5"]