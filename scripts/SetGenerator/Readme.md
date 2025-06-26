### **TrialSetGenerator.py**

### **Configuration**

* Setzt einen Zufalls-Seed für Reproduzierbarkeit.

* Definiert:

  * 20 Probanden

  * 120 Trials pro Proband

  * 100 Bilder pro Kategorie (nature, urban, indoor)

  * 20 % der Trials sollen Baseline-Trials sein, der Rest manipuliert.

* Drei Manipulationstypen: size, form, background, jeweils mit zwei Ausprägungen.

### **Paarbildung**

* Für jede Kategorie (nature, urban, indoor) werden 100 Bildnamen erzeugt (z. B. urban\_001.jpg).

* Es werden alle möglichen Bildpaare aus unterschiedlichen Kategorien gebildet

* Alle Paare werden zufällig durchgemischt.

### **Initialisierung**

* Leere Trial-Listen pro Proband.

* Für jeden Probanden wird gespeichert:

  * welche Bilder schon benutzt wurden,

  * wie viele Baselines und Manipulationen je Art/Ausprägung schon verwendet wurden.

### **Zuweisung der Paare**

* Für jedes Bildpaar:

  * Es wird je ein Trial an zwei unterschiedliche Probanden vergeben:

    * einer bekommt das Paar als img\_left \= A, img\_right \= B (normal)

    * der andere als img\_left \= B, img\_right \= A (gespiegelt)

  * Die Probanden werden dabei zyklisch paarweise durchlaufen (subject\_1 & subject\_2, subject\_3 & subject\_4).

### **Trial-Erstellung**

Für jeden Probanden (normal und gespiegelt):

* Wenn noch Baseline-Trials fehlen:

  * Setzt attribute \= none, value \= none

  * Wählt zufällig target\_image (links oder rechts)

  * Erstellt den cb\_index als z. B. baseline\_nature-urban\_L

* Sonst:

  * Wählt zufällig eine Manipulationsart und \-ausprägung, außer das entsprechende Limit ist noch nicht erreicht

  * Wählt zufällig die Seite, auf der das manipulierte Bild liegt

  * Setzt attribute, value, target\_image, cb\_index entsprechend

### **SetAnalyzer.py**
Der SetAnalyzer.py liefert Verteilungsanalysen über die subject\_sets.

| attribute\_distribution  | Häufigkeiten der verschiedenen Attribute (Manipulationen) insgesamt |
| :---- | :---- |
| cb\_index\_usage | Häufigkeit der verschiedenen cb\_indexes insgesamt |
| image\_usage | Häufigkeit der verschiedenen images insgesamt |
| subject\_summary | Häufigkeit der verschiedenen Attribute aufgeschlüsselt nach Probanden |

