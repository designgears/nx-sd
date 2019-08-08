FROM devkitpro/devkita64:20190720

RUN apt update -y && \
    apt install -y zip

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard f5b24bd

RUN make -j8 install

WORKDIR /developer/components/nx-hbmenu

ENTRYPOINT ["make", "-j8", "nx"]
