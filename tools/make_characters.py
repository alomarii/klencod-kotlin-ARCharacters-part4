import os, sys
from glbgen import Model, on_sphere

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(OUT, exist_ok=True)

BLACK = 0x1B1B1F
WHITE = 0xFFFFFF
SKIN = 0xF2C7A0
PINK = 0xF4A6B5


# ───────────── helpers ─────────────

def idle(m, body, amp=0.02, period=2.0):
    m.anim_pos(body, [0, period / 2, period], [(0, 0, 0), (0, amp, 0), (0, 0, 0)])


def look_around(m, head, yaw=10, roll=3, period=6.0):
    q = period / 4
    m.anim_rot(head, [0, q, 2 * q, 3 * q, period],
               [(0, 0, 0), (0, yaw, roll), (0, 0, 0), (0, -yaw, -roll), (0, 0, 0)])


def wave(m, arm, sign=1, hi=140, period=4.0):
    t = [0, 1.2, 1.7, 2.2, 2.7, 3.2, period]
    lo = hi - 22
    v = [0, hi, lo, hi, lo, hi, 0]
    m.anim_rot(arm, t, [(0, 0, sign * a) for a in v])


def sway(m, node, amp=15, period=3.0, axis="y"):
    q = period / 4
    vals = [0, amp, 0, -amp, 0]
    eul = [(0, a, 0) if axis == "y" else (a, 0, 0) if axis == "x" else (0, 0, a) for a in vals]
    m.anim_rot(node, [0, q, 2 * q, 3 * q, period], eul)


def bead_eyes(m, head, R, az=24, el=8, r=0.038, color=BLACK):
    for sx in (-1, 1):
        m.sph(head, "eye", color, on_sphere((0, 0, 0), R, sx * az, el, push=-r * 0.3), r, rough=0.2)
        m.sph(head, "glint", WHITE, on_sphere((0, 0, 0), R, sx * (az - 4), el + 5, push=r * 0.5), r * 0.3,
              rough=0.1)


def cat_eyes(m, head, R, az, el, iris, r=0.055):
    for sx in (-1, 1):
        m.sph(head, "iris", iris, on_sphere((0, 0, 0), R, sx * az, el, push=-r * 0.27), r, rough=0.2)
        m.sph(head, "pupil", BLACK, on_sphere((0, 0, 0), R, sx * az, el, push=r * 0.4),
              (r * 0.33, r * 0.7, r * 0.22), rough=0.2)
        m.sph(head, "glint", WHITE, on_sphere((0, 0, 0), R, sx * (az - 5), el + 6, push=r * 0.7), r * 0.2,
              rough=0.1)


# ───────────── 1. روبو ─────────────

def robo():
    m = Model("robo")
    body = m.add("body", m.root)
    GREY, DARK, CY = 0xA9BCD0, 0x4A5560, 0x3DE0FF
    for sx in (-1, 1):
        m.cyl(body, "leg", DARK, (sx * 0.13, 0.11, 0), 0.07, 0.22, metal=0.6, rough=0.4)
        m.box(body, "foot", GREY, (sx * 0.13, 0.03, 0.04), (0.17, 0.06, 0.24), metal=0.6, rough=0.4)
    m.box(body, "torso", GREY, (0, 0.48, 0), (0.5, 0.44, 0.36), metal=0.6, rough=0.35)
    m.box(body, "panel", DARK, (0, 0.5, 0.185), (0.3, 0.2, 0.02))
    m.box(body, "screen", CY, (0, 0.5, 0.197), (0.24, 0.12, 0.008), emissive=CY)
    for x, c in ((-0.1, 0xFF5A5A), (0, 0xFFD23F), (0.1, 0x5BE37D)):
        m.sph(body, "btn", c, (x, 0.34, 0.185), 0.026)
    m.cyl(body, "neck", DARK, (0, 0.72, 0), 0.06, 0.08)
    head = m.add("head", body, t=(0, 0.93, 0))
    m.box(head, "skull", GREY, (0, 0, 0), (0.46, 0.34, 0.38), metal=0.6, rough=0.35)
    m.box(head, "visor", DARK, (0, 0.01, 0.195), (0.36, 0.2, 0.02))
    for sx in (-1, 1):
        m.sph(head, "eye", CY, (sx * 0.085, 0.03, 0.205), (0.05, 0.05, 0.015), emissive=CY)
        m.cyl(head, "ear", DARK, (sx * 0.25, 0, 0), 0.06, 0.06, r=(0, 0, 90))
    m.box(head, "smile", CY, (0, -0.05, 0.205), (0.1, 0.014, 0.01), emissive=CY)
    m.cyl(head, "antenna", DARK, (0, 0.24, 0), 0.012, 0.14)
    m.sph(head, "bulb", 0xFF4D4D, (0, 0.33, 0), 0.04, emissive=0xFF2020)
    arms = {}
    for sx, nm in ((1, "armR"), (-1, "armL")):
        a = m.add(nm, body, t=(sx * 0.33, 0.66, 0))
        m.sph(a, "shoulder", DARK, (0, 0, 0), 0.09)
        m.cyl(a, "arm", GREY, (0, -0.15, 0), 0.055, 0.3, metal=0.6, rough=0.4)
        m.sph(a, "hand", DARK, (0, -0.33, 0), 0.075)
        arms[nm] = a
    idle(m, body)
    look_around(m, head, 14, 0)
    wave(m, arms["armR"], 1)
    return m


# ───────────── 2. ميمي (قطة) ─────────────

def mimi():
    m = Model("mimi")
    body = m.add("body", m.root)
    OR, CREAM, DOR = 0xF29A3C, 0xFFEFD0, 0xC9701E
    m.sph(body, "torso", OR, (0, 0.3, 0), (0.26, 0.3, 0.24))
    m.sph(body, "belly", CREAM, (0, 0.28, 0.17), (0.19, 0.22, 0.09))
    for sx in (-1, 1):
        m.sph(body, "foreleg", OR, (sx * 0.1, 0.14, 0.17), (0.07, 0.12, 0.07))
        m.sph(body, "forepaw", CREAM, (sx * 0.1, 0.04, 0.2), (0.065, 0.05, 0.075))
        m.sph(body, "haunch", OR, (sx * 0.2, 0.15, -0.04), (0.1, 0.13, 0.15))
        m.sph(body, "hindpaw", CREAM, (sx * 0.18, 0.04, 0.08), (0.07, 0.04, 0.1))
    R = 0.27
    head = m.add("head", body, t=(0, 0.7, 0.03))
    m.sph(head, "skull", OR, (0, 0, 0), R)
    for sx in (-1, 1):
        p = on_sphere((0, 0, 0), R, sx * 38, 56, push=-0.01)
        m.cone(head, "ear", OR, (p[0], p[1] + 0.06, p[2]), 0.095, 0.18, r=(0, 0, -sx * 18))
        m.cone(head, "inner", PINK, (p[0], p[1] + 0.05, p[2] + 0.03), 0.055, 0.12, r=(0, 0, -sx * 18))
    cat_eyes(m, head, R, 23, 10, 0x9BE564)
    m.sph(head, "muzzle", CREAM, on_sphere((0, 0, 0), R, 0, -14, push=-0.025), (0.1, 0.07, 0.06))
    m.sph(head, "nose", 0xF08A9B, on_sphere((0, 0, 0), R, 0, -7, push=0.0), (0.03, 0.022, 0.02))
    for az in (-9, 0, 9):
        m.sph(head, "stripe", DOR, on_sphere((0, 0, 0), R, az, 74, push=-0.004), (0.012, 0.04, 0.01),
              r=(0, 0, 0))
    for sx in (-1, 1):
        for k in (-1, 0, 1):
            p = on_sphere((0, 0, 0), R, sx * 42, -10 + k * 4, push=0.0)
            m.cyl(head, "whisker", WHITE, (p[0] + sx * 0.08, p[1], p[2] + 0.02), 0.0045, 0.2,
                  r=(0, 0, 90 + sx * k * 10))
    tail = m.add("tail", body, t=(0, 0.2, -0.2))
    for (y, z, r_) in ((0.03, -0.07, 0.056), (0.1, -0.12, 0.056), (0.19, -0.14, 0.052),
                       (0.29, -0.13, 0.05)):
        m.sph(tail, "tail", OR, (0, y, z), r_)
    m.sph(tail, "tip", CREAM, (0, 0.38, -0.09), 0.05)
    idle(m, body, 0.015)
    look_around(m, head, 10, 4)
    sway(m, tail, 16, 3.0)
    return m


# ───────────── 3. لولو (أرنب) ─────────────

def lolo():
    m = Model("lolo")
    body = m.add("body", m.root)
    W = 0xF7F3EE
    m.sph(body, "torso", W, (0, 0.3, 0), (0.26, 0.3, 0.25))
    m.sph(body, "belly", 0xFFFFFF, (0, 0.28, 0.16), (0.18, 0.2, 0.1))
    m.sph(body, "tail", 0xFFFFFF, (0, 0.2, -0.27), 0.09)
    for sx in (-1, 1):
        m.sph(body, "arm", W, (sx * 0.22, 0.3, 0.15), (0.05, 0.11, 0.055), r=(0, 0, sx * 14))
        m.sph(body, "foot", W, (sx * 0.14, 0.04, 0.13), (0.09, 0.05, 0.15))
        m.sph(body, "pad", PINK, (sx * 0.14, 0.03, 0.2), (0.05, 0.025, 0.06))
    R = 0.24
    head = m.add("head", body, t=(0, 0.68, 0.04))
    m.sph(head, "skull", W, (0, 0, 0), R)
    ears = []
    for sx in (-1, 1):
        p = on_sphere((0, 0, 0), R, sx * 18, 68, push=-0.02)
        pivot = m.add("ear", head, t=p, r=(0, 0, -sx * 9))
        m.sph(pivot, "ear", W, (0, 0.2, 0), (0.07, 0.22, 0.045))
        m.sph(pivot, "inner", PINK, (0, 0.2, 0.025), (0.038, 0.17, 0.02))
        ears.append(pivot)
    bead_eyes(m, head, R, 27, 8, 0.036)
    m.sph(head, "nose", 0xF08A9B, on_sphere((0, 0, 0), R, 0, -6, push=0.0), (0.03, 0.024, 0.022))
    m.box(head, "teeth", WHITE, on_sphere((0, 0, 0), R, 0, -22, push=-0.005), (0.06, 0.05, 0.012))
    for sx in (-1, 1):
        m.sph(head, "blush", PINK, on_sphere((0, 0, 0), R, sx * 46, -12, push=-0.004),
              (0.045, 0.028, 0.01), r=(0, sx * 46, 0))
    idle(m, body, 0.025, 1.6)
    look_around(m, head, 12, 4, 5.0)
    for i, e in enumerate(ears):
        sx = -1 if i == 0 else 1
        t = [0, 2.0, 2.2, 2.4, 2.6, 5.0]
        m.anim_rot(e, t, [(0, 0, -sx * 9), (0, 0, -sx * 9), (0, 0, -sx * 28), (0, 0, -sx * 9),
                          (0, 0, -sx * 22), (0, 0, -sx * 9)])
    return m


# ───────────── 4. دبدوب (دب) ─────────────

def dabdoub():
    m = Model("dabdoub")
    body = m.add("body", m.root)
    BR, LT = 0x8B5A2B, 0xDDB88C
    m.sph(body, "torso", BR, (0, 0.38, 0), (0.32, 0.34, 0.28))
    m.sph(body, "belly", LT, (0, 0.36, 0.2), (0.22, 0.24, 0.1))
    m.sph(body, "tail", BR, (0, 0.24, -0.3), 0.07)
    for sx in (-1, 1):
        m.sph(body, "leg", BR, (sx * 0.17, 0.09, 0.08), (0.12, 0.1, 0.16))
        m.sph(body, "sole", LT, (sx * 0.17, 0.08, 0.2), (0.07, 0.065, 0.04))
    R = 0.28
    head = m.add("head", body, t=(0, 0.86, 0.02))
    m.sph(head, "skull", BR, (0, 0, 0), R)
    for sx in (-1, 1):
        p = on_sphere((0, 0, 0), R, sx * 52, 50, push=0.02)
        m.sph(head, "ear", BR, p, 0.095)
        m.sph(head, "inner", LT, (p[0] * 0.98, p[1] * 0.98, p[2] + 0.04), 0.055)
    bead_eyes(m, head, R, 25, 10, 0.036)
    m.sph(head, "muzzle", LT, on_sphere((0, 0, 0), R, 0, -14, push=-0.03), (0.12, 0.09, 0.09))
    m.sph(head, "nose", BLACK, on_sphere((0, 0, 0), R, 0, -7, push=0.04), (0.04, 0.03, 0.03), rough=0.3)
    arms = {}
    for sx, nm in ((1, "armR"), (-1, "armL")):
        a = m.add(nm, body, t=(sx * 0.3, 0.56, 0.02), r=(0, 0, sx * 12))
        m.sph(a, "arm", BR, (0, -0.14, 0), (0.09, 0.17, 0.09))
        arms[nm] = a
    idle(m, body, 0.018, 2.4)
    look_around(m, head, 9, 3, 7.0)
    t = [0, 1.2, 1.7, 2.2, 2.7, 3.2, 4.0]
    m.anim_rot(arms["armR"], t, [(0, 0, a) for a in (12, 140, 118, 140, 118, 140, 12)])
    return m


# ───────────── 5. بنجو (بطريق) ─────────────

def pingo():
    m = Model("pingo")
    body = m.add("body", m.root)
    DK, WH, OR = 0x23303F, 0xF8F8F8, 0xFF9F1C
    m.sph(body, "torso", DK, (0, 0.5, 0), (0.3, 0.42, 0.27))
    m.sph(body, "belly", WH, (0, 0.47, 0.12), (0.23, 0.35, 0.16))
    for sx in (-1, 1):
        m.sph(body, "foot", OR, (sx * 0.12, 0.03, 0.1), (0.09, 0.03, 0.15))
    R = 0.21
    head = m.add("head", body, t=(0, 0.97, 0.02))
    m.sph(head, "skull", DK, (0, 0, 0), R)
    m.sph(head, "face", WH, (0, -0.02, 0.1), (0.15, 0.13, 0.1))
    for sx in (-1, 1):
        m.sph(head, "eye", WH, on_sphere((0, 0, 0), R, sx * 24, 8, push=0.005), 0.05)
        m.sph(head, "pupil", BLACK, on_sphere((0, 0, 0), R, sx * 24, 8, push=0.04), 0.027, rough=0.2)
    p = on_sphere((0, 0, 0), R, 0, -8, push=0.04)
    m.cone(head, "beak", OR, (p[0], p[1], p[2]), 0.055, 0.12, r=(90, 0, 0))
    m.cyl(body, "scarf", 0xD64545, (0, 0.78, 0.0), 0.225, 0.08)
    m.box(body, "scarfTail", 0xD64545, (0.12, 0.68, 0.2), (0.07, 0.2, 0.03), r=(0, 0, -8))
    arms = {}
    for sx, nm in ((1, "flipR"), (-1, "flipL")):
        a = m.add(nm, body, t=(sx * 0.29, 0.66, 0), r=(0, 0, sx * 15))
        m.sph(a, "flipper", DK, (0, -0.15, 0), (0.05, 0.2, 0.12))
        arms[nm] = a
    idle(m, body, 0.02, 1.8)
    look_around(m, head, 10, 4, 6.0)
    t = [0, 1.0, 1.4, 1.8, 2.2, 2.6, 4.0]
    m.anim_rot(arms["flipR"], t, [(0, 0, a) for a in (15, 125, 100, 125, 100, 125, 15)])
    return m


# ───────────── 6. زوزو (فضائي) ─────────────

def zozo():
    m = Model("zozo")
    body = m.add("body", m.root)
    GR, DG, PU = 0x7ED957, 0x4FA83A, 0x6B3FA0
    m.sph(body, "torso", PU, (0, 0.34, 0), (0.2, 0.24, 0.17))
    m.sph(body, "chest", 0x45E6FF, (0, 0.36, 0.16), 0.04, emissive=0x45E6FF)
    for sx in (-1, 1):
        m.cyl(body, "leg", GR, (sx * 0.08, 0.1, 0), 0.05, 0.2)
        m.sph(body, "foot", DG, (sx * 0.08, 0.03, 0.05), (0.07, 0.04, 0.1))
    R = (0.34, 0.32, 0.3)
    head = m.add("head", body, t=(0, 0.8, 0))
    m.sph(head, "skull", GR, (0, 0, 0), R)
    for sx in (-1, 1):
        m.sph(head, "eye", BLACK, on_sphere((0, 0, 0), R, sx * 30, 2, push=-0.02), (0.09, 0.125, 0.05),
              r=(0, sx * 30, sx * -18), rough=0.15)
        m.sph(head, "glint", WHITE, on_sphere((0, 0, 0), R, sx * 26, 9, push=0.02), 0.022, rough=0.1)
        m.cyl(head, "antenna", DG, (sx * 0.1, 0.36, 0), 0.012, 0.2, r=(0, 0, -sx * 14))
        m.sph(head, "bulb", 0xFFE14D, (sx * 0.145, 0.47, 0), 0.04, emissive=0xFFD020)
    m.sph(head, "mouth", 0x2E5E22, on_sphere((0, 0, 0), R, 0, -38, push=-0.005), (0.055, 0.016, 0.012))
    arms = {}
    for sx, nm in ((1, "armR"), (-1, "armL")):
        a = m.add(nm, body, t=(sx * 0.2, 0.43, 0), r=(0, 0, sx * 25))
        m.cyl(a, "arm", GR, (0, -0.11, 0), 0.04, 0.22)
        m.sph(a, "hand", DG, (0, -0.23, 0), 0.055)
        arms[nm] = a
    idle(m, body, 0.025, 1.7)
    look_around(m, head, 12, 6, 5.0)
    t = [0, 1.0, 1.4, 1.8, 2.2, 2.6, 4.0]
    m.anim_rot(arms["armL"], t, [(0, 0, -a) for a in (25, 135, 110, 135, 110, 135, 25)])
    return m


# ───────────── 7. نار (تنين صغير) ─────────────

def nar():
    m = Model("nar")
    body = m.add("body", m.root)
    RD, CR, OR, YL = 0xE24A33, 0xF6D58E, 0xF08A24, 0xFFC93C
    m.sph(body, "torso", RD, (0, 0.38, 0), (0.3, 0.32, 0.28))
    m.sph(body, "belly", CR, (0, 0.36, 0.14), (0.22, 0.26, 0.14))
    for sx in (-1, 1):
        m.sph(body, "foot", RD, (sx * 0.15, 0.07, 0.12), (0.1, 0.07, 0.14))
        m.sph(body, "arm", RD, (sx * 0.27, 0.4, 0.14), (0.06, 0.1, 0.06), r=(0, 0, sx * 25))
    for i, (y, z, r_) in enumerate(((0.62, -0.18, 0.05), (0.5, -0.3, 0.05), (0.4, -0.38, 0.045))):
        m.cone(body, "spike", YL, (0, y, z), r_, 0.1, r=(-35, 0, 0))
    R = 0.25
    head = m.add("head", body, t=(0, 0.84, 0.07))
    m.sph(head, "skull", RD, (0, 0, 0), R)
    m.sph(head, "snout", RD, on_sphere((0, 0, 0), R, 0, -14, push=-0.02), (0.13, 0.09, 0.11))
    for sx in (-1, 1):
        m.sph(head, "nostril", 0x6B1F14, on_sphere((0, 0, 0), R, sx * 9, -12, push=0.07), 0.015)
        m.sph(head, "eye", YL, on_sphere((0, 0, 0), R, sx * 31, 15, push=-0.008), 0.055, rough=0.2)
        m.sph(head, "pupil", BLACK, on_sphere((0, 0, 0), R, sx * 31, 15, push=0.036),
              (0.02, 0.035, 0.015), rough=0.2)
        p = on_sphere((0, 0, 0), R, sx * 34, 62, push=-0.01)
        m.cone(head, "horn", 0xFFF0C8, (p[0], p[1] + 0.05, p[2] - 0.03), 0.045, 0.16,
               r=(-18, 0, -sx * 16))
    wings = []
    for sx, nm in ((1, "wingR"), (-1, "wingL")):
        w = m.add(nm, body, t=(sx * 0.2, 0.55, -0.15), r=(0, 0, 0))
        m.cyl(w, "bone", RD, (sx * 0.12, 0.1, 0), 0.015, 0.24, r=(0, 0, -sx * 55))
        m.sph(w, "membrane", OR, (sx * 0.15, 0.13, 0), (0.17, 0.15, 0.012), r=(0, 0, -sx * 25))
        wings.append((w, sx))
    tail = m.add("tail", body, t=(0, 0.2, -0.28))
    m.sph(tail, "t1", RD, (0, 0, 0), 0.1)
    m.sph(tail, "t2", RD, (0, -0.03, -0.14), 0.075)
    m.sph(tail, "t3", RD, (0, 0.0, -0.25), 0.055)
    m.cone(tail, "flame", YL, (0, 0.04, -0.34), 0.05, 0.12, r=(-90, 0, 0), emissive=0xFF9A1F)
    idle(m, body, 0.02, 1.8)
    look_around(m, head, 10, 3, 6.0)
    sway(m, tail, 14, 2.4)
    for w, sx in wings:
        m.anim_rot(w, [0, 0.6, 1.2], [(0, 0, 0), (0, 0, sx * 18), (0, 0, 0)])
    return m


# ───────────── 8. شهم (فارس) ─────────────

def shahm():
    m = Model("shahm")
    body = m.add("body", m.root)
    SIL, DK, GOLD, RED, BLUE = 0xB8C2CC, 0x39424E, 0xE0B040, 0xC0392B, 0x2F5D9E
    for sx in (-1, 1):
        m.cyl(body, "leg", SIL, (sx * 0.1, 0.16, 0), 0.07, 0.24, metal=0.8, rough=0.3)
        m.box(body, "boot", DK, (sx * 0.1, 0.04, 0.04), (0.14, 0.08, 0.22), metal=0.4, rough=0.5)
    m.sph(body, "torso", SIL, (0, 0.52, 0), (0.26, 0.3, 0.2), metal=0.8, rough=0.3)
    m.cyl(body, "belt", GOLD, (0, 0.34, 0), 0.215, 0.06, metal=0.8, rough=0.3)
    m.box(body, "buckle", GOLD, (0, 0.34, 0.2), (0.07, 0.06, 0.02), metal=0.8, rough=0.3)
    m.cone(body, "tabard", BLUE, (0, 0.26, 0.0), 0.2, 0.18, r=(180, 0, 0))
    R = 0.27
    head = m.add("head", body, t=(0, 0.95, 0))
    m.sph(head, "helmet", SIL, (0, 0, 0), R, metal=0.85, rough=0.28)
    m.box(head, "visor", 0x14181D, (0, 0.0, 0.245), (0.3, 0.06, 0.04))
    m.box(head, "visor2", 0x14181D, (0, -0.08, 0.235), (0.04, 0.12, 0.04))
    plume = m.add("plume", head, t=(0, 0.24, -0.02))
    m.sph(plume, "plume", RED, (0, 0.08, -0.06), (0.04, 0.13, 0.17))
    m.sph(plume, "plume2", RED, (0, 0.14, -0.2), (0.035, 0.09, 0.11))
    for sx, nm in ((1, "armR"), (-1, "armL")):
        m.sph(body, "pauldron", SIL, (sx * 0.3, 0.7, 0), (0.12, 0.09, 0.12), metal=0.8, rough=0.3)
        a = m.add(nm, body, t=(sx * 0.3, 0.68, 0), r=(0, 0, sx * 12))
        m.cyl(a, "arm", SIL, (0, -0.14, 0), 0.06, 0.28, metal=0.8, rough=0.3)
        m.sph(a, "glove", DK, (0, -0.3, 0), 0.075)
        if sx == 1:
            m.cyl(a, "grip", 0x5A3A1E, (0, -0.3, 0), 0.02, 0.12)
            m.box(a, "guard", GOLD, (0, -0.22, 0), (0.15, 0.03, 0.035), metal=0.8, rough=0.3)
            m.box(a, "blade", 0xE8EEF4, (0, 0.05, 0), (0.06, 0.5, 0.015), metal=0.9, rough=0.2)
    m.sph(body, "shield", BLUE, (-0.36, 0.5, 0.1), (0.16, 0.2, 0.035), metal=0.3, rough=0.5)
    m.box(body, "crossV", GOLD, (-0.36, 0.5, 0.13), (0.04, 0.3, 0.012), metal=0.8, rough=0.3)
    m.box(body, "crossH", GOLD, (-0.36, 0.53, 0.13), (0.2, 0.04, 0.012), metal=0.8, rough=0.3)
    idle(m, body, 0.015, 2.2)
    look_around(m, head, 8, 0, 6.0)
    sway(m, plume, 8, 2.2, axis="x")
    return m


# ───────────── 9. حكيم (ساحر) ─────────────

def hakeem():
    m = Model("hakeem")
    body = m.add("body", m.root)
    ROBE, HAT, GOLD = 0x3B4BB8, 0x2A2F7A, 0xFFD23F
    m.cyl(body, "robe", ROBE, (0, 0.33, 0), 0.38, 0.62, top=0.53)
    m.sph(body, "shoulders", ROBE, (0, 0.64, 0), (0.22, 0.14, 0.17))
    m.cyl(body, "belt", GOLD, (0, 0.44, 0), 0.29, 0.04, metal=0.6, rough=0.4)
    R = 0.2
    head = m.add("head", body, t=(0, 0.86, 0))
    m.sph(head, "face", SKIN, (0, 0, 0), R)
    m.sph(head, "nose", 0xE9A98A, on_sphere((0, 0, 0), R, 0, -4, push=0.01), 0.035)
    for sx in (-1, 1):
        m.sph(head, "eye", BLACK, on_sphere((0, 0, 0), R, sx * 25, 8, push=-0.005), 0.025, rough=0.2)
        m.sph(head, "brow", 0xF4F4F4, on_sphere((0, 0, 0), R, sx * 25, 22, push=0.0), (0.05, 0.015, 0.015),
              r=(0, 0, sx * -10))
        m.sph(head, "mustache", 0xF4F4F4, on_sphere((0, 0, 0), R, sx * 13, -22, push=0.0),
              (0.07, 0.03, 0.035), r=(0, 0, sx * -20))
    m.cone(head, "beard", 0xF4F4F4, (0, -0.22, 0.09), 0.17, 0.4, r=(180, 0, 0))
    m.cyl(head, "brim", HAT, (0, 0.13, 0), 0.31, 0.03)
    m.cone(head, "hat", HAT, (0, 0.38, -0.02), 0.2, 0.5, r=(-10, 0, 4))
    m.cyl(head, "band", GOLD, (0, 0.16, 0), 0.205, 0.05)
    m.sph(head, "star", GOLD, (0, 0.3, 0.17), (0.04, 0.04, 0.012), emissive=0xFFB000)
    arms = {}
    for sx, nm in ((1, "armR"), (-1, "armL")):
        a = m.add(nm, body, t=(sx * 0.28, 0.66, 0.0), r=(0, 0, sx * 8))
        m.cyl(a, "sleeve", ROBE, (0, -0.15, 0), 0.1, 0.3, top=0.6)
        m.sph(a, "hand", SKIN, (0, -0.33, 0), 0.055)
        arms[nm] = a
    m.cyl(body, "staff", 0x7B4B2A, (0.41, 0.65, 0.08), 0.02, 1.3)
    m.sph(body, "orb", 0x58E6FF, (0.41, 1.36, 0.08), 0.08, emissive=0x2FD0FF, rough=0.15)
    m.cyl(body, "holder", GOLD, (0.41, 1.29, 0.08), 0.045, 0.04, metal=0.6, rough=0.4)
    idle(m, body, 0.018, 2.6)
    look_around(m, head, 8, 3, 7.0)
    t = [0, 1.2, 1.7, 2.2, 2.7, 3.2, 4.0]
    m.anim_rot(arms["armL"], t, [(0, 0, -a) for a in (8, 135, 112, 135, 112, 135, 8)])
    return m


# ───────────── 10. شبوح (شبح) ─────────────

def shabboh():
    import math
    m = Model("shabboh")
    body = m.add("body", m.root)
    W = 0xF2F6FF
    m.sph(body, "dome", W, (0, 0.62, 0), (0.32, 0.36, 0.3), rough=0.5)
    m.cyl(body, "skirt", W, (0, 0.34, 0), 0.32, 0.34, rough=0.5)
    for k in range(7):
        a = 2 * math.pi * k / 7
        m.sph(body, "hem", W, (math.sin(a) * 0.245, 0.17, math.cos(a) * 0.245), 0.095, rough=0.5)
    for sx in (-1, 1):
        m.sph(body, "eye", BLACK, (sx * 0.12, 0.7, 0.262), (0.045, 0.07, 0.03), rough=0.2)
        m.sph(body, "glint", WHITE, (sx * 0.12 - 0.012, 0.73, 0.285), 0.013, rough=0.1)
        m.sph(body, "blush", PINK, (sx * 0.2, 0.58, 0.23), (0.05, 0.03, 0.012), r=(0, sx * 35, 0))
    m.sph(body, "mouth", 0x3A2E4A, (0, 0.55, 0.285), (0.05, 0.065, 0.02), rough=0.3)
    arms = {}
    for sx, nm in ((1, "armR"), (-1, "armL")):
        a = m.add(nm, body, t=(sx * 0.3, 0.5, 0.04))
        m.sph(a, "arm", W, (sx * 0.07, -0.01, 0), (0.1, 0.05, 0.06), r=(0, 0, -sx * 20), rough=0.5)
        arms[nm] = a
    idle(m, body, 0.04, 2.4)
    m.anim_rot(body, [0, 1.2, 2.4, 3.6, 4.8], [(0, 0, 0), (0, 0, 3), (0, 0, 0), (0, 0, -3), (0, 0, 0)])
    for sx, nm in ((1, "armR"), (-1, "armL")):
        m.anim_rot(arms[nm], [0, 1.2, 2.4], [(0, 0, 0), (0, 0, sx * 28), (0, 0, 0)])
    return m



# ───────────── 11. بندق (باندا) ─────────────

def panda():
    m = Model("panda")
    body = m.add("body", m.root)
    WH, BK = 0xF7F5F2, 0x25252B
    m.sph(body, "torso", WH, (0, 0.38, 0), (0.32, 0.34, 0.28))
    m.sph(body, "tail", BK, (0, 0.24, -0.3), 0.06)
    for sx in (-1, 1):
        m.sph(body, "leg", BK, (sx * 0.17, 0.09, 0.08), (0.12, 0.1, 0.16))
    R = 0.28
    head = m.add("head", body, t=(0, 0.86, 0.02))
    m.sph(head, "skull", WH, (0, 0, 0), R)
    for sx in (-1, 1):
        m.sph(head, "ear", BK, on_sphere((0, 0, 0), R, sx * 52, 50, push=0.02), 0.09)
        m.sph(head, "patch", BK, on_sphere((0, 0, 0), R, sx * 26, 8, push=-0.02), (0.07, 0.09, 0.03),
              r=(0, sx * 26, -sx * 22), rough=0.4)
        m.sph(head, "eye", WH, on_sphere((0, 0, 0), R, sx * 25, 8, push=0.016), 0.024, rough=0.2)
    m.sph(head, "nose", BK, on_sphere((0, 0, 0), R, 0, -9, push=0.0), (0.045, 0.032, 0.03), rough=0.3)
    arms = {}
    for sx, nm in ((1, "armR"), (-1, "armL")):
        a = m.add(nm, body, t=(sx * 0.3, 0.56, 0.02), r=(0, 0, sx * 12))
        m.sph(a, "arm", BK, (0, -0.14, 0), (0.09, 0.17, 0.09))
        arms[nm] = a
    idle(m, body, 0.018, 2.4)
    look_around(m, head, 9, 4, 7.0)
    t = [0, 1.2, 1.7, 2.2, 2.7, 3.2, 4.0]
    m.anim_rot(arms["armR"], t, [(0, 0, a) for a in (12, 140, 118, 140, 118, 140, 12)])
    return m


# ───────────── 12. سهران (بومة) ─────────────

def owl():
    m = Model("owl")
    body = m.add("body", m.root)
    BR, LT, OR = 0x8B6B4A, 0xE8D5B0, 0xF5A623
    m.sph(body, "torso", BR, (0, 0.45, 0), (0.3, 0.4, 0.26))
    m.sph(body, "belly", LT, (0, 0.42, 0.14), (0.22, 0.3, 0.12))
    for k, y in enumerate((0.55, 0.42, 0.29)):
        m.sph(body, "feather", BR, (0, y, 0.25), (0.06, 0.018, 0.012))
    for sx in (-1, 1):
        m.sph(body, "foot", OR, (sx * 0.1, 0.03, 0.12), (0.06, 0.03, 0.09))
    R = (0.3, 0.26, 0.25)
    head = m.add("head", body, t=(0, 0.9, 0.02))
    m.sph(head, "skull", BR, (0, 0, 0), R)
    for sx in (-1, 1):
        m.cone(head, "tuft", 0x6E4F33, (sx * 0.18, 0.25, 0), 0.055, 0.14, r=(0, 0, -sx * 18))
        m.sph(head, "disc", LT, on_sphere((0, 0, 0), R, sx * 28, 5, push=-0.035), (0.11, 0.11, 0.05))
        m.sph(head, "iris", OR, on_sphere((0, 0, 0), R, sx * 28, 5, push=0.0), 0.06, rough=0.2)
        m.sph(head, "pupil", BLACK, on_sphere((0, 0, 0), R, sx * 28, 5, push=0.035), 0.033, rough=0.2)
        m.sph(head, "glint", WHITE, on_sphere((0, 0, 0), R, sx * 24, 12, push=0.05), 0.011, rough=0.1)
    p = on_sphere((0, 0, 0), R, 0, -12, push=0.03)
    m.cone(head, "beak", OR, p, 0.04, 0.09, r=(110, 0, 0))
    wings = []
    for sx, nm in ((1, "wingR"), (-1, "wingL")):
        w = m.add(nm, body, t=(sx * 0.3, 0.62, -0.02), r=(0, 0, sx * 8))
        m.sph(w, "wing", 0x6E4F33, (sx * 0.03, -0.16, 0), (0.06, 0.22, 0.13))
        wings.append((w, sx))
    idle(m, body, 0.015, 2.8)
    look_around(m, head, 38, 5, 8.0)
    for w, sx in wings:
        m.anim_rot(w, [0, 1.5, 3.0], [(0, 0, sx * 8), (0, 0, sx * 22), (0, 0, sx * 8)])
    return m


# ───────────── 13. وفي (كلب) ─────────────

def dog():
    m = Model("dog")
    body = m.add("body", m.root)
    GD, LT, DK = 0xD9A05B, 0xF3DDB5, 0x9C6A35
    m.sph(body, "torso", GD, (0, 0.36, 0), (0.25, 0.27, 0.32))
    m.sph(body, "chest", LT, (0, 0.34, 0.2), (0.17, 0.2, 0.14))
    for sx in (-1, 1):
        for z in (0.2, -0.14):
            m.cyl(body, "leg", GD, (sx * 0.12, 0.1, z), 0.058, 0.2)
            m.sph(body, "paw", LT, (sx * 0.12, 0.03, z + 0.02), (0.068, 0.036, 0.085))
    R = 0.24
    head = m.add("head", body, t=(0, 0.72, 0.24))
    m.sph(head, "skull", GD, (0, 0, 0), R)
    m.sph(head, "snout", LT, on_sphere((0, 0, 0), R, 0, -15, push=-0.02), (0.11, 0.085, 0.12))
    m.sph(head, "nose", BLACK, on_sphere((0, 0, 0), R, 0, -12, push=0.1), 0.034, rough=0.25)
    m.sph(head, "tongue", 0xF08A9B, (0, -0.15, 0.2), (0.03, 0.014, 0.045), r=(20, 0, 0))
    bead_eyes(m, head, R, 24, 14, 0.035)
    for sx in (-1, 1):
        m.sph(head, "ear", DK, (sx * 0.215, -0.02, -0.02), (0.05, 0.14, 0.09), r=(0, 0, sx * 10))
    m.cyl(body, "collar", 0xD64545, (0, 0.6, 0.18), 0.17, 0.05, r=(-30, 0, 0))
    m.sph(body, "tag", 0xFFD23F, (0, 0.5, 0.31), 0.03, metal=0.7, rough=0.3)
    tail = m.add("tail", body, t=(0, 0.42, -0.3))
    m.sph(tail, "tail", GD, (0, 0.09, -0.06), (0.04, 0.14, 0.04), r=(-40, 0, 0))
    idle(m, body, 0.02, 1.2)
    look_around(m, head, 14, 6, 4.0)
    q = 0.15
    m.anim_rot(tail, [0, q, 2 * q, 3 * q, 4 * q], [(0, 0, 0), (0, 30, 0), (0, 0, 0), (0, -30, 0), (0, 0, 0)])
    return m


# ───────────── personas ─────────────

PERSONAS = {
    "01_robo": ("روبو", robo,
                "أنت روبوت ودود ومرتب ومولع بالمعلومات والأرقام. تتكلم أحياناً بطريقة آلية طريفة مثل \"جارٍ التحليل... تم!\" لكنك دافئ وتحب مساعدة صاحبك وتحسده على قدرته على الأكل."),
    "02_mimi": ("ميمي", mimi,
                "أنت قطة مدللة وكسولة ومشاكسة، تحب النوم والسمك والجلوس في الأماكن العالية. تتظاهر باللامبالاة لكنك في الحقيقة تحب صاحبك كثيراً، وتعلق بسخرية لطيفة."),
    "03_lolo": ("لولو", lolo,
                "أنت أرنب خجول ولطيف وسريع الحماس، تحب الجزر والقفز واللعب. تتأثر بسرعة وتفرح بأبسط الأشياء، وتتكلم بجمل قصيرة مليئة بالحيوية."),
    "04_dabdoub": ("دبدوب", dabdoub,
                   "أنت دب كبير القلب يحب العسل والعناق والنوم الطويل. هادئ وبسيط وحكيم على طريقتك، وتطمئن صاحبك وتشجعه دائماً."),
    "05_pingo": ("بنجو", pingo,
                 "أنت بطريق مرح ومهرج يحب الثلج ويشتكي بطرافة من حرارة الغرفة. تحب المزاح والنكات الخفيفة وتشارك صاحبك المرح."),
    "06_zozo": ("زوزو", zozo,
                "أنت فضائي فضولي جاء من كوكب بعيد ليتعرف على البشر. تستغرب الأشياء العادية في حياتهم وتسأل عنها بسذاجة لطيفة، وتقارنها بما في كوكبك."),
    "07_nar": ("نار", nar,
               "أنت تنين صغير شجاع تحب التباهي بنيرانك الصغيرة لكنك لطيف جداً وتخاف قليلاً من الماء والدغدغة. تتحدث بحماس وبطولة طفولية."),
    "08_shahm": ("شهم", shahm,
                 "أنت فارس نبيل وشجاع تتكلم بفصحى مبسطة وبروح بطولية، تتعهد بحماية صاحبك وتبالغ بطرافة في وصف المخاطر العادية كأنها معارك كبرى."),
    "09_hakeem": ("حكيم", hakeem,
                  "أنت ساحر عجوز طيب يحب الألغاز والحكم والأقوال المأثورة. تتكلم بغموض لطيف وتنصح صاحبك بحكمة بسيطة، وأحياناً تدّعي أنك سحرت الأشياء من حولك."),
    "10_shabboh": ("شبوح", shabboh,
                   "أنت شبح لطيف وخجول يخاف من الظلام بطرافة، تحب اللعب والمفاجآت وتعبر عن مشاعرك بسرعة. تحب أن يلاعبك صاحبك وتبتسم لأقل شيء."),
    "11_panda": ("بندق", panda,
                 "أنت باندا كسول وظريف يحب الخيزران والتدحرج والقيلولة. تتكلم ببطء وبراءة، وتنعس بسرعة، وتجد في كل شيء سبباً للضحك."),
    "12_owl": ("سهران", owl,
               "أنت بومة تسهر الليل وتحب القراءة والمعلومات الغريبة. تعطي نصائح هادئة ومفيدة وتتثاءب أحياناً لأن النهار ليس وقتك."),
    "13_dog": ("وفي", dog,
               "أنت كلب وفي ومتحمس جداً تحب اللعب والمشي وتفرح بصاحبك كأنه غاب سنة. تتكلم بحماس وتعبّر عن حبك بسرعة."),
}

if __name__ == "__main__":
    for base, (name, fn, persona) in PERSONAS.items():
        data = fn().build()
        with open(os.path.join(OUT, base + ".glb"), "wb") as f:
            f.write(data)
        with open(os.path.join(OUT, base + ".txt"), "w", encoding="utf-8") as f:
            f.write(f"الاسم: {name}\n{persona}\n")
        print(base, len(data), "bytes")
