# TrustML

Il presente repository contiene il codice utilizzato per il lavoro di Tesi - per il corso di laurea triennale in Informatica presso l'Università degli Studi di Firenze - dal titolo "Come posso fidarmi di un Machine Learner?" con autore Leonardo Bargiotti.

Il dataset NSL-KDD non è mio ma è stato preso dalla repository ondivisa dagli autori originali a [https://www.unb.ca/cic/datasets/nsl.html]

Nel file di configurazione config.cfg è necessario specificare:
* il dataset in formato .csv oppure MNIST (prende in input il dataset contenente 70000 immagini 28x28 raffiguranti le 10 cifre scritte a mano, 60000 nel traning set e 10000 nel test set),
* i classificatori,
* il nome della colonna corrispondente alle classi,
* il numero massimo di righe che utlizzano i classificatori.

In particolare il contenuto è così suddiviso:
* trust_main: è il main che prende le informazioni la config.cfg per l'esecuzione e restituisce un file .csv contenete le colonne corrispondenti alle label dei dati, la classe corretta, la classe predetta, se la classificazione è giusta oppure no, le probabilità dei classificatori e le colonne corrispondenti alle strategie di trust utilizzate,
* Classifier: contiene l'implementazione dei classificatori,
* TrustCalculator: contiene l'implementazione delle strategie per il calcolo della fiducia.

Il codice è scritto in Python.
