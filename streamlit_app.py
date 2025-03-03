import streamlit as st
import requests
import time

FLASK_API_URL = "https://seer-api.onrender.com/streamlit-upload"

st.title("PDF Converter")
st.write("This app allows you to convert PDF documents to screen reader friendly text. Please upload your PDF document below to get started. Your converted document will be displayed below.")

uploaded_file = st.file_uploader("Choose a PDF file")

if uploaded_file is not None:
    # If a file is uploaded, set it in the session state and clear previous UI components
    st.session_state.uploaded_file = uploaded_file
    for key in list(st.session_state.keys()):
        if key != "uploaded_file":  # Don't clear the uploaded file state
            del st.session_state[key]
    
    upload_status = st.success(f"File uploaded: {uploaded_file.name}")
    processing_status = st.info(f"{uploaded_file.name} is now being converted...")

    audio_caption = st.caption("The audio player below will play sounds to indicate the status of your document conversion. Please feel free to stop the audio or adjust the volume as needed.")
    
    # Use a placeholder to dynamically replace audio
    audio_placeholder = st.empty()

    try:    
        loading_audio = st.audio("static/loading.wav", format="audio/wav", loop=True, autoplay=True)

        # Send file to Flask API
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        response = requests.post(FLASK_API_URL, files=files)
        response_json = response.json()

        loading_audio.empty()

        if response.status_code == 200:
            # Now play success sound
            success_audio_placeholder = st.empty()
            success_audio_placeholder.audio("static/success.wav", format="audio/wav", loop=False, autoplay=True)
            time.sleep(2)
            success_audio_placeholder.empty()

            upload_status.empty()
            processing_status.empty()
            audio_caption.empty()

            st.success("Document converted successfully! Your converted document is displayed below.")
            st.markdown(response_json["md"]) 
        else:
            error_audio_placeholder = st.empty()
            error_audio_placeholder.audio("static/error.wav", format="audio/wav", loop=False, autoplay=True)
            time.sleep(1)
            error_audio_placeholder.empty()

            upload_status.empty()
            processing_status.empty()
            audio_caption.empty()
            
            st.error(f"There was an error converting your document. Error: {response}")
    except Exception as e:
        error_audio_placeholder = st.empty()
        error_audio_placeholder.audio("static/error.wav", format="audio/wav", loop=False, autoplay=True)
        time.sleep(1)
        error_audio_placeholder.empty()

        upload_status.empty()
        processing_status.empty()
        audio_caption.empty()
        
        st.error(f"There was an error processing your document. Error: {e}")
