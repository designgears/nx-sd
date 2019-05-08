FROM devkitpro/devkita64:20190329

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard bc1786b
# bc1786b7b0f7e915fe0e554793b55144f57249f2
# pcv Set/GetClockRate changes in 8.0.0 (#266)
# version check on pre-8.0.0 pcv funcs
# clkrst API
# Add PcvModuleId enum

RUN make -j5 install

WORKDIR /developer/components/sys-clk

ENTRYPOINT ["make", "-j5"]
