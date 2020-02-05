FROM devkitpro/devkita64:20190720

COPY ./compile.sh /compile.sh
RUN chmod a+x /compile.sh

RUN dkp-pacman -Syu libnx --noconfirm
RUN dkp-pacman -Scc --noconfirm

ENTRYPOINT ["/compile.sh"]
