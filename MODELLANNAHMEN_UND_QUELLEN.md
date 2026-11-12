# Modellannahmen und Kalibrierung

Dieses Paket ist eine simulationsfähige Kalibrierung, keine Animation. Die Routen verwenden reale Ankerpunkte, Haversine-Distanzen mit Umwegfaktoren und verkehrsträgerspezifische Kosten-, Geschwindigkeits- und Emissionsfaktoren.

## Transparenz

In der aktuellen Ausführungsumgebung war kein Web-Recherchewerkzeug verfügbar. Deshalb sind aktuelle gesetzliche Mindestlöhne und konkrete Lieferantenangebote nicht als verifizierte Fakten eingetragen. Stattdessen werden fachlich plausible, editierbare Modellwerte verwendet. Die Werte sind in `data/economics/` zentral dokumentiert und für Sensitivitätsanalysen vorgesehen.

## Transportfaktoren

Die Bereiche orientieren sich an typischen europäischen Logistik- und GLEC/DEFRA-Größenordnungen: Seeschiff ca. 0,012 kg CO2e/tkm, Güterbahn ca. 0,022, Binnenschiff ca. 0,031, Lkw ca. 0,105 und Luftfracht ca. 0,602. Preise sind Marktmodellwerte pro Tonnenkilometer, keine Speditionsangebote.

## Zoll

Zoll wird einmal auf Basis des Ursprungslands beim Import nach Deutschland berechnet, nicht für Transitländer. EU-Lieferanten haben im Modell 0 % Binnenzoll. Die Nicht-EU-Sätze sind pauschale Szenariowerte und keine TARIC-Klassifizierung. Für eine rechtliche Berechnung wären Warennummern je Komponente erforderlich.

## Arbeitskosten

`loaded_labor_cost_eur_h` beschreibt modellierte Arbeitgeber-Gesamtkosten pro produktiver Stunde, nicht nur einen gesetzlichen Mindestlohn. Dadurch werden Lohnnebenkosten und Produktivität näherungsweise berücksichtigt.

## Gesamtkosten

Gesamtkosten = Material + Arbeit + Qualitätsverlust + Transport und Handling + Zoll + Risikoaufschlag + Kapitalbindung + CO2-Preis.
