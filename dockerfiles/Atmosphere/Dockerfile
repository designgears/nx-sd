FROM devkitpro/devkita64:latest

COPY ./sept-secondary.enc /sept-secondary.enc

RUN dkp-pacman -Syyu --noconfirm --needed \
        devkitA64 \
        devkitARM \
        devkitarm-rules \
        switch-freetype \
        switch-portlibs \
        switch-dev && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM
ENV SEPT_ENC_PATH="/sept-secondary.enc"

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN make -j5 install

WORKDIR /developer/components/Atmosphere

ENTRYPOINT ["make", "-j5"]