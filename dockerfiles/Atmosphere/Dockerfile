FROM devkitpro/devkita64_devkitarm:20190720

COPY ./sept-secondary_00.enc /sept-secondary_00.enc
COPY ./sept-secondary_01.enc /sept-secondary_01.enc
COPY ./cal0.patch /cal0.patch
COPY ./compile.sh /compile.sh

RUN chmod a+x /compile.sh
RUN dkp-pacman -Scc --noconfirm

ENV SEPT_00_ENC_PATH="/sept-secondary_00.enc"
ENV SEPT_01_ENC_PATH="/sept-secondary_01.enc"

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git reset --hard 3d682b6
RUN make -j8 install

WORKDIR /developer/components/Atmosphere

ENTRYPOINT ["/compile.sh"]
