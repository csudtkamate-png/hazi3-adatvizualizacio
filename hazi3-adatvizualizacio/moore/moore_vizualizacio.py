"""
Házi 3 – Moore törvénye: 50 év a számítógépek fejlődésében
==========================================================

Három vizualizáció egy fájlban:
  1. Tranzisztorszám a processzorokban (1971–2023) + Moore-féle trendvonal
  2. A merevlemezes tárolás ára (USD / GB), 1980–2024
  3. Videójátékok telepítési mérete (1985–2023)

Futtatás:
    py moore_vizualizacio.py
Kimenet: moore_vizualizacio.png (és egyenként diagram_1/2/3.png)

Adatforrások (kerekített, közelítő értékek):
  - Tranzisztorszám: Wikipedia – "Transistor count", Our World in Data
  - Tárolási ár: John C. McCallum – "Disk Drive Prices" / Our World in Data
  - Játékméretek: kiadói minimális gépigények, Wikipedia
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Stílus – visszafogott rács, vékony jelölők, egy fő szín
# ---------------------------------------------------------------------------
KEK = "#2a78d6"
SZURKE = "#898781"
TINTA = "#0b0b0b"
TINTA2 = "#52514e"
RACS = "#e1e0d9"
HATTER = "#fcfcfb"

plt.rcParams.update({
    "font.family": "Segoe UI",
    "font.size": 10,
    "axes.facecolor": HATTER,
    "figure.facecolor": HATTER,
    "axes.edgecolor": "#c3c2b7",
    "axes.labelcolor": TINTA2,
    "axes.titlecolor": TINTA,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": RACS,
    "grid.linewidth": 0.6,
    "xtick.color": SZURKE,
    "ytick.color": SZURKE,
})


def alcim(ax, szoveg):
    """Szürke alcím a diagram címe alatt."""
    ax.text(0, 1.02, szoveg, transform=ax.transAxes, fontsize=9.5,
            color=TINTA2, va="bottom")


# ---------------------------------------------------------------------------
# 1. adat: tranzisztorszám
# ---------------------------------------------------------------------------
tranzisztor = pd.DataFrame([
    ("Intel 4004", 1971, 2_250),
    ("Intel 8008", 1972, 3_500),
    ("Intel 8080", 1974, 4_500),
    ("Intel 8086", 1978, 29_000),
    ("Intel 80286", 1982, 134_000),
    ("Intel 80386", 1985, 275_000),
    ("Intel 80486", 1989, 1_180_000),
    ("Pentium", 1993, 3_100_000),
    ("Pentium Pro", 1995, 5_500_000),
    ("Pentium II", 1997, 7_500_000),
    ("Pentium III", 1999, 9_500_000),
    ("Pentium 4", 2000, 42_000_000),
    ("Core 2 Duo", 2006, 291_000_000),
    ("Core i7 (Nehalem)", 2008, 731_000_000),
    ("Core i7 (Sandy Bridge-E)", 2011, 2_270_000_000),
    ("Apple A11", 2017, 4_300_000_000),
    ("Apple M1", 2020, 16_000_000_000),
    ("Apple M1 Max", 2021, 57_000_000_000),
    ("Apple M2 Ultra", 2023, 134_000_000_000),
], columns=["chip", "ev", "tranzisztor"])

# Moore-féle elméleti görbe: kétévente duplázódás az Intel 4004-től
evek = np.arange(1971, 2024)
moore = 2_250 * 2 ** ((evek - 1971) / 2)

# Ténylegesen mért duplázódási idő (log-lineáris illesztés)
meredekseg = np.polyfit(tranzisztor["ev"], np.log2(tranzisztor["tranzisztor"]), 1)[0]
duplazodas = 1 / meredekseg

# ---------------------------------------------------------------------------
# 2. adat: merevlemez ára (USD / GB, nominális)
# ---------------------------------------------------------------------------
tarolas = pd.DataFrame({
    "ev":     [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024],
    "usd_gb": [437_500, 105_000, 11_200, 1_120, 11, 1.24, 0.09, 0.035, 0.016, 0.014],
})

# ---------------------------------------------------------------------------
# 3. adat: játékok telepítési mérete (GB)
# ---------------------------------------------------------------------------
jatekok = pd.DataFrame([
    ("Super Mario Bros.", 1985, 0.00004),
    ("Zelda: A Link to the Past", 1991, 0.001),
    ("Doom", 1993, 0.012),
    ("Half-Life", 1998, 0.4),
    ("World of Warcraft", 2004, 4),
    ("Crysis", 2007, 12),
    ("Skyrim", 2011, 6),
    ("The Witcher 3", 2015, 35),
    ("Red Dead Redemption 2", 2019, 150),
    ("Baldur's Gate 3", 2023, 150),
], columns=["jatek", "ev", "gb"])


# ---------------------------------------------------------------------------
# Rajzoló függvények
# ---------------------------------------------------------------------------
def diagram_tranzisztor(ax):
    ax.plot(evek, moore, color=SZURKE, lw=1.5, ls="--", zorder=1)
    ax.scatter(tranzisztor["ev"], tranzisztor["tranzisztor"], s=42,
               color=KEK, edgecolor=HATTER, linewidth=1.5, zorder=3)
    ax.set_yscale("log")
    ax.set_xlim(1968, 2026)
    ax.set_ylabel("Tranzisztorok száma (logaritmikus skála)")

    # Csak néhány mérföldkövet címkézünk
    cimkek = {"Intel 4004": (6, -14), "Pentium": (-58, 8), "Core 2 Duo": (-70, 6),
              "Apple M1": (-55, 6), "Apple M2 Ultra": (-95, 2)}
    for _, sor in tranzisztor[tranzisztor["chip"].isin(cimkek)].iterrows():
        ax.annotate(f"{sor['chip']} ({sor['ev']})", (sor["ev"], sor["tranzisztor"]),
                    xytext=cimkek[sor["chip"]], textcoords="offset points",
                    fontsize=8.5, color=TINTA)
    ax.annotate("Moore-görbe:\nkétévente duplázódás", (2003, 2_250 * 2 ** 16),
                xytext=(10, -40), textcoords="offset points", fontsize=8.5,
                color=SZURKE, style="italic")

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda y, _: {1e3: "1 ezer", 1e6: "1 millió", 1e9: "1 milliárd",
                      1e12: "1 billió"}.get(y, "")))
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())
    ax.set_title("1. Moore törvénye 50 év után is tartja magát", pad=24)
    alcim(ax, f"Tranzisztorszám processzoronként, 1971–2023 · mért duplázódási idő: "
              f"{duplazodas:.1f} év".replace(".", ","))


def diagram_tarolas(ax):
    ax.plot(tarolas["ev"], tarolas["usd_gb"], color=KEK, lw=2, zorder=2)
    ax.scatter(tarolas["ev"], tarolas["usd_gb"], s=36, color=KEK,
               edgecolor=HATTER, linewidth=1.5, zorder=3)
    ax.set_yscale("log")
    ax.set_ylabel("USD / GB (logaritmikus skála)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda y, _: f"${y:,.0f}".replace(",", " ") if y >= 1
        else f"${y:g}".replace(".", ",")))
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())

    for ev, ar, szoveg, eltolas in [(1980, 437_500, "$437 500", (8, 0)),
                                    (2024, 0.014, "$0,014", (-12, 10))]:
        ax.annotate(szoveg, (ev, ar), xytext=eltolas, textcoords="offset points",
                    fontsize=9, color=TINTA, fontweight="bold",
                    ha="left" if eltolas[0] > 0 else "right")
    szorzo = tarolas["usd_gb"].iloc[0] / tarolas["usd_gb"].iloc[-1]
    ax.set_title("2. A tárhely gyakorlatilag ingyenessé vált", pad=24)
    alcim(ax, f"Merevlemezes tárolás ára 1 GB-ra · 1980 óta kb. "
              f"{szorzo / 1e6:.0f} milliószor olcsóbb")


def diagram_jatekok(ax):
    ax.vlines(jatekok["ev"], 1e-5, jatekok["gb"], color=KEK, lw=2, alpha=0.35)
    ax.scatter(jatekok["ev"], jatekok["gb"], s=48, color=KEK,
               edgecolor=HATTER, linewidth=1.5, zorder=3)
    ax.set_yscale("log")
    ax.set_ylim(1e-5, 2_000)
    ax.set_xlim(1982, 2027)
    ax.set_ylabel("Telepítési méret (logaritmikus skála)")
    ax.yaxis.set_major_locator(mticker.FixedLocator([1e-5, 1e-3, 1e-1, 1e1, 1e3]))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda y, _: {1e-5: "10 KB", 1e-3: "1 MB", 1e-1: "100 MB",
                      1e1: "10 GB", 1e3: "1 TB"}.get(y, "")))
    ax.yaxis.set_minor_formatter(mticker.NullFormatter())

    for _, sor in jatekok.iterrows():
        # a BG3 felirata a pont fölé kerül, hogy ne ütközzön az RDR2-vel
        utolso = sor["jatek"] == "Baldur's Gate 3"
        ax.annotate(sor["jatek"], (sor["ev"], sor["gb"]),
                    xytext=(0, 8) if utolso else (-6, 4),
                    textcoords="offset points", fontsize=8, color=TINTA,
                    ha="center" if utolso else "right", va="bottom")
    ax.set_title("3. …és a játékok szépen ki is használják", pad=24)
    alcim(ax, "Ismert játékok telepítési mérete · 40 KB-tól 150 GB-ig "
              "(kb. 4 milliószoros növekedés)")


# ---------------------------------------------------------------------------
# Kirajzolás: egy összesítő kép + három külön kép
# ---------------------------------------------------------------------------
RAJZOLOK = [diagram_tranzisztor, diagram_tarolas, diagram_jatekok]

if __name__ == "__main__":
    fig, tengelyek = plt.subplots(3, 1, figsize=(10, 16))
    for rajzolo, ax in zip(RAJZOLOK, tengelyek):
        rajzolo(ax)
    fig.suptitle("Moore törvénye: 50 év a számítógépek fejlődésében",
                 fontsize=17, fontweight="bold", x=0.06, ha="left", y=0.995)
    fig.text(0.06, 0.005, "Források: Wikipedia (Transistor count), Our World in Data, "
             "J. C. McCallum – Disk Drive Prices, kiadói gépigények. Közelítő értékek.",
             fontsize=8, color=SZURKE)
    fig.tight_layout(rect=(0, 0.01, 1, 0.98), h_pad=3)
    fig.savefig("moore_vizualizacio.png", dpi=150)

    for i, rajzolo in enumerate(RAJZOLOK, start=1):
        fig_egy, ax = plt.subplots(figsize=(10, 5.5))
        rajzolo(ax)
        fig_egy.tight_layout()
        fig_egy.savefig(f"diagram_{i}.png", dpi=150)

    print(f"Mért duplázódási idő: {duplazodas:.2f} év")
    print("Kész: moore_vizualizacio.png, diagram_1.png, diagram_2.png, diagram_3.png")
