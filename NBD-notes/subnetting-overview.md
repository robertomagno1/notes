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

