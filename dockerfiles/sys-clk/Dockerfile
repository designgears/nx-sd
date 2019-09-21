FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git reset --hard f4fe337
RUN make -j8 install

WORKDIR /developer/components/sys-clk/sysmodule

ENTRYPOINT ["make", "-j8"]
