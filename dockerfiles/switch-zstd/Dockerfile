FROM archlinux:latest

ENV DEVKITPRO=/opt/devkitpro
ENV DEVKITARM=/opt/devkitpro/devkitARM
ENV DEVKITPPC=/opt/devkitpro/devkitPPC

RUN pacman-key --init
RUN pacman-key --recv F7FD5492264BB9D0
RUN pacman-key --lsign F7FD5492264BB9D0
RUN pacman -U https://downloads.devkitpro.org/devkitpro-keyring-r1.787e015-2-any.pkg.tar.xz --noconfirm

RUN echo "[dkp-libs]" >> /etc/pacman.conf
RUN echo "Server = https://downloads.devkitpro.org/packages" >> /etc/pacman.conf
RUN echo "[dkp-linux]" >> /etc/pacman.conf
RUN echo "Server = https://downloads.devkitpro.org/packages/linux" >> /etc/pacman.conf

RUN pacman -Syu --noconfirm

RUN useradd -r -s /usr/bin/nologin builder
RUN mkdir /builder
RUN chown builder.builder /builder -R
RUN ln -s /builder /developer

RUN pacman -Syu make cmake wget sudo fakeroot devkitA64 devkitpro-pkgbuild-helpers switch-dev --noconfirm

USER builder

WORKDIR /developer/components/pacman-packages/switch/zstd

ENTRYPOINT ["makepkg"]
