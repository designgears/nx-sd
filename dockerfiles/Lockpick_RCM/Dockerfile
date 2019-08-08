FROM devkitpro/devkita64_devkitarm:20190720

RUN dkp-pacman -Scc --noconfirm

WORKDIR /developer/components/Lockpick_RCM

ENTRYPOINT ["make", "-j8"]
