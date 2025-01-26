import whisper

def transcribe_audio(file_name="micinput.wav", model_size="small"):
    """
    Transcribes audio from a .wav file using the Whisper model.
    
    Args:
    - file_name (str): Path to the .wav file.
    - model_size (str): Whisper model size to load (e.g., "small", "base").
    
    Returns:
    - str: Transcribed text.
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(file_name)
    return result["text"]
