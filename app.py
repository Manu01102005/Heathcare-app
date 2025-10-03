import streamlit as st
import speech_recognition as sr
from textblob import TextBlob
import pandas as pd
from datetime import datetime

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
            "Doctor Name": "",
            "Doctor Contact": "",
            "Blood Type": "",
            "Allergies": "",
            "Conditions": ""
        }

# --- Voice Transcription Function ---
def transcribe_voice():
    """Listens to the microphone and returns the transcribed text."""
    r = sr.Recognizer()
    text = ""
    with sr.Microphone() as source:
        st.info("Listening... Please say something.")
        try:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=15)
            st.info("Recognizing...")
            text = r.recognize_google(audio)
        except sr.WaitTimeoutError:
            st.warning("Listening timed out. Please try again.")
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            st.error(f"Could not connect to Google services; {e}")
    return text

# --- Page Rendering Functions ---

# --- Find this function in your app.py file ---
def render_home():
    """Renders the Mindful AI Diary page."""
    st.title("Mindful AI Diary 🧠")
    st.write("A gentle space to share your thoughts. Type your feelings in the box below.")
    st.write("---")

    # --- THIS IS THE MODIFIED PART ---
    # We replace the button and transcribe_voice() with a text_area
    user_text = st.text_area("How are you feeling today?", height=200, placeholder="You can write about anything...")

    # The analysis part below remains the same and will run automatically when the user types
    if user_text:
        st.write("---")
        st.write(f"**You wrote:** *'{user_text}'*")
        
        blob = TextBlob(user_text)
        polarity = blob.sentiment.polarity
        
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

# Initialize state on first run
initialize_state()

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    if st.button("Home / AI Diary", use_container_width=True, type="primary" if st.session_state.page == 'Home' else "secondary"):
        st.session_state.page = 'Home'
    if st.button("Medicine Reminders", use_container_width=True, type="primary" if st.session_state.page == 'Reminders' else "secondary"):
        st.session_state.page = 'Reminders'
    if st.button("Emergency Contacts", use_container_width=True, type="primary" if st.session_state.page == 'Contacts' else "secondary"):
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
