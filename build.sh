#!/usr/bin/env bash
mkdir -p ./better-mirror/usr/bin
cp better-mirror.py ./better-mirror/usr/bin/better-mirror

dpkg -b ./better-mirror ./better-mirror.deb