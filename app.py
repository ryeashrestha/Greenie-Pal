import streamlit as st
import google.generativeai as genai
import random
from streamlit_sortables import sort_items

# -------------------------------
# Configure Gemini API
# -------------------------------
GOOGLE_API_KEY = "AIzaSyAHDq5HDywhmLY-qvoezAAbs4rKxAMbb7U"  # Your API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# -------------------------------
# Page Navigation via Session State
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_home():
    st.session_state.page = "home"

def go_quiz():
    st.session_state.page = "quiz"

# -------------------------------
# Home Page
# -------------------------------
def home():
    st.header("🤖 Greenie Pal")
    st.write("Your eco-friendly buddy that helps you discover sustainable tasks, ideas, and knowledge for a greener life.")

    # Eco Tip Section
    tip_col, suggestion_col = st.columns([2, 1])
    with tip_col:
        st.subheader("🌱 Daily Sustainability Tip")

        st.markdown("""
            <style>
            div.stButton > button {
                background-color: white;
                color: #2e7d32;
                border: 2px solid #2e7d32;
                border-radius: 8px;
                padding: 0.5em 1em;
                font-weight: 600;
                transition: all 0.3s ease-in-out;
            }
            div.stButton > button:hover {
                background-color: #2e7d32 !important;
                color: white !important;
                border: 2px solid #2e7d32 !important;
            }
            section[data-testid="stNotificationContent"] {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                background-color: #f1f8e9 !important;
                padding: 1em;
                font-size: 16px;
                font-weight: 500;
                color: #2e7d32;
            }
            </style>
        """, unsafe_allow_html=True)

        if "daily_tip" not in st.session_state:
            eco_tips = [
                "Say no to disposable plastic items",
                "Use LED or energy-saving lights",
                "Collect rainwater for plants",
                "Choose buses, trains, or shared rides",
                "Eat less meat—start with one day a week",
                "Bring a refillable water bottle everywhere",
                "Take shorter showers to save water and energy",
                "Turn kitchen scraps into compost",
                "Support local eco-friendly businesses.",
                "Grow local plants in your backyard",
                "Buy second-hand or thrift items to reduce waste",
            ]
            st.session_state.daily_tip = random.choice(eco_tips)
        st.container(height=100).info(st.session_state.daily_tip)

        if st.button("🌿 Get New Tip", use_container_width=True):
            st.session_state.daily_tip = random.choice(eco_tips)
            st.rerun()

    with suggestion_col:
        st.subheader("Sample Questions:")
        st.markdown("""
        - What causes climate change?
        - How to recycle batteries?
        - What are eco-friendly habits?
        - Should I avoid plastic straws?
        """)

    st.divider()

    if st.button("🧠 Wanna play Myth or Truth?", use_container_width=True):
        go_quiz()

    st.divider()
    st.subheader("Ask Greenie Pal")

    user_question = st.text_input(
        "Type your environmental question here:",
        placeholder="E.g., How do I minimize my carbon footprint?",
        key="ecobot_input"
    )

    if user_question:
        try:
            with st.spinner("Greenie Pal is thinking..."):
                prompt = f"""
                You are Greenie Pal, a friendly and informative chatbot designed to help people learn about environmental sustainability.
                You have access to a knowledge base of recycling information, eco tips, habit changes, sustainability FAQs, should-I questions, and information about environmental impacts.
                Answer questions clearly, concisely, and in a friendly manner. If you don't have a direct answer, provide general guidance or suggest related topics.

                User Question: {user_question}
                """
                response = model.generate_content(prompt)
                if response.text:
                    st.markdown(f"**Greenie Pal**: {response.text}")
                else:
                    st.error("**Greenie Pal**: I couldn't generate a response. Please try again.")
        except Exception as e:
            st.error(f"**Greenie Pal**: An error occurred: {e}")
    else:
        st.write("**Greenie Pal**: Hi! I'm here to help you with environmental questions. Ask me anything about sustainability!")

# -------------------------------
# Myth or Truth Quiz Page
# -------------------------------
def quiz():
    st.title("🧠 Myth or Truth Quiz")
    st.markdown("Drag each sustainability statement into the correct box!")

    myths = [
        "Plastic straws are the biggest ocean polluter.",
        "Electric cars have zero environmental impact.",
        "Climate change is only caused by natural cycles.",
        "All plastics are recyclable.",
        "Going vegan has no impact on the environment.",
        "Bamboo products are always sustainable."
    ]

    truths = [
        "Deforestation increases carbon emissions.",
        "Meat production contributes to global warming.",
        "Using public transport reduces your carbon footprint.",
        "Solar and wind energy are renewable.",
        "Recycling helps conserve natural resources.",
        "Climate change is intensified by human activity."
    ]

    if "quiz_started" not in st.session_state or not st.session_state.quiz_started:
        if st.button("Start Quiz"):
            st.session_state.quiz_started = True
            st.session_state.pool = myths + truths
            random.shuffle(st.session_state.pool)
            st.session_state.myth = []
            st.session_state.truth = []

    if st.session_state.get("quiz_started", False):
        myth_items, truth_items, pool_items = sort_items(
            {
                "Myth ❌": st.session_state.myth,
                "Truth ✅": st.session_state.truth,
                "Pool 🔄": st.session_state.pool,
            },
            multi_containers=True,
            direction="vertical",
            key="multi-sortable",
        )

        # Update session state lists
        st.session_state.myth = myth_items
        st.session_state.truth = truth_items
        st.session_state.pool = pool_items

        # Check answers button only if pool is empty
        if len(st.session_state.pool) == 0:
            if st.button("✅ Check My Answers"):
                user_myth_set = set(st.session_state.myth)
                user_truth_set = set(st.session_state.truth)

                correct_myth_set = set(myths)
                correct_truth_set = set(truths)

                correct_count = sum([s in correct_myth_set for s in user_myth_set]) + \
                                sum([s in correct_truth_set for s in user_truth_set])

                st.success(f"🎯 You got {correct_count}/12 correct!")

                with st.expander("📖 Show Correct Answers"):
                    st.markdown("**Myths:**")
                    for m in myths:
                        st.markdown(f"- ❌ {m}")
                    st.markdown("**Truths:**")
                    for t in truths:
                        st.markdown(f"- ✅ {t}")

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        # Clear quiz state to reset
        st.session_state.quiz_started = False
        st.session_state.myth = []
        st.session_state.truth = []
        st.session_state.pool = []
        st.experimental_rerun()

def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "quiz":
        quiz()

if __name__ == "__main__":
    main()