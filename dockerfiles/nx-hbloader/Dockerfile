FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard d1e5a5d
RUN make -j8 install

WORKDIR /developer/components/nx-hbloader

ENTRYPOINT ["make", "-j8"]
