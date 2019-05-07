FROM devkitpro/devkita64:latest

COPY ./sept-secondary.enc /sept-secondary.enc
COPY ./compile.sh /compile.sh

ENV SEPT_ENC_PATH="/sept-secondary.enc"

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkit-env \
    devkitA64 \
    devkitARM \
    devkitarm-rules \
    libnx \
    switch-tools \
    switch-dev

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /

ENTRYPOINT ["/compile.sh"]
