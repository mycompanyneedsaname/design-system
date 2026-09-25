# Formen: alles rund

Die Marke ist weich, nicht eckig. Das gilt für jede Fläche, jeden Kasten und jede Zeichnung.

- **Radius:** Buttons, Karten, Bilder, Plakate, Tabellen und farbige Flächen `var(--wp-radius)` 12px; kleine Karten `var(--wp-radius-sm)` 10px; Labels, Chips und Bildunterschriften `var(--wp-radius-xs)` 8px. Rahmen mit `overflow: hidden`, damit Inhalte die Rundung nicht anschneiden.
- **Keine spitzen Ecken:** keine Kästen mit 0px Radius, keine Pill-Form (voll gerundet) für Buttons. Kreise nur für Punkte, Zählzeichen und Symbol-Badges.
- **Linien:** immer `stroke-linecap: round` und `stroke-linejoin: round`.
- **Baukasten-Steine:** isometrische Quader mit **weicher Silhouette**: Die Außenkontur ist an jeder Ecke abgerundet (Radius ca. 28 % der Kantenlänge), die drei Innenkanten enden kurz vor der Kontur. Flächen Petrol-Töne (`#14474C` oben, `#0B3236` links, `#0E393D` rechts), Linie Lime 1,5 bis 1,6 px, Schraffur auf der rechten Seite für „umgesetzt“. Keine scharfkantigen Würfel.
- **Schatten** bleiben tabu, auch mit Rundung.

## Vorlage: ein Stein (Strom)

```html
<svg viewBox="-58 -78 116 144" aria-hidden="true"><clipPath id="pb15"><path d="M7.3 -67.8 L44.7 -46.2 Q52.0 -42.0 52.0 -33.6 L52.0 21.6 Q52.0 30.0 44.7 34.2 L7.3 55.8 Q0.0 60.0 -7.3 55.8 L-44.7 34.2 Q-52.0 30.0 -52.0 21.6 L-52.0 -33.6 Q-52.0 -42.0 -44.7 -46.2 L-7.3 -67.8 Q0.0 -72.0 7.3 -67.8 Z"/></clipPath><g clip-path="url(#pb15)">
<polygon points="-52.0,30.0 0.0,60.0 0.0,-12.0 -52.0,-42.0" fill="#0B3236"/>
<polygon points="52.0,30.0 0.0,60.0 0.0,-12.0 52.0,-42.0" fill="#0E393D"/>
<polygon points="0.0,-72.0 52.0,-42.0 0.0,-12.0 -52.0,-42.0" fill="#14474C"/>
<line x1="39.0" y1="37.5" x2="39.0" y2="-34.5" stroke="#C8F04A" data-ak="s" stroke-width="1" stroke-opacity=".45"/>
<line x1="26.0" y1="45.0" x2="26.0" y2="-27.0" stroke="#C8F04A" data-ak="s" stroke-width="1" stroke-opacity=".45"/>
<line x1="13.0" y1="52.5" x2="13.0" y2="-19.5" stroke="#C8F04A" data-ak="s" stroke-width="1" stroke-opacity=".45"/>
<path d="M1.7 -13.0 L50.2 -41.0 M-1.7 -13.0 L-50.2 -41.0 M0.0 -10.0 L0.0 58.0" fill="none" stroke="#C8F04A" data-ak="s" stroke-width="1.27" stroke-opacity=".75" stroke-linecap="round"/>
</g><path d="M7.3 -67.8 L44.7 -46.2 Q52.0 -42.0 52.0 -33.6 L52.0 21.6 Q52.0 30.0 44.7 34.2 L7.3 55.8 Q0.0 60.0 -7.3 55.8 L-44.7 34.2 Q-52.0 30.0 -52.0 21.6 L-52.0 -33.6 Q-52.0 -42.0 -44.7 -46.2 L-7.3 -67.8 Q0.0 -72.0 7.3 -67.8 Z" fill="none" stroke="#C8F04A" data-ak="s" stroke-width="1.5"/></svg>
```
