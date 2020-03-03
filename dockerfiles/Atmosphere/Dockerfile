FROM devkitpro/devkita64_devkitarm:20190720

COPY ./sept-secondary_00.enc /sept-secondary_00.enc
COPY ./sept-secondary_01.enc /sept-secondary_01.enc
COPY ./sept-secondary_dev_00.enc /sept-secondary_dev_00.enc
COPY ./sept-secondary_dev_01.enc /sept-secondary_dev_01.enc
COPY ./cal0.patch /cal0.patch
COPY ./compile.sh /compile.sh

RUN dkp-pacman -Syu libnx --noconfirm
RUN dkp-pacman -Scc --noconfirm

RUN apt update -y && apt install python -y

ENV SEPT_00_ENC_PATH="/sept-secondary_00.enc"
ENV SEPT_01_ENC_PATH="/sept-secondary_01.enc"
ENV SEPT_DEV_00_ENC_PATH="/sept-secondary_dev_00.enc"
ENV SEPT_DEV_01_ENC_PATH="/sept-secondary_dev_01.enc"

WORKDIR /developer/components/Atmosphere

ENTRYPOINT ["/compile.sh"]
