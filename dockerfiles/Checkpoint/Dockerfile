FROM debian:buster

ENV DEBIAN_FRONTEND=noninteractive

ENV DEVKITPRO=/opt/devkitpro
ENV DEVKITARM=/opt/devkitpro/devkitARM
ENV PATH=${DEVKITPRO}/tools/bin:$PATH

RUN apt-get update && \
    apt-get install -y apt-utils && \
    apt-get install -y --no-install-recommends sudo ca-certificates pkg-config curl wget bzip2 xz-utils make git bsdtar doxygen gnupg libxml2 xz-utils python3 gcc && \
    apt-get clean

RUN wget https://github.com/devkitPro/pacman/releases/download/devkitpro-pacman-1.0.1/devkitpro-pacman.deb && \
    dpkg -i devkitpro-pacman.deb && \
    rm devkitpro-pacman.deb && \
    dkp-pacman -Scc --noconfirm

RUN dkp-pacman -Syyu --noconfirm switch-dev devkitARM devkitarm-rules && \
    dkp-pacman -S --needed --noconfirm `dkp-pacman -Slq dkp-libs | grep '^switch-'` && \
    dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/Checkpoint

ENTRYPOINT ["make", "-j8"]
