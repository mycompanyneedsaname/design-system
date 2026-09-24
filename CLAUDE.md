# CLAUDE.md · Wendepunkt Ingenieure Design System

Markenentwicklung für **Wendepunkt Ingenieure – Büro für Energie- und Ressourceneffizienz** (GbR, Thüringen/Leipzig). Gründer: Michael Schenk (Ressourceneffizienz) und Tobias Wintsche (Energieeffizienz). Zielgruppe: Geschäftsführung und Technik in KMU des verarbeitenden Gewerbes.

Sprache mit dem Nutzer: **Deutsch**. Commit-Messages: Englisch.

## Struktur

| Pfad | Inhalt | Status |
|---|---|---|
| `markenwelt/build.py` | **Quelle** der aktuellen Markenwelt. Erzeugt `markenwelt/index.html` und `markenwelt/markensystem.html`. | aktiv |
| `markenwelt/index.html` | Generiert: **Landingpage** (Wendepunkt, Team, Baukasten). Das ist das veröffentlichte Artifact. Nie direkt bearbeiten. | aktiv, Fokus |
| `markenwelt/markensystem.html` | Generiert: Markensystem (Signaturelement, Bausteine, Icons, Plakate, Anwendung, Farben/Schriften). Seit 24.09. ausgelagert, derzeit nicht im Fokus. | ruht |
| `logo/vergleich.html` | Vergleich zweier Logo-Kurven. Entscheidung gefallen, nur Beleg. | abgeschlossen |
| `richtungen/index.html` | Frühere drei Richtungen (Nachgerechnet, Werkbank, Kernig) plus Kombination. | historisch |
| `README.md` | Chronik der Entwürfe und Entscheidungen. | pflegen |
| `HANDOFF.md` | Aktueller Stand, offene Punkte, nächste Schritte. | pflegen |

## Arbeitsablauf für Änderungen an der Markenwelt

1. `markenwelt/build.py` bearbeiten. Es ist ein Python-f-String-Template: geschweifte Klammern in CSS/JS **verdoppeln** (`{{ }}`). Keine Backslashes und keine gleichartigen Anführungszeichen innerhalb von `{...}`-Ausdrücken, sonst SyntaxError. Hilfswerte vorher in Variablen legen.
2. Bauen: `python3 markenwelt/build.py` schreibt `markenwelt/index.html` und `markenwelt/markensystem.html` (Pfade fest eingetragen). Die Aufteilung geschieht am Ende von `build.py` über den HTML-Kommentar `MARKENSYSTEM`: Alles davor ist Landingpage, alles danach Markensystem.
3. Einmal rendern und ansehen (Playwright ist global installiert):
   ```js
   import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
   const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
   ```
   Google Fonts sind in der Sandbox gesperrt, lokal rendern also Ersatzschriften. Auf der veröffentlichten Seite laden sie korrekt.
   Screenshots immer unter **neuem Dateinamen** speichern: Das Read-Tool zeigt sonst ein zwischengespeichertes altes Bild.
4. Committen und auf `claude/new-session-syvaun` pushen.
5. Artifact neu veröffentlichen: Artifact-Tool, `file_path` = `markenwelt/index.html`. Aus einer neuen Session **mit `url`** veröffentlichen (siehe HANDOFF.md), sonst entsteht ein neues Artifact.

## Artifact-Kommentare

Die Gründer kommentieren direkt im Artifact („Send to Claude“). Ablauf pro Kommentar: Änderung in `build.py`, bauen, committen, pushen, neu veröffentlichen, dann mit `ArtifactComments` im Thread kurz auf Deutsch antworten und den Thread auflösen. In der Session nur eine kurze Zeile schreiben. Kommentare sind oft knapp („löschen.“, „streichen“): Der Anker-Kontext zeigt, welches Element gemeint ist.

## Feste Entscheidungen (nicht ohne Rückfrage ändern)

- **Logo:** Kurve mit genau einem Wendepunkt, **steilste Stelle am Punkt**: SVG-Pfad `M6 52 C 30 52 34 12 58 12`, Punkt `cx=32 cy=32 r=5.5`. Wortmarke IBM Plex Sans, „Wendepunkt“ 600, „Ingenieure“ 400, gleich groß. Die x³-Variante mit flachster Stelle am Punkt ist verworfen.
- **Produktname:** „Der Modulare Effizienz-Baukasten“. Nicht „Effizienz-Kompass“. **Keine Tagesangaben** (kein „2 + 2 Tage“, kein „vier Tage“).
- **Reihenfolge der Startseite** (Wunsch Tobias, 24.09.): 1. Wendepunkt als Einstieg, 2. Team, 3. Modularer Effizienz-Baukasten. Den Referenzen-Abschnitt haben die Gründer wieder entfernt (kommt erst mit echten Projekten). Das Markensystem steht seit 24.09. in einer eigenen Datei (`markensystem.html`), die Gründer konzentrieren sich erst auf die Landingpage.
- **1 · Wendepunkt (Einstieg, Sand, `#start`):** H1 „Der Wendepunkt ist der Moment, ab dem es anders läuft.“ / „Wir sind ein Büro für Energie- und Ressourceneffizienz und suchen ihn gemeinsam mit Ihnen.“, dabei „Energie- und Ressourceneffizienz“ mit Lime-Textmarker (Klasse `.hl`). (Kleine Zeile und Schild darüber wurden als „geht unter“ bzw. „deplatziert“ verworfen.) / Button „Kostenfreies Erstgespräch vereinbaren“ (hellgrün #C8F04A, Petrol-Rahmen, ohne Icon). Der Kontakt-Button steht **nicht** im Einstieg, sondern ganz unten im Baukasten-Abschnitt (`#kontakt`, Wunsch 24.09.). Kurve mit handschriftlichen Notizen: davor „steigende Betriebskosten, CO₂-Ausstoß & Rohstoff-Knappheit“, danach „sinkende Betriebskosten, Flexibilität & Resilienz“, am Punkt „hier.“ mit Lime-Textmarker. Darunter eine Beweiszeile (`.wp-proof`): „150 · Rund 150 Betriebe im verarbeitenden Gewerbe haben wir schon von innen gesehen.“ Auf dem Handy (≤ 640 px) werden die Notizen in der SVG ausgeblendet und als Liste `.wp-mnotes` (davor / hier / danach) unter der Kurve gezeigt.
- **Ruhe (Wunsch 24.09., „zu wirr“):** Kein Übergang 1 → 2 (Linie/Pfeil „wer „wir“ sind:“ entfernt). Höchstens eine Lime-Markierung pro Block: Einstieg „Energie- und Ressourceneffizienz“ + „hier.“, Team nur „persönlich“. In den Porträttexten nur Fett, kein Grün.
- **2 · Team (`#team`):** Überschrift „Wir nehmen es persönlich.“ („persönlich“ mit Lime-Textmarker; alle Textmarker `.hl` und die Zitate werden beim Hereinscrollen animiert gezogen), Porträts von Michael Schenk (Ressourceneffizienz) und Tobias Wintsche (Energieeffizienz), das Fachgebiet steht im Fließtext („verantwortet bei uns …“, bei beiden), nicht als Label. Texte aus Notion „3.5.1 Fragen an Tobias und Michael“. Fotos fehlen noch: gezeichnete Duotone-Platzhalter mit Label „Platzhalter“. Keine Zitate mehr (auf Wunsch gelöscht, 24.09.). Keine Notizen unter den Fotos (auf Wunsch gelöscht). Darunter (`.team-link`, nur Desktop) laufen zwei symmetrische Linien, „Ressourcen“ (links) und „Energie“ (rechts), in der Mitte zusammen („beides zusammen gedacht.“) und führen über die Sektionsgrenze in den Baukasten: Dort (`.bk-link`) wird die Linie Lime und endet mit einem Punkt über „Unser Versprechen:“ (die separate Platte „Ihr Betrieb“ ist wieder entfernt). **Die Wendepunkt-Kurve nicht als Verbindung zwischen Energie und Ressourcen verwenden**: Sie steht für vorher/nachher, nicht für zwei gleichwertige Felder. Nie Lime als Schriftfarbe auf hell.
- **3 · Baukasten (`#baukasten`, Petrol):** zentriert gestapelt (`.bk-stack`): „Unser Versprechen:“ (klein) / „Der Modulare Effizienz-Baukasten.“ / „Weniger Verbrauch, mehr Spielraum.“, darunter mittig der Konfigurator, die Auswahl-Buttons und ganz unten der Erstgespräch-Button. Der Button ist ein `mailto:` auf **kontakt@wendepunkt-ingenieure.de (Platzhalter)**, darunter eine Zeile mit E-Mail und Telefon (**+49 000 000000, Platzhalter**). Danach ein schmaler Footer (`.site-foot`) mit Firmierung und Links Impressum / Datenschutz (**Ziele `#impressum`, `#datenschutz` sind Platzhalter**). Auf dem Handy ersetzt `.tl-m` („Ressourcen + Energie / beides zusammen gedacht.“) die ausgeblendeten Team-Linien.
- **Baukasten-Konfigurator:** neun Handlungsfelder auf 3×3-Grundplatte, zwei Gruppen. Energie: Strom, Wärme, Kälte, Druckluft, Speicher. Ressourcen: Material, Wasser, Reststoffe, Betriebsstoffe. **Kein PV**, keine Gruppe „Eigenerzeugung“. Steine abgerundet, oben Medien-Symbol, vorne Prozessname (passt sich der Breite an). Unter der Zeichnung die Auswahl-Buttons und (seit Version 76, Wunsch „alle 6 Punkte umsetzen“) ein Satz zum Ablauf: „Für jeden Stein: messen, nachrechnen, umsetzen. Sie entscheiden, welche Steine auf die Platte kommen.“ Keine Erklär-Box, keine Zahlenzeile.
- **Persönliche Handschrift:** Die Gründer wollen „keine KI-Anmutung, sondern unsere Handschrift“. Die Handschrift-Notiz am Baukasten ist **auf Wunsch entfernt** (24.09., „stört“); der `NOTE`-Text im JS bleibt als Reserve, ist aber ohne Element wirkungslos. Handschrift lebt derzeit an der Kurve im Einstieg und in der Team-Verbindung. Kein getippter Einleitungstext, keine Unterschrift.
- **Navigation:** nur „Kontakt“ (springt zum Erstgespräch-Button, `#kontakt`). Frühere Punkte Effizienz-Baukasten · Praxisbeispiele · Team sind auf Wunsch entfernt.
- **Ecken:** Die Gründer wollen es „runder“. Buttons 10 bis 12 px Radius, Baukasten-Steine mit weicher Silhouette. Das überstimmt die Briefing-Regel gegen Rundungen, Schatten bleiben aber tabu.
- **Signaturelement:** Korrekturzeichen nach DIN 16511 (feine 2-px-Streichung, nummeriertes Zeichen, korrigierter Wert in Mono am Rand). Kein dicker Marker-Strich, keine Marker-Schrift.
- **Kein Punktraster** im Hintergrund.
- **Farben:** Petrol #0F3B3F, Tiefe #071F22, Papier #F7F5F0, Sand #E9E1CF, Nebel #EEF0EC. Akzentfarbe ist **Lime #C8F04A** (entschieden 24.09., „nur die zweite Farbvariante weiterverfolgen“). Ocker, Mint und Terrakotta sind verworfen, der Farbschalter ist entfernt. Lime nur als Marker, Punkt oder Fläche; auf hellem Grund nie als Schrift. Der Logo-Punkt bekommt auf hellem Grund einen feinen Ring in der Kurvenfarbe. In `build.py` heißt die Konstante aus historischen Gründen noch `OCKER`, sie enthält aber Lime.
- **Schriften:** IBM Plex Sans (Text/Headlines), IBM Plex Mono (Zahlen/Labels), Kalam nur für kleine Notizen.

## Tabus aus dem Briefing

Keine Verläufe, keine Pill-Buttons, keine Karten mit Schatten, kein zentrierter Hero mit zwei Buttons, keine Windräder, Glühbirnen, Blätter oder Weltkugeln, kein Inter, keine pauschale ROI-Zahl im Hero, kein Beratersprech. Kontrast mindestens WCAG AA. Lime auf Papier/Weiß ist nie Schrift (ca. 1,2 : 1).

## Git

- Branch: `claude/new-session-syvaun`. Es ist der einzige Branch im Repo, deshalb gibt es noch keinen Pull Request.
- Commit-Footer laut System-Reminder der jeweiligen Session setzen.
