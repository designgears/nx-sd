FROM devkitpro/devkita64:20200405

RUN dkp-pacman -Syu --noconfirm
RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard a272fa7
RUN make -j8 install

WORKDIR /developer/components/Tesla-Menu

ENTRYPOINT ["make", "-j8"]
