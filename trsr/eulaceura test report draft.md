
22h1 on 10.18
------
|Eulaceura 2.0 22H1|-|
|---|---|
|python|3.9.9|
|kernel|5.10.0|
|bash|5.1.8|

desktop with preinstalled graphical environment, 
systemd log not printed to ttyS by default.

0. root password: `Eulaceura12#$`
> 还有一组 user/pass 是 eula/ceura
> > eula 默认 locale 是 `zh_CN.UTF-8` 在 hvc0 （QEMU SDL console）上会乱码
1. dnf/zypper 没有默认软件源 `/etc/zypp/repos.d/Eulaceura.repo`
	```
	zypper addrepo https://repo.tarsier-infra.com/eulaceura/dist/22H1/source/ 22h1src
	zypper addrepo https://repo.tarsier-infra.com/eulaceura/dist/22H1/L/ 22h1-l
	zypper addrepo https://repo.tarsier-infra.com/eulaceura/dist/22H1/M/ 22h1-m
	```
2.  预装了 lightdm+kiran. tty 未测试, 用 lightdm-kiran-greeter 直接进行登录验证会无法输入密码。
> 10/27 补充： `-device virtio-vga` 启动可以获得一个图形输出。 
5.  `mpv` 爆炸。参见 openEuler/RISCV 已有相关 issue.
6.  

