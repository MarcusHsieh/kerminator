from micinput import MicRecorder
from whisperSTT import transcribe_audio
from nlpkermit import KermitResponder

import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk

class KermitGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kerminator")
        self.root.geometry("1280x800")
        self.root.configure(bg="#C0D3C5")

        # init kermit responder class
        self.kermit = KermitResponder()

        # create a MicRecorder instance
        self.mic_recorder = MicRecorder(file_name="micinput.wav")

        # state variables
        self.is_recording = False
        self.is_processing = False

        # ui components
        self._create_ui()

        # bind spacebar => toggle mic
        self.root.bind("<space>", self.toggle_microphone)

    def _create_ui(self):
        # kermit image
        try:
            kermit_image = Image.open("public/kermit-think.png")
            kermit_image = kermit_image.resize((200, 200), Image.LANCZOS)
            self.kermit_photo = ImageTk.PhotoImage(kermit_image)
            kermit_image_label = tk.Label(self.root, image=self.kermit_photo, bg="#C0D3C5")
            kermit_image_label.place(relx=0.5, rely=0.21, anchor="center")
        except FileNotFoundError:
            print("Error: 'kermit-think.png' not found.")

        # main frame
        frame_width = 700
        frame_height = 500
        frame = tk.Frame(self.root, bg="#466362", width=frame_width, height=frame_height, relief="ridge", bd=2)
        frame.place(relx=0.5, rely=0.6, anchor="center")
        frame.pack_propagate(False)

        # user input display
        tk.Label(frame, text=" User Input: ", bg="#466362", font=("Helvetica", 14), height=2).pack(pady=10)
        user_input_frame = tk.Frame(frame, bg="#466362")
        user_input_frame.pack(pady=5, fill="both", expand=True)

        self.user_input_text = tk.Text(
            user_input_frame,
            wrap="word",
            bg="#e8e8e8",
            fg="#333333",
            font=("Helvetica", 12),
            relief="solid",
            height=5,
            width=60,
            padx=5,
            pady=5,
            spacing3=3,
        )
        self.user_input_text.pack(pady=5)

        # kermit response display
        tk.Label(frame, text=" Kermit Response: ", bg="#466362", font=("Helvetica", 14), height=2).pack(pady=10)
        kermit_response_frame = tk.Frame(frame, bg="#466362")
        kermit_response_frame.pack(pady=5, fill="both", expand=True)

        self.kermit_response_text = tk.Text(
            kermit_response_frame,
            wrap="word",
            bg="#e8e8e8",
            fg="#333333",
            font=("Helvetica", 12),
            relief="solid",
            height=8,
            width=60,
            padx=5,
            pady=5,
            spacing3=3,
        )
        self.kermit_response_text.pack(pady=5)

        # mic button
        self.mic_button = tk.Button(
            frame,
            text="Press Spacebar to Record",
            command=self.toggle_microphone,
            bg="#4caf50",
            fg="white",
            font=("Helvetica", 14),
            relief="flat",
            activebackground="#388e3c",
            activeforeground="white",
            height=2,
            width=30,
        )
        self.mic_button.pack(pady=20)

    def toggle_microphone(self, event=None):
        """Toggles microphone recording on/off with spacebar."""
        # ensure NO interrupt if alreading in pipeline
        if self.is_processing:
            self.update_text(self.kermit_response_text, "Pipeline in progress. Please wait...")
            return

        # check if currently recording
        if self.is_recording:
            # stop recording + start the pipeline in a separate thread
            self.stop_recording()
            Thread(target=self.process_audio, daemon=True).start()
        else:
            # start recording
            self.start_recording()

    def start_recording(self):
        """Begins microphone recording."""
        self.is_recording = True
        self.mic_button.config(text="Recording... (press Space to stop)", bg="#d32f2f", activebackground="#c62828")

        # clear previous texts
        self.clear_text(self.user_input_text)
        self.clear_text(self.kermit_response_text)

        # start capturing audio
        self.mic_recorder.start_recording()

    def stop_recording(self):
        """Stops microphone recording."""
        self.is_recording = False
        self.mic_button.config(text="Press Spacebar to Record", bg="#4caf50", activebackground="#388e3c")

        # stop mic recording
        self.mic_recorder.stop_recording()

    def process_audio(self):
        """
        Handles the pipeline: 
        1) Transcribe audio 
        2) Generate Kermit's response
        """
        try:
            self.is_processing = True
            # STT
            self.update_text(self.user_input_text, "Transcribing audio...")
            transcribed_text = transcribe_audio(file_name="micinput.wav")
            self.update_text(self.user_input_text, transcribed_text)

            # NLP
            self.update_text(self.kermit_response_text, "Generating response...")
            response = self.kermit.get_response(transcribed_text)
            self.update_text(self.kermit_response_text, response)

        except Exception as e:
            self.update_text(self.kermit_response_text, f"Error: {str(e)}")

        finally:
            self.is_processing = False

    def update_text(self, text_widget, content):
        """Updates a text widget with new content."""
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)
        text_widget.see(tk.END)

    def clear_text(self, text_widget):
        """Clears a text widget."""
        text_widget.delete(1.0, tk.END)

    def run(self):
        """tkinter main loop"""
        self.root.mainloop()
        self.mic_recorder.terminate()


if __name__ == "__main__":
    app = KermitGUI()
    app.run()
