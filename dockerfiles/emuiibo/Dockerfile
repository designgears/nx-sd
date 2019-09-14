FROM devkitpro/devkita64:20190720

COPY ./compile.sh /compile.sh

RUN chmod a+x /compile.sh

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git reset --hard 40d7e0d
RUN make -j8 install

WORKDIR /

ENTRYPOINT ["/compile.sh"]
