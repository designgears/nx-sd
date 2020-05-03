FROM devkitpro/devkita64:20200405

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard 8cbac97
RUN make -j8 install

WORKDIR /developer/components/JKSV

ENTRYPOINT ["make", "-j8"]
