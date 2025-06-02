# Esercizio Passo-Passo: IP Subnetting da `192.168.0.0/24`

Di seguito presento una guida dettagliata per comprendere **passo per passo** l’“Exercise 1: IP Subnetting” tratto dalle slide del corso :contentReference[oaicite:0]{index=0}. L’esercizio parte da un blocco padre `192.168.0.0/24` e richiede di ricavarne **6 reti interne** (3 LAN “multi-host” + 3 collegamenti punto-punto fra router).  

---

## 1.  Analisi preliminare: riconoscere le 6 reti

Nel diagramma di riferimento compaiono tre router (A, B, C) e tre LAN di host, oltre a tre link punto-punto fra i router. In sintesi:

1. **Router B** è collegato a due LAN:
   - **pc-net**: servono 100 host (più 1 indirizzo per l’interfaccia di B).  
   - **ws-net**: servono 50 host (più 1 indirizzo per l’interfaccia di B).  

2. **Router A** è collegato a una LAN:
   - **x-net-1**: servono 20 host (più 1 indirizzo per l’interfaccia di A).  

3. I router **A**, **B**, **C** sono interconnessi tramite tre link punto-punto:
   - **Link-1** (fra B e A): servono 2 indirizzi (uno per la I/F di B, uno per la I/F di A).  
   - **Link-2** (fra B e C): servono 2 indirizzi (uno per la I/F di B, uno per la I/F di C).  
   - **Link-3** (fra A e C): servono 2 indirizzi (uno per la I/F di A, uno per la I/F di C).  

4. **Router C** ha un’ulteriore interfaccia verso l’“Internet” (nuvola esterna), ma **questo collegamento non** va conteggiato nel piano interno: il blocco IP lato provider è già assegnato e non fa parte delle reti “da progettare” :contentReference[oaicite:1]{index=1}.

Pertanto, **le 6 reti interne** da creare sono:

1. **pc-net** (100 host + interfaccia B) → rete “multi-host”  
2. **ws-net** (50 host + interfaccia B) → rete “multi-host”  
3. **x-net-1** (20 host + interfaccia A) → rete “multi-host”  
4. **Link-1** (2 indirizzi: eth2 di B ↔ eth0 di A) → rete “punto-punto”  
5. **Link-2** (2 indirizzi: eth3 di B ↔ eth2 di C) → rete “punto-punto”  
6. **Link-3** (2 indirizzi: eth2 di A ↔ eth0 di C) → rete “punto-punto”  

> **Nota importante:**  
> Una LAN “multi-host” ha bisogno di **N<sub>host</sub> + 1** indirizzi (i N<sub>host</sub> corrispondono ai computer veri e propri e “+1” è l’interfaccia del router collegato).  
> Ogni link “punto-punto” ha bisogno di esattamente 2 indirizzi host (uno per ciascun router).

---

## 2.  Calcolo del numero di bit `nh` per ogni rete

In IPv4 la regola per determinare quanti bit servono nella porzione **Host ID** affinché siano disponibili almeno **_M_** indirizzi utili è:

2^nh − 2 ≥ M



dove:
- `nh` = numero di bit destinati agli host  
- `2^nh` = numero totale di indirizzi del blocco (inclusi network e broadcast)  
- `– 2` = sottrazione di indirizzo di rete (tutti 0) e indirizzo di broadcast (tutti 1).  

Per ciascuna delle sei reti, applichiamo questa formula; i risultati sono riportati nelle slide :contentReference[oaicite:2]{index=2}:

1. **pc-net**  
   - Occorrono **101** indirizzi (100 host + 1 interfaccia del router).  
   - Cerco `nh` tale che `2^nh − 2 ≥ 101`:  
     - Se `nh = 6` → `64 − 2 = 62` (INSUFFICIENTE)  
     - Se `nh = 7` → `128 − 2 = 126` (sufficiente)  
   - **Conclusione:** `nh = 7` → **prefisso = /25** (32 − 7 = 25 bit di rete).  

2. **ws-net**  
   - Occorrono **51** indirizzi (50 host + 1 interfaccia di B).  
   - Cerco `nh` tale che `2^nh − 2 ≥ 51`:  
     - `nh = 5` → `32 − 2 = 30` (INSUFFICIENTE)  
     - `nh = 6` → `64 − 2 = 62` (sufficiente)  
   - **Conclusione:** `nh = 6` → **prefisso = /26** (32 − 6 = 26 bit di rete).  

3. **x-net-1**  
   - Occorrono **21** indirizzi (20 host + 1 interfaccia di A).  
   - Cerco `nh` tale che `2^nh − 2 ≥ 21`:  
     - `nh = 4` → `16 − 2 = 14` (INSUFFICIENTE)  
     - `nh = 5` → `32 − 2 = 30` (sufficiente)  
   - **Conclusione:** `nh = 5` → **prefisso = /27** (32 − 5 = 27 bit di rete).  

4. **Link-1 (B ↔ A)**  
   - Occorrono **2** indirizzi (interfacce di B e A).  
   - Cerco `nh` tale che `2^nh − 2 ≥ 2`:  
     - `nh = 2` → `4 − 2 = 2` (sufficiente)  
   - **Conclusione:** `nh = 2` → **prefisso = /30** (32 − 2 = 30 bit di rete).  

5. **Link-2 (B ↔ C)**  
   - Occorrono **2** indirizzi (interfacce di B e C).  
   - Stessa logica → `nh = 2` → **prefisso = /30**.  

6. **Link-3 (A ↔ C)**  
   - Occorrono **2** indirizzi (interfacce di A e C).  
   - Stessa logica → `nh = 2` → **prefisso = /30**.  

Riassumendo:

| Rete        | Host necessari | `2^nh − 2 ≥ #host` | `nh` | Prefisso (maschera)  |  
|-------------|----------------|--------------------|------|----------------------|  
| pc-net      | 101            | `2^7 − 2 = 126 ≥ 101`  | 7   | `/25` (`255.255.255.128`)  |  
| ws-net      | 51             | `2^6 − 2 = 62 ≥ 51`   | 6   | `/26` (`255.255.255.192`)  |  
| x-net-1     | 21             | `2^5 − 2 = 30 ≥ 21`   | 5   | `/27` (`255.255.255.224`)  |  
| Link-1      | 2              | `2^2 − 2 = 2 ≥ 2`    | 2   | `/30` (`255.255.255.252`)  |  
| Link-2      | 2              | `2^2 − 2 = 2 ≥ 2`    | 2   | `/30` (`255.255.255.252`)  |  
| Link-3      | 2              | `2^2 − 2 = 2 ≥ 2`    | 2   | `/30` (`255.255.255.252`)  |  

> Questi valori (`nh` e prefissi) sono esattamente quelli riportati nelle slide del professore :contentReference[oaicite:3]{index=3}.

---

## 3.  Suddivisione del blocco `192.168.0.0/24` in 6 sottoreti

Partiamo dal blocco “padre” `192.168.0.0/24` (maschera `255.255.255.0`) e lo spezziamo in **ordine decrescente** di dimensione (dall’host-count più grande al più piccolo), in modo da usare i bit in modo “compatto” senza sovrapposizioni.  

> **Regola generale (VLSM):**  
> - Prima assegniamo la sottorete più ampia (`/25` per 126 indirizzi)  
> - Poi prendiamo il blocco libero rimasto e ricaviamo la sottorete `/26`  
> - Poi `/27`, e infine i tre blocchi `/30`.  

### 3.1.  Allocazione di **pc-net** (`/25`)

- **Prefisso scelto:** `192.168.0.0/25`  
  - Rete = `192.168.0.0`  
  - Maschera = `255.255.255.128`  
  - **Host utilizzabili:** `192.168.0.1 … 192.168.0.126` (126 indirizzi)  
  - **Broadcast:** `192.168.0.127`  

- **Assegnazioni specifiche** :contentReference[oaicite:4]{index=4}:  
  - Interfaccia **eth0 di router B** (gateway di pc-net) = `192.168.0.1/25`  
  - Gli host (100 dispositivi veri) vanno da `192.168.0.2` fino a `192.168.0.101`.  
    - Rimane spazio ancora da `192.168.0.102` a `192.168.0.126` per futuri ampliamenti.  

**Blocco occupato**: da `192.168.0.0` a `192.168.0.127`  

---

### 3.2.  Allocazione di **ws-net** (`/26`)

A questo punto il primo blocco ("/25") occupa `192.168.0.0 – 192.168.0.127`. Il prossimo indirizzo “libero” è `192.168.0.128`.  

- **Prefisso scelto:** `192.168.0.128/26`  
  - Rete = `192.168.0.128`  
  - Maschera = `255.255.255.192`  
  - **Host utilizzabili:** `192.168.0.129 … 192.168.0.190` (62 indirizzi)  
  - **Broadcast:** `192.168.0.191`  

- **Assegnazioni specifiche** :contentReference[oaicite:5]{index=5}:  
  - Interfaccia **eth1 di router B** (gateway di ws-net) = `192.168.0.129/26`  
  - Gli host (50 dispositivi veri) vanno da `192.168.0.130` a `192.168.0.179`.  
    - Rimangono **liberi** gli indirizzi da `192.168.0.180 a 192.168.0.190` per futuri ampliamenti.  

**Blocco occupato**: da `192.168.0.128` a `192.168.0.191`  

---

### 3.3.  Allocazione di **x-net-1** (`/27`)

Dopo il blocco `/26` (che finisce a `192.168.0.191`), il prossimo indirizzo “libero” è `192.168.0.192`.  

- **Prefisso scelto:** `192.168.0.192/27`  
  - Rete = `192.168.0.192`  
  - Maschera = `255.255.255.224`  
  - **Host utilizzabili:** `192.168.0.193 … 192.168.0.222` (30 indirizzi)  
  - **Broadcast:** `192.168.0.223`  

- **Assegnazioni specifiche** :contentReference[oaicite:6]{index=6}:  
  - Interfaccia **eth1 di router A** (gateway di x-net-1) = `192.168.0.193/27`  
  - Gli host (20 dispositivi veri) vanno da `192.168.0.194` a `192.168.0.213`.  
    - Rimangono **liberi** gli indirizzi da `192.168.0.214 a 192.168.0.222` per possibili ampliamenti.  

**Blocco occupato**: da `192.168.0.192` a `192.168.0.223`  

---

### 3.4.  Allocazione di **Link-1** (`/30`)

Dopo il blocco `/27` (che finisce a `192.168.0.223`), il prossimo indirizzo “libero” = `192.168.0.224`. Vogliamo una sottorete `/30` (4 indirizzi totali, di cui 2 host).  

- **Prefisso scelto:** `192.168.0.224/30`  
  - Rete = `192.168.0.224`  
  - Maschera = `255.255.255.252`  
  - **Host utilizzabili:** `192.168.0.225` e `192.168.0.226`  
  - **Broadcast:** `192.168.0.227`  

- **Assegnazioni specifiche** :contentReference[oaicite:7]{index=7}:  
  - **eth2 di router B** = `192.168.0.225/30`  
  - **eth0 di router A** = `192.168.0.226/30`  

**Blocco occupato**: da `192.168.0.224` a `192.168.0.227`  

---

### 3.5.  Allocazione di **Link-2** (`/30`)

Dopo Link-1 (`192.168.0.224/30` → termina a `192.168.0.227`), il prossimo indirizzo “libero” = `192.168.0.228`. Anche questo sarà un `/30`.  

- **Prefisso scelto:** `192.168.0.228/30`  
  - Rete = `192.168.0.228`  
  - Maschera = `255.255.255.252`  
  - **Host utilizzabili:** `192.168.0.229` e `192.168.0.230`  
  - **Broadcast:** `192.168.0.231`  

- **Assegnazioni specifiche** :contentReference[oaicite:8]{index=8}:  
  - **eth3 di router B** = `192.168.0.229/30`  
  - **eth2 di router C** = `192.168.0.230/30`  

**Blocco occupato**: da `192.168.0.228` a `192.168.0.231`  

---

### 3.6.  Allocazione di **Link-3** (`/30`)

A questo punto avremmo potuto prendere il blocco libero successivo immediatamente dopo `192.168.0.231`, cioè `192.168.0.232`. Tuttavia, nelle slide l’esercente ha scelto di **saltare** alcuni indirizzi e utilizzare il blocco che inizia a `192.168.0.248` per semplicità (magari lasciando spazio per reti di servizio o per evitare confusione).  

- **Prefisso scelto:** `192.168.0.248/30`  
  - Rete = `192.168.0.248`  
  - Maschera = `255.255.255.252`  
  - **Host utilizzabili:** `192.168.0.249` e `192.168.0.250`  
  - **Broadcast:** `192.168.0.251`  

- **Assegnazioni specifiche** :contentReference[oaicite:9]{index=9}:  
  - **eth2 di router A** = `192.168.0.249/30`  
  - **eth0 di router C** = `192.168.0.250/30`  

> **Perché saltare da .231 a .248?**  
> Non è “obbligatorio” scegli `192.168.0.248`; si poteva usare `192.168.0.232/30` e così via.  
> In questo caso, però, l’esercente ha preferito lasciare un intervallo libero (`.232 … .247`) per poterci in futuro “inserire” altre reti di servizio o link aggiuntivi.  

**Blocco occupato**: da `192.168.0.248` a `192.168.0.251`  

---

### 3.7.  Riepilogo complessivo delle 6 sottoreti

| N. | Rete         | Prefisso         | Rete (network)   | Maschera                 | Host utilizzabili (range)                         | Broadcast         | Interfacce router       |  
|----|--------------|------------------|------------------|--------------------------|---------------------------------------------------|-------------------|-------------------------|  
| 1  | pc-net       | `192.168.0.0/25` | `192.168.0.0`    | `255.255.255.128`        | `192.168.0.1 … 192.168.0.126` (126 indirizzi)     | `192.168.0.127`   | `B eth0 → 192.168.0.1`   |  
|    |              |                  |                  |                          | (router B: .1; host reali da .2 a .101)            |                   |                         |  
| 2  | ws-net       | `192.168.0.128/26`| `192.168.0.128`  | `255.255.255.192`        | `192.168.0.129 … 192.168.0.190` (62 indirizzi)    | `192.168.0.191`   | `B eth1 → 192.168.0.129` |  
|    |              |                  |                  |                          | (router B: .129; host reali da .130 a .179)        |                   |                         |  
| 3  | x-net-1      | `192.168.0.192/27`| `192.168.0.192`  | `255.255.255.224`        | `192.168.0.193 … 192.168.0.222` (30 indirizzi)    | `192.168.0.223`   | `A eth1 → 192.168.0.193` |  
|    |              |                  |                  |                          | (router A: .193; host reali da .194 a .213)        |                   |                         |  
| 4  | Link-1 (B↔A) | `192.168.0.224/30`| `192.168.0.224`  | `255.255.255.252`        | `192.168.0.225 … 192.168.0.226` (2 indirizzi)     | `192.168.0.227`   | `B eth2 → .225; A eth0 → .226` |  
| 5  | Link-2 (B↔C) | `192.168.0.228/30`| `192.168.0.228`  | `255.255.255.252`        | `192.168.0.229 … 192.168.0.230` (2 indirizzi)     | `192.168.0.231`   | `B eth3 → .229; C eth2 → .230` |  
| 6  | Link-3 (A↔C) | `192.168.0.248/30`| `192.168.0.248`  | `255.255.255.252`        | `192.168.0.249 … 192.168.0.250` (2 indirizzi)     | `192.168.0.251`   | `A eth2 → .249; C eth0 → .250` |  

> **Rimangono liberi** gli indirizzi da `192.168.0.232 a 192.168.0.247` (16 indirizzi) e quelli da `192.168.0.252 a 192.168.0.255` (4 indirizzi), complessivamente 20 indirizzi di riserva. :contentReference[oaicite:10]{index=10}  

---

## 4.  Commenti e motivazioni “alla lavagna”

1. **Perché 6 reti, non 3?**  
   - **Studente:** “Professore, vedo solo 3 LAN con 100, 50 e 20 host: perché nella slide c’è scritto “How many networks? 6?””  
   - **Professore:** “Ottima domanda! Le **prime tre** reti (pc-net, ws-net, x-net-1) sono LAN “multi-host”, ovvero domini di broadcast tradizionali in cui possono coesistere tutti gli host di ogni gruppo. Ma, per far “parlare” i tre router fra di loro, abbiamo bisogno di **tre collegamenti punto-punto** (Link-1, Link-2, Link-3). Ognuno di questi link, anche se ospita solo **due interfacce** (un “host” di ciascun router), dev’essere trattato come una piccola **subnet IPv4** a sé stante. Senza quest’ultimo passaggio non potremmo assegnare un IP alle interfacce dei router, e di conseguenza non potremmo attivare il routing interno. Quindi, nel conteggio totale delle reti interne, si sommano:  
     1. pc-net (100 host)  
     2. ws-net (50 host)  
     3. x-net-1 (20 host)  
     4. Link-1 (B ↔ A)  
     5. Link-2 (B ↔ C)  
     6. Link-3 (A ↔ C)  
     e perciò sono **6** reti, non 3.   

2. **Perché usare `/30` per ogni Link punto-punto?**  
   - Ogni link punto-punto deve fornire **esattamente 2 indirizzi host** (uno per ciascun router). In IPv4 il blocco più piccolo che consente 2 indirizzi host utili + indirizzo di rete + broadcast è **`/30`** (4 indirizzi totali, di cui 2 utilizzabili).  
   - Alcuni sistemi moderni (RFC 3021) supportano `/31` (2 indirizzi totali: 0 e 1, senza broadcast), ma nelle esercitazioni didattiche quasi sempre si insegna a usare `/30` per chiarezza. :contentReference[oaicite:12]{index=12}  

3. **Perché saltare da `.231` a `.248` per Link-3?**  
   - Non c’è un vincolo tecnico che obblighi a usare il blocco `192.168.0.248/30` per Link-3: si poteva usare `192.168.0.232/30`, `192.168.0.236/30`, ecc.  
   - Il docente ha preferito lasciare **uno spazio “intermedio”** (`.232 … .247`) come area di riserva, utile per:  
     - future espansioni interne (nuove LAN di test, reti di management, VLAN di sicurezza)  
     - evitare di “impazzire” nel contare troppi blocchi consecutivi quando si disegna sulla lavagna.  
   - In sintesi, è una scelta di praticità didattica per avere un “buffer” di indirizzi fra i link che non “si accavallino” facilmente. :contentReference[oaicite:13]{index=13}  

---

## 5.  Assegnazione finale e possibili tabelle di routing

### 5.1.  Riepilogo assegnazione indirizzi a interfacce router

- **Router B**  
  - `eth0` (verso pc-net) = `192.168.0.1/25`  
  - `eth1` (verso ws-net) = `192.168.0.129/26`  
  - `eth2` (verso Link-1) = `192.168.0.225/30`  
  - `eth3` (verso Link-2) = `192.168.0.229/30`  

- **Router A**  
  - `eth0` (verso Link-1) = `192.168.0.226/30`  
  - `eth1` (verso x-net-1) = `192.168.0.193/27`  
  - `eth2` (verso Link-3) = `192.168.0.249/30`  

- **Router C**  
  - `eth0` (verso Link-3) = `192.168.0.250/30`  
  - `eth1` (verso Link-2) = `192.168.0.230/30`  
  - `eth2` (verso Internet) = (assegnato dal provider, non usato nel conteggio)  

> **Nota:** vista la posizione di ogni interfaccia, ogni router ha 3 interfacce “interne” (A e B e C), e − per C − una quarta verso l’Internet.

---

### 5.2.  Esempio di tabella di routing per **Router B** :contentReference[oaicite:14]{index=14}

Destinazione	Maschera	Next Hop	Interfaccia Uscita
192.168.0.0	255.255.255.128 (/25)	–	eth0 (pc-net)
192.168.0.128	255.255.255.192 (/26)	–	eth1 (ws-net)
192.168.0.192	255.255.255.224 (/27)	192.168.0.226	eth2 (Link-1 verso A)
192.168.0.248	255.255.255.252 (/30)	192.168.0.226	eth2 (via Link-1 → router A → Link-3)
192.168.0.234	255.255.255.252 (/30)	192.168.0.230	eth3 (Link-2 verso C)
0.0.0.0	0.0.0.0	192.168.0.230	eth3 (rotta di default verso Internet via C)


- **Rete diretta 192.168.0.0/25** → esce su `eth0`  
- **Rete diretta 192.168.0.128/26** → esce su `eth1`  
- **Rete 192.168.0.192/27 (x-net-1)** non è direttamente connessa: per raggiungerla, B deve passare per A → primo hop: `192.168.0.226` (su `eth2`, Link-1).  
- **Rete 192.168.0.248/30 (Link-3)** è collegata ad A; per raggiungerla, B invia il pacchetto a `192.168.0.226` (su Link-1), quindi A lo instraderà su Link-3.  
- **Rete 192.168.0.234/30 (Link-3 verso C)** in realtà B la vede come “rete 192.168.0.230/30” (Link-2); quindi, per arrivare a C → esce su `eth3`.  
- **Default route (0.0.0.0/0)** → verso `192.168.0.230` (eth3), ovvero il gateway interno di C.  
  - C a sua volta, tramite impostazione analogamente definita, invierà all’esterno i pacchetti Internet.  

**Attenzione:** le voci “Next Hop” sono spesso l’indirizzo primario dell’interfaccia di un router vicino (qui, A o C), ma bisogna comunque rispettare la sequenza di passaggio.  

---

## 6.  Sintesi finale e consigli per lo studio

1. **Identificare sempre tutti i segmenti fisici/logici** che occorre trattare come “reti IP” indipendenti:
   - LAN multi-host → prefissi più grandi (`/25`, `/26`, `/27` etc.)  
   - Link punto-punto → prefissi `/30` (o, su piattaforme avanzate, `/31`).  

2. **Applicare la formula** `2^nh − 2 ≥ #host_totali` (includendo le interfacce dei router) per trovare il valore `nh` e poi calcolare il **prefisso**:  
   > `maschera = 32 − nh` → ad esempio, se `nh = 7` → `/25`.  

3. **Usare un approccio VLSM**: cominciare ad allocare la sottorete più grande dal blocco “padre” e procedere a ruota ordinata, in modo da non sprecare spazio e non sovrapporre intervalli.  

4. **Verificare sempre i confini** (“network address” e “broadcast address”) di ogni sottorete, annotandoli chiaramente sul disegno:  
   - Dopo aver messo `/25`, il successivo blocco libero inizia a `.128`  
   - Dopo aver messo `/26` che finisce a `.191`, la prossima parte libera inizia a `.192`  
   - Dopo `/27` che finisce a `.223`, la parte libera inizia a `.224`  
   - E così via.  

5. **Lasciare “spazi vuoti”** se si prevede di fare futuri ampliamenti, oppure per avere maggiore chiarezza quando si disegna sulla lavagna.  

6. **Configurare la tabella di routing** su ciascun router in modo coerente:  
   - Voci “Dirette” (reti a cui il router è direttamente connesso)  
   - Voci “Indirette” (next hop sui link punto-punto)  
   - Rotta di default per l’accesso a Internet (impostata solo sul router di frontiera, qui C).  

Questo conclude la spiegazione **passo-passo** dell’esercizio di subnetting tratto dalle slide . Seguendo questi passaggi, dovresti ora avere chiaro come:
- Individuare le reti interne da progettare (6 reti totali);  
- Calcolare `nh` e la maschera corretta per ogni rete;  
- Suddividere `192.168.0.0/24` senza sovrapposizioni;  
- Assegnare indirizzi IP a ciascuna interfaccia router e host;  
- Compilare tabelle di routing coerenti.  

Buono studio e buon subnetting!  
