FROM devkitpro/devkita64:20190329

COPY ./Makefile /Makefile

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard bc1786b

RUN make -j5 install

WORKDIR /

ENTRYPOINT ["make", "-j5"]
