"""
Házi 3 – Steam: 20 év PC-s játékozás
====================================

Három vizualizáció egy fájlban:
  1. Hány játék jelenik meg évente a Steamen? (2004–2024)
  2. Egyidejű felhasználói csúcs évente (2010–2024)
  3. Minden idők legtöbb egyidejű játékosát elért játékai

Futtatás:
    py steam_vizualizacio.py
Kimenet: steam_vizualizacio.png (és egyenként diagram_1/2/3.png)

Adatforrások (kerekített, közelítő értékek):
  - Megjelenések: SteamDB / Statista – "Number of games released on Steam"
  - Felhasználói csúcsok: SteamDB – Steam concurrent users (éves maximum)
  - Játékos-csúcsok: SteamDB / SteamCharts – all-time peak
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# ---------------------------------------------------------------------------
# Stílus
# ---------------------------------------------------------------------------
KEK = "#2a78d6"
VKEK = "#86b6ef"
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
# 1. adat: megjelent játékok száma évente
# ---------------------------------------------------------------------------
megjelenes = pd.DataFrame({
    "ev": list(range(2004, 2025)),
    "jatekok": [7, 6, 69, 115, 163, 249, 271, 271, 380, 435, 1_773, 2_964,
                4_207, 6_357, 9_050, 8_033, 10_263, 11_773, 12_723, 14_535, 18_957],
})

# Fontos platformváltozások
esemenyek = {
    2012: "Steam Greenlight:\na közösség szavaz",
    2013: "Early Access",
    2017: "Steam Direct:\n100 $ és bárki\nfeltölthet",
}

# ---------------------------------------------------------------------------
# 2. adat: éves egyidejű felhasználói csúcs (millió fő)
# ---------------------------------------------------------------------------
felhasznalok = pd.DataFrame({
    "ev": list(range(2010, 2025)),
    "millio": [3.3, 4.6, 6.0, 7.2, 8.5, 11.0, 13.0, 16.0, 18.5, 18.8,
               24.8, 27.4, 30.0, 33.6, 39.2],
})

# ---------------------------------------------------------------------------
# 3. adat: minden idők egyidejű játékos-csúcsa (millió fő)
# ---------------------------------------------------------------------------
csucsok = pd.DataFrame([
    ("PUBG: Battlegrounds", 2018, 3.26, False),
    ("Black Myth: Wukong", 2024, 2.42, False),
    ("Palworld", 2024, 2.10, True),
    ("Counter-Strike 2", 2025, 1.86, False),
    ("Monster Hunter Wilds", 2025, 1.38, False),
    ("Lost Ark", 2022, 1.33, False),
    ("Dota 2", 2016, 1.29, False),
    ("Cyberpunk 2077", 2020, 1.05, False),
    ("Elden Ring", 2022, 0.95, False),
    ("Baldur's Gate 3", 2023, 0.88, False),
], columns=["jatek", "ev", "millio", "kis_studio"])


# ---------------------------------------------------------------------------
# Rajzoló függvények
# ---------------------------------------------------------------------------
def diagram_megjelenes(ax):
    ax.bar(megjelenes["ev"], megjelenes["jatekok"], color=KEK, width=0.75)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(ezres))
    ax.set_xlim(2003.3, 2024.7)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(4))
    ax.set_ylim(0, 22_000)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("Megjelent játékok száma")
    for ev, szoveg in esemenyek.items():
        y = megjelenes.loc[megjelenes["ev"] == ev, "jatekok"].iloc[0]
        ax.annotate(szoveg, (ev, y), xytext=(ev - 1.2 if ev < 2017 else ev - 1.6,
                    y + (6_500 if ev == 2012 else 3_000 if ev == 2013 else 6_000)),
                    fontsize=8.5, color=TINTA2, ha="center",
                    arrowprops=dict(arrowstyle="-", color=SZURKE, lw=0.8))
    for ev in (2004, 2024):
        y = megjelenes.loc[megjelenes["ev"] == ev, "jatekok"].iloc[0]
        ax.annotate(ezres(y), (ev, y), xytext=(0, 4), textcoords="offset points",
                    ha="center", fontsize=9, fontweight="bold", color=TINTA)
    ax.set_title("1. Az indie-robbanás: 7 játékból évi 19 000", pad=24)
    alcim(ax, "A Steamen évente megjelent játékok száma, 2004–2024 · "
              "2024-ben naponta átlag 52 új játék jelent meg")


def diagram_felhasznalok(ax):
    ax.plot(felhasznalok["ev"], felhasznalok["millio"], color=KEK, lw=2, zorder=2)
    ax.scatter(felhasznalok["ev"], felhasznalok["millio"], s=36, color=KEK,
               edgecolor=HATTER, linewidth=1.5, zorder=3)
    ax.set_ylim(0, 45)
    ax.set_xlim(2009.5, 2025)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f"{y:.0f} M"))
    ax.set_ylabel("Egyszerre bejelentkezett felhasználók (millió)")
    ax.annotate("COVID-lezárások:\n+32% egy év alatt", (2020, 24.8), xytext=(2016.6, 29),
                fontsize=8.5, color=TINTA2, ha="center",
                arrowprops=dict(arrowstyle="-", color=SZURKE, lw=0.8))
    ax.annotate("PUBG-láz", (2018, 18.5), xytext=(2016.2, 21.5), fontsize=8.5,
                color=TINTA2, ha="center",
                arrowprops=dict(arrowstyle="-", color=SZURKE, lw=0.8))
    for ev, ertek in [(2010, 3.3), (2024, 39.2)]:
        ax.annotate(f"{ertek:.1f} M".replace(".", ","), (ev, ertek), xytext=(0, 9),
                    textcoords="offset points", ha="center", fontsize=9,
                    fontweight="bold", color=TINTA)
    ax.set_title("2. Egyszerre 39 millióan játszanak", pad=24)
    alcim(ax, "A Steam éves egyidejű felhasználói csúcsa, 2010–2024 · "
              "kb. 12-szeres növekedés 14 év alatt")


def diagram_csucsok(ax):
    rend = csucsok.iloc[::-1]
    szinek = [KEK if kicsi else VKEK for kicsi in rend["kis_studio"]]
    ax.barh(rend["jatek"] + " (" + rend["ev"].astype(str) + ")", rend["millio"],
            color=szinek, height=0.6)
    for i, ertek in enumerate(rend["millio"]):
        ax.text(ertek + 0.04, i, f"{ertek:.2f} M".replace(".", ","), va="center",
                fontsize=8.5, color=TINTA)
    ax.set_xlim(0, 3.7)
    ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", colors=TINTA, length=0)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:g} M"))
    ax.set_xlabel("Egyidejű játékosok csúcsa (millió)")
    ax.text(2.6, 5.8, "A Palworldöt egy kis japán\nstúdió (Pocketpair) készítette,\n"
                    "mégis a 3. helyen áll", fontsize=8.5, color=KEK, va="center")
    ax.set_title("3. A rekorderek: battle royale, kínai AAA és egy indie meglepetés", pad=24)
    alcim(ax, "Minden idők legmagasabb egyidejű játékosszáma a Steamen")


RAJZOLOK = [diagram_megjelenes, diagram_felhasznalok, diagram_csucsok]

if __name__ == "__main__":
    fig, tengelyek = plt.subplots(3, 1, figsize=(10, 16))
    for rajzolo, ax in zip(RAJZOLOK, tengelyek):
        rajzolo(ax)
    fig.suptitle("Steam: 20 év PC-s játékozás számokban", fontsize=17,
                 fontweight="bold", x=0.06, ha="left", y=0.995)
    fig.text(0.06, 0.005, "Források: SteamDB, Statista, SteamCharts. Kerekített, "
             "közelítő értékek.", fontsize=8, color=SZURKE)
    fig.tight_layout(rect=(0, 0.01, 1, 0.98), h_pad=3)
    fig.savefig("steam_vizualizacio.png", dpi=150)

    for i, rajzolo in enumerate(RAJZOLOK, start=1):
        fig_egy, ax = plt.subplots(figsize=(10, 5.5))
        rajzolo(ax)
        fig_egy.tight_layout()
        fig_egy.savefig(f"diagram_{i}.png", dpi=150)

    print(f"2024-ben naponta: {megjelenes['jatekok'].iloc[-1] / 366:.1f} játék")
    print("Kész: steam_vizualizacio.png, diagram_1.png, diagram_2.png, diagram_3.png")
