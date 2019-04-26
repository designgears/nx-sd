FROM devkitpro/devkita64:20181128

RUN dkp-pacman -Scc --noconfirm

ENV DEVKITARM=${DEVKITPRO}/devkitARM

WORKDIR /developer/components/Tinfoil88

ENTRYPOINT ["make", "-j5"]
