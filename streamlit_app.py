import streamlit as st
import requests
import time

FLASK_API_URL = "https://seer-api.onrender.com/streamlit-upload"

st.title("PDF Converter")
st.write("This app allows you to convert PDF documents to screen reader-friendly text. Depending on the size of the document, it may take a few minutes to convert. Please upload your PDF document below to get started. Your converted document will be displayed below.")
st.write("Before converting another document, please clear the current document by clicking the 'x' button to the right of the selected document.")

# Initialize session state for processing
if "processing" not in st.session_state:
    st.session_state["processing"] = False
if "was_processing" not in st.session_state:
    st.session_state["was_processing"] = False

# Create file uploader first
uploaded_file = st.file_uploader("Choose a PDF file", disabled=st.session_state["processing"])

# Check if file was cleared (user clicked "x")
if st.session_state["was_processing"] and uploaded_file is None:
    st.session_state["processing"] = False
    st.session_state["was_processing"] = False
    st.rerun()

# Then check if a file was just uploaded and handle processing state
if uploaded_file is not None and not st.session_state["processing"]:
    st.session_state["processing"] = True
    st.session_state["was_processing"] = True
    st.rerun()

if uploaded_file is not None:
    upload_status = st.success(f"File uploaded: {uploaded_file.name}")
    processing_status = st.info(f"{uploaded_file.name} is now being converted...")

    # audio_caption = st.caption("The audio player below will play sounds to indicate the status of your document conversion.")
    # loading_audio = st.audio("static/loading.wav", format="audio/wav", loop=True, autoplay=True)

    try:    
        # Send file to Flask API
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(FLASK_API_URL, files=files)
        response_json = response.json()

        # loading_audio.empty()

        if response.status_code == 200:
            success_audio_placeholder = st.empty()
            success_audio_placeholder.audio("static/success.wav", format="audio/wav", loop=False, autoplay=True)
            time.sleep(1)
            success_audio_placeholder.empty()

            upload_status.empty()
            processing_status.empty()
            # audio_caption.empty()

            st.success("Document converted successfully! Your converted document is displayed below.")
            st.markdown(response_json["md"]) 
        else:
            error_audio_placeholder = st.empty()
            error_audio_placeholder.audio("static/error.wav", format="audio/wav", loop=False, autoplay=True)
            time.sleep(1)
            error_audio_placeholder.empty()

            upload_status.empty()
            processing_status.empty()
            # audio_caption.empty()
            
            st.error(f"There was an error converting your document. Error: {response}")

    except Exception as e:
        # loading_audio.empty()

        error_audio_placeholder = st.empty()
        error_audio_placeholder.audio("static/error.wav", format="audio/wav", loop=False, autoplay=True)
        time.sleep(1)
        error_audio_placeholder.empty()

        upload_status.empty()
        processing_status.empty()
        # audio_caption.empty()
        
        st.error(f"There was an error processing your document. Error: {e}")

    # Reset processing state after completion
    st.session_state["processing"] = False
