FROM devkitpro/devkita64:20190502

RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/EdiZon

ENTRYPOINT ["make", "-j8"]
