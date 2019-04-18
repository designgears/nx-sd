FROM devkitpro/devkita64:20190329

COPY ./Makefile /Makefile

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /emuiibo

ENTRYPOINT ["make", "-j5"]
