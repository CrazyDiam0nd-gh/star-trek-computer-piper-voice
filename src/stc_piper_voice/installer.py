"""Download the voice from a GitHub Release, verify it, and put it where Piper can find it.

Standard library only, so this file also works on its own:
    curl -fsSL https://raw.githubusercontent.com/CrazyDiam0nd-gh/star-trek-computer-piper-voice/main/src/stc_piper_voice/installer.py | python3 - install --dest ...
"""
import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

__version__ = "0.1.0"

REPO = "CrazyDiam0nd-gh/star-trek-computer-piper-voice"
VOICE = "en_US-ships_computer-high"
FILES = [f"{VOICE}.onnx", f"{VOICE}.onnx.json"]
SUMS = "SHA256SUMS"


class InstallError(Exception):
    """A problem the user can fix; shown without a traceback."""


def release_base_url(tag=None):
    if tag:
        return f"https://github.com/{REPO}/releases/download/{tag}"
    return f"https://github.com/{REPO}/releases/latest/download"


def parse_sums(text):
    """Parse `sha256sum` output into {filename: hexdigest}."""
    sums = {}
    for line in text.splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            sums[parts[1].strip().lstrip("*")] = parts[0].lower()
    return sums


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url, dest):
    try:
        with urllib.request.urlopen(url, timeout=60) as r, open(dest, "wb") as out:
            shutil.copyfileobj(r, out)
    except (urllib.error.URLError, OSError) as e:
        raise InstallError(
            f"Could not download {url} ({e}). Check the tag exists on the Releases page "
            "and that you are online."
        ) from e


def fetch_verified(base_url, workdir):
    """Download SHA256SUMS and the voice files into workdir; return their paths after checking hashes."""
    sums_path = Path(workdir) / SUMS
    download(f"{base_url}/{SUMS}", sums_path)
    sums = parse_sums(sums_path.read_text(encoding="utf-8"))
    paths = []
    for name in FILES:
        if name not in sums:
            raise InstallError(f"{name} is not listed in {SUMS}; the release looks incomplete.")
        path = Path(workdir) / name
        download(f"{base_url}/{name}", path)
        actual = sha256_file(path)
        if actual != sums[name]:
            raise InstallError(f"Checksum mismatch for {name} (expected {sums[name]}, got {actual}). Not installing.")
        paths.append(path)
    return paths


def install_local(paths, dest):
    dest = Path(dest).expanduser()
    dest.mkdir(parents=True, exist_ok=True)
    for p in paths:
        shutil.copy2(p, dest / p.name)
    return dest


def scp_command(paths, target):
    return ["scp", *[str(p) for p in paths], target.rstrip("/") + "/"]


def install_scp(paths, target):
    cmd = scp_command(paths, target)
    if subprocess.run(cmd).returncode != 0:
        raise InstallError(f"scp failed: {' '.join(cmd)}")


def run_install(args):
    base_url = (args.base_url or release_base_url(args.tag)).rstrip("/")
    if not args.dest and not args.scp:
        raise InstallError("Choose where to put the voice: --dest DIR (local) or --scp user@host:/share/piper (remote).")
    if args.dry_run:
        print(f"Would download {', '.join(FILES)} from {base_url}")
        print(f"and verify them against {SUMS}, then copy to {args.dest or args.scp}")
        return 0
    with tempfile.TemporaryDirectory() as tmp:
        paths = fetch_verified(base_url, tmp)
        print("Checksums OK.")
        if args.dest:
            print(f"Installed to {install_local(paths, args.dest)}")
        if args.scp:
            install_scp(paths, args.scp)
            print(f"Copied to {args.scp}")
    print(
        "Next: restart Piper. In Home Assistant also reload Settings > Devices & services > "
        f"Wyoming Protocol > Piper, then pick the voice '{VOICE}'. See the README for the speaking settings."
    )
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="stc-piper-voice", description=__doc__.split("\n")[0])
    p.add_argument("--version", action="version", version=f"stc-piper-voice {__version__}")
    sub = p.add_subparsers(dest="command", required=True)
    i = sub.add_parser("install", help="download, verify and install the voice")
    i.add_argument("--dest", help="local folder Piper reads voices from")
    i.add_argument("--scp", metavar="USER@HOST:PATH", help="copy to a remote folder with scp (e.g. root@homeassistant:/share/piper)")
    i.add_argument("--tag", help="release tag to install (default: latest)")
    i.add_argument("--base-url", help="override the download location (testing / mirrors)")
    i.add_argument("--dry-run", action="store_true", help="show what would happen without downloading")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return run_install(args)
    except InstallError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
