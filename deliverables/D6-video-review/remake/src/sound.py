"""Soundtrack synthesizer: renders a WAV from the page's cue list (window.CUES).
Everything is synthesized here (no samples, no licensed music), so every hit lands on its frame.
Cue kinds: beat (music bed: kick/hat/bass, with sidechain pump), pad (chord), kick, snare, hat,
whoosh, riser, impact, pop, click, type, ding, swell, tick.
Usage: python3 sound.py cues.json out.wav
"""
import json, sys, wave
import numpy as np

SR = 48000
spec = json.load(open(sys.argv[1]))
start, end = spec.get("start", 0), spec.get("end", spec["dur"])
N = int((end - start) * SR) + SR
mix = {k: np.zeros(N) for k in ("drums", "music", "fx")}
duck = np.ones(N)
rng = np.random.default_rng(3)

def at(t): return int((t - start) * SR)
def env_exp(n, tau): return np.exp(-np.arange(n) / (tau * SR))
def lp(x, a):  # one-pole low-pass, a in (0,1): higher = brighter
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s += a * (x[i] - s); y[i] = s
    return y
def lp_sweep(x, a0, a1):
    y = np.empty_like(x); s = 0.0; a = np.geomspace(max(a0, 1e-4), max(a1, 1e-4), len(x))
    for i in range(len(x)): s += a[i] * (x[i] - s); y[i] = s
    return y
def hp(x, a): return x - lp(x, a)
def add(bus, t, sig, g=1.0):
    i = at(t)
    if i >= N or i + len(sig) <= 0: return
    j0 = max(0, -i); sig = sig[j0:]; i = max(i, 0); n = min(len(sig), N - i)
    mix[bus][i:i + n] += g * sig[:n]
def note(m): return 440.0 * 2 ** ((m - 69) / 12)

def kick(g=1.0, dur=0.42):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = 48 + 110 * np.exp(-tt / 0.028)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * env_exp(n, 0.16) + 0.25 * rng.standard_normal(n) * env_exp(n, 0.003)
    return g * np.tanh(1.6 * s)
def snare():
    n = int(0.25 * SR); tt = np.arange(n) / SR
    nz = hp(rng.standard_normal(n), 0.25) * env_exp(n, 0.06)
    return 0.7 * nz + 0.35 * np.sin(2 * np.pi * 190 * tt) * env_exp(n, 0.04)
def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    return 0.32 * hp(rng.standard_normal(n), 0.6) * env_exp(n, 0.05 if open_ else 0.012)
def whoosh(d=0.45, up=True):
    n = int(d * SR); x = rng.standard_normal(n)
    y = lp_sweep(x, 0.01, 0.35) if up else lp_sweep(x, 0.35, 0.01)
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.5
    return 1.4 * y * e
def riser(d=1.0):
    n = int(d * SR); tt = np.arange(n) / SR
    y = lp_sweep(rng.standard_normal(n), 0.005, 0.4) * (tt / d) ** 2
    s = np.sin(2 * np.pi * np.cumsum(np.geomspace(200, 1400, n)) / SR) * (tt / d) ** 3 * 0.25
    return 0.9 * (y + s)
def impact():
    n = int(1.6 * SR); tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-tt / 0.05)) / SR) * env_exp(n, 0.5)
    nz = lp(rng.standard_normal(n), 0.2) * env_exp(n, 0.15)
    return np.tanh(1.3 * (boom + 0.5 * nz))
def pop(f=700):
    n = int(0.09 * SR); tt = np.arange(n) / SR
    return 0.5 * np.sin(2 * np.pi * np.cumsum(np.linspace(f, f * 1.5, n)) / SR) * env_exp(n, 0.025)
def click():
    n = int(0.02 * SR)
    return 0.6 * hp(rng.standard_normal(n), 0.5) * env_exp(n, 0.002)
def type_tick():
    n = int(0.03 * SR)
    return 0.22 * lp(hp(rng.standard_normal(n), 0.3), 0.5) * env_exp(n, 0.004)
def tick():
    n = int(0.04 * SR); tt = np.arange(n) / SR
    return 0.25 * np.sin(2 * np.pi * 2400 * tt) * env_exp(n, 0.006)
def ding():
    n = int(1.4 * SR); tt = np.arange(n) / SR
    return 0.28 * (np.sin(2 * np.pi * 1318.5 * tt) + 0.6 * np.sin(2 * np.pi * 1975.5 * tt) + 0.2 * np.sin(2 * np.pi * 2637 * tt)) * env_exp(n, 0.35)
def swell(d=1.2):
    n = int(d * SR); tt = np.arange(n) / SR
    return 0.5 * lp(rng.standard_normal(n), 0.05) * (tt / d) ** 2 * np.exp(-np.maximum(0, tt - d * .9) * 30)
def saw(f, n):
    tt = np.arange(n) / SR
    return 2 * ((tt * f) % 1) - 1
def pad(t0, t1, notes, g=0.12, bright=0.04):
    n = int((t1 - t0) * SR); s = np.zeros(n)
    for m in notes:
        for det in (-0.08, 0.0, 0.08):
            s += saw(note(m + det), n)
    s = lp(s / (len(notes) * 3), bright)
    a = np.minimum(1, np.arange(n) / (0.35 * SR)) * np.minimum(1, (n - np.arange(n)) / (0.4 * SR))
    add("music", t0, s * a, g * 6)

for c in spec["cues"]:
    k, t = c["k"], c.get("t", 0)
    g = c.get("g", 1.0)
    if k == "beat":  # music bed with kick on the beat, offbeat hats, a bass line and sidechain pump
        bpm, t0, t1 = c["bpm"], c["t0"], c["t1"]; b = 60 / bpm; roots = c.get("roots", [45])
        i = 0; tb = t0
        while tb < t1 - 1e-6:
            if c.get("kick", True): add("drums", tb, kick(0.9 * g))
            j = at(tb); n = int(0.28 * SR)
            if 0 <= j < N: duck[j:j + n] = np.minimum(duck[j:j + n], 0.35 + 0.65 * (1 - np.exp(-np.arange(min(n, N - j)) / (0.07 * SR))))
            if c.get("hats", True): add("drums", tb + b / 2, hat(i % 4 == 3))
            if c.get("snare", False) and i % 2 == 1: add("drums", tb, snare(), 0.8)
            r = roots[(i // 4) % len(roots)]
            nb = int(b * 0.9 * SR); bass = lp(saw(note(r), nb), 0.02) * env_exp(nb, 0.25)
            add("music", tb + b / 2, bass, 0.9 * g)
            i += 1; tb += b
    elif k == "pad": pad(c["t0"], c["t1"], c["notes"], c.get("g", 0.12), c.get("bright", 0.04))
    elif k == "kick": add("drums", t, kick(g))
    elif k == "snare": add("drums", t, snare(), g)
    elif k == "hat": add("drums", t, hat(), g)
    elif k == "whoosh":
        d = c.get("d", 0.45); add("fx", t - d * 0.6, whoosh(d, c.get("up", True)), 0.6 * g)
    elif k == "riser":
        d = c.get("d", 1.0); add("fx", t - d, riser(d), 0.5 * g)
    elif k == "impact": add("fx", t, impact(), g)
    elif k == "pop": add("fx", t, pop(c.get("f", 700)), g)
    elif k == "click": add("fx", t, click(), g)
    elif k == "type": add("fx", t, type_tick(), g)
    elif k == "tick": add("fx", t, tick(), g)
    elif k == "ding": add("fx", t, ding(), g)
    elif k == "swell":
        d = c.get("d", 1.2); add("fx", t - d, swell(d), g)

out = mix["drums"] * 0.8 + mix["music"] * duck * 0.7 + mix["fx"] * 0.9
out = np.tanh(out * 1.3) / np.tanh(1.3)
fade = int(0.35 * SR); last = at(end)
out[max(0, last - fade):last] *= np.linspace(1, 0, min(fade, last))
out = out[:last]
out = out / (np.max(np.abs(out)) + 1e-9) * 0.89
st = np.stack([out, out], 1)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype(np.int16).tobytes())
