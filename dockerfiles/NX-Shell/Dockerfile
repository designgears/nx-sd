FROM devkitpro/devkita64:20190502

COPY ./compile.sh /compile.sh

RUN chmod a+x /compile.sh

RUN dkp-pacman -Syyu --noconfirm \
    switch-libwebp && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM
ENV DEVKITA64=${DEVKITPRO}/devkitA64

WORKDIR /developer/components/NX-Shell

ENTRYPOINT ["/compile.sh"]
