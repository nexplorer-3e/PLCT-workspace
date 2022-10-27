### Yet another Quick Start for openEuler RISC-V packaging 另一个面向 Tarsier Interns 的 openEuler RISC-V 打包高速上手指南

其实也是一份 pretask walkthrough, 方便想要速通但是没有 `osc` 使用经验而 google open build service guide 的同学

prerequirement: 熟悉 Git ；注册一个方便公开的邮箱。

___

#### 0x0 在 QEMU 上启动 openEuler RISC-V 并运行 neofetch

请参考[这篇教程](https://gitee.com/openeuler/RISC-V/blob/master/doc/tutorials/vm-qemu-oErv.md)。
其他站点下载 image/kernel 的方法尚未经过测试，且未必是最新的。
由于缺少必要组件， QEMU for Windows 无法通过 `qemu-system-riscv64`&`start-vm.sh` 脚本直接启动。对于使用较旧版本 Windows 系统的 member, 这里推荐使用 VirtualBox 搭建一个不含图形环境的 vm, 并配置端口转发。
由于此处下载到的镜像环境是比较完善的，直接克隆 [`neofetch` 仓库](https://github.com/dylanaraps/neofetch)就可以运行了。
另外，推荐在 rootfs 上使用 `qemu-user` 加快运行速度。
由于 `neofetch` 年久失修，这里推荐安装另一个较先进的 fork:
```bash
pip install hyfetch
ln -s /usr/local/bin/neowofetch /usr/local/bin/neofetch
```

#### 0x1 在本地编译 coreutils
参考下文 修包#2 。

另外，也可以使用 git 手动 clone `_services` 里所指向的仓库的指定的 commit ，并在 clone 后的目录执行 `osc build` 。（详见[这里](https://gitee.com/zxs-un/doc-port2riscv64-openEuler/blob/master/doc/build-obs-osc-gitignore.md#%E5%AE%9E%E6%93%8D%E4%B8%8A%E6%89%8B)）

一些需要提前说明的是：
 - 在 0x0 下好的镜像里是自带 `osc` 的，但是需要你
   1. `$ osc -A https://build.tarsier-infra.com` 按照提示进行初步设定
   2. 使用你最喜欢的编辑器编辑 `~/.config/osc/oscrc` 
```yaml
[general]
# ...
# ...
apiurl = https://build.tarsier-infra.com/ 
#^原来的 apiurl 是 opensuse.org
``` 
    
当然，使用 `sed` 也是可以的。
    `$ sed "s/opensuse.org/build.tarsier-infra.com/g" ~/.config/osc/oscrc`
  - Tarsier 只对 https://gitee.com/openeuler-risc-v 下的仓库有管理权限。因此在发起 Pull requests 的时候请 pull 到 openeuler-risc-v 的同名仓库下而不是 src-openeuler 下的仓库。

### 快速上手

#### 一些事项

 - 若无特殊说明，下文所写的 OBS 均指代 `Open Build Service`, **基于** Gitee 托管的源码进行二进制分发包构建的服务。
 OBS 一般不存放源码和 patch, 可以看作是由 `_service` 文件控制的 CI 。
 有关 `_service` 文件的入门指南可以参考 [这篇文章](https://blog.51cto.com/u_15127420/3247112)。
 
 - 一个给 git 用户快速上手 osc 的偏门指南：

| osc command | git command |
|--|--|
| osc co <project> <package> | git remote add origin <repository> |
| osc up -S | git pull |
| osc addremove | git add -A |
| osc ci -m <message> | git commit -m <message> |

另外还有 `osc build` 用于本地构建源码仓库，请参见下文。

 - 看到这一步时你应当已经将 `osc` 的 apiurl 指向了 tarsier 的服务器，如果没有，请看 0x1 。

#### 注册账户
 - 注册一个 [Gitee](https://gitee.com) 账户。OBS 源码包是从 Git 上拉取编译的。
 - [签署 openEuler CLA](https://gitee.com/link?target=https%3A%2F%2Fclasign.osinfra.cn%2Fsign%2FZ2l0ZWUlMkZvcGVuZXVsZXI%3D)。 
 - 注册一个 [Tarsier 管辖的](https://build.tarsier-infra.com) OBS 账户。

#### 修包
将 pretask 发给 wuwei 之后就可以开始修包了。

0. ww 拉的群里都可以问。
1. 挑选了一个心仪的包，然后尝试在自己的 branch repo 修好它。在 2022/08/29 时，对软件包的认领需在双周刊查阅最新的情况。
   - https://gitee.com/openeuler/RISC-V/issues/I1U0YD?from=project-issue
 这是分析构建失败原因的一份简略参考文档。 
2. 然后就可以按照标准的 workflow 在自己中意的环境里开工了。
   - https://gitee.com/openeuler/RISC-V/blob/master/doc/tutorials/workflow-for-build-a-package.md
这个是不含具体操作方法的 workflow example 。
   - https://gitee.com/zxs-un/doc-port2riscv64-openEuler/blob/master/doc/build-obs-osc-gitignore.md
这个在介绍了 workflow 的同时，讲解了如何使用 Git 和 `osc build` 进行构建的方法。另外一种不使用 git fetch` 的方法可在[这里](https://gitee.com/zxs-un/doc-port2riscv64-openEuler/blob/master/doc/build-osc-obs-service.md)查阅。
3. 就如同上面文档所讲到的，一般情况下你需要给 oe-r-v 组织下的仓库开 pr 。 pr 完了先将 `_service` 里的 revision 和 url 指向上游的仓库，再 submit request 。 request 里的理由是写在页面最后的。
 - https://gitee.com/openeuler/community/blob/master/zh/contributors/packaging.md
这是包的规范。
 - https://www.openeuler.org/zh/blog/zhengyaohui/2022-03-21-ci_guild.html
这是给大忙人看的 commit 规范，方便 ci 锅了的时候核对。（具体要以 openeuler-ci-bot 给出的门禁参考手册为准）
4. 碰到什么问题，见 #0 。

[OBS 官方大手册](https://openbuildservice.org/help/manuals/obs-user-guide/)。 tarsier-oerv 仓库有些实用的[脚本](https://github.com/isrc-cas/tarsier-oerv/tree/main/scripts)。

#### 修包以外的其他工作
当然你也可以做别的测试，比如
  - 将 RISC-V 上的某个发行版作为日常使用并向 openEuler/RISC-V 提 issue 。
  - 看看群里都在聊什么然后找你想要了解的。
  - 写一些比这个文档更优秀的文档。
_不过，能作为硬性的*可见外部交付*判据依旧是关掉的 PR 。提升自己的能力，去干大项目吧_

**Tarsier 的中心工作围绕着将 RISC-V 推动成为主要发行版的 tier-1 展开**，但是你也可以关注其他架构推进成为成熟架构的流程。 **Tarsier 是一个包容的社区，敢问你就能在这里有立足之地。**

#### 附注
1. 善用（但不要依赖）搜索引擎。 openEuler 是中文社区所以 Bing 会是搜索资料的不错选择。同时不要嫌弃 CSDN, 能解决问题的方法就是好方法。
2. 不要依赖搜索引擎。不要急于上手做事，熟悉 obs 的结构以及熟练使用轮子会比需要时去 Google 一个 solution 更加提升工作效率。从零修复工业项目的进程不是看了一会 stackoverflow 就能移植出来的。

edited on 10.10
