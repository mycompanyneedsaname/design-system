# design-sync Notizen

- **Kein React:** Wendepunkt hat keine Komponenten. Die Gründer haben am 25.09. „Marke ohne Komponenten“ gewählt: Sync als tokens-only DS (`[ZERO_MATCH] ... treating as tokens-only DS` ist erwartet).
- **Quelle:** `brand/styles.css` und `brand/docs/icons.md` erzeugt `markenwelt/build.py` (Abschnitt „Marken-Paket für Claude Design“). Vor jedem Sync `python3 markenwelt/build.py` laufen lassen. `brand/docs/marke.md` und `logo.md` sind von Hand gepflegt.
- **Build:** `node .ds-sync/package-build.mjs --config .design-sync/config.json --node-modules ./.ds-sync/node_modules --entry ./brand/index.js --out ./ds-bundle`. `react@18` und `react-dom@18` müssen in `.ds-sync/node_modules` liegen (Vendor-Pflicht des Konverters), sonst „react not found under --node-modules“.
- **Render-Check:** Playwright global unter `/opt/node22/lib/node_modules/playwright`; in `.ds-sync/node_modules/playwright` symlinken. Chromium unter `/opt/pw-browsers`.
- **Guidelines** landen unter `guidelines/docs/*.md` (nicht `guidelines/*.md`); die Pfade im Header müssen dazu passen.
- **Auth:** In claude.ai/code liefert `DesignSync` ohne vorheriges `/design-login` (interaktive CLI) bzw. „Send to Claude Code Web“ aus Claude Design einen Autorisierungsfehler.

## Known render warns

- `[DTS_REACT]` beim Build: irrelevant, es gibt keine Komponenten.
- `[FONT_REMOTE]`: Plex Sans/Mono und Kalam kommen per Google-Fonts-`@import`; gewollt.

## Re-sync risks

- `brand/docs/marke.md` enthält Kernsätze und Rechner-Richtwerte von Hand; ändert sich die Landingpage, hier nachziehen.
- Die `wp-`-Klassen spiegeln CSS aus `build.py` (`.hl`, `.wp-cta`, `.pers-role`, `.korr`, `.bc-sum`) statisch ohne Animation. Ändert sich dort ein Wert, wird er nur übernommen, wenn der Export-Abschnitt ihn mitzieht.
- Fonts hängen am Netz (Google Fonts), nichts wird mitgeliefert.
