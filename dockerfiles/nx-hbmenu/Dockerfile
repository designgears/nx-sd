FROM devkitpro/devkita64:20190329

RUN apt install -y zip

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/nx-hbmenu

ENTRYPOINT ["make", "nx"]
