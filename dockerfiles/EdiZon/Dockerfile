FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git reset --hard f17773c
RUN make -j8 install

WORKDIR /developer/components/EdiZon

ENTRYPOINT ["make", "-j8"]
