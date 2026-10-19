"""
Házi 3 – Birodalmak felemelkedése és bukása
===========================================

Három vizualizáció egy fájlban:
  1. A legnagyobb birodalmak legnagyobb kiterjedése (millió km²)
  2. Mikor és meddig léteztek? – idővonal
  3. A nagyobb birodalom tovább élt? – terület és élettartam

Futtatás:
    py birodalmak_vizualizacio.py
Kimenet: birodalmak_vizualizacio.png (és egyenként diagram_1/2/3.png)

Adatforrás: Wikipedia – "List of largest empires" (Taagepera és Turchin
becslései alapján), valamint az egyes birodalmak szócikkei. A kezdő és
záró évek történészi konvenciók, más forrás más évet is mondhat.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Stílus
# ---------------------------------------------------------------------------
KEK = "#2a78d6"
VKEK = "#86b6ef"
NARANCS = "#eb6834"
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

FOLD_SZARAZFOLD = 148.9  # millió km²


def alcim(ax, szoveg):
    ax.text(0, 1.02, szoveg, transform=ax.transAxes, fontsize=9.5,
            color=TINTA2, va="bottom")


def evszam(x, _=None):
    return f"i. e. {-x:.0f}" if x < 0 else f"{x:.0f}"


def tizedes(x):
    return f"{x:.1f}".replace(".", ",")


# ---------------------------------------------------------------------------
# Adat: név, kezdet, vég, legnagyobb terület (millió km²), csúcs éve
# ---------------------------------------------------------------------------
birodalmak = pd.DataFrame([
    ("Brit Birodalom", 1607, 1997, 35.5, 1920),
    ("Mongol Birodalom", 1206, 1368, 24.0, 1270),
    ("Orosz Birodalom", 1721, 1917, 22.8, 1895),
    ("Csing-dinasztia (Kína)", 1644, 1912, 14.7, 1790),
    ("Spanyol Birodalom", 1492, 1976, 13.7, 1810),
    ("Omajjád Kalifátus", 661, 750, 11.1, 720),
    ("Abbászida Kalifátus", 750, 1258, 11.1, 750),
    ("Portugál Birodalom", 1415, 1999, 10.4, 1820),
    ("Han-dinasztia (Kína)", -202, 220, 6.0, -50),
    ("Perzsa (Akhaimenida) Birodalom", -550, -330, 5.5, -500),
    ("Nagy Sándor birodalma", -336, -323, 5.2, -323),
    ("Oszmán Birodalom", 1299, 1922, 5.2, 1683),
    ("Római Birodalom", -27, 476, 5.0, 117),
    ("Bizánci Birodalom", 395, 1453, 2.8, 555),
    ("Habsburg Monarchia", 1526, 1918, 0.7, 1914),
], columns=["nev", "kezdet", "veg", "terulet", "csucs"])

birodalmak["elettartam"] = birodalmak["veg"] - birodalmak["kezdet"]
korrelacio = np.corrcoef(birodalmak["terulet"], birodalmak["elettartam"])[0, 1]
# Kiugró érték nélkül: mennyit számít egyetlen pont (Bizánc)?
bizanc_nelkul = birodalmak[birodalmak["nev"] != "Bizánci Birodalom"]
korrelacio_bizanc_nelkul = np.corrcoef(bizanc_nelkul["terulet"], bizanc_nelkul["elettartam"])[0, 1]


# ---------------------------------------------------------------------------
# Rajzoló függvények
# ---------------------------------------------------------------------------
def diagram_terulet(ax):
    rend = birodalmak.sort_values("terulet")
    szinek = [NARANCS if n == "Habsburg Monarchia" else KEK for n in rend["nev"]]
    ax.barh(rend["nev"], rend["terulet"], color=szinek, height=0.65)
    for i, (t, nev) in enumerate(zip(rend["terulet"], rend["nev"])):
        szazalek = t / FOLD_SZARAZFOLD * 100
        ax.text(t + 0.4, i, f"{tizedes(t)} M km²  ({szazalek:.0f}%)".replace("(0%)", "(<1%)"),
                va="center", fontsize=8.5, color=TINTA)
    ax.set_xlim(0, 44)
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", colors=TINTA, length=0)
    ax.set_xlabel("Legnagyobb kiterjedés (millió km²) · zárójelben: a Föld szárazföldjének hány %-a")
    ax.set_title("1. A Brit Birodalom a szárazföld negyedét uralta", pad=24)
    alcim(ax, "Legnagyobb kiterjedés · narancs: a Habsburg Monarchia, "
              "amelynek Magyarország is része volt")


def diagram_idovonal(ax):
    rend = birodalmak.sort_values("kezdet", ascending=False).reset_index(drop=True)
    ax.barh(rend.index, rend["elettartam"], left=rend["kezdet"], color=VKEK,
            height=0.6, zorder=2)
    ax.scatter(rend["csucs"], rend.index, s=40, color=KEK, edgecolor=HATTER,
               linewidth=1.2, zorder=3, label="Legnagyobb kiterjedés éve")
    for i, sor in rend.iterrows():
        ax.text(sor["veg"] + 25, i, f"{sor['nev']} · {sor['elettartam']} év",
                va="center", fontsize=8.5, color=TINTA)
    ax.set_yticks([])
    ax.grid(axis="y", visible=False)
    ax.set_xlim(-650, 3100)
    ax.xaxis.set_major_locator(mticker.FixedLocator(range(-500, 2001, 500)))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(evszam))
    ax.spines["left"].set_visible(False)
    ax.legend(loc="upper right", frameon=False)
    ax.set_title("2. Néhány évtizedtől több mint ezer évig", pad=24)
    alcim(ax, "A birodalmak fennállása időrendben · Nagy Sándoré 13 évig, "
              "Bizáncé 1058 évig tartott")


def diagram_osszefugges(ax):
    ax.scatter(birodalmak["terulet"], birodalmak["elettartam"], s=60, color=KEK,
               edgecolor=HATTER, linewidth=1.5, zorder=3)
    meredekseg, tengelymetszet = np.polyfit(birodalmak["terulet"], birodalmak["elettartam"], 1)
    x = np.linspace(0, 37, 50)
    ax.plot(x, meredekseg * x + tengelymetszet, color=SZURKE, lw=1.5, ls="--", zorder=1)
    # Feliratok eltolása pontban; negatív x = a pont bal oldalára kerül
    eltolasok = {"Brit Birodalom": (-10, 8), "Mongol Birodalom": (8, -10),
                 "Orosz Birodalom": (-8, 2), "Abbászida Kalifátus": (-8, 4),
                 "Római Birodalom": (-8, 0), "Oszmán Birodalom": (8, 2),
                 "Portugál Birodalom": (8, 2)}
    for _, sor in birodalmak.iterrows():
        dx, dy = eltolasok.get(sor["nev"], (8, -3))
        nev = sor["nev"].replace(" (Akhaimenida)", "")
        ax.annotate(nev, (sor["terulet"], sor["elettartam"]),
                    xytext=(dx, dy), textcoords="offset points", fontsize=8.5,
                    color=TINTA, ha="right" if dx < 0 else "left")
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 1150)
    ax.set_xlabel("Legnagyobb kiterjedés (millió km²)")
    ax.set_ylabel("Fennállás (év)")
    ax.set_title("3. A méret nem garancia a hosszú életre", pad=24)
    alcim(ax, (f"Terület és élettartam · korreláció: r = {korrelacio:.2f}, "
               f"Bizánc nélkül csak r = {korrelacio_bizanc_nelkul:.2f}").replace(".", ","))


RAJZOLOK = [diagram_terulet, diagram_idovonal, diagram_osszefugges]

if __name__ == "__main__":
    fig, tengelyek = plt.subplots(3, 1, figsize=(10, 18))
    for rajzolo, ax in zip(RAJZOLOK, tengelyek):
        rajzolo(ax)
    fig.suptitle("Birodalmak felemelkedése és bukása", fontsize=17,
                 fontweight="bold", x=0.06, ha="left", y=0.995)
    fig.text(0.06, 0.005, "Forrás: Wikipedia – List of largest empires (Taagepera, "
             "Turchin becslései) és a birodalmak szócikkei. Közelítő értékek.",
             fontsize=8, color=SZURKE)
    fig.tight_layout(rect=(0, 0.01, 1, 0.98), h_pad=3)
    fig.savefig("birodalmak_vizualizacio.png", dpi=150)

    for i, rajzolo in enumerate(RAJZOLOK, start=1):
        fig_egy, ax = plt.subplots(figsize=(10, 6))
        rajzolo(ax)
        fig_egy.tight_layout()
        fig_egy.savefig(f"diagram_{i}.png", dpi=150)

    print(f"Korreláció (terület ~ élettartam): r = {korrelacio:.3f}")
    print(f"Korreláció Bizánc nélkül: r = {korrelacio_bizanc_nelkul:.3f}")
    print(birodalmak[["nev", "terulet", "elettartam"]].to_string(index=False))
    print("Kész: birodalmak_vizualizacio.png, diagram_1.png, diagram_2.png, diagram_3.png")
