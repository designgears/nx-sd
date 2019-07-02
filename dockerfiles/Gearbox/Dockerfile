FROM devkitpro/devkita64:20190502

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/Gearbox

ENTRYPOINT ["make", "-j8"]
