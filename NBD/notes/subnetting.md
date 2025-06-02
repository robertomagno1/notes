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
