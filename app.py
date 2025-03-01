import streamlit as st
import threading
import recorder
import transcripter
import painter


if "record_active" not in st.session_state:
    st.session_state.record_active = threading.Event()
    st.session_state.recording_status = "Ready to start!"
    st.session_state.recording_completed = False
    st.session_state.latest_image = ""
    st.session_state.messages = []
    st.session_state.frames = []


def start_recording():
    st.session_state.record_active.set()
    st.session_state.frames = []
    st.session_state.recording_status = "🔴 **Recording...**"
    st.session_state.recording_completed = False

    threading.Thread(target=recorder.record, args=(st.session_state.record_active, st.session_state.frames)).start()

def stop_recording():
    st.session_state.record_active.clear()
    st.session_state.recording_status = "✅ **Record is Completed**"
    st.session_state.recording_completed = True

st.set_page_config(page_title="VoiceDraw", layout="wide", page_icon="./icons/app_icon.png")
st.image(image="./icons/app_banner.jpeg", use_container_width=True)
st.title("VoiceDraw: Generating Image With Voice")
st.divider()

col_audio, col_image = st.columns([1, 4])

with col_audio:
    st.subheader("Voice Recording")
    st.divider()
    status_message = st.info(st.session_state.recording_status)
    st.divider()

    subcol_left, subcol_right = st.columns([1, 2])

    with subcol_left:
        start_btn = st.button(label="Start", key="btn_recording_start", on_click=start_recording, disabled=st.session_state.record_active.is_set())
        stop_btn = st.button(label="Stop", key="btn_recording_stop", on_click=stop_recording, disabled=not st.session_state.record_active.is_set())
    with subcol_right:
        recorded_audio = st.empty()

        if st.session_state.recording_completed:
            recorded_audio.audio(data="voice_prompt.wav")
    
    st.divider()
    latest_image_edit = st.checkbox(label="Edit Latest Image")