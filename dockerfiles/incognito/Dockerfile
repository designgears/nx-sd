FROM devkitpro/devkita64

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkitA64 \
    devkitARM \
    switch-portlibs \
    devkitarm-rules && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/incognito

ENTRYPOINT ["make", "-j5"]
