import hashlib

import pytest

from stc_piper_voice import installer as inst


def make_release(tmp_path, corrupt=False):
    rel = tmp_path / "release"
    rel.mkdir()
    lines = []
    for name in inst.FILES:
        data = f"data for {name}".encode("utf-8")
        (rel / name).write_bytes(data)
        lines.append(f"{hashlib.sha256(data).hexdigest()}  {name}")
    (rel / inst.SUMS).write_text("\n".join(lines) + "\n", encoding="utf-8")
    if corrupt:
        (rel / inst.FILES[0]).write_bytes(b"tampered")
    return rel.as_uri()


def test_parse_sums():
    assert inst.parse_sums("ABC  a.onnx\nDEF *b.json\n\n") == {"a.onnx": "abc", "b.json": "def"}


def test_release_urls():
    assert inst.release_base_url().endswith("/releases/latest/download")
    assert inst.release_base_url("v1.0.0").endswith("/releases/download/v1.0.0")


def test_install_local(tmp_path):
    dest = tmp_path / "piper"
    rc = inst.main(["install", "--base-url", make_release(tmp_path), "--dest", str(dest)])
    assert rc == 0
    assert sorted(p.name for p in dest.iterdir()) == sorted(inst.FILES)


def test_checksum_mismatch_installs_nothing(tmp_path, capsys):
    dest = tmp_path / "piper"
    rc = inst.main(["install", "--base-url", make_release(tmp_path, corrupt=True), "--dest", str(dest)])
    assert rc == 1
    assert "Checksum mismatch" in capsys.readouterr().err
    assert not dest.exists()


def test_needs_a_destination(capsys):
    assert inst.main(["install"]) == 1
    assert "--dest" in capsys.readouterr().err


def test_dry_run_downloads_nothing(tmp_path, capsys):
    dest = tmp_path / "piper"
    assert inst.main(["install", "--dry-run", "--dest", str(dest)]) == 0
    assert not dest.exists()


def test_missing_release_is_a_clean_error(tmp_path, capsys):
    rc = inst.main(["install", "--base-url", (tmp_path / "nope").as_uri(), "--dest", str(tmp_path / "d")])
    assert rc == 1
    assert "Could not download" in capsys.readouterr().err


def test_scp_command(tmp_path):
    cmd = inst.scp_command([tmp_path / "a", tmp_path / "b"], "root@ha:/share/piper")
    assert cmd[0] == "scp" and cmd[-1] == "root@ha:/share/piper/"
