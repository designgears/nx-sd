FROM devkitpro/devkita64:20200405

COPY ./compile.sh /compile.sh
RUN chmod a+x /compile.sh

RUN dkp-pacman -Scc --noconfirm

RUN git clone https://github.com/switchbrew/libnx.git
WORKDIR /libnx
RUN git fetch && git reset --hard e79c8a2
RUN make -j8 install

ENTRYPOINT ["/compile.sh"]
