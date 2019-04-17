FROM devkitpro/devkita64:20190329

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkitARM \
    devkitarm-rules && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/Lockpick_RCM

ENTRYPOINT ["make", "-j5"]
