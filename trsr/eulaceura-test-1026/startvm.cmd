call qemu-system-riscv64 ^
-smp 4 -m 4G ^
-machine virt -bios fw_boot.bin ^
-spice disable-ticketing=on,port=16969 ^

-device virtio-gpu ^
-device virtio-blk-device,drive=hd0 -drive file=sys_disk.qcow2,id=hd0,format=qcow2 ^
-device virtio-net-device,netdev=usernet -netdev user,id=usernet,ipv6=off,hostfwd=tcp::2222-:22,hostfwd=tcp::5900-:5900,hostfwd=udp::177-:177 ^
-device qemu-xhci -usb ^
-device usb-audio,audiodev=snd0 -audiodev sdl,id=snd0 ^
-device usb-kbd -device usb-tablet 

REM -display gtk,show-tabs=on ^

REM eulaceura does not have modules for usb-audio

REM -audio model=help
REM DO NOT TRY TO GET HELP BY -audiodev USE 
REM -audio-help