import streamlit as st
import random

st.set_page_config(page_title="Statistik-Impostor", layout="centered")
st.title("🎓 Statistik-Impostor")

# --- Session Keys absichern ---
for key in ["players", "impostors", "word", "current_index", "reveal_order", "emojis", "game_started"]:
    if key not in st.session_state:
        st.session_state[key] = None

# --- Emoji-Liste ---
emoji_list = [
    "😀", "😃", "😄", "😁", "😆", "😅", "😂", "😊", "😇", "🙂", "🙃", "😉",
    "😎", "😍", "😘", "🥰", "😜", "🤓", "🧐", "🤠", "🥳", "🤗", "🤔",
    "👩🏻", "👨🏽", "👩🏿", "👨🏼", "👩🏾", "👨🏻", "👩🏼", "👨🏿",
    "🐱", "🐶", "🐵", "🦊", "🐸", "🐼", "🐧", "🐯", "🦁", "🐮",
    "🐷", "🐰", "🐨", "🐙", "🐢"
]
random.shuffle(emoji_list)

# --- Spieler*innenliste ---
st.subheader("1. Namen der Spieler*innen")
names = st.text_area("Gib die Namen (eine Zeile pro Person) ein:").splitlines()

# --- Begriffe ---
default_words = [
    "Vorhersage", "Modell", "Trainingdaten", "Testdaten", "Overfitting",
    "Underfitting", "Bias", "Varianz", "Supervised Learning", "Unsupervised Learning",
    "Regressionsgerade", "Residuum", "Fehlerquadratsumme (RSS)", "Bestimmtheitsmaß (R²)", "Intercept",
    "Koeffizient", "Least Squares", "Einflussgröße", "Korrelation", "Dummy-Variable",
    "Modellannahmen", "Homoskedastizität", "Normalverteilung der Fehler", "Unabhängigkeit der Fehler", "Lineare Beziehung",
    "Durbin-Watson", "VIF (Variance Inflation Factor)", "Multikollinearität", "Heteroskedastizität", "Residuenplot",
    "Kreuzvalidierung", "Validierungsfehler", "Trainingsfehler", "Lasso", "Regularisierung",
    "AIC", "BIC", "Adjustiertes R²", "Klassifikator", "Genauigkeit", "KNN", "Naive Bayes", "Logistische Regression"
]

st.subheader("2. Anzahl der Impostors")
n_impostors = st.number_input("Wie viele Impostors sollen mitspielen?", min_value=1, max_value=5, value=1, step=1)

st.subheader("3. Statistik-Begriffe")
wordlist = st.text_area("Optional: Eigene Begriffe eingeben (eine Zeile pro Begriff):", value="\n".join(default_words)).splitlines()

# --- Spiel starten ---
if st.button("🔁 Rollen zufällig verteilen") and len(names) >= 4:
    players = [name.strip() for name in names if name.strip()]
    if len(players) < 4:
        st.warning("Mindestens 4 Spieler*innen erforderlich.")
    else:
        n_impostors = min(n_impostors, len(players) - 1)
        impostors = random.sample(players, n_impostors)
        word = random.choice(wordlist).strip()
        random.shuffle(players)

        # Emojis zuordnen
        emojis = {name: emoji_list[i % len(emoji_list)] for i, name in enumerate(players)}

        st.session_state["players"] = players
        st.session_state["impostors"] = impostors
        st.session_state["word"] = word
        st.session_state["current_index"] = 0
        st.session_state["reveal_order"] = players.copy()
        random.shuffle(st.session_state["reveal_order"])
        st.session_state["emojis"] = emojis
        st.session_state["game_started"] = True

# --- Spielrunde ---
if st.session_state.get("game_started", False):
    st.subheader("4. Rollen nacheinander aufdecken")

    idx = st.session_state["current_index"]
    reveal_order = st.session_state["reveal_order"]
    emojis = st.session_state.get("emojis", {})

    if idx < len(reveal_order):
        current_player = reveal_order[idx]
        st.markdown(f"<h2 style='text-align: center;'> <span style='font-size: 120px'>{emojis.get(current_player, '')}</span> </h2>", unsafe_allow_html=True)
        with st.expander(f"📱 {emojis[current_player]} {current_player} – Hier tippen zum Aufdecken"):
            if current_player in st.session_state["impostors"]:
                st.warning("Du bist der/die IMPOSTOR 🤫. Versuche nicht aufzufliegen!")
            else:
                st.success(f"Geheimer Begriff: **{st.session_state['word']}**")

        if st.button("➡️ Weitergeben"):
            st.session_state["current_index"] += 1
            st.rerun()

    else:
        st.success("🎉 Alle Rollen wurden aufgedeckt!")
        st.subheader("5. Diskussion & Reihenfolge")
        st.markdown("💬 Gebt nun reihum eure Hinweise. Versucht, nicht zu offensichtlich zu sein – aber zeigt, dass ihr das Wort kennt!")
        st.markdown("---")
        st.markdown("➡️ Vorschlag für Startperson:")
        start_player = random.choice(st.session_state['players'])
        st.write(f"{emojis[start_player]} {start_player}")

        st.markdown("---")
        st.markdown("🔎 Wer ist verdächtig? Am Ende stimmt ihr ab – dann wird aufgelöst!")

