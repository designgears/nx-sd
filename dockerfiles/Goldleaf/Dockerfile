FROM devkitpro/devkita64:latest

COPY ./Makefile /Makefile
COPY ./compile.sh /compile.sh

RUN chmod a+x /compile.sh

RUN dkp-pacman -Syyu --noconfirm --needed \
        devkitA64 \
        devkitARM \
        devkitarm-rules \
        switch-freetype \
        switch-portlibs \
        switch-dev && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /

ENTRYPOINT ["/compile.sh"]
