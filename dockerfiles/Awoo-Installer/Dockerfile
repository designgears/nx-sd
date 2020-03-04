FROM devkitpro/devkita64:20190720

COPY ./switch-zstd-1.4.3-1-any.pkg.tar.xz /switch-zstd-1.4.3-1-any.pkg.tar.xz
RUN chmod a+x /switch-zstd-1.4.3-1-any.pkg.tar.xz

RUN dkp-pacman -U switch-zstd-1.4.3-1-any.pkg.tar.xz --noconfirm
RUN dkp-pacman -Syu libnx --noconfirm
RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/Awoo-Installer

ENTRYPOINT ["make", "-j8"]