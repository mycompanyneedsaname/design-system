# Wendepunkt Ingenieure · Design System

Marke: **Wendepunkt Ingenieure – Büro für Energie- und Ressourceneffizienz** (GbR, 2026, Thüringen/Leipzig).

## Stand

| # | Deliverable | Ort | Status |
|---|---|---|---|
| 1 | Drei Richtungen (Moodboard, Mini-System, Logo-Skizze, Hero) | `richtungen/index.html` | Arbeitsstand: Kombination Logo 1 + Farben 2 |
| 2 | Design System (Tokens, Typo, Spacing, Icons, Komponenten) | folgt nach Auswahl | offen |
| 3–7 | Logo final, Website, Vorlagen, Briefkopf, Visitenkarte, LinkedIn | folgt | offen |

## Entscheidung Logo (24.09.2026)

Das Logo bleibt wie es ist: Kurve mit der steilsten Stelle am Wendepunkt, „Wendepunkt“ 600, „Ingenieure“ 400. Die Variante mit flachster Stelle am Punkt (`logo/vergleich.html`) ist verworfen.

## Entwurf 4: Markenwelt nach Moodboard (aktuell)

`markenwelt/index.html` (Landingpage) und `markenwelt/markensystem.html` (Markensystem, seit 24.09. getrennt), beide erzeugt durch `markenwelt/build.py` (isometrische Bausteine werden berechnet, nicht von Hand gezeichnet).

- **Signaturelement:** gedruckte Behauptung, Marker-Strich in Ocker, Ergebnis in Handschrift (Kalam 700) mit Einheit und Kontext.
- **Produktbild:** der modulare Effizienz-Baukasten als isometrische Bausteine auf der Grundplatte „Effizienz-Kompass“.
- **Hand-Icons:** zwölf Ein-Strich-Icons, leicht gewellt, Ocker auf Petrol, Petrol auf Papier.
- **Flächen:** Petrol #0F3B3F und Tiefe #071F22 mit Punktraster für Bühne und Social; Papier #F7F5F0, Sand #E9E1CF, Nebel #EEF0EC für Dokumente.
- **Logo:** unverändert Michas Variante, Punkt in Ocker.

Herkunft: ecoworks (dunkler Grund, Isometrie, Schraffur), The Academy for Climate Jobs (Durchstreichen, Marker, Hand-Icons, Foto-Annotation), Anthropic (Papier, Sand, Plakatserie, ruhige Grotesk). Nicht übernommen: Neongrün, Terrakotta, Kritzeleien um Gesichter.

## Vorher: Kombination Logo 1 + Farben 2

Logo aus Richtung 1 in Michas Gewichtung (IBM Plex Sans, „Wendepunkt“ 600, „Ingenieure“ 400), Bildmarke Kurve mit Punkt. Farben aus Richtung 2: Weiß #FFFFFF, Petrol #0F3B3F, Ocker #D9A441, Fläche #EEF0EC. Der Punkt im Logo ist ocker, Petrol übernimmt Kennzahlen, Button und Priorität A. Typografie bleibt IBM Plex Sans + IBM Plex Mono.

## Richtungen (Version 2, verbindliche Werte laut Briefing)

1. **Nachgerechnet** – Präzisionsinstrument. #F7F5F0 · #1A1A18 · Kupfer #B85C38 · Linien #D8D3C8. IBM Plex Sans 600/400 + IBM Plex Mono. Signet: Kurve mit genau einem Krümmungswechsel.
2. **Werkbank** – Nah an der Halle. #FFFFFF · Petrol #0F3B3F · Ocker #D9A441 · Fläche #EEF0EC. Space Grotesk 500 + Source Sans 3. Signet: Kurvenwende im Quadrat, kleingeschriebene Wortmarke, Dreiwort-Claim.
3. **Kernig** – Editorial, plakativ. #111111 / #FFFFFF · Safran #F2B705 · Grau #8A8A8A. Archivo Expanded 700 + Archivo 400 + Archivo Narrow. Signet: Pfeil-Wende.

Kontrast-Hinweise: Kupfer auf Grund 4,2 : 1 (nur große Zahlen), Ocker auf Weiß 2,3 : 1 (nie Schrift), Grau auf Weiß 3,5 : 1 (nur große Schrift).

Die Seite `richtungen/index.html` ist eigenständig (nur Google Fonts als externe Abhängigkeit) und kann direkt im Browser geöffnet werden.

## Nächster Schritt

Nach der Auswahl einer Richtung wird sie hier als Code-Paket (Tokens + React-Komponenten + Preview-HTML) ausgebaut, sodass `/design-sync` das System nach Claude Design hochladen kann.

- **24.09.2026:** Akzentfarbe festgelegt auf Lime #C8F04A („nur die zweite Farbvariante weiterverfolgen“). Ocker, Mint und Terrakotta verworfen, Farbschalter entfernt.
