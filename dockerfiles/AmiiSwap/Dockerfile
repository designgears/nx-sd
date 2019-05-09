FROM devkitpro/devkita64:20190502

COPY ./compile.sh /compile.sh

RUN chmod a+x /compile.sh

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/AmiiSwap

ENTRYPOINT ["/compile.sh"]
