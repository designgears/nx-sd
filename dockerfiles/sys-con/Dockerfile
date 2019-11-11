FROM devkitpro/devkita64:20190720

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch
RUN git reset --hard d4c5fbdf0f80a19ecfa4b553b6267641210a8e43
RUN make -j8 install

WORKDIR /developer/components/sys-con

ENTRYPOINT ["make", "-f", "MakefileSysmodule", "-j8"]
