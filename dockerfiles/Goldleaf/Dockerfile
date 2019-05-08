FROM devkitpro/devkita64:20190329

COPY ./Makefile /Makefile
COPY ./compile.sh /compile.sh

RUN chmod a+x /compile.sh

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /

ENTRYPOINT ["/compile.sh"]
