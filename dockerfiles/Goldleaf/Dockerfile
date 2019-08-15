FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/Goldleaf/Goldleaf

ENTRYPOINT ["make", "-j8"]
