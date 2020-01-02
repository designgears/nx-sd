FROM devkitpro/devkita64:20190720

ENV PLATFORM="switch"

RUN dkp-pacman -Syu libnx --noconfirm
RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/hb-appstore

ENTRYPOINT ["make", "-j8"]
