# Wendepunkt Ingenieure · So baust du mit dieser Marke

Dieses Design-System hat **keine React-Komponenten**. Es liefert eine Stilvorlage (`styles.css`) mit CSS-Variablen und `wp-`-Klassen plus Leitfäden in `guidelines/docs/` (`marke.md`, `logo.md`, `icons.md`). Baue Layouts mit normalem JSX/HTML und setze diese Klassen und Variablen ein. Erfinde keine eigenen Farben, Schriften oder Icons. Lies vor dem Gestalten `guidelines/docs/marke.md`: dort stehen Kernsätze, Farbregeln und Tabus.

## Farben und Schriften (nur diese)

`var(--wp-petrol)` #0F3B3F · `var(--wp-deep)` #071F22 · `var(--wp-lime)` #C8F04A · `var(--wp-paper)` #F7F5F0 · `var(--wp-sand)` #E9E1CF · `var(--wp-mist)` #EEF0EC · `var(--wp-ink)` · `var(--wp-muted)` · `var(--wp-line-light)` · `var(--wp-line-dark)`. Schriften: `var(--wp-sans)` (IBM Plex Sans), `var(--wp-mono)` (Plex Mono, für Zahlen und Labels), `var(--wp-hand)` (Kalam, nur kurze Notizen). Radius `var(--wp-radius)` 12px.

**Harte Regel:** Lime ist nie Schriftfarbe auf Papier, Sand, Nebel oder Weiß. Lime nur als Marker, Punkt, Linie, Fläche, oder als Schrift/Zahl auf Petrol und Tiefe. Auf Lime-Flächen immer Petrol-Schrift. Keine Verläufe, keine Schatten auf Karten, keine Pill-Buttons, kein Punktraster, nie Inter.

## Klassen

| Zweck | Klassen |
|---|---|
| Flächen | `wp-paper`, `wp-sand`, `wp-mist` (hell), `wp-petrol`, `wp-deep` (dunkel, weiße Schrift) |
| Layout | `wp-body`, `wp-wrap` (max. 1200px), `wp-section` (72px oben/unten) |
| Schrift | `wp-h1`, `wp-h2`, `wp-h3`, `wp-lead`, `wp-eyebrow` (Mono-Label), `wp-num` (Mono-Zahl), `wp-hand` (Notiz), `wp-muted` |
| Marker | `wp-hl` (Lime-Textmarker, höchstens einer pro Block), `wp-korr` mit `wp-alt`, `wp-km`, `wp-neu` (Korrekturzeichen) |
| Bausteine | `wp-cta` (einziger Button), `wp-link`, `wp-role` (Fachgebiet über dem Namen), `wp-card` (Linie statt Schatten), `wp-sum` + `wp-foot` (große Summe auf Petrol), `wp-logo` + `wp-w1`/`wp-w2`, `wp-icon`, `wp-badge` |

Innerhalb von `wp-petrol`/`wp-deep` stellen sich `wp-korr`, `wp-role`, `wp-cta` und `wp-card` selbst auf den dunklen Grund um.

## Beispiel

```jsx
<section className="wp-section wp-sand">
  <div className="wp-wrap">
    <span className="wp-eyebrow">Praxisbeispiel</span>
    <h2 className="wp-h2">Wir nehmen es <mark className="wp-hl">persönlich</mark>.</h2>
    <p className="wp-lead">In rund <strong>150 Betrieben</strong> des verarbeitenden Gewerbes haben wir das schon getan.</p>
    <div className="wp-korr" style={{fontSize: 32, fontWeight: 600, marginTop: 24}}>
      <span className="wp-alt">Rechnet sich sofort.</span><span className="wp-km">1</span>
      <span className="wp-neu"><span className="wp-km">1</span>Druckluft 5 Monate · Beleuchtung 3,3 Jahre</span>
    </div>
    <a className="wp-cta" href="#kontakt" style={{marginTop: 32}}>Kostenfreies Erstgespräch vereinbaren</a>
  </div>
</section>
```

Logo-Markup steht in `guidelines/docs/logo.md`, die zwölf Icons als SVG in `guidelines/docs/icons.md`. Texte auf Deutsch in Sie-Form, kein Beratersprech, Zahlen immer mit Einheit.
