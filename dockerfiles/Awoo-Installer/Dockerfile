FROM devkitpro/devkita64:20190720

COPY ./switch-zstd-1.4.3-1-any.pkg.tar.xz /switch-zstd-1.4.3-1-any.pkg.tar.xz
RUN chmod a+x /switch-zstd-1.4.3-1-any.pkg.tar.xz

RUN dkp-pacman -U switch-zstd-1.4.3-1-any.pkg.tar.xz --noconfirm
RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard ce39433
RUN make -j8 install

WORKDIR /developer/components/Awoo-Installer

ENTRYPOINT ["make", "-j8"]