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
