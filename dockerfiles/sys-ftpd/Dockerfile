FROM devkitpro/devkita64:20190502

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/sys-ftpd

ENTRYPOINT ["make", "-j8"]
