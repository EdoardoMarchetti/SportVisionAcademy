MANDATORY_KEYS = ['Nome', 'Cognome', 'Email', 'Telefono', 'Età']

score_categories = ['Tecnologia', 'Calcio', 'Personale', 'Economico']

SHEET = 'Sheet1'

CATEGORIES_MAPPING = {
    'Tecnologia':'Tecnologia in dotazione', 
    'Calcio':'Ruolo di Allenatore',
    'Personale':'Motivazione e Determinazione',
    'Economico':'Capacità di investimento'
}

SELECTBOX_PLACEHOLDE = "Scegli un'opzione"


MESSAGE_INTRO = """Questo questionario è stato sviluppato per individuare le caratteristiche chiave di chi vuole ottenere la
certificazione come **Match Analyst**, considerando aspetti *emozionali, tecnologici, finanziari e sportivi*.
Rispondendo con attenzione, l’intelligenza artificiale elaborerà le informazioni e ti assegnerà a una
delle quattro fasce, ciascuna associata a competenze differenti. \n
**Ti incoraggiamo a fornire dati accurati e sinceri per una valutazione corretta.**"""


MESSAGE_OUTRO ="""
Il sistema sta elaborando le tue risposte per identificare la fascia di appartenenza più adatta a te, in
base alle tue caratteristiche emozionali, tecnologiche, finanziarie e sportive. I risultati verranno
presentati attraverso grafici dettagliati che evidenzieranno i tratti principali del tuo profilo.
Questi dati ci aiuteranno a condividerti il miglior piano formativo, perfettamente personalizzato sulle
tue esigenze e potenzialità.
Ti ringraziamo per il tempo e l'attenzione dedicati!"""

RADAR_INFO = """Questo grafico paragona il tuo profilo personale rispetto agli utenti della nostra scuola tramite due ragnatele: una rappresenta il tuo punteggio personale, l'altra
mostra il punteggio medio degli utenti che hanno compilato il questionario prima di te.
Più i punti del tuo grafico si allontanano dal centro, maggiore sarà la tua qualità in quella specifica
area"""

PIZZA_INFO = """
Questo grafico paragona il tuo profilo personale rispetto agli utenti della nostra scuola tramite mostrandoti la tua posizione in percentili.
Ciò significa che più è alto il tuo punteggio, migliore è il tuo piazzamento. Ad esempio se il tuo percentile è 90, allora in quella determinata area risulti migliore rispetto al 90% dei nostri studenti. 
"""