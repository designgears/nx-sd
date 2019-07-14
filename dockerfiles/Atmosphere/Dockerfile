FROM devkitpro/devkita64_devkitarm:20190510

COPY ./sept-secondary_00.enc /sept-secondary_00.enc
COPY ./sept-secondary_01.enc /sept-secondary_01.enc

RUN dkp-pacman -Syyu --noconfirm --needed \
        devkitA64 \
        devkitARM \
        devkitarm-rules \
        switch-freetype \
        switch-portlibs \
        switch-dev && \
    dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM
ENV SEPT_00_ENC_PATH="/sept-secondary_00.enc"
ENV SEPT_01_ENC_PATH="/sept-secondary_01.enc"

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard 40d7e0d

RUN make -j8 install

WORKDIR /developer/components/Atmosphere

ENTRYPOINT ["make", "-j8"]
