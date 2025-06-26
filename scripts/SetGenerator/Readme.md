### [**Configuration**](http://SetAnalyzer.py)

* [Setzt einen Zufalls-Seed für Reproduzierbarkeit.](http://SetAnalyzer.py)

* [Definiert:](http://SetAnalyzer.py)

  * [20 Probanden](http://SetAnalyzer.py)

  * [120 Trials pro Proband](http://SetAnalyzer.py)

  * [100 Bilder pro Kategorie (nature, urban, indoor)](http://SetAnalyzer.py)

  * [20 % der Trials sollen Baseline-Trials sein, der Rest manipuliert.](http://SetAnalyzer.py)

* [Drei Manipulationstypen: size, form, background, jeweils mit zwei Ausprägungen.](http://SetAnalyzer.py)

### [**Paarbildung**](http://SetAnalyzer.py)

* [Für jede Kategorie (nature, urban, indoor) werden 100 Bildnamen erzeugt (z. B. urban\_001.jpg).](http://SetAnalyzer.py)

* [Es werden alle möglichen Bildpaare aus unterschiedlichen Kategorien gebildet](http://SetAnalyzer.py)

* [Alle Paare werden zufällig durchgemischt.](http://SetAnalyzer.py)

### [**Initialisierung**](http://SetAnalyzer.py)

* [Leere Trial-Listen pro Proband.](http://SetAnalyzer.py)

* [Für jeden Probanden wird gespeichert:](http://SetAnalyzer.py)

  * [welche Bilder schon benutzt wurden,](http://SetAnalyzer.py)

  * [wie viele Baselines und Manipulationen je Art/Ausprägung schon verwendet wurden.](http://SetAnalyzer.py)

### [**Zuweisung der Paare**](http://SetAnalyzer.py)

* [Für jedes Bildpaar:](http://SetAnalyzer.py)

  * [Es wird je ein Trial an zwei unterschiedliche Probanden vergeben:](http://SetAnalyzer.py)

    * [einer bekommt das Paar als img\_left \= A, img\_right \= B (normal)](http://SetAnalyzer.py)

    * [der andere als img\_left \= B, img\_right \= A (gespiegelt)](http://SetAnalyzer.py)

  * [Die Probanden werden dabei zyklisch paarweise durchlaufen (subject\_1 & subject\_2, subject\_3 & subject\_4).](http://SetAnalyzer.py)

### [**Trial-Erstellung**](http://SetAnalyzer.py)

[Für jeden Probanden (normal und gespiegelt):](http://SetAnalyzer.py)

* [Wenn noch Baseline-Trials fehlen:](http://SetAnalyzer.py)

  * [Setzt attribute \= none, value \= none](http://SetAnalyzer.py)

  * [Wählt zufällig target\_image (links oder rechts)](http://SetAnalyzer.py)

  * [Erstellt den cb\_index als z. B. baseline\_nature-urban\_L](http://SetAnalyzer.py)

* [Sonst:](http://SetAnalyzer.py)

  * [Wählt zufällig eine Manipulationsart und \-ausprägung, außer das entsprechende Limit ist noch nicht erreicht](http://SetAnalyzer.py)

  * [Wählt zufällig die Seite, auf der das manipulierte Bild liegt](http://SetAnalyzer.py)

  * [Setzt attribute, value, target\_image, cb\_index entsprechend](http://SetAnalyzer.py)

[Der SetAnalyzer.py liefert Verteilungsanalysen über die subject\_sets.](http://SetAnalyzer.py)

| [attribute\_distribution](http://SetAnalyzer.py)  | [Häufigkeiten der verschiedenen Attribute (Manipulationen) insgesamt](http://SetAnalyzer.py) |
| :---- | :---- |
| [cb\_index\_usage](http://SetAnalyzer.py) | [Häufigkeit der verschiedenen cb\_indexes insgesamt](http://SetAnalyzer.py) |
| [image\_usage](http://SetAnalyzer.py) | [Häufigkeit der verschiedenen images insgesamt](http://SetAnalyzer.py) |
| [subject\_summary](http://SetAnalyzer.py) | [Häufigkeit der verschiedenen Attribute aufgeschlüsselt nach Probanden](http://SetAnalyzer.py) |

