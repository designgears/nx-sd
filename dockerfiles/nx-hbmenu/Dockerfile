FROM devkitpro/devkita64:20190720

RUN apt update -y && \
    apt install -y zip

RUN dkp-pacman -Syu libnx --noconfirm
RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/nx-hbmenu

ENTRYPOINT ["make", "-j8", "nx"]
