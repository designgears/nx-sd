FROM devkitpro/devkita64

COPY ./default_icon.jpg /developer/libnx-Goldleaf/nx/default_icon.jpg
COPY ./Makefile /developer/Makefile

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkitA64 \
    devkitARM \
    switch-freetype \
    switch-libdrm_nouveau \
    switch-portlibs \
    devkitarm-rules && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/Goldleaf/

ENTRYPOINT ["make" "-j5"]
