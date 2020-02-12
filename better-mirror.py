#!/usr/bin/env python3

import re
import os
import urllib
import xmltodict
import subprocess
import sys
from threading import Thread

# check if we have privileges
if not os.getuid() == 0:
    sys.exit("\n\033[31mcan you run as root or sudo, please?\033[0m\n")

# check if supported distros
supported_distros = ['kali-rolling']
with open("/etc/os-release") as release:
    version = re.search("VERSION_CODENAME=\"(.*)\"", release.read())
    if not version:
        sys.exit(
            "\n\033[31mI don't know what distros you are using :(\033[0m\n")
    else:
        if not version[1] in supported_distros:
            sys.exit(
                "\n\033[31m{} is not supported in these days\033[0m\n".format(version[1]))

verboseMode = False
enableSource = False

threads = list()
results = dict()
hostlist = dict()
selectedMirror = ""


def ascii():
    print("""\
 ___ _____   _   ____    __  __ _ ___ ___  __  ___ 
| _ )__ / |_| |_|__ /_ _|  \/  / | _ \ _ \/  \| _ \\
| _ \|_ \  _|  _||_ \ '_| |\/| | |   /   / () |   /
|___/___/\__|\__|___/_| |_|  |_|_|_|_\_|_\\\\__/|_|_\\
  
better-mirror 1.0.0 - H31iUMx49
https://github.com/heinthanth/better-mirror

    """)


def help():
    ascii()
    print("usage: better-mirror [option] [mode]")
    print("\noptions:")
    print("\t-c, --choose\t: perform mirror choosing")
    print("\t-h, --help\t: display help message")
    print("\t-s, --src\t: enable source repository")
    print()
    print("modes:")
    print("\t-v, --verbose\t: enable verbose mode")
    print()


def measurelatency(hostname):
    res = ""
    p = subprocess.Popen(['ping', '-c 4', hostname],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    res = [x.decode('utf-8') for x in p]
    if not res[0]:
        results[hostname] = 9999
        res = "\033[31merror\033[0m"
    else:
        latencies = re.findall(r'time=([0-9\.]*)\sms', res[0])
        latencies = list(map(float, latencies))
        average = sum(latencies) / len(latencies)
        results[hostname] = average
        res = "\033[32m" + str(round(average, 2)) + " ms\033[0m"

    if verboseMode:
        print("\033[33m[*]\033[0m pinging \033[32m{hostname}\033[0m ... latency {latency}".format(
            hostname=hostname, latency=res))


def main():
    # get list of mirror from meta4 file
    meta_xml = urllib.request.urlopen("http://http.kali.org/README.meta4")
    lists = xmltodict.parse(meta_xml)

    print("\033[33m[*]\033[0m calculating the mirror latency ...")
    for info in lists["metalink"]["file"]["url"]:
        url = urllib.parse.urlparse(info["#text"])
        hostlist[url.netloc] = str(url.path).replace("/README", "")
        thread = Thread(target=measurelatency, args=[url.netloc])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    if verboseMode:
        print("\033[33m[*]\033[0m finding the best mirror ...")
    result = sorted(results.items(), key=lambda item: item[1])

    selected = result[0]
    print("\033[33m[*]\033[0m found! the selected mirror: \033[32m{}\033[0m ... latency \033[32m{} ms\033[0m".format(
        selected[0], round(selected[1], 3)))
    selectedMirror = selected[0]

    if verboseMode:
        print(
            "\033[33m[*]\033[0m backuping original /etc/apt/sources.list to /etc/apt/sources.list.bak")
    os.popen('cp /etc/apt/sources.list /etc/apt/sources.list.bak')

    print("\033[33m[*]\033[0m updating /etc/apt/sources.list")
    newcontent = []
    try:
        read_only_sources_list = open("/etc/apt/sources.list", "r")
        for line in read_only_sources_list:
            if(re.search(r'# add with better-mirror', line)):
                # will skip this line
                pass
            elif re.search(r'^deb http(?:s|)://(.*)/kali kali-rolling', line):
                newcontent.append("\n# " + line)
            elif re.search(r'^deb-src http(?:s|)://(.*)/kali kali-rolling', line):
                newcontent.append("# " + line + "\n")
            elif re.search(r'^#\s*deb http(?:s|)://(.*)/kali kali-rolling', line):
                newcontent.append("\n" + line)
            elif re.search(r'^#\s*deb-src http(?:s|)://(.*)/kali kali-rolling', line):
                newcontent.append(line + "\n")
            elif line.strip() == "":
                pass
            else:
                newcontent.append(line)
        newcontent.append("\ndeb http://{hostname}{path} kali-rolling main non-free contrib # add with better-mirror\n".format(
            hostname=selectedMirror, path=hostlist[selectedMirror]))
        if enableSource:
            newcontent.append("deb-src http://{hostname}{path} kali-rolling main non-free contrib # add with better-mirror\n".format(
                hostname=selectedMirror, path=hostlist[selectedMirror]))
    except PermissionError:
        sys.exit(
            "\033[31m[*] unsufficient permission ... cannot open /etc/apt/sources.list\033[0m")
    finally:
        read_only_sources_list.close()

    try:
        source_list = open("/etc/apt/sources.list", "w")
        for line in newcontent:
            source_list.writelines(line)
    except PermissionError:
        sys.exit(
            "\033[31m[*] unsufficient permission ... cannot write /etc/apt/sources.list\033[0m")
    finally:
        source_list.close()

    print("\033[33m[*]\033[0m performing 'apt-get update' for you")
    if verboseMode:
        os.system("apt-get update")
    else:
        os.system("apt-get update -qq")
    print("\033[33m[*]\033[0m Done!")


if len(sys.argv) == 1:
    help()
    exit(1)
else:
    # parse the argument
    if "-h" in sys.argv or "--help" in sys.argv:
        help()
        exit(0)
    if "-v" in sys.argv or "--verbose" in sys.argv:
        verboseMode = True
    if "-s" in sys.argv or "--src" in sys.argv:
        enableSource = True
    if "-c" in sys.argv or "--choose" in sys.argv:
        ascii()
        main()
    else:
        help()
        exit(1)
