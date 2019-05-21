FROM devkitpro/devkita64:latest

COPY ./Makefile /Makefile
COPY ./compile.sh /compile.sh
COPY ./default_icon.jpg /default_icon.jpg

RUN chmod a+x /compile.sh

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /

ENTRYPOINT ["/compile.sh"]
