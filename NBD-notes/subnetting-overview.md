# Introduzione al Subnetting IP

In questo documento troverai una panoramica completa sul **subnetting IP**, con definizioni, concetti teorici, esempi pratici ed esercizi svolti, basati anche sulle slide del corso di **Networking**. L’obiettivo è spiegare passo-passo:
1. Cos’è un indirizzo IP e come è strutturato
2. Il ragionamento delle classi (classful addressing) e le sue limitazioni
3. Il concetto di **subnetting** e la suddivisione di un blocco di indirizzi
4. Calcolo di maschere, prefissi e tamponamenti (CIDR/VLSM)
5. Un esercizio completo di subnetting tratto dalle slide del professore, con calcoli e tabelle

---

## 1. Cos’è un indirizzo IPv4

Un indirizzo IPv4 è un numero binario a 32 bit, solitamente scritto in **notazione decimale puntata** (e.g. `192.168.0.1`), suddiviso in due parti principali:

- **Network Portion (prefisso)**: i bit più significativi, comuni a tutti gli host di una stessa rete.
- **Host Portion**: i bit meno significativi, usati per identificare un singolo host all’interno di quella rete.

Ad esempio, l’indirizzo:

128.208.0.0/24

vuol dire che i primi 24 bit (192.168.0) identificano la rete, mentre gli ultimi 8 bit servono a distinguere gli host in quella rete. In binario:

10000000 11010000 00000000 | 00000000
^ Prefisso /24 (network) ^ Host (8 bit)


Il prefisso `/24` corrisponde alla **maschera di sottorete** `255.255.255.0`.

> **Figura 1:** Un esempio di IP prefix e subnet mask :contentReference[oaicite:0]{index=0}

---

## 2. Classful Addressing (indirizzamento a classi) e sue limitazioni

Fino al 1993 si usava l’**indirizzamento per classi**, in cui gli indirizzi IPv4 erano divisi in:
- **Classe A**: `0.0.0.0 – 127.255.255.255` (prefisso fisso `/8`)
- **Classe B**: `128.0.0.0 – 191.255.255.255` (prefisso fisso `/16`)
- **Classe C**: `192.0.0.0 – 223.255.255.255` (prefisso fisso `/24`)
- (e due classi riservate: D per multicast e E per scopi futuri)

Il grosso problema del classful era lo **spreco di indirizzi**: ad esempio, assegnare a un’azienda un intero blocco di Classe B (circa 65 536 indirizzi) quando in realtà aveva bisogno di poche centinaia di IP, significava sprecare migliaia di indirizzi.

---

## 3. Nasce il Subnetting: suddividere un blocco in più reti

Il **subnetting** consente di:
1. Prendere un blocco di indirizzi (ad esempio un `/16` o un `/24`) ed **“spezzarlo”** in più sotto‐blocchi, ognuno dei quali fungerà da rete distinta all’interno dell’organizzazione.
2. Far sì che, **all’esterno**, tutto ciò appaia ancora come un singolo blocco (ovvero, verso Internet si annuncia un’unica rotta), mentre **all’interno** si hanno varie “sub‐partizioni” utili a isolare i diversi dipartimenti, sedi o segmenti di rete.

> **Definizione (slide):**  
> “Subnetting: An available block of addresses is split into several parts for internal use as multiple networks, while still acting like a single network to the outside world.” :contentReference[oaicite:1]{index=1}

### 3.1. Esempio teorico di suddivisione

Supponiamo di avere un blocco `/16` (ad esempio `128.208.0.0/16`). Possiamo dividerlo così (la suddivisione **non** deve essere uniforme, purché i nuovi prefissi siano “bit‐aligned”):

- **Half (metà)** del blocco, cioè un `/17`, va al Dipartimento di Informatica
- **Un quarto** del blocco, cioè un `/18`, va al Dipartimento di Ingegneria Elettrica
- **Un ottavo** del blocco, cioè un `/19`, va al Dipartimento di Arte
- **Rimane** un ottavo non allocato (libero)

In binario, i prefissi risultanti potrebbero essere:

- Informatica  `10000000 11010000 1|xxxxxxx xxxxxxxx`  → `/17`
- Ingegneria  `10000000 11010000 00|xxxxxx xxxxxxxx` → `/18`
- Arte        `10000000 11010000 011|xxxxx xxxxxxxx` → `/19`

Quando un router riceve un pacchetto con destinazione, controlla **AND** tra indirizzo IP di destinazione e subnet mask per determinare a quale sub‐rete appartiene :contentReference[oaicite:2]{index=2}.

---

## 4. Calcolare le sottoreti: maschere, prefissi e numero di host

### 4.1. Formula fondamentale

Per ogni nuova sottorete dobbiamo garantire abbastanza indirizzi per gli host (computer, server, stampanti, ecc.) **e** lasciare spazio per:

- L’**indirizzo di rete** (network address, tutti gli host bit a 0)
- L’**indirizzo di broadcast** (tutti gli host bit a 1)
- Gli indirizzi utilizzabili (**host addresses**)

Se una sottorete deve ospitare **_N_ host** (escludendo router, stampanti ecc.), la regola è:

2^nh - 2 ≥ N


dove `nh` = numero di bit assegnati alla porzione **host**:
- `2^nh` = numero totale di indirizzi (network + host + broadcast)
- Sottraendo 2 otteniamo gli indirizzi effettivamente utilizzabili da host.

#### 4.1.1. Esempio: quanti bit servono per 100 host?
- Cerchiamo `nh` tale che `2^nh - 2 ≥ 100`
  - Se `nh = 6` → `2^6 - 2 = 64 - 2 = 62` (NON basta)
  - Se `nh = 7` → `2^7 - 2 = 128 - 2 = 126` (Basta, 126 ≥ 100)
- Quindi servono **7 bit** per la parte host, restano `32 - 7 = 25` bit per la parte network → maschera `/25`.

---

### 4.2. Notazione CIDR (Classless Inter-Domain Routing)

- L’introduzione del **CIDR** (classless addressing) ha abolito definitivamente il vincolo delle “classi A, B, C fisse” e ha reso possibile usare prefissi di qualsiasi lunghezza da `/0` a `/32`.
- L’indirizzo viene così scritto come `a.b.c.d/x` dove `/x` indica quanti bit sono usati per la porzione di **rete** (network‐prefix).
- Il vantaggio principale è la **maggiore granularità**, il minor spreco di indirizzi e la possibilità di fare **aggregation** (riassumere rotte) evitando l’esplosione delle route sui router di backbone.

---

### 4.3. VLSM (Variable Length Subnet Mask)

- Con il VLSM possiamo suddividere un blocco in sottoreti di lunghezza **differente**, a seconda del numero di host necessari in ciascuna.
- Si usa quando, ad esempio, in una LAN servono 100 host, in un’altra 50, in un’altra 20 e così via: si assegnano blocchi di dimensione diversa dentro lo stesso /24 o /16, purché non si sovrappongano.
- **Condizione**: i prefissi di ogni sottorete devono essere “allineati” sui confini di bit (bit‐aligned) per evitare sovrapposizioni.

---

## 5. Esempio pratico: esercizio di subnetting tratto dalle slide del professore

Di seguito riportiamo passo‐passo l’**Exercise 1: IP Subnetting** delle slide, partendo dal blocco **`192.168.0.0/24`** e suddividendo in **6 reti** interne (3 LAN multi‐host + 3 collegamenti punto‐punto tra router). Si illustrano i calcoli, la scelta dei prefissi e l’assegnazione degli intervalli.

> **Scenario di rete (riassunto grafico):**  
> - **Router B** collegato a due LAN:
>   1. **pc-net**: 100 host
>   2. **ws-net**: 50 host  
> - **Router A** collegato a una LAN:
>   3. **x-net-1**: 20 host  
> - I router A, B, C sono a loro volta interconnessi via **Link-1**, **Link-2**, **Link-3** (collegamenti punto‐punto).  
> - Il router C ha, infine, un’interfaccia verso l’**Internet** (rappresentata come nuvola esterna).  
>
> In questo esercizio **non** si conta la connessione verso Internet (è un blocco IP già assegnato dal provider).  
> Occorrono quindi **6 reti interne**:
> 1. pc-net (LAN, 100 host)  
> 2. ws-net (LAN, 50 host)  
> 3. x-net-1 (LAN, 20 host)  
> 4. Link-1 (punto-punto: interfaccia B ↔ interfaccia A)  
> 5. Link-2 (punto-punto: interfaccia B ↔ interfaccia C)  
> 6. Link-3 (punto-punto: interfaccia A ↔ interfaccia C)  

### 5.1. Calcolo dei prefissi per le LAN multi-host

#### 5.1.1. **pc-net** (100 host + 1 indirizzo router)
- Serve in totale 101 indirizzi (100 host + 1 interfaccia del router).  
- Servono quindi `nh` bit di host tali che `2^nh - 2 ≥ 101`.  
  - Se `nh = 6` → `2^6 - 2 = 64 - 2 = 62` (insufficiente)  
  - Se `nh = 7` → `2^7 - 2 = 128 - 2 = 126` (sufficiente)  
- Quindi **nh = 7 bit** per gli host → **prefisso = /25** (32 − 7 = 25).  
- In notazione decimale, la maschera è `255.255.255.128`.

> Da qui in avanti, ogni LAN avrà un blocco dedicato; prendiamo come “blocco padre” `192.168.0.0/24` e rompiamolo in modo ordinato.

#### 5.1.2. **ws-net** (50 host + 1 interfaccia router)
- Serve 51 indirizzi totali.  
- `nh` bit di host tali che `2^nh - 2 ≥ 51`:  
  - `nh = 5` → `2^5 - 2 = 32 - 2 = 30` (insufficiente)  
  - `nh = 6` → `2^6 - 2 = 64 - 2 = 62` (sufficiente)  
- **nh = 6 bit** → **prefisso = /26** (32 − 6 = 26), maschera `255.255.255.192`.

#### 5.1.3. **x-net-1** (20 host + 1 interfaccia router)
- Serve 21 indirizzi totali.  
- `nh` bit di host tali che `2^nh - 2 ≥ 21`:  
  - `nh = 4` → `2^4 - 2 = 16 - 2 = 14` (insufficiente)  
  - `nh = 5` → `2^5 - 2 = 32 - 2 = 30` (sufficiente)  
- **nh = 5 bit** → **prefisso = /27** (32 − 5 = 27), maschera `255.255.255.224`.

> **Riepilogo parziale delle LAN** :contentReference[oaicite:3]{index=3}  
> - pc-net → `/25` (128 indirizzi totali, 126 host)  
> - ws-net → `/26` (64 indirizzi totali, 62 host)  
> - x-net-1 → `/27` (32 indirizzi totali, 30 host)

---

### 5.2. Calcolo dei prefissi per i collegamenti punto-punto

Ogni **link** fra due router richiede **esattamente 2 indirizzi host** (uno per ciascun lato). In IPv4, il blocco più piccolo che supporta 2 indirizzi host effettivi è un **`/30`** (4 indirizzi totali: 2 host + network + broadcast). Alcune piattaforme supportano il `/31` (RFC 3021), ma nelle esercitazioni didattiche si usa `/30`.

#### 5.2.1. **Link-1** (fra interfaccia di `B` e interfaccia di `A`)
- Servono 2 indirizzi totali.  
- **Prefisso = `/30`**, maschera `255.255.255.252`.

#### 5.2.2. **Link-2** (fra interfaccia di `B` e interfaccia di `C`)
- Stessa logica: **prefisso = `/30`**.

#### 5.2.3. **Link-3** (fra interfaccia di `A` e interfaccia di `C`)
- **Prefisso = `/30`**.

> **Riepilogo link punto-punto** :contentReference[oaicite:4]{index=4}  
> - Link-1 (B↔A) → `/30`  
> - Link-2 (B↔C) → `/30`  
> - Link-3 (A↔C) → `/30`

---

### 5.3. Assegnazione concreta degli intervalli all’interno di `192.168.0.0/24`

Partendo da `192.168.0.0/24`, divideremo in ordine crescente di prefisso (da largest a smallest) per sfruttare al meglio lo spazio e mantenere tutto contiguo:

1. **pc-net: `192.168.0.0/25`**  
   - Rete = `192.168.0.0`  
   - Maschera = `255.255.255.128`  
   - Host disponibili = `192.168.0.1` … `192.168.0.126`  
   - Broadcast = `192.168.0.127`  

2. **ws-net: `192.168.0.128/26`**  
   - Rete = `192.168.0.128`  
   - Maschera = `255.255.255.192`  
   - Host disponibili = `192.168.0.129` … `192.168.0.190`  
   - Broadcast = `192.168.0.191`  

3. **x-net-1: `192.168.0.192/27`**  
   - Rete = `192.168.0.192`  
   - Maschera = `255.255.255.224`  
   - Host disponibili = `192.168.0.193` … `192.168.0.222`  
   - Broadcast = `192.168.0.223`  

A questo punto abbiamo “consumato” gli indirizzi da `192.168.0.0` a `192.168.0.223`. Rimangono liberi gli indirizzi da `192.168.0.224` a `192.168.0.255`, **32 indirizzi** totali, che useremo per i tre link punto-punto (ognuno `/30` usa 4 indirizzi).

4. **Link-1 (B↔A): `192.168.0.224/30`**  
   - Rete = `192.168.0.224`  
   - Maschera = `255.255.255.252`  
   - Host disponibili = `192.168.0.225` (interfaccia B), `192.168.0.226` (interfaccia A)  
   - Broadcast = `192.168.0.227`  

5. **Link-2 (B↔C): `192.168.0.228/30`**  
   - Rete = `192.168.0.228`  
   - Maschera = `255.255.255.252`  
   - Host disponibili = `192.168.0.229` (interfaccia B), `192.168.0.230` (interfaccia C)  
   - Broadcast = `192.168.0.231`  

6. **Link-3 (A↔C): `192.168.0.232/30`**  
   - Rete = `192.168.0.232`  
   - Maschera = `255.255.255.252`  
   - Host disponibili = `192.168.0.233` (interfaccia A), `192.168.0.234` (interfaccia C)  
   - Broadcast = `192.168.0.235`  

**Rimanenti** (residuo libero): `192.168.0.236` – `192.168.0.255` (20 indirizzi) lasciati in riserva per eventuali ampliamenti. :contentReference[oaicite:5]{index=5}

---

### 5.4. Tabella riepilogativa delle 6 subnet interne

| #   | Nome Rete       | Tipo                 | Prefisso   | Rete           | Host disponibili                         | Broadcast       |
|-----|-----------------|----------------------|------------|----------------|------------------------------------------|-----------------|
| 1   | **pc-net**      | LAN multi-host       | `192.168.0.0/25` | `192.168.0.0`  | `192.168.0.1 – 192.168.0.126` (126 host)  | `192.168.0.127` |
| 2   | **ws-net**      | LAN multi-host       | `192.168.0.128/26` | `192.168.0.128`| `192.168.0.129 – 192.168.0.190` (62 host) | `192.168.0.191` |
| 3   | **x-net-1**     | LAN multi-host       | `192.168.0.192/27` | `192.168.0.192`| `192.168.0.193 – 192.168.0.222` (30 host) | `192.168.0.223` |
| 4   | **Link-1 (B↔A)**| Punto-punto (2 host) | `192.168.0.224/30` | `192.168.0.224`| `192.168.0.225 (B), 192.168.0.226 (A)`    | `192.168.0.227` |
| 5   | **Link-2 (B↔C)**| Punto-punto (2 host) | `192.168.0.228/30` | `192.168.0.228`| `192.168.0.229 (B), 192.168.0.230 (C)`    | `192.168.0.231` |
| 6   | **Link-3 (A↔C)**| Punto-punto (2 host) | `192.168.0.232/30` | `192.168.0.232`| `192.168.0.233 (A), 192.168.0.234 (C)`    | `192.168.0.235` |

> **Rimane libero**: `192.168.0.236 – 192.168.0.255` (20 indirizzi) :contentReference[oaicite:6]{index=6}

---

### 5.5. Assegnazione degli indirizzi alle interfacce router

1. **Router B**  
   - `eth0` (interfaccia interna verso `pc-net`): `192.168.0.1/25`  
   - `eth1` (interfaccia interna verso `ws-net`): `192.168.0.129/26`  
   - `eth2` (interfaccia verso Link-1): `192.168.0.225/30`  
   - `eth3` (interfaccia verso Link-2): `192.168.0.229/30`  

2. **Router A**  
   - `eth0` (interfaccia verso Link-1): `192.168.0.226/30`  
   - `eth1` (interfaccia interna verso `x-net-1`): `192.168.0.193/27`  
   - `eth2` (interfaccia verso Link-3): `192.168.0.233/30`  

3. **Router C**  
   - `eth0` (interfaccia verso Link-3): `192.168.0.234/30`  
   - `eth1` (interfaccia verso Link-2): `192.168.0.230/30`  
   - `eth2` (interfaccia verso Internet): (blocco IP fornito dal provider, non considerato nel conteggio)

> In questo modo, ogni router ha un indirizzo univoco su ciascuna delle reti interne, e i pacchetti IP saranno instradati correttamente. :contentReference[oaicite:7]{index=7}

---

### 5.6. Esempio di routing (schema generico)

Dopo aver assegnato i prefissi e gli indirizzi alle interfacce, ciascun router deve configurare il **routing interno**. Ad esempio, una possibile tabella di routing semplificata per:

- **Router B** (vedi slide) conterrà voci per:
  - `192.168.0.0/25` → interfaccia `eth0` (pc-net)  
  - `192.168.0.128/26` → interfaccia `eth1` (ws-net)  
  - `192.168.0.192/27` → next hop (192.168.0.226) tramite `eth2` (Link-1)  
  - `192.168.0.232/30` → next hop (192.168.0.230) tramite `eth3` (Link-2)  
  - Rota di default → l’interfaccia verso Internet via router C (192.168.0.230)  

- **Router A**:
  - `192.168.0.192/27` → interfaccia `eth1` (x-net-1)  
  - `192.168.0.0/25` e `192.168.0.128/26` → next hop (192.168.0.225) tramite `eth0` (Link-1)  
  - `192.168.0.232/30` → interfaccia `eth2` (Link-3)  
  - Rota di default → via `192.168.0.234` (Link-3) a router C  

- **Router C**:
  - Rotte interne (verso Link-2, Link-3) per raggiungere `pc-net`, `ws-net`, `x-net-1`  
  - Rotta di default verso Internet (interfaccia del provider)

> Nelle slide il **Routing Table di Router B** è mostrato nella pagina successiva all’assegnazione IP :contentReference[oaicite:8]{index=8}.

---

## 6. Ulteriori concetti: route summarization e longest‐prefix match

Dopo aver creato molte sottoreti, può essere utile **aggregare** (“riassumere”) alcune rotte simili in un’unica voce di routing. Questo riduce il numero di entry nella tabella di routing dei router di livello superiore.

- **Route aggregation (supernetting):** unisce più prefissi contigui in un blocco più grande.  
  - Esempio: se abbiamo le reti `192.168.0.0/24` e `192.168.1.0/24`, possiamo annunciarle insieme come `192.168.0.0/23`.  
- I router usano il **longest‐prefix match** per decidere la destinazione più specifica:
  - Se arrivano pacchetti per `192.168.0.50`, questa corrisponde a `/24` e verrà instradata di conseguenza.  
  - Se arrivano pacchetti per `192.168.1.100` e abbiamo un’aggregazione `/23`, verranno anch’essi catturati dalla route più specifica.

> **CIDR e route summarization** :contentReference[oaicite:9]{index=9}

---

## 7. Esempi aggiuntivi e suggerimenti pratici

### 7.1. Esempio di subnetting su un blocco /16

Supponiamo di ricevere dal provider un blocco **`172.16.0.0/16`**. All’interno vogliamo creare:

1. Una LAN da 400 host  
2. Una LAN da 100 host  
3. Una LAN da 50 host  
4. Una LAN da 10 host  

**Passi**:
1. **LAN 400 host**  
   - `nh` bit: `2^nh - 2 ≥ 400` → `nh = 9` → `2^9 - 2 = 510` (ok)  
   - **prefisso = /23** (32 − 9 = 23), maschera `255.255.254.0`.  
   - Assegno il primo blocco: `172.16.0.0/23` → rango `172.16.0.1 – 172.16.1.254`.

2. **LAN 100 host**   
   - `nh` bit: `2^nh - 2 ≥ 100` → `nh = 7` → `2^7 - 2 = 126`  
   - **prefisso = /25**, maschera `255.255.255.128`.  
   - Successivo blocco libero dopo `/23`: il `/23` occupa `172.16.0.0` – `172.16.1.255`, quindi la rete libera inizia da `172.16.2.0`.  
   - Assegno `172.16.2.0/25` → rango `172.16.2.1 – 172.16.2.126`.

3. **LAN 50 host**   
   - `nh` bit: `2^nh - 2 ≥ 50` → `nh = 6` → `/26`  
   - Il blocco libero seguente dopo `/25`: `/25` è `172.16.2.0 – 172.16.2.127`, prossimo inizio `172.16.2.128/26`.  
   - Assegno `172.16.2.128/26` → rango `172.16.2.129 – 172.16.2.190`.

4. **LAN 10 host**   
   - `nh` bit: `2^nh - 2 ≥ 10` → `nh = 4` → `/28` (16 indirizzi totali, 14 host)  
   - Il blocco libero seguente dopo `/26`: `/26` è `172.16.2.128 – 172.16.2.191`, prossimo `172.16.2.192/28`.  
   - Assegno `172.16.2.192/28` → rango `172.16.2.193 – 172.16.2.206`.

In questo modo, senza sprechi, otteniamo quattro sottoreti di diversa grandezza dentro lo stesso `/16`. Questo approccio si chiama **VLSM** (Variable Length Subnet Mask).

---

### 7.2. Esempio di “classful → classless”: passaggio a CIDR

Un router di backbone riceve queste reti:
- `10.0.0.0/8`  
- `10.1.0.0/16`  
- `10.1.1.0/24`  
- `10.1.2.0/24`  
- `10.2.0.0/16`  

Si desidera ridurre il numero di rotte e aggregare dove possibile:
1. **`10.1.1.0/24`** e **`10.1.2.0/24`** contigui si possono unire in **`10.1.0.0/23`** (copre da `10.1.0.0` a `10.1.1.255`).  
2. A sua volta, **`10.1.0.0/23`** e **`10.1.2.0/24`** non si possono aggregare tutte assieme perché non sono contigue; bisognerebbe avere un blocco da `/22` per coprire `10.1.0.0 – 10.1.3.255`.  
3. **`10.2.0.0/16`** rimane isolata;  
4. Infine, viene riassunto tutto in `10.0.0.0/8` (se si vuole pubblicare un’unica rotta al provider), ma occorre stare attenti all’ordine del longest‐prefix match in tabelle di routing interne.

---

## 8. Riepilogo dei punti chiave

1. **Ogni segmento di rete IP** (sia LAN multi-host sia link punto-punto) deve avere un proprio **prefisso IP** distinto.  
2. Per **LAN multi-host**, si calcola il numero di bit `nh` di host con `2^nh - 2 ≥ numero_host_desiderati + numero_interfacce_router`.  
3. Per **link punto-punto** si utilizzano quasi sempre i prefissi **`/30`** (in IPv4) perché servono esattamente 2 indirizzi host.  
4. Il **CIDR** consente di usare prefissi di lunghezza variabile (da `/0` a `/32`), eliminando il problema del “classful waste”.  
5. Il **VLSM** permette di assegnare a ogni sottorete interna una maschera diversa a seconda dei bisogni di host, purché le sottoreti non si sovrappongano.  
6. La **route summarization** (“supernetting”) riduce il numero di rotte su router di livello superiore, sfruttando il “longest‐prefix match”.

---

## 9. Esercizi consigliati per esercitarsi

1. **Suddividere `10.10.0.0/16` in 5 reti** con rispettivi:
   - 200 host  
   - 50 host  
   - 20 host  
   - 10 host  
   - 2 host (link punto-punto)  
2. **Data la rete `192.168.100.0/24`**, creare almeno 4 sottoreti di dimensione diversa (ad es. 60 host, 30 host, 10 host, 2 host), elencare:
   - Prefissi e maschere  
   - Intervalli host utilizzabili  
   - Indirizzi di broadcast  
3. **Routing Table Simulation**  
   - Partendo dal sottorete come in Esercizio 1 (`192.168.0.0/24` splittato in 6 reti), scrivere la **routing table completa** per ciascun router (A, B, C), includendo rotte dirette e rotte di rete interna.

---

## 10. Conclusioni

Il **subnetting IP** è una competenza fondamentale per la progettazione di reti: consent e di:

- Utilizzare in modo **ottimale** lo spazio di indirizzamento IPv4 (che è ormai limitato).  
- Organizzare la rete in modo **gerarchico**, semplificando il **routing** e migliorando la sicurezza (isolamento tra dipartimenti).  
- Ridurre le **tabelle di routing** mediante tecniche di **CIDR** e **route summarization**.  

Le slide del corso di Networking mostrano un esempio concreto di come suddividere un `/24` in 6 reti distinte (3 LAN + 3 link punto-punto) con tutti i calcoli necessari, che abbiamo riassunto in dettaglio sopra .  

Per approfondire, si consiglia di rivedere:
- Slide su **Classless Inter-Domain Routing (CIDR)**, con esempi di aggregazione prefissi.  
- Slide su **Routing e longest‐prefix match** per vedere come i router selezionano la rotta più specifica.  
- Esercizi pratici su **VLSM** e pianificazione di indirizzi IPv6 (in IPv6 la logica di suddivisione è analoga ma con 128 bit totali).

---
**Bibliografia interna (slide di riferimento):**  
- Definizione e figure su subnetting, blocchi IP e subnet mask :contentReference[oaicite:11]{index=11}  
- Exercise 1: IP Subnetting (calcolo bit, prefissi, assegnazione indirizzi) :contentReference[oaicite:12]{index=12}  
- Classless Inter-Domain Routing (CIDR, route summarization) :contentReference[oaicite:13]{index=13}  


