import pyaudio
import wave

def record_audio(file_name="micinput.wav", record_seconds=6, rate=16000, chunk=1024):
    """
    Records audio from the microphone and saves it as a .wav file.
    
    Args:
    - file_name (str): Name of the output .wav file.
    - record_seconds (int): Duration of the recording in seconds.
    - rate (int): Sample rate of the recording.
    - chunk (int): Buffer size for audio chunks.
    """
    # audio recording settings
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)
    print("Recording...")
    frames = [stream.read(chunk) for _ in range(0, int(rate / chunk * record_seconds))]
    print("Done recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # save recording to a .wav file
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
