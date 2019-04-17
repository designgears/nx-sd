FROM devkitpro/devkita64:20190329

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM
ENV DEVKITA64=${DEVKITPRO}/devkitA64

WORKDIR /developer/components/NX-Shell

ENTRYPOINT ["make", "-j5"]
