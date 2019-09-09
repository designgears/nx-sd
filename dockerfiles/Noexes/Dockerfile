FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/Noexes/server/source/noexs

ENTRYPOINT ["make", "-j8"]
