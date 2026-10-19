8S2 Design PWA v1.2.0 – Tools

11 schede grafiche responsive con collegamenti ai Tools originali Wix. Le funzionalità degli strumenti si eseguono sul sito Wix. Tutte le altre sezioni precedenti sono mantenute.
Pubblicare il contenuto dello ZIP nella root del repository GitHub Pages.


## Blog RSS (v1.2.1)
Il Blog carica `data/blog.json`, generato da `scripts/update_blog.py` dal feed Wix.
GitHub Actions (`.github/workflows/update-blog.yml`) esegue la sincronizzazione ogni 6 ore e manualmente.
**Per attivarlo:** caricare TUTTI i file, inclusa la cartella nascosta `.github`, nel repository GitHub Pages; aprire Actions → Aggiorna blog RSS → Run workflow. In Settings → Actions → General, autorizzare `Read and write permissions` al GITHUB_TOKEN, se necessario. GitHub Pages deve pubblicare dal branch che contiene `data/blog.json` oppure tramite un deploy che includa tale file.
Al primo caricamento, `data/blog.json` è vuoto: non vengono inventati articoli. Se RSS non è disponibile, lo script fallisce senza cancellare il precedente JSON. I lettori aprono gli articoli sul sito Wix.

## Ottimizzazione generale v1.2.2
- Rimossi i vecchi generatori Tools provvisori non più richiamati; le 11 schede rimandano ai Tools Wix.
- Service worker aggiornato: cache versionata, risorse statiche recuperate dalla cache, pagine con priorità rete e fallback offline; risposte HTTP fallite non salvate. Il Blog RSS continua a richiedere connessione e rimane da verificare in produzione.
- Migliorati i bersagli touch del menu a sei voci, focus da tastiera e preferenza di movimento ridotto.
- Nessuna modifica a prezzi, contenuti, link o immagini.
- I test reali di installazione e navigazione su dispositivi restano necessari.

## v1.2.6 – Ordine delle sezioni
Nel menu Altre sezioni, l’ordine è: Chi siamo, Portfolio, Prezzi e preventivi. Le sezioni HTML seguono lo stesso ordine.


## v1.2.6
Aggiunta grafica “Perché rivolgersi a 8S2 Design?” nella Home, immediatamente prima del box prenotazione call.


Versione 1.2.5: sostituita la grafica nella Home sopra il pulsante di prenotazione call con il nuovo banner fornito.


## v1.2.6
- Inserita la grafica originale “Realizza e promuovi il tuo sito web” nella pagina Contatti, dopo il box dei link.

## v1.2.7 — Icone ufficiali
Icone PWA 192/512, Apple Touch 180, favicon ICO e PNG 16/32/48 derivate dal logo ufficiale fornito.
