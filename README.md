# Better Mirror

```text
 ___ _____   _   ____    __  __ _ ___ ___  __  ___
| _ )__ / |_| |_|__ /_ _|  \/  / | _ \ _ \/  \| _ \
| _ \|_ \  _|  _||_ \ '_| |\/| | |   /   / () |   /
|___/___/\__|\__|___/_| |_|  |_|_|_|_\_|_\\__/|_|_\
```

A Linux package that find the fastest mirror and configure apt to use that.

Just a fork of [IceM4nn/mirrorscript-v2](https://github.com/IceM4nn/mirrorscript-v2)

## Installation

```shell
$ git clone https://github.com/heinthanth/better-mirror
$ cd better-mirror
$ chmod +x build.sh
$ ./build.sh
$ sudo dpkg -i better-mirror.deb
```

## Help

```shell
$ sudo better-mirror -h

 ___ _____   _   ____    __  __ _ ___ ___  __  ___
| _ )__ / |_| |_|__ /_ _|  \/  / | _ \ _ \/  \| _ \
| _ \|_ \  _|  _||_ \ '_| |\/| | |   /   / () |   /
|___/___/\__|\__|___/_| |_|  |_|_|_|_\_|_\\__/|_|_\

better-mirror 1.0.0 - H31iUMx49
https://github.com/heinthanth/better-mirror


usage: better-mirror [option] [mode]

options:
        -c, --choose    : perform mirror choosing
        -h, --help      : display help message
        -s, --src       : enable source repository

modes:
        -v, --verbose   : enable verbose mode
```

## Sample Output

```shell
$ sudo better-mirror -v -c
 ___ _____   _   ____    __  __ _ ___ ___  __  ___
| _ )__ / |_| |_|__ /_ _|  \/  / | _ \ _ \/  \| _ \
| _ \|_ \  _|  _||_ \ '_| |\/| | |   /   / () |   /
|___/___/\__|\__|___/_| |_|  |_|_|_|_\_|_\\__/|_|_\

better-mirror 1.0.0 - H31iUMx49
https://github.com/heinthanth/better-mirror


[*] calculating the mirror latency ...
[*] pinging kali.download ... latency 23.0 ms
[*] pinging ftp.jaist.ac.jp ... latency 117.5 ms
[*] pinging ftp.free.fr ... latency 213.5 ms
[*] pinging ftp.belnet.be ... latency 222.5 ms
[*] pinging mirror.neostrada.nl ... latency 223.75 ms
[*] pinging mirror.serverius.net ... latency 218.25 ms
[*] pinging ftp2.nluug.nl ... latency 232.75 ms
[*] pinging mirrors.dotsrc.org ... latency 216.75 ms
[*] pinging ftp1.nluug.nl ... latency 235.5 ms
[*] pinging ftp.acc.umu.se ... latency 231.0 ms
[*] pinging archive.linux.duke.edu ... latency 304.25 ms
[*] pinging mirror.pwnieexpress.com ... latency 341.25 ms
[*] pinging mirror-1.truenetwork.ru ... latency 322.5 ms
[*] pinging mirror.karneval.cz ... latency 336.5 ms
[*] pinging hlzmel.fsmg.org.nz ... latency 324.5 ms
[*] pinging wlglam.fsmg.org.nz ... latency 330.75 ms
[*] pinging archive-4.kali.org ... latency 252.0 ms
[*] pinging mirrors.ocf.berkeley.edu ... latency 251.0 ms
[*] pinging ftp.halifax.rwth-aachen.de ... latency 257.25 ms
[*] pinging ftp.hands.com ... latency 197.0 ms
[*] finding the best mirror ...
[*] found! the selected mirror: kali.download ... latency 23.0 ms
[*] backuping original /etc/apt/sources.list to /etc/apt/sources.list.bak
[*] updating /etc/apt/sources.list
[*] performing 'apt-get update' for you
Hit:1 http://kali.download/kali kali-rolling InRelease
Ign:2 http://dl.google.com/linux/chrome/deb stable InRelease
Hit:3 http://dl.google.com/linux/chrome/deb stable Release
Hit:4 http://packages.microsoft.com/repos/vscode stable InRelease
Reading package lists... Done
[*] Done!
```
