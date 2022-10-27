Windows 下的  `gcc`  发行版目录
===
### 这是什么
https://guyutongxue.github.io/blogs/build_mingw.html
有关 Windows 下的 GNU Tools 现状可以看 https://news.ycombinator.com/item?id=31792790
see also: https://winlibs.com/philosophy.html
只列举还在维护的 gcc distribution.  不满于 msys2 index 的版本滞后情况于是决定自己手搓。
### The List
update on 20221020

| Toolchains | Website | Version |
| --- | --- | - |
| WinLibs | https://winlibs.com | GCC 12.2 |
| MinGW-w64-Builds | https://github.com/niXman/mingw-builds-binaries/releases | 
| TDM-GCC | | 
| LLVM-MinGW | | 
| Cygwin [2] | | 

注：
1. 不推荐基于 MinGW 的发行版，虽然 just works 但过于老旧无人维护
    比如 Mingw-builds (sourceforge)
2. Cygwin 的版本较 MSYS2 已有滞后，且 Cygwin 下许多 lib 已处于 Unmaintained 的状态，版本很可能不是最新的。
3. 


> Written with [StackEdit](https://stackedit.io/).
