# Spaß-Club-Demo

## Beschreibung

Diese Software wurde zu Demonstrationszwecken erstellt. Das Onlineportal ermöglicht das Erfassen von Spielergebnissen
mit einigen relevanten Metainformationen.

## Starten der App

Wenn alle Packages in requirements.txt verfügbar sind, in app.py ausführen.
Getestet wurde diese Software mit Python 3.10.


## Dashboard

Auf dem Dashboard finden Sie einige Beispiele für Widgets.

### Widgets

#### Die letzte Runde

In dieser Kachel wird die aktuellste Runde (nach Datum/Uhrzeit) angezeigt.

#### Die aktivsten Spieler

In dieser Kachel wird angezeigt, welche 3 Spieler die meisten eingetragenen Ergebnisse (nur Anzahl, unabhängig von der
Punktzahl) haben.

#### Das letzte Event

In dieser Kachel wird das aktuellste Event mit allen gespielten Runden angezeigt.

Weitere Widgets können auf Wunsch hinzugefügt werden.

## Aktivitäten

In der Tabelle "activity" werden Aktivitäten erfasst.

## Spieler

In der Tabelle "player" werden Spieler erfasst.

## Orte

In der tabelle "locations" werden Spielorte erfasst. Jedes Event und jede Runde findet an einem solchen Ort statt.

## Events

In der Tabelle "events" werden Events erfasst. Events fassen mehrere Runden zusammen.

## Runden

In der tabelle "match" werden Spielrunden erfasst. Eine Runde KANN zu einem Event gehören. Um Ergebnisse zu erfassen,
muss vorher die Runde erfasst werden.

## Ergebnisse

In der tabelle "score" werden Spielergebnisse erfasst. Ein Ergebnis setzt sich zusammen aus Runde, Spieler, Zeitpunkt
und Punktzahl.

## Test-Daten zurücksetzen

Mit dem Button "Test-Daten zurücksetzen" wird die aktuelle Datenbank gelöscht und wieder mit Testdaten gefüllt. Diese
Funktion existiert nur zur Demonstration.

### Hinweis

Wenn die Datenbank in einem anderen Programm geöffnet ist, können die Daten nicht zurückgesetzt werden!
