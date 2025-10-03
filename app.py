import streamlit as st
import speech_recognition as sr
from textblob import TextBlob
import pandas as pd
from st_audiorec import st_audiorec
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Mindful Elder Care",
    page_icon="❤️",
    layout="wide"
)

# --- State Management ---
# Initialize session state variables if they don't exist
def initialize_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'
    if 'reminders' not in st.session_state:
        st.session_state.reminders = []
    if 'contacts' not in st.session_state:
        st.session_state.contacts = []
    if 'medical_details' not in st.session_state:
        st.session_state.medical_details = {
            "Doctor Name": "", "Doctor Contact": "", "Blood Type": "",
            "Allergies": "", "Conditions": ""
        }

# --- Audio to Text Conversion Function ---
def audio_to_text(audio_bytes):
    """Converts audio bytes to text using SpeechRecognition."""
    if not audio_bytes:
        return ""
    
    r = sr.Recognizer()
    # Use an in-memory WAV file
    wav_file = io.BytesIO(audio_bytes)
    with sr.AudioFile(wav_file) as source:
        try:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.error("Could not understand the audio. Please try speaking clearly.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google service; {e}")
    return ""


# --- Page Rendering Functions ---

def render_home():
    """Renders the Mindful AI Diary page with client-side voice input."""
    st.title("Mindful AI Diary 🧠")
    st.write("A gentle space to share your thoughts. Just tap the microphone, speak, and tap again.")
    st.write("---")

    # --- THIS IS THE NEW VOICE COMPONENT ---
    # It records audio in the browser and sends it to the Python backend
    audio_bytes = st_audiorec()

    if audio_bytes:
        st.info("Audio recorded. Now analyzing your thoughts...")
        # Convert audio to text
        user_text = audio_to_text(audio_bytes)

        if user_text:
            st.write(f"**You said:** *'{user_text}'*")
            blob = TextBlob(user_text)
            polarity = blob.sentiment.polarity
            st.write("---")
            st.subheader("A Thought for You:")
            if polarity > 0.2:
                st.success("That sounds wonderful! It's lovely to hear such positivity. Keep embracing that joy.")
            elif polarity < -0.2:
                st.warning("It sounds like you're going through a tough moment. Remember to be kind to yourself. A quiet cup of tea can be a comforting friend.")
            else:
                st.info("Thank you for sharing. Taking a moment to reflect is a gift to yourself.")

def render_reminders():
    """Renders the Medicine Reminders page."""
    st.title("Medicine Reminders 💊")
    st.write("Add your medicine schedules here to get a clear overview.")
    
    with st.form("reminder_form", clear_on_submit=True):
        st.subheader("Add a New Reminder")
        col1, col2, col3 = st.columns(3)
        with col1:
            medicine_name = st.text_input("Medicine Name")
        with col2:
            dosage = st.text_input("Dosage (e.g., 1 pill)")
        with col3:
            time = st.time_input("Time to Take")
        
        submitted = st.form_submit_button("Add Reminder")
        if submitted and medicine_name:
            st.session_state.reminders.append({"Medicine": medicine_name, "Dosage": dosage, "Time": time.strftime("%I:%M %p")})
            st.success("Reminder added!")

    st.write("---")
    st.subheader("Your Current Reminders")
    if not st.session_state.reminders:
        st.info("You have no reminders set.")
    else:
        df = pd.DataFrame(st.session_state.reminders)
        st.table(df)

def render_contacts():
    """Renders the Emergency Contacts page."""
    st.title("Emergency Contacts ☎️")
    st.write("Keep important numbers handy for quick access.")

    with st.form("contact_form", clear_on_submit=True):
        st.subheader("Add a New Contact")
        col1, col2 = st.columns(2)
        with col1:
            contact_name = st.text_input("Contact Name")
        with col2:
            contact_number = st.text_input("Phone Number")
        
        submitted = st.form_submit_button("Add Contact")
        if submitted and contact_name:
            st.session_state.contacts.append({"Name": contact_name, "Number": contact_number})
            st.success("Contact added!")

    st.write("---")
    st.subheader("Your Contact List")
    if not st.session_state.contacts:
        st.info("You have no contacts saved.")
    else:
        for contact in st.session_state.contacts:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{contact['Name']}**: {contact['Number']}")
            with col2:
                st.link_button("Call Now", url=f"tel:{contact['Number']}")

def render_medical_details():
    """Renders the My Medical Details page."""
    st.title("My Medical Details ❤️‍🩹")
    st.write("Store your key medical information here. This is for your reference only and is not shared.")
    
    details = st.session_state.medical_details
    details["Doctor Name"] = st.text_input("Primary Doctor's Name", value=details["Doctor Name"])
    details["Doctor Contact"] = st.text_input("Primary Doctor's Contact", value=details["Doctor Contact"])
    details["Blood Type"] = st.text_input("Blood Type", value=details["Blood Type"])
    details["Allergies"] = st.text_area("Known Allergies", value=details["Allergies"])
    details["Conditions"] = st.text_area("Ongoing Medical Conditions", value=details["Conditions"])
    
    if st.button("Save Details"):
        st.session_state.medical_details = details
        st.success("Your medical details have been saved!")


# --- Main App Logic ---

initialize_state()

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    if st.button("Home / AI Diary", use_container_width=True, type="primary" if st.session_state.page == 'Home' else "secondary"):
        st.session_state.page = 'Home'
    if st.button("Medicine Reminders", use_container_width=True, type="primary" if st.session_state.page == 'Reminders' else "secondary"):
        st.session_state.page = 'Reminders'
    if st.button("Emergency Contacts", use_container_width=I have selected "streamlit
textblob
SpeechRecognition
st-audiorec
pandas" text between  and  in the most up-to-date Canvas "List of Dependencies" document above and am asking a query about/based on this text below.
Instructions to follow:
  * Don't output/edit the document if the query is Direct/Simple. For example, if the query asks for a simple explanation, output a direct answer.
  * Make sure to **edit** the document if the query shows the intent of editing the document, in which case output the entire edited document, **not just that section or the edits**.
    * Don't output the same document/empty document and say that you have edited it.
    * Don't change unrelated text in the document.
  * Don't output  and  in your final response.
  * Any references like "this" or "selected text" refers to the text between  and  tags.
  * Just acknowledge my request in the introduction.
  * Make sure to refer to the document as "Canvas" in your response.

give code of above changesTrue, type="primary" if st.session_state.page == 'Contacts' else "secondary"):
        st.session_state.page = 'Contacts'
    if st.button("My Medical Details", use_container_width=True, type="primary" if st.session_state.page == 'Medical Details' else "secondary"):
        st.session_state.page = 'Medical Details'
    
    st.info("Note: All data is cleared when you close this browser tab.")


# Display the selected page
if st.session_state.page == 'Home':
    render_home()
elif st.session_state.page == 'Reminders':
    render_reminders()
elif st.session_state.page == 'Contacts':
    render_contacts()
elif st.session_state.page == 'Medical Details':
    render_medical_details()

