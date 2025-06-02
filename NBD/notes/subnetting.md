# Esercizio 1: IP Subnetting

**Domanda:** Spiegami perché sono 6 reti (networks) nella slide sul subnetting, analizza tutto l’esercizio e rispiegamelo come farebbe un professore di networking.

---

## 1. Il contesto generale

Nel diagramma vediamo tre router principali, indicati con le lettere **A**, **B** e **C**, collegati fra loro e ciascuno “a monte” o “a valle” di reti locali (LAN) o dell’Internet. In particolare:

1. **Router B** è collegato a due LAN:
   - la LAN denominata **pc-net**, che dovrà contenere 100 host;
   - la LAN denominata **ws-net**, che dovrà contenere 50 host.

2. **Router A** è collegato a una LAN:
   - la LAN denominata **x-net-1**, che dovrà contenere 20 host.

3. **Router C** è collegato all’**Internet**, che in questo schema viene vista come una rete esterna.

4. I router **A**, **B** e **C** sono collegati fra loro con tre collegamenti punto-punto (Link). In particolare:
   - **Link-1** fra **B** ↔ **A**
   - **Link-2** fra **B** ↔ **C**
   - **Link-3** fra **A** ↔ **C**

Lo schema complessivo (semplificato) è:

 pc-net   100 host
      │
      B
     / \
Link-1/ \Link-2
A C — Internet
│ (rete esterna)
x-net-1 20 |
20 host |
\Link-3/



---

## 2. Cosa intendiamo con “numero di reti” (o “subnet”)

Quando si chiede “quante reti?” in un esercizio di subnetting, si intende individuare **ogni segmento di collegamento fisico o logico** che deve ricevere un proprio blocco IP (prefisso). In IPv4, ogni rete (o subnet) ha:

- Un **indirizzo di rete** (network address).
- Una **maschera** (subnet mask).
- Un **broadcast** (indirizzo di broadcast).
- Una serie di **indirizzi host** utilizzabili.

Per progettare il piano di indirizzamento IP, dobbiamo quindi “riconoscere” ogni tratto di comunicazione (sia LAN tradizionali che collegamenti punto-punto) e assegnarvi un blocco IP distinto.

### 2.1. Tipologie di segmenti di rete nel diagramma

1. **Reti LAN “multi-host”** (domini di broadcast):
   - **pc-net** (100 host)
   - **ws-net** (50 host)
   - **x-net-1** (20 host)

2. **Collegamenti punto-punto tra router** (router-router links):
   - **Link-1** (fra B e A)
   - **Link-2** (fra B e C)
   - **Link-3** (fra A e C)

3. **Collegamento verso Internet** (rete esterna)  
   Il collegamento del router **C** verso l’Internet non viene conteggiato nel “numero di reti interne” perché è già un blocco assegnato dal provider e non è parte del piano di subnetting aziendale da progettare.

---

## 3. Identificazione delle 6 reti interne

### 3.1. Le 3 LAN “di host”

1. **pc-net** (100 host)  
   È una LAN collegata a **B** (router). Tutti gli host di `pc-net` condividono lo stesso prefisso IP.  
   → **Rete interna #1**.

2. **ws-net** (50 host)  
   È un’altra LAN collegata sempre a **B**. Serve 50 indirizzi IP.  
   → **Rete interna #2**.

3. **x-net-1** (20 host)  
   È una LAN collegata a **A**. Serve 20 indirizzi IP.  
   → **Rete interna #3**.

### 3.2. I 3 collegamenti punto-punto tra router

4. **Link-1 (B ↔ A)**  
   Collegamento diretto fra l’interfaccia di **B** e l’interfaccia di **A**. In IPv4 va trattato come una subnet a sé stante con **due** host (i router stessi).  
   → **Rete interna #4**.

5. **Link-2 (B ↔ C)**  
   Collegamento diretto fra l’interfaccia di **B** e l’interfaccia di **C**. Anche questa è una subnet “punti-a-punto” con due host.  
   → **Rete interna #5**.

6. **Link-3 (A ↔ C)**  
   Collegamento diretto fra l’interfaccia di **A** e l’interfaccia di **C**. Stessa logica: è un’altra piccola subnet con solo due host (i due router).  
   → **Rete interna #6**.

> **Nota importante:** ciascun collegamento router–router **deve** avere un proprio blocco IP (in genere un `/30` in IPv4), anche se contiene solo due indirizzi host utili. Se non assegnassimo un blocco IP dedicato a ogni link, i router non avrebbero un mutual next-hop corretto e i protocolli di routing non saprebbero su quale prefisso collegarli.

---

## 4. Perché non si conta la connessione verso Internet

Nel diagramma è mostrata la nuvola **Internet** collegata a **C**, ma **quel segmento non viene incluso** nel conteggio delle reti “internamente suddivise” per questi motivi:

1. **Blocco IP fornito dal provider:** di solito l’indirizzo (o il piccolo blocco /30) assegnato per la connessione al provider ISP è già prefissato da chi eroga il servizio.  
2. **Esercizi didattici:** tipicamente si chiede di contare e pianificare le subnet all’interno dell’organizzazione/azienda. La connessione verso Internet è esterna a questo perimetro e, perciò, non rientra nelle “6 reti” di cui parla la slide.

---

## 5. Ripartizione e dimensionamento delle subnet

Una volta individuati i **6 segmenti di rete interni**, il passo successivo di un esercizio di subnetting sarebbe:

1. **Stimare quanti host servono in ogni LAN “multi-host”** e assegnare la maschera più adatta.
2. **Stimare quanti indirizzi servono in ogni collegamento punto-punto** e assegnare la maschera più piccola (tipicamente `/30`).

Di seguito un esempio di **piano di indirizzamento IPv4** che raggruppa tutte e sei le reti in un unico blocco “padre” (ad esempio `192.168.1.0/24`), partendo da zero e procedendo in ordine:

| Rete fisica     | Numero di host necessari | Prefisso IPv4 consigliato | # indirizzi totali |    Note    |
|-----------------|--------------------------|---------------------------|--------------------|------------|
| **pc-net**      | 100                      | `/25`                     | 128 (126 utili)    | primo blocco: `192.168.1.0/25` |
| **ws-net**      | 50                       | `/26`                     | 64 (62 utili)      | secondo blocco: `192.168.1.128/26` |
| **x-net-1**     | 20                       | `/27`                     | 32 (30 utili)      | terzo blocco: `192.168.1.192/27` |
| **Link-1 (B↔A)**| 2                        | `/30`                     | 4 (2 utili)        | quarto blocco: `192.168.1.224/30` |
| **Link-2 (B↔C)**| 2                        | `/30`                     | 4 (2 utili)        | quinto blocco: `192.168.1.228/30` |
| **Link-3 (A↔C)**| 2                        | `/30`                     | 4 (2 utili)        | sesto blocco: `192.168.1.232/30` |

### 5.1. Assegnazione dettagliata degli intervalli

1. **Rete `pc-net` (100 host) → `192.168.1.0/25`**  
   - Rete = `192.168.1.0`  
   - Maschera = `255.255.255.128`  
   - Host utilizzabili = `192.168.1.1` … `192.168.1.126` (126 indirizzi validi)  
   - Broadcast = `192.168.1.127`  

2. **Rete `ws-net` (50 host) → `192.168.1.128/26`**  
   - Rete = `192.168.1.128`  
   - Maschera = `255.255.255.192`  
   - Host utilizzabili = `192.168.1.129` … `192.168.1.190` (62 indirizzi validi)  
   - Broadcast = `192.168.1.191`  

3. **Rete `x-net-1` (20 host) → `192.168.1.192/27`**  
   - Rete = `192.168.1.192`  
   - Maschera = `255.255.255.224`  
   - Host utilizzabili = `192.168.1.193` … `192.168.1.222` (30 indirizzi validi)  
   - Broadcast = `192.168.1.223`  

4. **Link-1 (B ↔ A) → `192.168.1.224/30`**  
   - Rete = `192.168.1.224`  
   - Maschera = `255.255.255.252`  
   - Host utilizzabili = `192.168.1.225` (interfaccia B), `192.168.1.226` (interfaccia A)  
   - Broadcast = `192.168.1.227`  

5. **Link-2 (B ↔ C) → `192.168.1.228/30`**  
   - Rete = `192.168.1.228`  
   - Maschera = `255.255.255.252`  
   - Host utilizzabili = `192.168.1.229` (interfaccia B), `192.168.1.230` (interfaccia C)  
   - Broadcast = `192.168.1.231`  

6. **Link-3 (A ↔ C) → `192.168.1.232/30`**  
   - Rete = `192.168.1.232`  
   - Maschera = `255.255.255.252`  
   - Host utilizzabili = `192.168.1.233` (interfaccia A), `192.168.1.234` (interfaccia C)  
   - Broadcast = `192.168.1.235`  

**Rimangono liberi** gli indirizzi da `192.168.1.236` a `192.168.1.255` (20 indirizzi), che si possono tenere in riserva per futuri ampliamenti o per un’eventuale rete di gestione.

---

## 6. Ricapitolando: “Perché 6 reti?”

1. **Le 3 reti LAN multi-host**:
   - pc-net (100 host)  
   - ws-net (50 host)  
   - x-net-1 (20 host)  

2. **I 3 collegamenti punto-punto fra router** (ognuno richiede un blocco /30):
   - Link-1 (B ↔ A)  
   - Link-2 (B ↔ C)  
   - Link-3 (A ↔ C)  

3. **La connessione verso Internet** non è conteggiata perché è un blocco esterno già assegnato dal provider.

In totale, **6 reti interne** devono essere progettate e suddivise in IPv4. Questo è il motivo per cui sulla slide, quando compare la domanda “How many networks?”, la risposta è scritta “6”.

---

## 7. Conclusione “alla lavagna”

> **Domanda dello studente:**  
> “Professore, guardi che ci sono solo 3 LAN con 100, 50 e 20 host: perché la slide parla di 6 reti, non di 3?”  
>
> **Risposta del professore:**  
> “Perché, oltre alle tre LAN di host, ci sono altri **tre** segmenti di collegamento tra i router che devono essere trattati come subnet IPv4 separate. Anche un singolo collegamento “punti-a-punti” fra due router richiede un suo proprio prefisso (tipicamente `/30`) per assegnare un indirizzo IP a ciascuna interfaccia del router. Se non assegnassimo un blocco IP distinto a `Link-1`, `Link-2` e `Link-3`, i router non avrebbero un next-hop definito e non saprebbero scambiarsi routing o pacchetti dati. Quindi, le reti interne da progettare sono 6: tre di tipo “LAN” (100, 50, 20 host) e tre di tipo “Punto-Punto” (ogni link router–router).”
>
> **Nota finale:** la connessione verso Internet non si conta perché è un blocco IP fornito dal provider, già preconfigurato: non fa parte del piano di subnetting interno che dobbiamo suddividere.

Con questa spiegazione dettagliata, ora è chiaro **quali** sono le sei reti, **perché** ciascun collegamento router–router è considerato una rete a sé e **come** assegnare le maschere IP in modo ordinato per ricavare tutti i prefissi senza sovrapposizioni.  
