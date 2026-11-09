"""Genera los audios de ejemplo del capítulo 11 (Morse sintetizado, sin grabaciones ajenas).

Uso, desde la raíz del repositorio:
    python3 herramientas/audio11.py docs/assets/audio

Requisito: el codificador MP3 `lame`, que se llama como programa externo
(en macOS, `brew install lame`; en Debian o Ubuntu, `apt install lame`). Los
audios publicados se generaron con LAME 3.100 (64 bits). Cada clip se sintetiza en WAV
temporal (8 kHz, 16 bits, mono) con un tono de 600 Hz y flancos de coseno alzado
de 5 ms, y se codifica en MP3 mono a 8 kbit/s: 1 kB por segundo.

Clips (los indicativos son ficticios):
- 11-paris-20.mp3: PARIS PARIS a 20 ppm.
- 11-paris-farnsworth.mp3: PARIS PARIS con caracteres a 20 ppm y 10 ppm de media.
- 11-cq.mp3: CQ CQ CQ DE EA0ZZZ EA0ZZZ K a 18 ppm.
- 11-clics.mp3: VVV con flancos instantáneos y después VVV con flancos de 5 ms.
"""
import math
import os
import struct
import subprocess
import sys
import tempfile
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from morse11 import eventos, farnsworth, t_punto  # noqa: E402

OUT = sys.argv[1]
FS = 8000
TONO = 600
AMPL = 0.5


def sintetiza(texto, c_ppm, s_ppm=None, subida=0.005):
    """Muestras de audio para un texto: caracteres a c_ppm y media de s_ppm (Farnsworth)."""
    u_car = t_punto(c_ppm)
    u_esp = farnsworth(c_ppm, s_ppm) if s_ppm else u_car
    muestras = [0.0] * int(0.3 * FS)
    fase = 0
    for on, u, tipo in eventos(texto):
        d = u * (u_car if tipo == "c" else u_esp)
        n = int(round(d * FS))
        if not on:
            muestras += [0.0] * n
            continue
        m = int(subida * FS)
        for k in range(n):
            if m and k < m:
                g = 0.5 - 0.5 * math.cos(math.pi * k / m)
            elif m and k >= n - m:
                g = 0.5 - 0.5 * math.cos(math.pi * (n - 1 - k) / m)
            else:
                g = 1.0
            muestras.append(AMPL * g * math.sin(2 * math.pi * TONO * fase / FS))
            fase += 1
    return muestras


def guarda(nombre, muestras):
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "clip.wav")
        with wave.open(wav, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(FS)
            w.writeframes(b"".join(struct.pack("<h", int(32767 * s)) for s in muestras))
        destino = os.path.join(OUT, nombre)
        subprocess.run(["lame", "--quiet", "-m", "m", "-b", "8", "--resample", "8",
                        "--tt", nombre, wav, destino], check=True)
    print(f"{nombre}: {len(muestras) / FS:.1f} s, {os.path.getsize(destino) / 1024:.1f} KiB")


os.makedirs(OUT, exist_ok=True)
guarda("11-paris-20.mp3", sintetiza("PARIS PARIS", 20))
guarda("11-paris-farnsworth.mp3", sintetiza("PARIS PARIS", 20, 10))
guarda("11-cq.mp3", sintetiza("CQ CQ CQ DE EA0ZZZ EA0ZZZ K", 18))
silencio = [0.0] * int(0.8 * FS)
guarda("11-clics.mp3", sintetiza("VVV", 18, subida=0) + silencio + sintetiza("VVV", 18))
