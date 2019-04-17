FROM devkitpro/devkita64:20190329

COPY ./default_icon.jpg /developer/libnx-Goldleaf/nx/default_icon.jpg
COPY ./Makefile /developer/Makefile

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/Goldleaf/

ENTRYPOINT ["make", "-j5"]
