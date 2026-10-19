"""
Házi 3 – Középkori csaták számokban (732–1526)
==============================================

Három vizualizáció egy fájlban:
  1. Mekkora seregek harcoltak? – a két sereg összlétszáma csatánként
  2. A nagyobb sereg nyert? – győztes / vesztes létszámaránya
  3. Ki halt meg? – a győztes és a vesztes veszteségaránya

Futtatás:
    py csatak_vizualizacio.py
Kimenet: csatak_vizualizacio.png (és egyenként diagram_1/2/3.png)

Adatforrás: Wikipedia (az egyes csaták szócikkei). A középkori létszámok
és veszteségek erősen vitatottak; a becslési tartományok közepét használtam,
kerekítve. A veszteség itt halottat, sebesültet és foglyot is jelent.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Stílus
# ---------------------------------------------------------------------------
KEK = "#2a78d6"
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


def alcim(ax, szoveg):
    ax.text(0, 1.02, szoveg, transform=ax.transAxes, fontsize=9.5,
            color=TINTA2, va="bottom")


def ezres(x, _=None):
    return f"{x:,.0f}".replace(",", " ")


# ---------------------------------------------------------------------------
# Adat: csata, év, győztes, vesztes, létszámok, veszteségek (None = nincs
# megbízható becslés), magyar részvétel
# ---------------------------------------------------------------------------
csatak = pd.DataFrame([
    ("Poitiers", 732, "Frankok", "Omajjádok", 17_500, 22_500, 1_500, 10_000, False),
    ("Augsburg (Lechmező)", 955, "Keleti frankok", "Magyarok", 8_500, 15_000, None, None, True),
    ("Hastings", 1066, "Normannok", "Angolszászok", 10_000, 8_000, 2_000, 4_000, False),
    ("Manzikert", 1071, "Szeldzsukok", "Bizánc", 25_000, 40_000, None, None, False),
    ("Hattin", 1187, "Ajjúbidák", "Keresztesek", 30_000, 20_000, 2_000, 17_000, False),
    ("Muhi", 1241, "Mongolok", "Magyarok", 25_000, 27_500, None, 10_000, True),
    ("Crécy", 1346, "Angolok", "Franciák", 12_000, 25_000, 300, 4_000, False),
    ("Grünwald", 1410, "Lengyel–litván", "Német Lovagrend", 32_000, 27_000, 5_000, 22_000, False),
    ("Azincourt", 1415, "Angolok", "Franciák", 8_000, 14_000, 400, 8_000, False),
    ("Várna", 1444, "Oszmánok", "Magyar–lengyel", 55_000, 25_000, None, None, True),
    ("Mohács", 1526, "Oszmánok", "Magyarok", 55_000, 26_000, 1_500, 16_000, True),
], columns=["csata", "ev", "gyoztes", "vesztes", "gy_letszam", "v_letszam",
            "gy_veszteseg", "v_veszteseg", "magyar"])

csatak["osszes"] = csatak["gy_letszam"] + csatak["v_letszam"]
csatak["arany"] = csatak["gy_letszam"] / csatak["v_letszam"]
csatak["cimke"] = csatak["csata"] + " (" + csatak["ev"].astype(str) + ")"
esely_ellen = (csatak["arany"] < 1).sum()


# ---------------------------------------------------------------------------
# Rajzoló függvények
# ---------------------------------------------------------------------------
def diagram_letszam(ax):
    for magyar, szin, nev in [(False, KEK, "Egyéb csaták"),
                              (True, NARANCS, "Magyar részvétellel")]:
        resz = csatak[csatak["magyar"] == magyar]
        ax.scatter(resz["ev"], resz["osszes"], s=60, color=szin, label=nev,
                   edgecolor=HATTER, linewidth=1.5, zorder=3)
    for _, sor in csatak.iterrows():
        lent = sor["csata"] in ("Hastings", "Augsburg (Lechmező)", "Azincourt")
        ax.annotate(sor["csata"], (sor["ev"], sor["osszes"]),
                    xytext=(0, -15 if lent else 8), textcoords="offset points",
                    fontsize=8.5, color=TINTA, ha="center")
    ax.set_ylim(0, 95_000)
    ax.set_xlim(680, 1580)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(ezres))
    ax.set_ylabel("A két sereg összlétszáma (fő)")
    ax.legend(loc="upper left", frameon=False)
    ax.set_title("1. A középkori seregek meglepően kicsik voltak", pad=24)
    alcim(ax, "Becsült összlétszám csatánként · Hastings sorsdöntő csatájában "
              "kb. 18 000 ember harcolt, ennyi fér el egy mai sportcsarnokban")


def diagram_arany(ax):
    rend = csatak.iloc[::-1]
    szinek = [KEK if a >= 1 else NARANCS for a in rend["arany"]]
    ax.barh(rend["cimke"], rend["arany"] - 1, left=1, color=szinek, height=0.6)
    ax.axvline(1, color=TINTA2, lw=1)
    ax.set_xscale("log")
    ax.set_xlim(0.4, 2.5)
    ax.xaxis.set_major_locator(mticker.FixedLocator([0.5, 0.75, 1, 1.5, 2]))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:g}×".replace(".", ",")))
    ax.xaxis.set_minor_formatter(mticker.NullFormatter())
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", colors=TINTA, length=0)
    ax.set_xlabel("Győztes sereg létszáma / vesztes sereg létszáma (logaritmikus skála)")
    # Irányfeliratok a legfelső sáv fölé, hogy ne takarjanak oszlopot
    ax.set_ylim(-0.6, len(csatak) + 0.4)
    ax.text(2.4, len(csatak) - 0.1, "A nagyobb sereg nyert →", ha="right",
            color=KEK, fontsize=9, fontweight="bold")
    ax.text(0.42, len(csatak) - 0.1, "← A kisebb sereg nyert", ha="left",
            color=NARANCS, fontsize=9, fontweight="bold")
    ax.set_title("2. A híres csaták felét a kisebb sereg nyerte", pad=24)
    alcim(ax, f"{len(csatak)} csatából {esely_ellen} alkalommal győzött a "
              "létszámhátrányban lévő fél")


def diagram_veszteseg(ax):
    resz = csatak.dropna(subset=["gy_veszteseg", "v_veszteseg"]).iloc[::-1]
    gy = resz["gy_veszteseg"] / resz["gy_letszam"] * 100
    v = resz["v_veszteseg"] / resz["v_letszam"] * 100
    y = np.arange(len(resz))
    ax.hlines(y, gy, v, color=RACS, lw=3, zorder=1)
    ax.scatter(gy, y, s=70, color=KEK, edgecolor=HATTER, linewidth=1.5,
               zorder=3, label="Győztes")
    ax.scatter(v, y, s=70, color=NARANCS, edgecolor=HATTER, linewidth=1.5,
               zorder=3, label="Vesztes")
    for yi, ertek in zip(y, v):
        ax.annotate(f"{ertek:.0f}%", (ertek, yi), xytext=(9, 0),
                    textcoords="offset points", va="center", fontsize=8.5, color=TINTA)
    ax.set_yticks(y, resz["cimke"])
    ax.tick_params(axis="y", colors=TINTA, length=0)
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    ax.set_xlabel("Veszteség a sereg létszámához képest (halott, sebesült, fogoly)")
    ax.legend(loc="lower right", frameon=False)
    atlag_gy, atlag_v = gy.mean(), v.mean()
    ax.set_title("3. A vesztes fél sokszorosát veszítette", pad=24)
    alcim(ax, f"Átlagos veszteség: győztes kb. {atlag_gy:.0f}%, vesztes kb. "
              f"{atlag_v:.0f}% · a legtöbben a menekülés közben estek el")


RAJZOLOK = [diagram_letszam, diagram_arany, diagram_veszteseg]

if __name__ == "__main__":
    fig, tengelyek = plt.subplots(3, 1, figsize=(10, 17))
    for rajzolo, ax in zip(RAJZOLOK, tengelyek):
        rajzolo(ax)
    fig.suptitle("Középkori csaták számokban (732–1526)", fontsize=17,
                 fontweight="bold", x=0.06, ha="left", y=0.995)
    fig.text(0.06, 0.005, "Forrás: Wikipedia, az egyes csaták szócikkei. A középkori "
             "létszámok vitatottak: a becslések közepét, kerekítve használtam.",
             fontsize=8, color=SZURKE)
    fig.tight_layout(rect=(0, 0.01, 1, 0.98), h_pad=3)
    fig.savefig("csatak_vizualizacio.png", dpi=150)

    for i, rajzolo in enumerate(RAJZOLOK, start=1):
        fig_egy, ax = plt.subplots(figsize=(10, 5.8))
        rajzolo(ax)
        fig_egy.tight_layout()
        fig_egy.savefig(f"diagram_{i}.png", dpi=150)

    print(f"Kisebb sereg győzött: {esely_ellen}/{len(csatak)}")
    print(csatak[["csata", "osszes", "arany"]].to_string(index=False))
    print("Kész: csatak_vizualizacio.png, diagram_1.png, diagram_2.png, diagram_3.png")
