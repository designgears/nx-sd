FROM devkitpro/devkita64:20190502

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/nx-hbloader

ENTRYPOINT ["make", "-j8"]
