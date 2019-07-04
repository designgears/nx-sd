FROM devkitpro/devkita64_devkitarm:20190510

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

RUN make -j8 install

WORKDIR /developer/components/sys-ftpd

ENTRYPOINT ["make", "-j8"]
