# Gap-Analyse zur Aufgabenstellung

## Bereits umgesetzt

- Weltkarte mit Lieferanten, Häfen, Flughäfen, Bahnterminals, Lagern und Werk
- Sechs parallele Komponentenlieferketten
- Multimodaler gewichteter Graph mit LKW, Bahn, See, Luft und Binnenschiff
- Strategien FASTEST, CHEAPEST, LOWEST_CO2 und MOST_RESILIENT
- Multisourcing mit Ersatzlieferanten
- Ereignisse für Krieg, Streik, Lieferantenausfall, Knoten- und Kanalblockade
- Automatisches Rerouting und KPI-Aktualisierung
- Kostenmodell mit Einkauf, Arbeit, Transport, Zoll, Qualität, Risiko, Bestand und CO2
- KPI-Dashboard und Vergleich mit Referenzlauf

## Für eine vollständige Prüfungsumsetzung noch offen oder nur teilweise vorhanden

1. **Szenario speichern und laden**: In den Diagrammen vorgesehen, aber kein belastbarer JSON-Import/Export aus der UI.
2. **Ergebnisse exportieren**: CSV/JSON-Bericht mit Run-ID, Seed, Konfiguration, Routen und KPI-Zeitreihe fehlt.
3. **Echte stochastische Simulation**: Reproduzierbarer Random Seed, Verteilungen für Nachfrage, Transportzeit und Reparaturdauer fehlen oder sind nur Demo-Rauschen.
4. **Bestands- und Produktionskopplung**: Inventory-Klassen existieren, sind aber nicht vollständig mit den sechs Komponenten, Aufträgen und Montagefreigabe verbunden.
5. **Kapazitätsrestriktionen**: Supplier- und Edge-Kapazitäten werden gespeichert, aber Routing und Warteschlangen berücksichtigen sie noch nicht.
6. **Nachfrageszenarien**: Nachfrageanstieg ist als UI-Szenario vorhanden, beeinflusst aber Beschaffungsmenge, Bestand und Kapazitätsauslastung noch nicht durchgängig.
7. **Kalibrierung und Validierung**: Modellannahmen sind dokumentiert; formale Plausibilitäts-, Sensitivitäts- und Vergleichsläufe fehlen als automatisierter Bericht.
8. **Netzwerkdaten verwalten**: Admin-Use-Case ist konzeptionell vorhanden, aber kein UI-Editor für Knoten, Kanten und Wirtschaftsparameter.
9. **Windows-EXE-Abnahme**: Buildskript ist vorhanden; Funktionsprüfung auf einem fremden Windows-Rechner ohne Entwicklungsumgebung bleibt notwendig.
10. **Persistenz**: JSON ist vorhanden, SQLite-Tabellen für Simulation Runs, Events, Routes und KPI Results sind noch nicht produktiv angebunden.

## Priorität für die Demo

Für eine stabile Vorführung sind Suez-Rerouting, Ersatzlieferanten, Strategieänderung, sechs Lieferketten, KPI-Aufteilung und Reset ausreichend. Export, Stochastik, Kapazitätswarteschlangen und SQLite sollten transparent als nächste Ausbaustufe bezeichnet werden.
