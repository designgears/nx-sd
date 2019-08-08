FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/Gearbox

ENTRYPOINT ["make", "-j8"]
