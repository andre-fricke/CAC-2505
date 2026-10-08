#!/bin/sh
set -eu
cd "$(dirname "$0")"
for name in CAC-Mac-Typ-RAM CAC-Mac-Typ-RAM-Robust CAC-Mac-Port-Lesen CAC-VRR-RAM-Test CAC-Mac-Baseline; do
  xcrun swiftc -module-cache-path "${TMPDIR:-/tmp}/cac2505-swift-module-cache" "$name.swift" -framework IOKit -o "$name"
done
