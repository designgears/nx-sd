FROM devkitpro/devkita64:20190329

COPY ./Makefile /Makefile
COPY ./compile.sh /compile.sh

RUN chmod a+x /compile.sh

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

RUN git clone https://github.com/switchbrew/libnx.git

WORKDIR /libnx

RUN git reset --hard bc1786b

RUN make -j5 install

WORKDIR /

ENTRYPOINT ["/compile.sh"]
