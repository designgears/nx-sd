FROM devkitpro/devkita64_devkitarm:20190720

COPY ./sept-secondary_00.enc /sept-secondary_00.enc
COPY ./sept-secondary_01.enc /sept-secondary_01.enc

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard 26876ce
RUN make -j8 install

ENV SEPT_00_ENC_PATH="/sept-secondary_00.enc"
ENV SEPT_01_ENC_PATH="/sept-secondary_01.enc"

WORKDIR /developer/components/Atmosphere

ENTRYPOINT ["make", "-j8"]
