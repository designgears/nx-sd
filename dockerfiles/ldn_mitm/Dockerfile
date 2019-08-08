FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/ldn_mitm

ENTRYPOINT ["make", "-j8"]
