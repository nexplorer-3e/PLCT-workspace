## 另一个在 systemd-nspawn 容器 / chroot 环境进行 openEuler RISC-V 支持的部署备忘录
本文是对 [基于 systemd-nspawn 和 QEMU User Mode 搭建 openEuler RISC-V 软件包的快速开发环境](https://gitee.com/openeuler/RISC-V/blob/master/doc/tutorials/qemu-user-mode.md) 的补充，期间参考了[Debian wiki](https://wiki.debian.org/QemuUserEmulation) 的 qemu 容器指南。宿主机就是 Debian 的话应该不会遇到什么问题就能搭建起 rootfs 实现快速开发。
#### why
 - 众所周知 qemu system emulation 速度是很慢的。经过简单的测试，在同一设备上， qemu user-mode container 浮点性能较 tarsier 提供的 `start-vm.sh` 启动的 qemu system emulater 提高了 100%。
 - 启动快速，不需要 OpenSBI 的加载环节；文件系统不以 disk image 形式存在，便于宿主机与开发环境进行文件传输。
#### 较原文的补充
较为流行的发行版都提供了 `qemu-user` 的预编译二进制包，不需要手动编译。
就使用体验而言，加载一个 rootfs container 较 `osc build --vm-type=nspawn` 更加用户友好。

### 使用指南

 0. 确认宿主机的内核是否支持 binfmt_misc 。
```bash
$ mount |grep binfmt
```
如果没有输出，尝试加载 binfmt_misc 。
```bash
# mount binfmt_misc -t binfmt_misc /proc/sys/fs/binfmt_misc
```
若无法加载，则可能是内核不支持 binfmt_misc。此时可以考虑 `proot` 之类的用户态实现 (#2)，较慢但仍快于 system emulation。
 
 1. 对于包管理器已经提供了 `qemu-user-static` `binfmt-support` `systemd-container` 的发行版：
   - 安装以上软件包。
   - 确保 binfmt_misc 处于可用状态。
```bash
$ grep "riscv" -r /proc/sys/fs/binfmt_misc/
/proc/sys/fs/binfmt_misc/qemu-riscv64:interpreter /usr/libexec/qemu-binfmt/riscv64-binfmt-P
```
输出含 `riscv64` 字样即可。若不可用，参考 Debian wiki 使用 `update-binfmts` 配置 binfmt_misc 。
   - 在 repo.tarsier-infra.com 获取最新的 rootfs tarball 并解包。
```bash
$ mkdir oe-rootfs && cd oe-rootfs
$ curl -fSL <>.tar.gz |tar xz
```
   - 进入 oe-rv userspace 容器：
```bash
# systemd-nspawn -D .
```
不出意料的话就会进入 root shell. 执行 `uname -a`:
```bash
[root@oe-rootfs ~]# uname -m
riscv64
```
可以看到 arch 已经是 riscv64 的形状了。 

同时也可以参照原文使用 `osc build --vm-type=nspawn` 进行软件包构建。

 2. 对于没有提供 `qemu-user-static` 的发行版
  - 尝试编译。参考原文。
  - 因为依赖问题（依赖的库无法方便地在目标平台上编译等等）而无法编译的，考虑使用 `proot` (#3) 。
 
 3. 对于内核不支持 binfmt_misc 的发行版（以 Termux 为例）
  - 部署 [`proot`](https://github.com/proot-me/proot) 环境。
```bash
$ pkg in proot
```
  - 获取可用的 `qemu-user` （不需要 `static` ）
```bash
$ pkg in qemu-riscv64-user
```
 - 在 repo.tarsier-infra.com 获取最新的 rootfs tarball 并解包。
```bash
$ mkdir oe-rootfs && cd oe-rootfs
$ curl -fSL <>.tar.gz |tar xz
```
   - 进入 oe-rv userspace 容器：
```bash
## 下面是一个提取自 `proot-distro` 的样例
$ unset LD_PRELOAD; proot -q qemu-riscv64 --bind=/vendor --bind=/system --bind=/data/data/com.termux/files/usr --bind=/linkerconfig/ld.config.txt --bind=/apex --bind=/storage/self/primary:/sdcard --bind=/data/data/com.termux/files/home --bind=/data/data/com.termux/cache --bind=/data/dalvik-cache --bind=$PWD/tmp:/dev/shm --bind=$PWD/proc/.vmstat:/proc/vmstat --bind=$PWD/proc/.version:/proc/version --bind=$PWD/proc/.uptime:/proc/uptime --bind=$PWD/proc/.stat:/proc/stat --bind=$PWD/proc/.loadavg:/proc/loadavg --bind=/sys --bind=/proc/self/fd/2:/dev/stderr --bind=/proc/self/fd/1:/dev/stdout --bind=/proc/self/fd/0:/dev/stdin --bind=/proc/self/fd:/dev/fd --bind=/proc --bind=/dev/urandom:/dev/random --bind=/dev --root-id --cwd=/root -L --sysvipc --link2symlink --kill-on-exit --rootfs=/data/data/com.termux/files/usr/var/lib/proot-distro/installed-rootfs/openeuler /usr/bin/env -i HOME=/root LANG=C.UTF-8 TERM=xterm-256color /bin/su -l root
## 或者
$ ENV="LANG=C.UTF-8 TERM=xterm-256color HOME=/root" LD_PRELOAD= proot -q qemu-riscv64 -S $PWD /usr/bin/env -i $ENV /bin/su -l root
## 在 Android 12 下可能会出现 warning linkerconfig ，此时在 `proot` 参数里加一个 `-b /linkerconfig/ld.config.txt` 即可
...
[root@localhost ~]#
```

  - 由于容器不是由 systemd 启动的，因此某些已被 systemd 接管的服务可能无法正常使用。以下是一些问题的解决方案：
    - `curl: could not resolve hostname`
    > `$ echo 'nameserver 8.8.8.8'>/etc/resolv.conf`
    
    - `$LANG, $LC_* invalid`
    > `# dnf reinstall glibc-common -y`
   
