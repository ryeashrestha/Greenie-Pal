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
# Global Quiz Data
# -------------------------------
all_statements = {
    "Plastic straws are the biggest ocean polluter.": "Myth",
    "Electric cars have zero environmental impact.": "Myth",
    "Climate change is only caused by natural cycles.": "Myth",
    "All plastics are recyclable.": "Myth",
    "Going vegan has no impact on the environment.": "Myth",
    "Bamboo products are always sustainable.": "Myth",
    "Deforestation increases carbon emissions.": "Truth",
    "Meat production contributes to global warming.": "Truth",
    "Using public transport reduces your carbon footprint.": "Truth",
    "Solar and wind energy are renewable.": "Truth",
    "Recycling helps conserve natural resources.": "Truth",
    "Climate change is intensified by human activity.": "Truth",
    "Organic food always has a lower carbon footprint.": "Myth",
    "Fast fashion is one of the biggest polluters.": "Truth",
    "Bottled water is safer than tap water.": "Myth"
}

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

        # Always define eco_tips
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

        # Initialize tip only once
        if "daily_tip" not in st.session_state:
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
# Quiz Page
# -------------------------------
def quiz():
    st.title("Myth or Truth Quiz")
    st.markdown("Test your sustainability knowledge!")

    if st.session_state.get("quiz_started"):
        st.markdown("### Choose 'Myth' or 'Truth' for each statement:")

        for idx, (statement, _) in enumerate(st.session_state.questions):
            selected = st.radio(
                f"{idx+1}. {statement}",
                ["Myth", "Truth"],
                key=f"q{idx}"
            )
            st.session_state.answers[f"q{idx}"] = selected

        if st.button("Submit Quiz"):
            correct = 0
            for idx, (_, correct_answer) in enumerate(st.session_state.questions):
                if st.session_state.answers.get(f"q{idx}") == correct_answer:
                    correct += 1

            st.success(f"You got {correct} out of 15 correct!")

            with st.expander("See Correct Answers"):
                for idx, (statement, correct_answer) in enumerate(st.session_state.questions):
                    user_ans = st.session_state.answers.get(f"q{idx}")
                    correct_status = "✅" if user_ans == correct_answer else "❌"
                    st.markdown(f"{correct_status} {idx+1}. **{statement}** — Correct: *{correct_answer}*, Your answer: *{user_ans or 'Not answered'}*")

    else:
        st.session_state.quiz_started = True
        st.session_state.questions = list(all_statements.items())
        random.shuffle(st.session_state.questions)
        st.session_state.answers = {}
        st.rerun()

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.session_state.quiz_started = False
        st.session_state.questions = []
        st.session_state.answers = {}
        st.rerun()

# -------------------------------
# Main App Router
# -------------------------------
def main():
    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "quiz":
        quiz()

if __name__ == "__main__":
    main()
