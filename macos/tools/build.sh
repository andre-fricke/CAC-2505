#!/bin/sh
set -eu
cd "$(dirname "$0")"
for name in CAC-Mac-Typ-RAM CAC-VRR-RAM-Test CAC-Mac-Baseline; do
  xcrun swiftc "$name.swift" -framework IOKit -o "$name"
done
