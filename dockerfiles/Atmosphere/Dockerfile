FROM devkitpro/devkita64:20190502

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

WORKDIR /developer/components/Atmosphere

ENTRYPOINT ["make", "-j5"]
