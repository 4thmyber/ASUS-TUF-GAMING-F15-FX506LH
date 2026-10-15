#!/usr/bin/env bash
# Validation gate, run locally and by CI. Proves the EFI is *valid*, not that it *boots*:
# boot-test on real hardware with the checklist in docs/runbook.md.
set -euo pipefail
cd "$(dirname "$0")/.."

OC_VERSION="$(cat .opencore-version)"
CACHE="${OC_CACHE:-$HOME/.cache/opencore}/$OC_VERSION"

if [ ! -d "$CACHE/Utilities/ocvalidate" ]; then
  mkdir -p "$CACHE"
  curl -fsSL -o "$CACHE/oc.zip" \
    "https://github.com/acidanthera/OpenCorePkg/releases/download/$OC_VERSION/OpenCore-$OC_VERSION-RELEASE.zip"
  unzip -oq "$CACHE/oc.zip" 'Utilities/ocvalidate/*' 'X64/EFI/*' -d "$CACHE"
  rm "$CACHE/oc.zip"
fi

case "$(uname -s)" in
  Darwin) OCV="$CACHE/Utilities/ocvalidate/ocvalidate" ;;
  *)      OCV="$CACHE/Utilities/ocvalidate/ocvalidate.linux" ;;
esac
chmod +x "$OCV"

echo "== ocvalidate $OC_VERSION"
out="$("$OCV" EFI/OC/Config.plist)"
echo "$out" | tail -n 3
echo "$out" | grep -q "No issues found"

echo "== check_efi"
python3 scripts/check_efi.py "$CACHE"
