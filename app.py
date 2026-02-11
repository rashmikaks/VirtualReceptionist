import streamlit as st
import os
from datetime import datetime
from agent import ChatAgent

# --- Setup directories ---
KB_DIR = "kb"
LOG_DIR = "logs"
os.makedirs(KB_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --- Profiles ---
def load_profiles():
    return {
        "hospital": {
            "organization": "CityCare Hospital",
            "role": "Assist patients with appointments, departments, and doctor availability.",
            "tone": "Polite, caring, and professional.",
            "logo": "https://cdn-icons-png.flaticon.com/512/2966/2966484.png",
            "kb": f"{KB_DIR}/hospital_kb.txt",
        },
        "hotel": {
            "organization": "GrandStay Hotel",
            "role": "Help guests with room bookings, amenities, check-in, and local attractions.",
            "tone": "Warm, welcoming, and helpful.",
            "logo": "https://cdn-icons-png.flaticon.com/512/2285/2285547.png",
            "kb": f"{KB_DIR}/hotel_kb.txt",
        },
        "college": {
            "organization": "ABC College",
            "role": "Guide students about admissions, departments, and campus facilities.",
            "tone": "Friendly, informative, and academic.",
            "logo": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "kb": f"{KB_DIR}/college_kb.txt",
        },
    }

PROFILES = load_profiles()

# --- Streamlit page setup ---
st.set_page_config(page_title="AI Virtual Receptionist", page_icon="🤖", layout="wide")

# --- Refined CSS ---
st.markdown("""
    <style>
    /* Global background */
    [data-testid="stAppViewContainer"] {
        background-color: #f8fafc;
    }
        .receptionist-card {
        background: #ffffff;
        border-radius: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease-in-out;
    }
    .receptionist-card:hover {
        transform: scale(1.02);
    }
            
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #eee !important;
        padding: 2rem 1.5rem 1rem 1.5rem !important;
        box-shadow: 2px 0 8px rgba(0,0,0,0.05);
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        text-align: center !important;
    }

    .sidebar-logo {
        display: flex;
        justify-content: center;
    }

    .sidebar-logo img {
        width: 70px;
    }

    /* Chat container */
    .chat-wrapper {
        display: flex;
        flex-direction: column;
        height: 90vh;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        padding: 1.2rem 2rem;
        overflow: hidden;
    }

    .chat-scroll {
        flex-grow: 1;
        overflow-y: auto;
        padding-right: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Chat bubbles */
    .user-bubble {
        background-color: #e3f2fd;
        padding: 10px 14px;
        border-radius: 12px;
        margin: 8px 0;
        align-self: flex-end;
        max-width: 75%;
    }

    .ai-bubble {
        background-color: #f1f8e9;
        padding: 10px 14px;
        border-radius: 12px;
        margin: 8px 0;
        align-self: flex-start;
        max-width: 75%;
    }

    /* Chat input */
    div[data-testid="stChatInputContainer"] {
        background-color: white !important;
        border: 1px solid #ccc !important;
        border-radius: 30px !important;
        padding: 6px 15px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-top: 0.5rem;
    }

    /* Subtle scrollbar */
    .chat-scroll::-webkit-scrollbar {
        width: 6px;
    }
    .chat-scroll::-webkit-scrollbar-thumb {
        background-color: #ccc;
        border-radius: 10px;
    }

    /* Mobile responsiveness */
    @media (max-width: 900px) {
        section[data-testid="stSidebar"] {
            display: none;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("<div class='sidebar-logo'><img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png'></div>", unsafe_allow_html=True)
    st.title("AI Receptionist")
    st.divider()

    profile_choice = st.selectbox("Choose Organization Type:", list(PROFILES.keys()))
    persona = PROFILES[profile_choice]

    st.markdown(f"""
        <div class='receptionist-card'>
            <img src='{persona["logo"]}' width='100'>
            <h3 style='margin-top:10px;'>{persona["organization"]}</h3>
        </div>
    """, unsafe_allow_html=True)

    # Load Knowledge Base
    knowledge = ""
    kb_path = persona.get("kb")
    if kb_path and os.path.exists(kb_path):
        with open(kb_path, "r", encoding="utf-8") as f:
            knowledge = f.read()
        st.success("Knowledge base loaded.")
    else:
        st.warning("No KB found for this organization.")

# --- Initialize chat ---
if "current_profile" not in st.session_state or st.session_state["current_profile"] != profile_choice:
    st.session_state["agent"] = ChatAgent(name="Receptionist", persona=persona, knowledge=knowledge)
    st.session_state["messages"] = [
        {"role": "assistant", "content": f"👋 Hi! Welcome to {persona['organization']}. How can I assist you today?"}
    ]
    st.session_state["current_profile"] = profile_choice

agent = st.session_state["agent"]

# --- Chat area ---
chat_container = st.container()

# Display chat messages or intro
with chat_container:
    if len(st.session_state["messages"]) == 1:
        # --- Show intro before first message ---
        intro_msg = st.session_state["messages"][0]["content"]
        st.markdown(f"""
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:70vh;text-align:center;">
                <img src="{persona['logo']}" width="100" style="margin-bottom:1rem;">
                <h1 style="color:#222;margin-bottom:0.5rem;">{persona['organization']}</h1>
                <p style="color:#555;font-size:1.1rem;max-width:600px;">{intro_msg}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # --- Show chat conversation ---
        chat_area = st.container()
        with chat_area:
            for msg in st.session_state["messages"]:
                if msg["role"] == "user":
                    st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='ai-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

# --- Chat Input ---
user_input = st.chat_input("Type your message...")

# Handle input and AI reply
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    ai_reply = agent.get_response(st.session_state["messages"])
    st.session_state["messages"].append({"role": "assistant", "content": ai_reply})

    # Log
    log_entry = (
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
        f"[{persona['organization']}] USER: {user_input}\nAI: {ai_reply}\n{'-'*50}\n"
    )
    with open(os.path.join(LOG_DIR, "conversations.log"), "a", encoding="utf-8") as f:
        f.write(log_entry)

    # Refresh UI immediately
    st.rerun()
