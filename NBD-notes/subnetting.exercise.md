
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
