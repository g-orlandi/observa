<h2> Documentazione progetto Tecnologie Web </h2>
<h1 align="center">Observa</h1>

<p align="center">Giovanni Orlandi / A.A. 2024-2025</p>

---

README e' presente su github e lo mando insieme a quando mando questo file

---

Funzionalita' richieste

---

Organizzazione logica dell'applicazione

---

Scelte implementative

--- 

Test fatti

---

Risultati raggiunti

---

Possibili migliorie



## Template

Sono stati suddivisi in due app:

1. users -> tutti i template che riguardano la gestione dell'utente
2. frontend -> tutti i template che sono visti dall'utente e che non riguardano direttamente la gestione dell'utente

2. Frontend
   
**/templates/frontend/** -> a piu' alto livello ci sono i template di base; ne sono stati realizzati 3, per diversi livelli di riutilizzabilita':

- templates/frontend/base.html -> questo e' il template usato da praticamente tutte le pagine come punto di partenza. Molto generico e "scarno", ma serve per dare omogeneita' a tutte le pagine
- templates/frontend/info_base.html -> template comune a tutte le pagine di visualizzazione con la stessa struttura, ovvero con i due selettori e i valori attuali/storici. Estende dal base.html e aggiunge altre cose, molto utilizzate
- templates/fronted/info.html -> si distingue da info_base.html, estendolo, perche' questo template e' quello usato dalle pagine che mostrano misure singole (/backup, /network, /resources), mentre l'altro viene usato anche dalla dashboard che e' un po' differente. Aver creato un'ulteriore pagina permette di "riciclare" questo template su tutte e 3 le pagine citate, rendendolo riutilizzabile grazie alle variabili di contesto passate dalle views. Risulta anche abbastanza facile cosi' facendo l'aggiunta/modifica di widget e grafici, basta infatti cambiare solo le variabili di contesto (e aggiungere le query al db) per vedere cambiamenti nel fe.

**/templates/frontend/pages** -> contiene i file delle pagine che l'utente vede. 

- endpoints.html -> la pagina che si occupa del listing degli endpoint e utilizza le dialog per aggiunte, modifiche e eliminazione (presenti nella cartella components). 
- dashboard.html -> come detto, e' la pagina che implementa la visione sinottica e che estende da info_base.html
- resources.html -> resources e' l'unica pagina delle 3 (/network, /backup e appunto /resources) che non estende direttamente info.html, perche' ci sono certi widget un po' piu' complessi. Si poteva anche gestire quelli, ma dopo il DTL diventava ancora piu' complesso; e' stata invece prevista una sezione per aggiungere altri widget a quelli passati dalle variabili di contesto, cosi' da rendere possibile in modo agevole queste ulteriori personalizzazioni.



**templates/frontend/components** -> racchiude un insieme di singole componenti, semplicemente incluse in altre pagine e messe in file separati per rendere un po' piu' pulito il codice, oltre a componenti utili per getire le modali di aggiunta di endpoint.