FROM devkitpro/devkita64:20190502

RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/incognito

ENTRYPOINT ["make", "-j8"]
