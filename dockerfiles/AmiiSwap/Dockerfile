FROM devkitpro/devkita64:20190329

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/AmiiSwap

ENTRYPOINT ["make", "-j5"]
