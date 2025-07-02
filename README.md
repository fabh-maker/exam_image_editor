# Image editor
Scrivere un programma python che permetta di comporre delle immagini.

I moduli e le classi vanno sviluppati nel package *image_editor*.
Non spostare o rinominare moduli e classi esistenti e non modificare le signature dei metodi.

In *main.py* viene fornito del semplice codice, da voi modificabile, che testa le funzionalità base.
Esso mostra esempi di uso dei metodi principali dei controlli richiesti.

Tutte le eccezioni, se non altrimenti specificato, sono di tipo *ImageEditorException* definito nel modulo *exceptions*.


## R1: Elementi grafici (5/18)
La dataclass *TupleRC*, già implementata, rappresenta una tupla di valori riga (r) e colonna (c).

La classe astratta *GraphicalElement*, definita nel modulo *elements*, rappresenta un elemento grafico.
Un elemento grafico è essenzialmente una matrice bidimensionale di pixel.
Ogni pixel è rappresentato da un numero intero nel range [0, 255] che ne identifica il colore in scala di grigi (0->Nero, 255->Bianco).

La classe ha le seguenti properties:
- ```name(self) -> str``` nome dell'elemento grafico.
- ```dims(self) -> TupleRC``` dimensioni dell'elemento grafico, in termini di numero di righe e colonne della matrice di pixel, rappresentate come una *TupleRC* (r = righe, c = colonne).
- ```bitmap(self) -> List[List[int]]``` la matrice di pixel dell'elemento grafico (**PROPERTY ASTRATTA**).

La classe *ImageEditor*, definita nel modulo *image_editor*, permette creare due tipologie di elementi grafici.

Il metodo
```python
new_rectangle(self, name: str, dims: TupleRC, color: int) -> GraphicalElement
```
restituisce un elemento grafico rettangolare monocromatico (tutti i pixel hanno lo stesso colore), il cui nome, dimensioni e colore sono passati come parametri.

Il metodo
```python
new_image(self, name: str, fname: str) -> GraphicalElement
```
restituisce un elemento grafico rappresentante un'immagine caricata da file.
Il metodo accetta come parametri il nome dell'elemento grafico e il nome del file da cui caricare l'immagine.
Le immagini sono salvate in un formato testuale.
Su ogni riga del file, corrispondente a una riga della matrice di pixel, i colori di ciascun pixel sono rappresentati da numeri interi separati da spazi.
Un esempio di file d'immagine è *data/img.txt*.

I metodi ```new_rectangle``` e ```new_image``` lanciano un'eccezione se un elemento grafico con lo stesso nome, di qualunque tipo esso sia, è già stato definito.

**ATTENZIONE**: quando il tipo dell'oggetto restituito da un metodo è **GraphicalElement**, la notazione include anche le classi figlie (**GraphicalElement** è astratto).


## R2 Layer (5/18)
La classe *Layer*, definita nel modulo *elements*, rappresenta un livello (layer) dell'immagine che si vuole comporre tramite il programma.
Ogni layer contiene un elemento grafico, che viene sovrapposto a quello contenuto nel layer sottostante per la creazione dela composizione finale.
La posizione di un elemento grafico in un layer è definito tramite le coordinate del pixel corrispondente al vertice in alto a sinistra, espresse come riga e colonna (r, c).

La classe ha le seguenti properties:
- ```elm(self) -> GraphicalElement``` elemento grafico contenuto nel layer.
- ```pos(self) -> TupleRC``` coordinate dell'elemento grafico contenuto nel layer.
- ```below(self) -> Optional["Layer"]``` layer sottostante, **None** se invocata sul primo layer.
- ```above(self) -> Optional["Layer"]``` layer sovrastante, **None** se invocata sull'ultimo layer.

Il metodo
```python
add_layer(self, elm_name: str, pos: TupleRC) -> Layer
```
della classe *ImageEditor*, permette di creare un nuovo layer da aggiungere in cima a quelli già presenti.
Riceve come parametri il nome dell'elemento grafico da inserire nel layer e la sua posizione.
Lo **STESSO** elemento grafico può essere inserito **IN PIÙ DI UN LAYER**.
Il metodo lancia un'eccezione se l'elemento grafico da inserire nel layer non è stato definito.

**ATTENZIONE**: le coordinate (r,c) di un elemento grafico in un layer possono assumere valori negativi.

**SUGGERIMENTO** le connessioni tra layer (properties **above** e **below**) formano una double-linked list.


## R3: Riordinamento layer (4/18)
Il metodo
```python
move_below(self, layer: Layer) -> None
```
della classe *ImageEditor* permette di spostare un layer passato come parametro più in basso di una posizione.
Tutti i collegamenti *below* e *above* devono essere aggiornati per i layer interessati dallo spostamento.
Se il layer passato come parametro è già quello più in basso non devono essere effettuati cambiamenti.


## R4: Rendering (4/18)
Il metodo
```python
overlay(self, layer: "GraphicalElement", pos: TupleRC) -> None
```
della classe *GraphicalElement* permette di modificare l'elemento grafico su cui è invocato, sovrapponendone un secondo.
Il metodo accetta come parametri l'elemento grafico da sovrapporre e la sua posizione (r, c).
Assumere che l'elemento grafico da modificare sia posizionato in (0, 0).

L'elemento grafico modificato **NON** deve variare le sue dimensioni, ma i suoi pixel devono assumere il colore di quello sovrastante nelle zone di sovrapposizione.

L'elemento grafico che viene sovrapposto **NON** deve essere modificato.

Il metodo
``` python
render(self, dims: TupleRC) -> GraphicalElement
```
della classe *Layer* permette di renderizzare il layer, **CREANDO** un elemento grafico dato dalla sovrapposizione degli elementi grafici contenuti nel layer stesso e in quelli sottostanti.
Gli elementi grafici ciascun layer, partendo dal quello più in basso, devono essere sovrapposti, uno dopo l'altro, a un nuovo elemento grafico rettangolare che agisce come sfondo.
La posizione del rettangolo di sfondo è (0, 0), mentre la posizione degli elementi da sovrapporre è quella indicata in ciascun layer.
Le dimensioni dell'elemento grafico di sfondo, che saranno le medesime dell'elemento grafico risultante, sono quelle passate come parametro al metodo.
Il rettangolo di sfondo deve essere nero (0).

**NESSUN** elemento grafico contenuto nei layer deve essere **MODIFICATO**.

**SUGGERIMENTO**: per effettuare il rendering creare un il nuovo elemento grafico di sfondo e invocare più volte **overlay** sui di esso, al fine di sovrapporre, di volta in volta, gli elementi grafici di ciascun layer.
In questo modo gli elementi grafici contenuti nei layer non vengono modificati.
