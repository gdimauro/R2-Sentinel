"""Prova che i controlli di igiene FALLISCONO davvero.

Un controllo che non e' mai stato visto fallire non e' un controllo: e' una
speranza. Ogni regola qui sotto viene provata su un repository git usa-e-getta
in cui si commette deliberatamente la violazione.

Questi test girano in CI e non richiedono hardware.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHECK = ROOT / "scripts/ci/check_hygiene.py"


def git(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)


@pytest.fixture()
def repo(tmp_path: pathlib.Path) -> pathlib.Path:
    """Repository temporaneo con lo stesso .gitattributes/.gitignore del progetto."""
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q", ".")
    git(r, "config", "user.email", "test@r2-sentinel.local")
    git(r, "config", "user.name", "test")
    for f in (".gitattributes", ".gitignore"):
        (r / f).write_text((ROOT / f).read_text())
    (r / "README.md").write_text("# repo di prova\n")
    git(r, "add", "-A")
    git(r, "commit", "-qm", "base")
    return r


def stage(repo: pathlib.Path, path: str, content: bytes) -> None:
    p = repo / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)
    # -f perche' molte di queste violazioni sono gia' in .gitignore:
    # qui verifichiamo la SECONDA barriera, non la prima.
    git(repo, "add", "-f", path)


def run_check(repo: pathlib.Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECK), "--staged", "--root", str(repo)],
        capture_output=True, text=True,
        env={**os.environ, "R2S_ROOT": str(repo)})


# --------------------------------------------------------------------------- #
# Le regole devono fallire
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("rule,path,content", [
    ("R1", "software/vision/yolo11n.pt", b"\x80\x02fake torch weights"),
    ("R1", "software/vision/detector.onnx", b"\x08\x01fake onnx"),
    ("R1", "software/vision/detector.hef", b"HEF\x00fake hailo"),
    ("R2", "datasets/piccioni/train/img001.txt", b"0 0.5 0.5 0.2 0.2\n"),
    ("R3", "software/ros2_ws/maps/casa.pgm", b"P5\n100 100\n255\n" + b"\x00" * 100),
    ("R3", "software/ros2_ws/mappe/map_casa.yaml", b"image: casa.pgm\nresolution: 0.05\n"),
    ("R4", "software/acoustic/notte_2026_08_20.wav", b"RIFF\x00\x00\x00\x00WAVEfmt "),
    ("R4", "docs/journal/media/balcone.mp4", b"\x00\x00\x00\x18ftypmp42"),
    ("R5", ".env", b"R2S_MQTT_PASS=SuperSegreta123\n"),
    ("R5", "software/config/secrets.yaml", b"mqtt_pass: 'abcd1234efgh'\n"),
    ("R5", "software/config/broker.yaml", b"host: 10.0.0.5\npassword: hunter2hunter2\n"),
    ("R6", "cad/export/testa_pan_tilt.step", b"ISO-10303-21;\nHEADER;\n" + b"X" * 5000),
    ("R6", "cad/export/testa_pan_tilt.stl", b"solid testa\n" + b"Y" * 5000),
    ("R8", "software/acoustic/recordings/salotto.flac", b"fLaC\x00\x00"),
])
def test_regola_fallisce(repo, rule, path, content):
    stage(repo, path, content)
    r = run_check(repo)
    assert r.returncode == 1, (
        f"la regola {rule} NON ha bloccato {path}\n"
        f"stdout:\n{r.stdout}\nstderr:\n{r.stderr}")
    assert f"[{rule}]" in r.stdout, (
        f"bloccato, ma non dalla regola attesa {rule}:\n{r.stdout}")


def test_r7_binario_oltre_5mb(repo):
    """Un binario > 5 MB fuori da LFS deve fallire anche se l'estensione e' innocua."""
    stage(repo, "hardware/dump.bin", os.urandom(6 * 1024 * 1024))
    r = run_check(repo)
    assert r.returncode == 1
    assert "[R7]" in r.stdout


def test_step_come_puntatore_lfs_passa(repo):
    """Il caso legittimo: un .step gia' convertito in puntatore LFS non blocca.

    Simuliamo il puntatore invece di richiedere git-lfs installato, perche' il
    controllo deve valere anche su una macchina senza LFS (che e' proprio il
    caso pericoloso da coprire).
    """
    pointer = (b"version https://git-lfs.github.com/spec/v1\n"
               b"oid sha256:" + b"a" * 64 + b"\nsize 123456\n")
    assert len(pointer) < 200
    stage(repo, "cad/export/ok.step", pointer)
    r = run_check(repo)
    assert r.returncode == 0, r.stdout


def test_repository_pulito_passa(repo):
    stage(repo, "software/ros2_ws/src/r2s_vision/nuovo.py", b"x = 1\n")
    r = run_check(repo)
    assert r.returncode == 0, r.stdout


def test_placeholder_credenziale_non_e_falso_positivo(repo):
    """Un controllo che urla su un segnaposto viene disattivato in tre giorni."""
    stage(repo, "software/config/broker.example.yaml",
          b"host: localhost\npassword: ${R2S_MQTT_PASS}\napi_key: CHANGEME\n")
    r = run_check(repo)
    assert r.returncode == 0, f"falso positivo su segnaposto:\n{r.stdout}"


def test_env_example_ammesso(repo):
    stage(repo, ".env.example", b"R2S_MQTT_USER=\nR2S_MQTT_PASS=\n")
    r = run_check(repo)
    assert r.returncode == 0, r.stdout


def test_fixture_audio_sintetica_ammessa(repo):
    stage(repo, "tests/fixtures/audio/tono400.synth.wav", b"RIFF" + b"\x00" * 1000)
    r = run_check(repo)
    assert r.returncode == 0, r.stdout


def test_deroga_richiede_motivo(repo):
    """Una deroga senza motivo non e' una deroga: e' un buco."""
    (repo / ".ci-hygiene-allow").write_text("software/vision/yolo11n.pt\n")
    stage(repo, "software/vision/yolo11n.pt", b"fake")
    git(repo, "add", "-f", ".ci-hygiene-allow")
    r = run_check(repo)
    assert r.returncode == 1, "una deroga priva di motivazione e' stata accettata"

    (repo / ".ci-hygiene-allow").write_text(
        "software/vision/yolo11n.pt  peso di prova richiesto dal test di regressione X\n")
    git(repo, "add", "-f", ".ci-hygiene-allow")
    r = run_check(repo)
    assert r.returncode == 0, r.stdout
    assert "DEROGA" in r.stdout
