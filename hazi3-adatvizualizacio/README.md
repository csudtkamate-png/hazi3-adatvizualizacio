# Házi 3 – Adatvizualizáció és történetmesélés

Négy téma, mindegyikhez három diagram és egy rövid történet.

| Mappa | Téma | Történet |
|---|---|---|
| `moore/` | Moore törvénye: 50 év a számítógépek fejlődésében | [tortenet.md](moore/tortenet.md) |
| `kozepkori-csatak/` | Középkori csaták számokban (732–1526) | [tortenet.md](kozepkori-csatak/tortenet.md) |
| `steam/` | Steam: 20 év PC-s játékozás számokban | [tortenet.md](steam/tortenet.md) |
| `birodalmak/` | Birodalmak felemelkedése és bukása | [tortenet.md](birodalmak/tortenet.md) |

Minden mappában:
- `*_vizualizacio.py` – a script, amely mindhárom diagramot elkészíti
- `*_vizualizacio.png` – a három diagram egy képen
- `diagram_1.png`, `diagram_2.png`, `diagram_3.png` – a diagramok külön-külön
- `tortenet.md` – a diagramok köré írt történet

## Futtatás

Szükséges csomagok: `numpy`, `pandas`, `matplotlib`. A scriptet a saját mappájából kell futtatni, mert oda menti a képeket:

```
cd moore
python moore_vizualizacio.py
```

Az adatok a scriptekben vannak, kerekített, közelítő értékekként. A források az egyes történetek végén szerepelnek.
