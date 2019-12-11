FROM devkitpro/devkita64:20190720

COPY ./contents.patch /contents.patch
COPY ./compile.sh /compile.sh
RUN chmod a+x /compile.sh

RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/sys-clk-Editor

ENTRYPOINT ["make", "-j8"]
