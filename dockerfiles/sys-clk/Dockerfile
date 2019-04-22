FROM devkitpro/devkita64:20190329

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

RUN git clone -b pcv-8 https://github.com/p-sam/libnx.git
WORKDIR /libnx
RUN make -j5 install

WORKDIR /developer/components/sys-clk

ENTRYPOINT ["make", "-j5"]
