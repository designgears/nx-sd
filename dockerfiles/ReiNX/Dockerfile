FROM devkitpro/devkita64:latest

COPY ./sept-secondary.enc /sept-secondary.enc
COPY ./compile.sh /compile.sh

ENV SEPT_ENC_PATH="/sept-secondary.enc"

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkitA64 \
    devkitARM \
    devkitarm-rules \
    switch-freetype \
    switch-portlibs \
    switch-dev && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard bc1786b

RUN make -j5 install

WORKDIR /

ENTRYPOINT ["/compile.sh"]
