import pyaudio
import wave
import os

def record(record_active, frames):
    """
    Record audio while record_active is set and save to voice_prompt.wav
    
    Parameters:
    - record_active: threading.Event() to control recording state
    - frames: list to store recorded audio frames
    """
    try:
        audio = pyaudio.PyAudio()

        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024
        )

        # Clear the frames list to ensure we're starting fresh
        frames.clear()
        
        # Record audio frames while the record_active event is set
        while record_active.is_set():
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

        # Properly close resources
        stream.stop_stream()  # Method call, not property
        stream.close()
        audio.terminate()

        # Save the recorded audio to a file
        with wave.open("voice_prompt.wav", "wb") as sound_file:
            sound_file.setnchannels(1)
            sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            sound_file.setframerate(44100)
            sound_file.writeframes(b''.join(frames))
        
        # Verify the file was created successfully
        if not os.path.exists("voice_prompt.wav"):
            print("Error: Audio file was not created")
            
    except Exception as e:
        print(f"Error in recording: {str(e)}")