FROM devkitpro/devkita64:20190502

COPY ./sept-secondary.enc /sept-secondary.enc
COPY ./compile.sh /compile.sh

RUN chmod a+x /compile.sh

RUN dkp-pacman -Syyu --noconfirm --needed \
    devkit-env \
    devkitA64 \
    devkitARM \
    devkitarm-rules \
    libnx \
    switch-tools \
    switch-dev

ENV DEVKITARM=${DEVKITPRO}/devkitARM
ENV SEPT_ENC_PATH="/sept-secondary.enc"

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard 9c887a1

RUN make -j8 install

WORKDIR /

ENTRYPOINT ["/compile.sh"]
