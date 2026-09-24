# CLAUDE.md · Wendepunkt Ingenieure Design System

Markenentwicklung für **Wendepunkt Ingenieure – Büro für Energie- und Ressourceneffizienz** (GbR, Thüringen/Leipzig). Gründer: Michael Schenk (Ressourceneffizienz) und Tobias Wintsche (Energietechnik). Zielgruppe: Geschäftsführung und Technik in KMU des verarbeitenden Gewerbes.

Sprache mit dem Nutzer: **Deutsch**. Commit-Messages: Englisch.

## Struktur

| Pfad | Inhalt | Status |
|---|---|---|
| `markenwelt/build.py` | **Quelle** der aktuellen Markenwelt. Erzeugt `markenwelt/index.html`. | aktiv |
| `markenwelt/index.html` | Generiert. Nie direkt bearbeiten, immer `build.py` ändern und neu bauen. | aktiv |
| `logo/vergleich.html` | Vergleich zweier Logo-Kurven. Entscheidung gefallen, nur Beleg. | abgeschlossen |
| `richtungen/index.html` | Frühere drei Richtungen (Nachgerechnet, Werkbank, Kernig) plus Kombination. | historisch |
| `README.md` | Chronik der Entwürfe und Entscheidungen. | pflegen |
| `HANDOFF.md` | Aktueller Stand, offene Punkte, nächste Schritte. | pflegen |

## Arbeitsablauf für Änderungen an der Markenwelt

1. `markenwelt/build.py` bearbeiten. Es ist ein Python-f-String-Template: geschweifte Klammern in CSS/JS **verdoppeln** (`{{ }}`). Keine Backslashes und keine gleichartigen Anführungszeichen innerhalb von `{...}`-Ausdrücken, sonst SyntaxError. Hilfswerte vorher in Variablen legen.
2. Bauen: `python3 markenwelt/build.py` schreibt `markenwelt/index.html` (das Skript hat den Zielpfad `/home/user/design-system/markenwelt/index.html` fest eingetragen).
3. Einmal rendern und ansehen (Playwright ist global installiert):
   ```js
   import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
   const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
   ```
   Google Fonts sind in der Sandbox gesperrt, lokal rendern also Ersatzschriften. Auf der veröffentlichten Seite laden sie korrekt.
4. Committen und auf `claude/new-session-syvaun` pushen.
5. Artifact neu veröffentlichen: Artifact-Tool, `file_path` = `markenwelt/index.html`. Aus einer neuen Session **mit `url`** veröffentlichen (siehe HANDOFF.md), sonst entsteht ein neues Artifact.

## Artifact-Kommentare

Die Gründer kommentieren direkt im Artifact („Send to Claude“). Ablauf pro Kommentar: Änderung in `build.py`, bauen, committen, pushen, neu veröffentlichen, dann mit `ArtifactComments` im Thread kurz auf Deutsch antworten und den Thread auflösen. In der Session nur eine kurze Zeile schreiben. Kommentare sind oft knapp („löschen.“, „streichen“): Der Anker-Kontext zeigt, welches Element gemeint ist.

## Feste Entscheidungen (nicht ohne Rückfrage ändern)

- **Logo:** Kurve mit genau einem Wendepunkt, **steilste Stelle am Punkt**: SVG-Pfad `M6 52 C 30 52 34 12 58 12`, Punkt `cx=32 cy=32 r=5.5`. Wortmarke IBM Plex Sans, „Wendepunkt“ 600, „Ingenieure“ 400, gleich groß. Die x³-Variante mit flachster Stelle am Punkt ist verworfen.
- **Produktname:** „Der Modulare Effizienz-Baukasten“. Nicht „Effizienz-Kompass“. **Keine Tagesangaben** (kein „2 + 2 Tage“, kein „vier Tage“).
- **Hero-Headline:** „Unser Versprechen:“ (klein) / „Der Modulare Effizienz-Baukasten.“ / „Gemessen. Nachgerechnet. Umgesetzt.“
- **Wendepunkt-Sektion** direkt unter dem Hero: „Der Wendepunkt ist der Moment, ab dem es anders läuft.“ / „Wir suchen ihn gemeinsam mit Ihnen.“ / Button „Kostenfreies Erstgespräch“ (hellgrün #C8F04A, Petrol-Rahmen, ohne Icon). Der Kontakt-Button steht nur hier, nicht im Hero.
- **Signaturelement:** Korrekturzeichen nach DIN 16511 (feine 2-px-Streichung, nummeriertes Zeichen, korrigierter Wert in Mono am Rand). Kein dicker Marker-Strich, keine Marker-Schrift.
- **Kein Punktraster** im Hintergrund.
- **Farben:** Petrol #0F3B3F, Tiefe #071F22, Papier #F7F5F0, Sand #E9E1CF, Nebel #EEF0EC. Marker-/Akzentfarbe ist **noch offen**: Schalter mit Ocker #D9A441, Lime #C8F04A, Mint #5DE3A1, Terrakotta #E4744C. Die Gründer mögen Lime. Die Wendepunkt-Sektion ist fest auf Lime gesetzt.
- **Schriften:** IBM Plex Sans (Text/Headlines), IBM Plex Mono (Zahlen/Labels), Kalam nur für kleine Notizen.

## Tabus aus dem Briefing

Keine Verläufe, keine Pill-Buttons, keine abgerundeten Karten mit Schatten, kein zentrierter Hero mit zwei Buttons, keine Windräder, Glühbirnen, Blätter oder Weltkugeln, kein Inter, keine pauschale ROI-Zahl im Hero, kein Beratersprech. Kontrast mindestens WCAG AA. Ocker auf Weiß ist nie Schrift (2,3 : 1).

## Git

- Branch: `claude/new-session-syvaun`. Es ist der einzige Branch im Repo, deshalb gibt es noch keinen Pull Request.
- Commit-Footer laut System-Reminder der jeweiligen Session setzen.
