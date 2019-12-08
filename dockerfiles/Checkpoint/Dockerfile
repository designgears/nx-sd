FROM debian:buster

ENV DEVKITPRO=/opt/devkitpro
ENV DEVKITARM=/opt/devkitpro/devkitARM

COPY ./contents.patch /contents.patch
COPY ./compile.sh /compile.sh
RUN chmod a+x /compile.sh

RUN apt update
RUN apt install -y wget gpg libxml2 xz-utils make python3 git pkg-config gcc

RUN wget https://github.com/devkitPro/pacman/releases/download/devkitpro-pacman-1.0.1/devkitpro-pacman.deb

RUN dpkg -i devkitpro-pacman.deb

RUN dkp-pacman -Sy switch-dev 3ds-dev switch-portlibs switch-pkg-config --noconfirm

RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/Checkpoint

ENTRYPOINT ["/compile.sh"]
