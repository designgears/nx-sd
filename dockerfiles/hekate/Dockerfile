FROM devkitpro/devkita64:20190502

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkitARM \
    devkitarm-rules && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/hekate

ENTRYPOINT ["make", "-j5"]
