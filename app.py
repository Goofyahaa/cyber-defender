import random
import time
from datetime import date
import streamlit as st

st.set_page_config(page_title="Cyber Defender", page_icon="🛡️", layout="centered")
st.markdown("""<style>
.stApp {background:#07111f;color:#edf5ff}
[data-testid="stMetric"] {background:#101d2d;padding:12px;border-radius:12px;border:1px solid #22354a}
h1,h2,h3 {color:#45e0c1!important}
.stButton>button {background:#17273a;color:#edf5ff;border:1px solid #30445a;border-radius:10px;min-height:50px;width:100%;font-weight:700}
.stButton>button:hover {border-color:#45e0c1;color:#45e0c1}
</style>""",unsafe_allow_html=True)
PHISHING = [
    ("Uw bankrekening wordt vandaag geblokkeerd. Klik onmiddellijk op deze link om uw account te verifiëren.", "PHISHING", "Dreigen met blokkering en tijdsdruk proberen je overhaast te laten klikken. Open bankzaken via de officiële app."),
    ("Je collega stuurt vanaf zijn bekende werkadres: ‘Kun je het verslag van gisteren nog eens delen? Dank je!’", "VEILIG", "Er wordt niet om een wachtwoord, betaling of onverwachte download gevraagd. Controleer bij twijfel de afzender."),
    ("Je hebt een telefoon gewonnen! Vul binnen 5 minuten je schoolwachtwoord in om de prijs te claimen.", "PHISHING", "Een onverwachte prijs, tijdsdruk en een verzoek om je wachtwoord zijn duidelijke alarmsignalen."),
    ("De IT-helpdesk meldt gepland onderhoud. Open het intranet via je opgeslagen bladwijzer.", "VEILIG", "De melding vraagt niet om geheime gegevens en verwijst naar een bekende route."),
    ("Een onbekende afzender stuurt ‘Factuur.pdf.exe’ en dreigt met een boete als je het bestand niet opent.", "PHISHING", "Een uitvoerbaar bestand vermomd als pdf en een dreigement zijn verdacht. Open en meld het niet."),
    ("Een vriend vraagt in de chat om de verificatiecode die zojuist naar jouw telefoon is gestuurd.", "PHISHING", "Verificatiecodes zijn persoonlijk. Deel ze met niemand; neem via een ander kanaal contact op."),
    ("Je pakket is tegengehouden. Betaal nu € 1,25 via deze onverwachte link.", "PHISHING", "Controleer bezorginformatie via de officiële app of website, niet via een onverwachte betaal-link."),
    ("Een docent stuurt vanaf het bekende schooladres een lokaalwijziging en noemt het nieuwe lokaalnummer.", "VEILIG", "Dit is een gewone mededeling zonder verzoek om inloggegevens of betaling."),
]

PASSWORDS = ["12345", "Welkom2024", "StudyBuddy42", "July2026", "V!olet-M0on", "River-Cobalt!92-Sky", "aaaaaaaa", "Cedar!Orbit73"]

MALWARE = [
    ("Een besmet bestand voegt zichzelf toe aan andere bestanden en verspreidt zich als die worden geopend.", "VIRUS", "Een virus hecht zich aan bestanden en verspreidt zich wanneer die bestanden worden uitgevoerd of gedeeld."),
    ("Een nep-game lijkt normaal, maar installeert stiekem software die aanvallers toegang geeft.", "TROJAN", "Een trojan doet zich voor als nuttige software en verbergt een schadelijke functie."),
    ("Bestanden zijn versleuteld en er verschijnt een eis om geld te betalen voor herstel.", "RANSOMWARE", "Ransomware vergrendelt of versleutelt bestanden en eist vaak losgeld."),
    ("Een programma houdt ongemerkt bij welke websites iemand bezoekt en stuurt die informatie door.", "SPYWARE", "Spyware verzamelt ongemerkt informatie over een gebruiker of apparaat."),
    ("Een geïnfecteerd document verspreidt schadelijke code wanneer gedeelde kopieën worden gestart.", "VIRUS", "De code besmet bestanden en verspreidt zich via kopieën: dat past bij een virus."),
    ("Een nep-update voor een videospeler installeert ook een verborgen achterdeur.", "TROJAN", "De software lijkt legitiem, maar verbergt een achterdeur. Dat is kenmerkend voor een trojan."),
    ("Een schadelijk programma besmet nieuwe systeembestanden die daarna worden gestart.", "VIRUS", "Een virus verspreidt zich door andere bestanden te besmetten."),
    ("Een browserextensie verzamelt in het geheim zoekopdrachten en bezochte pagina's.", "SPYWARE", "De extensie bespioneert browsegedrag en verzamelt gegevens: dat is spyware."),
]

WEBSITES = [
    ("http://secure-bank-login.example", "VERDACHT", "Geen HTTPS en lokwoorden als ‘secure’ en ‘login’ maken dit verdacht."),
    ("https://bank.example", "VEILIG", "In dit fictieve scenario is dit het afgesproken bankdomein met HTTPS."),
    ("https://bank.example.security-check.test/account", "VERDACHT", "Het echte domein is security-check.test; ‘bank.example’ staat alleen als misleidend subdomein ervoor."),
    ("https://portal.school.example/rooster", "VEILIG", "Dit is het afgesproken fictieve schooldomein met HTTPS en een normale pagina."),
    ("https://free-prize-login.example/claim-now", "VERDACHT", "Lokwoorden als ‘free-prize’ en ‘login’ blijven verdacht, ook met HTTPS."),
    ("http://bank.example/sign-in", "VERDACHT", "Het domein klopt, maar deze pagina gebruikt geen versleutelde HTTPS-verbinding."),
    ("https://school.example.login-check.test/leerling", "VERDACHT", "Het echte domein is login-check.test; school.example is hier een misleidend subdomein."),
    ("https://portal.school.example/lessen", "VEILIG", "Dit is het afgesproken fictieve schooldomein. Controleer altijd het volledige webadres."),
]

FINAL_EVENTS = [
    ("Op je bureau ligt een onbekende USB-stick met het label ‘Salaris’. Wat doe je?", "USB NIET AANSLUITEN", ["USB AANSLUITEN", "USB NIET AANSLUITEN"], "Goed: sluit een onbekende USB-stick niet aan. Meld hem bij de IT-verantwoordelijke.", "Een onbekende USB-stick kan malware bevatten. Sluit hem niet aan en meld hem bij IT."),
    ("Je ontvangt een dringende e-mail met een link naar een ‘nieuw beveiligingsportaal’. Wat doe je?", "LINK BLOKKEREN", ["LINK OPENEN", "LINK BLOKKEREN"], "Goed: open de link niet. Meld het bericht als phishing en gebruik de bekende route.", "Open de onverwachte link niet. Meld het bericht als phishing."),
    ("Er is een aanmeldpoging vanaf een onbekende locatie. Je hebt die zelf niet gestart.", "ACCOUNT BLOKKEREN", ["ACCOUNT BLOKKEREN", "ACCOUNT NEGEREN"], "Goed: weiger de aanmelding en meld de poging volgens de beveiligingsprocedure.", "Negeer de melding niet. Weiger de onbekende aanmelding en meld die."),
    ("Een waarschuwing meldt dat bestanden op een gedeelde computer plotseling worden versleuteld.", "APPARAAT ISOLEREN", ["APPARAAT ISOLEREN", "BESTANDEN OPENEN"], "Goed: verbreek de netwerkverbinding en waarschuw direct de IT-beveiliging.", "Open geen bestanden. Isoleer het apparaat van het netwerk en waarschuw IT."),
]

RANKS = [
    (5000, "Elite Cyber Defender"),
    (3500, "Cyber Defender"),
    (2200, "Security Analyst"),
    (1200, "Security Trainee"),
    (400, "Cyber Student"),
    (0, "Beginner"),
]

def rank_for_xp(xp):
    for threshold, name in RANKS:
        if xp >= threshold:
            return name
    return "Beginner"

def password_strength(password):
    """Geef een eenvoudige, uitlegbare wachtwoordscore van 0 tot 100."""
    score = min(40, len(password) * 2)
    notes = [f"Lengte: {len(password)} tekens."]
    checks = [
        (any(c.islower() for c in password), 10, "kleine letters"),
        (any(c.isupper() for c in password), 10, "hoofdletters"),
        (any(c.isdigit() for c in password), 10, "cijfers"),
        (any(not c.isalnum() for c in password), 15, "speciale tekens"),
    ]
    for present, points, label in checks:
        if present:
            score += points
            notes.append(f"Bevat {label}: +{points}.")
        else:
            notes.append(f"Mist {label}.")

    lower = password.lower()
    common = any(word in lower for word in ("welkom", "password", "qwerty", "admin", "school", "letmein"))
    digits = "".join(c for c in password if c.isdigit())
    year = any(str(value) in digits for value in range(2000, 2036))
    sequence = any(part in lower for part in ("1234", "abcd", "qwer", "0000"))
    if common or year or sequence:
        score -= 20
        notes.append("Veelgebruikt woord, jaartal of voorspelbare reeks: -20.")
    if len(password) >= 4 and len(set(password)) <= 2:
        score -= 20
        notes.append("Bijna alleen herhaalde tekens: -20.")

    score = max(0, min(100, score))
    if score <= 30:
        label = "ZWAK"
    elif score <= 60:
        label = "GEMIDDELD"
    elif score <= 80:
        label = "STERK"
    else:
        label = "ZEER STERK"
    return score, label, notes

BANKS = [
    ("Phishing", "Herken berichten die je naar een val proberen te lokken.", "choice", PHISHING, ["PHISHING", "VEILIG"]),
    ("Wachtwoordbeveiliging", "Beoordeel lengte, variatie en voorspelbaarheid.", "password", PASSWORDS, ["ZWAK", "GEMIDDELD", "STERK", "ZEER STERK"]),
    ("Malware", "Koppel het gedrag aan de juiste soort schadelijke software.", "choice", MALWARE, ["VIRUS", "TROJAN", "RANSOMWARE", "SPYWARE"]),
    ("Websitebeveiliging", "Controleer domein en verbinding vóór je gegevens invult.", "choice", WEBSITES, ["VEILIG", "VERDACHT"]),
    ("Eindscenario", "Neem vier veilige beslissingen.", "final", FINAL_EVENTS, []),
]

def init():
    if 'phase' not in st.session_state:
        st.session_state.phase='menu'
    if 'scores' not in st.session_state:
        st.session_state.scores=[]

def start(name):
    s=st.session_state
    s.name=name.strip()[:18] or 'Player'
    s.levels=[]
    for title,subtitle,kind,bank,options in BANKS:
        questions=list(bank) if kind=='final' else random.sample(bank,6)
        random.shuffle(questions)
        s.levels.append(dict(title=title,subtitle=subtitle,kind=kind,questions=questions,options=options))
    s.level_index=0;s.question_index=0;s.score=0;s.xp=0;s.lives=3
    s.correct=0;s.mistakes=0;s.final_all_correct=True
    s.saved=False;s.phase='question';s.deadline=time.monotonic()+15

def answer(choice=None):
    s=st.session_state
    if s.phase!='question':return
    remaining=max(0,int(s.deadline-time.monotonic()+0.999))
    timed_out=remaining<=0
    level=s.levels[s.level_index];q=level['questions'][s.question_index]
    if level['kind']=='password':
        actual,expected,notes=password_strength(q)
        explanation=f"Analyse: {actual}/100 — {expected}.\n"+'\n'.join(notes)
    elif level['kind']=='final':
        expected=q[1];explanation=q[3] if choice==expected else q[4]
    else:
        expected,explanation=q[1],q[2]
    good=not timed_out and choice==expected
    if good:
        points=100+remaining*3;s.score+=points;s.xp+=100;s.correct+=1
        s.feedback=f'GOED GEZIEN · +{points} PUNTEN · +100 XP'
    else:
        s.score-=50;s.lives-=1;s.mistakes+=1
        if level['kind']=='final':s.final_all_correct=False
        s.feedback='TIJD IS OM · -50 PUNTEN · -1 LEVEN' if timed_out else 'NIET HELEMAAL · -50 PUNTEN · -1 LEVEN'
        if level['kind'] not in ('final','password'):
            explanation=f'Juiste antwoord: {expected}. {explanation}'
    s.good=good;s.explanation=explanation;s.phase='feedback'

def finish(won,game_over=False):
    s=st.session_state;s.won=won;s.game_over=game_over;s.phase='result'
    if not s.saved:
        s.scores.append(dict(name=s.name,score=s.score,xp=s.xp,rank=rank_for_xp(s.xp),date=str(date.today())))
        s.scores.sort(key=lambda r:r['score'],reverse=True)
        s.scores=s.scores[:10];s.saved=True

def continue_game():
    s=st.session_state;level=s.levels[s.level_index]
    if s.lives<=0:finish(False,True)
    elif s.question_index+1<len(level['questions']):
        s.question_index+=1;s.phase='question';s.deadline=time.monotonic()+15
    elif s.level_index<4:
        s.score+=500;s.xp+=500;s.phase='level_complete'
    else:
        if s.final_all_correct:s.score+=500;s.xp+=500
        finish(s.final_all_correct)

def next_level():
    s=st.session_state;s.level_index+=1;s.question_index=0
    s.deadline=time.monotonic()+15;s.phase='question'

init()
s=st.session_state
st.title('◈ CYBER DEFENDER')
st.caption('CYBERSECURITY TRAINING SIMULATOR · WEB EDITION')

if s.phase=='menu':
    st.header('BESCHERM WAT BELANGRIJK IS.')
    st.write('Herken cyberdreigingen. Neem slimme beslissingen. Houd het systeem veilig.')
    st.info('5 LEVELS / 28 BESLISSINGEN / 3 LEVENS')
    if st.button('🎮 START GAME',type='primary'):s.phase='name';st.rerun()
    if st.button('📖 HOW TO PLAY'):s.phase='howto';st.rerun()
    if st.button('🏆 HIGH SCORES'):s.phase='scores';st.rerun()
    st.caption('Fictieve oefenscenario’s. Gebruik geen echte wachtwoorden.')
elif s.phase=='name':
    st.header('Kies je codenaam')
    with st.form('start'):
        name=st.text_input('Codenaam',value='CyberStudent',max_chars=18)
        if st.form_submit_button('START TRAINING',type='primary'):start(name);st.rerun()
    if st.button('TERUG'):s.phase='menu';st.rerun()
elif s.phase=='howto':
    st.header('Zo werkt de training')
    st.write('**01 Herken:** phishing, wachtwoorden, malware, websites en een eindscenario.')
    st.write('**02 Beslis:** 15 seconden per vraag.')
    st.write('**03 Leer:** goed antwoord +100 punten en XP, plus een snelheidsbonus.')
    st.write('**04 Blijf alert:** fout of te laat = -50 punten en één leven. Je begint met drie levens.')
    st.write('**05 Klim omhoog:** afgerond level = 500 bonuspunten en XP.')
    if st.button('TERUG NAAR MENU'):s.phase='menu';st.rerun()
elif s.phase=='scores':
    st.header('HIGH SCORES')
    st.caption('Scores van deze browsersessie; niet gedeeld tussen spelers.')
    if not s.scores:st.info('Nog geen scores. Start een training!')
    for i,row in enumerate(s.scores,1):
        st.write(f"**{i:02d}. {row['name']}** — {row['score']} punten · {row['rank']}")
    if st.button('TERUG NAAR MENU'):s.phase='menu';st.rerun()
elif s.phase=='question':
    level=s.levels[s.level_index];q=level['questions'][s.question_index]
    st.subheader(f"LEVEL {s.level_index+1}/5 · {level['title']}")
    a,b,c,d=st.columns(4)
    a.metric('SCORE',s.score);b.metric('XP',s.xp);c.metric('LEVEL',f'{s.level_index+1}/5');d.metric('LEVENS',f'{s.lives}/3')
    st.progress(s.question_index/len(level['questions']))
    st.caption(f"VRAAG {s.question_index+1}/{len(level['questions'])} · {level['subtitle']}")
    if level['kind']=='password':
        st.markdown('### Hoe sterk is dit wachtwoord?');st.code(q)
    else:
        st.markdown('### '+q[0])
    options=q[2] if level['kind']=='final' else level['options']
    cols=st.columns(2)
    for i,opt in enumerate(options):
        if cols[i%2].button(opt,key=f"answer_{s.level_index}_{s.question_index}_{i}"):
            answer(opt);st.rerun()
    @st.fragment(run_every='1s')
    def clock():
        remaining=max(0,int(s.deadline-time.monotonic()+0.999))
        if remaining<=0:
            answer();st.rerun(scope='app')
        st.metric('⏱️ SECONDEN',remaining)
        st.progress(remaining/15)
    clock()
elif s.phase=='feedback':
    st.subheader('FEEDBACK')
    if s.good:st.success(s.feedback)
    else:st.error(s.feedback)
    st.write(s.explanation)
    if st.button('VOLGENDE',type='primary'):continue_game();st.rerun()
elif s.phase=='level_complete':
    st.success('✓ LEVEL VOLTOOID')
    st.write('Je krijgt 500 bonuspunten en 500 XP.')
    st.write(f'SCORE {s.score} · XP {s.xp} · RANK {rank_for_xp(s.xp)} · LEVENS {s.lives}/3')
    if st.button('VOLGEND LEVEL',type='primary'):next_level();st.rerun()
    if st.button('HOOFDMENU'):s.phase='menu';st.rerun()
elif s.phase=='result':
    if s.game_over:st.error('GAME OVER — Je cybersecurity-training is mislukt.')
    elif s.won:st.success('MISSION COMPLETE! — Alle dreigingen zijn veilig afgehandeld.')
    else:st.warning('MISSION FAILED — Niet alle dreigingen in het eindscenario zijn gestopt.')
    a,b,c,d=st.columns(4)
    a.metric('SCORE',s.score);b.metric('XP',s.xp);c.metric('GOED',s.correct);d.metric('FOUT',s.mistakes)
    st.subheader(f'RANK · {rank_for_xp(s.xp).upper()}')
    st.caption('Score is tijdelijk opgeslagen voor deze browsersessie.')
    if st.button('OPNIEUW',type='primary'):s.phase='name';st.rerun()
    if st.button('HIGH SCORES'):s.phase='scores';st.rerun()
    if st.button('HOOFDMENU'):s.phase='menu';st.rerun()
