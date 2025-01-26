import pyaudio
import wave
import threading

class MicRecorder:
    """
    A class that handles dynamic microphone recording: 
    start_recording() until stop_recording() is called.
    Audio is then written to a .wav file.
    """

    def __init__(self, file_name="micinput.wav", rate=16000, chunk=1024):
        """
        Args:
            file_name (str): Name of the output .wav file.
            rate (int): Sampling rate.
            chunk (int): Buffer size for reading audio.
        """
        self.file_name = file_name
        self.rate = rate
        self.chunk = chunk

        self.p = pyaudio.PyAudio()
        self.stream = None

        self.frames = []
        self.is_recording = False
        self.record_thread = None

    def start_recording(self):
        """Begin capturing audio from the mic in a separate thread."""
        
        if self.is_recording:
            return  # ALREADY RECORDING

        self.is_recording = True
        self.frames = []

        # open audio input stream
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        # start thread to read mic data (LOOP)
        self.record_thread = threading.Thread(target=self._record_loop)
        self.record_thread.start()

    def _record_loop(self):
        """Continuously reads audio data into self.frames while is_recording is True."""
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def stop_recording(self):
        """Stop recording and write captured data to self.file_name."""
        if not self.is_recording:
            return  # ALREADY RECORDING

        self.is_recording = False
        if self.record_thread:
            self.record_thread.join()  # wait for record thread to finish

        # stop and close audio stream
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        # write frames to .wav file
        wf = wave.open(self.file_name, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Recording saved to: {self.file_name}")

    def terminate(self):
        """Terminate the PyAudio instance."""
        self.p.terminate()
