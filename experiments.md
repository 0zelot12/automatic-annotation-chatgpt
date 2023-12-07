# Variables

## Only definitions (Zero-Shot)

## One-Shot (Beispiele)

## One-Shot (Beispiele + IOB-Format (Meta-Language Definition Pattern))

# Metrics

## Precision

## Recall

## F-Score

### Exact Match

### Partial Match

### Catergorical Relaxation

#### Welche Kategorien können zusammengefasst werden?

##### AND-Gateway + XOR-Gateway

##### Further Specification + Condition Specification

##### Further Specification + No Annotation

### Fragment Match

# Experiments

Die Dokumente werden einzeln und nacheinander bzw. Satz für Satz an das Modell zum annotieren gebeben.
Die relevanten Metriken werden pro Satz und Dokument berechnet und zum Schluss werden die Metriken noch mal zusammgengefasst.

<!-- doc-1.1
    - Sentence 1
        - Precision
        - Recall
        - F-Score
        - Length
    - Sentence 2
        - Precision
        - Recall
        - F-Score
        - Length
    - Precision
    - Recall
    - F-Score
    - Length
- Precision
- Recall
- F-Score
... -->

Das Experiment muss mindestens zwei bis drei mal ausgeführt werden, da ChatGPT nicht deterministisch arbeitet.
