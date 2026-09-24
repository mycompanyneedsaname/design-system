# HANDOFF · Stand 24.09.2026

## Wo wir stehen

Die Gründer arbeiten an der **Markenwelt**: Deliverable 1 aus dem Briefing, jetzt als ausgearbeitete Startseite plus Markensystem. Sie geben Feedback per Kommentar direkt im Artifact.

**Live-Seite (Hauptarbeit):** https://claude.ai/artifact/NRh2JC1PZLoyYuV4VstHeP
(UUID-Form in Kommentar-Benachrichtigungen: `https://claude.ai/code/artifact/ad826d4f-3948-4412-b55c-7b5bc7f6ae10`). Aktuell Version 31, privat. Die Freigabe macht der Nutzer über das Share-Menü.

Weitere Artifacts:
- Logo-Kurvenvergleich (abgeschlossen): https://claude.ai/artifact/UsjPbmEEpBYStt4gh1TZeu
- Frühere drei Richtungen (historisch): https://claude.ai/artifact/4QPfXqBFdVBtJZyoHRLtb6

Aus einer neuen Session ein Artifact **immer mit `url`** neu veröffentlichen und es vorher mit `action: "read"` lesen.

## Aufbau der Markenwelt-Seite (von oben nach unten)

Kopfleiste (Petrol): Logo ohne Untertitel (steht jetzt im Einstieg), Navigation als Sprunglinks (#baukasten, #praxis, #team), Farbschalter „Marker“.

**Startseite (Reihenfolge seit Version 30):**
1. **Wendepunkt** (Sand, `#start`): „Wir sind ein Büro für Energie- und Ressourceneffizienz.“, H1, Satz, Lime-Button, animierte Kurve mit Handschrift davor/danach und „hier.“. Von den Gründern ausdrücklich geliebt.
2. **Team** (`#team`): Micha und Tobias mit Rolle, zwei Sätzen und einem handschriftlichen Zitat. Foto-Platzhalter.
3. **Referenzen** (`#praxis`, Nebel): drei knappe Zeilen, Beispielwerte.
4. **Baukasten** (Petrol, `#baukasten`): Versprechen-Headline plus klickbarer isometrischer Baukasten, neun Felder (Energie: Strom, Wärme, Kälte, Druckluft, Speicher; Ressourcen: Material, Wasser, Reststoffe, Betriebsstoffe), Handschrift-Notiz, die je Stein wechselt.

**Trennband „Ab hier: Markensystem“**, danach:
3. **Signaturelement**: drei Beispiele mit Korrekturzeichen.
4. **Baukasten-Übersicht** (`#bausteine`): zwölf isometrische Module.
5. **Icons und Fotografie**: Hand-Icons, Foto mit Annotation.
6. **Plakatserie**: Kurve, Baukasten, Korrektur.
7. **Anwendung**: Bericht, LinkedIn-Post, Visitenkarte, E-Mail-Signatur.
8. **Mini-System**: Farben, Schriften, Regeln.
9. **Herkunft**: Was aus dem Moodboard (ecoworks, Academy for Climate Jobs, Anthropic) übernommen wurde.

## Offene Punkte

- **Offener Kommentar-Thread** `b2ecf904-e9a3-4ddd-93d3-e3ef5e4e16fe` zur Unterzeile: gesetzt ist „Weniger Verbrauch, mehr Spielraum.“, angeboten wurden „Effizienz, die sich rechnet.“ und „Weniger Energie. Weniger Material. Mehr Luft.“ Antwort der Gründer abwarten, dann ggf. tauschen und den Thread auflösen.
- **Offener Kommentar-Thread** `c4f123c5-264b-48ad-ad31-030e61e93764` zur Feld-Gruppierung: Frage, ob die Baukasten-Übersicht weiter unten nachgezogen werden soll. Gruppierung wurde seitdem weiter angepasst (Speicher zu Energie, PV gestrichen).

- **Akzentfarbe:** Lime ist Favorit, aber noch nicht entschieden. Der Schalter bleibt, bis die Gründer festlegen. Danach Schalter entfernen und die Farbe fest setzen. Dabei prüfen: Ein Lime-Punkt im Logo auf hellem Grund hat wenig Kontrast. Eventuell bleibt der Punkt auf hellen Flächen petrol- oder ockerfarben.
- **Baukasten-Übersicht weiter unten** (zwölf Module) mischt noch Leistungen (Messen, Nachrechnen …) und alte Medien (Abwärme, PV, Speicher einzeln). Auch Plakat 02 und die Handschrift-Notizen am Foto nennen teils noch alte Felder. Sollte an die neue Gruppierung aus dem Hero angepasst werden.
- **Abschnitte 3 bis 9** haben noch kein direktes Feedback bekommen. Sie enthalten noch Texte, die zum neuen Stand passen sollten. Nach Tagen oder „Effizienz-Kompass“ ist bereits bereinigt.
- **Handschrift:** Kalam ist Platzhalter und den Gründern besonders wichtig („die Leute haben keinen Bock mehr auf KI“). Angefragt: ein Foto mit der Standard-Notiz und den neun Feld-Notizen, mit dickem Filzstift auf weißem Papier. Dann als SVG-Pfade oder als eigene Schrift einbauen.
- **Gründerfotos und echte Referenzen** fehlen noch. Die Team-Texte stammen aus den Notion-Antworten und sollten von den Gründern gegengelesen werden. Alle Zahlen auf der Seite sind Beispielwerte.
- **Pull Request:** Das Repo hat nur den Branch `claude/new-session-syvaun`. Einen PR gibt es erst, wenn ein Basis-Branch wie `main` existiert.

## Nächste Deliverables laut Briefing (nach Freigabe der Markenwelt)

2. Design System als Code-Paket (Tokens, Typo-Skala, Spacing, 12 Icons, Diagramm-Stil, Button, Formular, Tabelle) für `/design-sync`. Den Befehl startet der Nutzer selbst.
3. Wort-Bild-Marke final (Voll-, Kurz-, Signet-Version, SW/negativ, SVG + PNG).
4. Website-Startseite Desktop und Mobile.
5. Angebots- und Berichtsvorlage A4.
6. Briefkopf nach DIN 5008 und E-Mail-Signatur.
7. Visitenkarte und LinkedIn-Material.

## Quellen

- Briefing: zwei hochgeladene „Claude-Design-Input_Wendepunkt-Ingenieure“-Dateien, nicht im Repo. Der Kern steht in CLAUDE.md.
- Notion: „2.5 Brand Briefing“ und „3.5.1 Fragen an Tobias und Michael“ (über den Notion-Connector erreichbar).
- Moodboard-PDF des Nutzers: ecoworks, The Academy for Climate Jobs, Claude by Anthropic. Produktidee „Efficiency as a Service“ bzw. „Modularer Effizienz-Baukasten“.
