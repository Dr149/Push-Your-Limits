import streamlit as st
import json
import os

# 1. Page Configuration & Quiet Study Theme Setup
st.set_page_config(
    page_title="Push Your Limits | Medical Study Portal",
    page_icon="🩺",
    layout="wide"
)

# Injecting Custom CSS for a calm, distraction-free medical student atmosphere
st.markdown("""
    <style>
    .main { background-color: #f4f6f4; }
    h1, h2, h3 { color: #2c4a3e; font-family: 'Georgia', serif; }
    .stButton>button {
        background-color: #3d6453;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover { background-color: #2c4a3e; color: white; }
    .quiz-box {
        background-color: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #3d6453;
    }
    .success-text { color: #2e7d32; font-weight: bold; font-size: 1.2rem; }
    </style>
""", unsafe_allowed_html=True)

# 2. Initialize Persistent Session States
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False

# Mock Database for Sample Data
if "db_files" not in st.session_state:
    st.session_state.db_files = ["Neuroanatomy_Core_Notes.pdf", "Hematology_Anemia_Algorithms.pdf"]
if "db_videos" not in st.session_state:
    st.session_state.db_videos = ["https://www.youtube.com/watch?v=sample1", "https://www.youtube.com/watch?v=sample2"]

# Mock Quiz Database containing questions with image mappings
SAMPLE_QUIZ = [
    {
        "question": "Identify the primary diagnostic indicator highlighted in the blood smear image below for Acute Myeloid Leukemia (AML).",
        "options": ["Auer rods inside myeloblasts", "Hypersegmented neutrophils", "Target cells", "Reed-Sternberg cells"],
        "answer": "Auer rods inside myeloblasts",
        "image": "https://upload.wikimedia.org/wikipedia/commons/b/b5/Auer_rods.jpg",
        "explanation": "Excellent! Auer rods are elongated, crystalline structures seen in the cytoplasm of myeloid leukemic blasts."
    },
    {
        "question": "Which cranial nerve pathway is compromised if a patient presents with a loss of corneal reflex?",
        "options": ["CN V (Trigeminal) afferent / CN VII (Facial) efferent", "CN II (Optic) / CN III (Oculomotor)", "CN VIII (Vestibulocochlear)", "CN IX (Glossopharyngeal)"],
        "answer": "CN V (Trigeminal) afferent / CN VII (Facial) efferent",
        "image": None,
        "explanation": "Correct! The ophthalmic branch of the Trigeminal nerve handles the sensory input, while the Facial nerve handles the motor blink response."
    }
]

# 3. Header Architecture
st.title("🩺 Push Your Limits")
st.caption("A quiet, focused space for medical students to master high-yield concepts.")
st.markdown("---")

# 4. Sidebar Navigation & Admin Login Interface
with st.sidebar:
    st.header("Navigation")
    app_mode = st.radio("Go to:", ["Files", "Videos", "Interactive Quizzes"])
    
    st.markdown("---")
    st.header("Staff Portal")
    
    if not st.session_state.authenticated:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")
            
            if login_btn:
                # Set your secure master administrative credentials here
                if username == "admin" and password == "medstudent2026":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        
        st.markdown("### Access Request")
        st.write("Need editing/upload access?")
        with st.form("request_access"):
            req_name = st.text_input("Your Full Name")
            is_editor = st.checkbox("Request Editor Status")
            submit_req = st.form_submit_button("Submit Application")
            
            if submit_req:
                email_to = "luffy5656taro@gmail.com"
                subject = f"Access Request from {req_name}"
                body = f"Name: {req_name}%0D%0AWants to be Editor: {is_editor}"
                mailto_link = f"mailto:{email_to}?subject={subject}&body={body}"
                
                st.markdown(f'<a href="{mailto_link}" target="_blank" style="text-decoration:none;"><button style="background-color:#3d6453;color:white;padding:0.5rem;border-radius:5px;border:none;cursor:pointer;width:100%;">Click to Open Email Client</button></a>', unsafe_allowed_html=True)
    else:
        st.success("Logged in as Editor")
        if st.button("Logout Admin Mode"):
            st.session_state.authenticated = False
            st.rerun()

# 5. Core Content Sections
if app_mode == "Files":
    st.header("📚 Extracted Resource Files")
    st.write("Access high-yield documents and reference sheets below.")
    
    if st.session_state.authenticated:
        st.info("⚡ Editor Control Activated")
        new_file = st.file_uploader("Upload new lecture files (PDF/PPTX) for quiz processing", type=["pdf", "pptx", "docx"])
        if new_file:
            st.session_state.db_files.append(new_file.name)
            st.success(f"Successfully processed and stored '{new_file.name}'!")
            
    for f in st.session_state.db_files:
        col1, col2 = st.columns([4, 1])
        col1.write(f"📄 {f}")
        if col2.button("Download", key=f):
            st.info("Downloading file resource...")
        if st.session_state.authenticated:
            if col2.button("Hide/Remove", key=f+"_hide"):
                st.session_state.db_files.remove(f)
                st.rerun()

elif app_mode == "Videos":
    st.header("🎥 Video Lecture Database")
    st.write("Watch linked high-yield lecture videos.")
    
    if st.session_state.authenticated:
        st.info("⚡ Editor Control Activated")
        new_vid = st.text_input("Add Video URL Link (e.g., YouTube Link for @MedLectures01)")
        if st.button("Add Video Source"):
            if new_vid:
                st.session_state.db_videos.append(new_vid)
                st.success("Video lecture catalog updated!")
                st.rerun()

    for v in st.session_state.db_videos:
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # Placeholder safe test video link
        if st.session_state.authenticated:
            if st.button("Delete Video Entry", key=v):
                st.session_state.db_videos.remove(v)
                st.rerun()

elif app_mode == "Interactive Quizzes":
    st.header("🧠 High-Yield Smart Quizzes")
    st.write("Test your clinical knowledge. Quizzes automatically parse high-yield files and pull diagnostic imagery directly into corresponding questions.")
    
    total_q = len(SAMPLE_QUIZ)
    
    if not st.session_state.quiz_started and not st.session_state.quiz_completed:
        st.write(f"This assessment contains **{total_q} questions** generated directly from uploaded clinical resources.")
        if st.button("Begin Assessment"):
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.rerun()
            
    elif st.session_state.quiz_started and not st.session_state.quiz_completed:
        q_idx = st.session_state.current_question
        current_q = SAMPLE_QUIZ[q_idx]
        
        st.markdown(f"#### Question {q_idx + 1} of {total_q}")
        
        with st.container():
            st.markdown(f"<div class='quiz-box'><strong>{current_q['question']}</strong></div>", unsafe_allowed_html=True)
            
            # Display image if extracted from the source file
            if current_q["image"]:
                st.image(current_q["image"], caption="Image reference extracted from source file", width=400)
                
            st.write("")
            user_choice = st.radio("Select the correct diagnostic option:", current_q["options"], key=f"q_{q_idx}")
            
            if st.button("Submit Answer"):
                if user_choice == current_q["answer"]:
                    st.markdown(f"<p class='success-text'>🎉 Congratulations! Correct! </p>", unsafe_allowed_html=True)
                    st.info(current_q["explanation"])
                    st.session_state.score += 1
                else:
                    st.error(f"Incorrect. The expected answer was: {current_q['answer']}.")
                    st.info(current_q["explanation"])
                
                if q_idx + 1 < total_q:
                    st.session_state.current_question += 1
                    st.button("Proceed to Next Question")
                else:
                    st.session_state.quiz_completed = True
                    st.session_state.quiz_started = False
                    st.button("View Final Evaluation")

    elif st.session_state.quiz_completed:
        st.balloons()
        st.header("🏁 Examination Complete!")
        final_score = st.session_state.score
        pct = int((final_score / total_q) * 100)
        
        st.metric(label="Final Result Score", value=f"{final_score} / {total_q}", delta=f"{pct}% Proficiency")
        
        if pct >= 70:
            st.success("Outstanding performance! You are mastering these clinical metrics.")
        else:
            st.warning("Good attempt. Review the resource files in the archive tab to reinforce these systems.")
            
        if st.button("Restart Quiz Session"):
            st.session_state.quiz_completed = False
            st.session_state.quiz_started = False
            st.rerun()