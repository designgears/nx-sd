FROM devkitpro/devkita64:20181128

COPY ./compile.sh /compile.sh

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

ENTRYPOINT ["/compile.sh"]
