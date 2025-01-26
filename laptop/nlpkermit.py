import re
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

class KermitResponder:
    def __init__(self, 
                 model_name="meta-llama/Llama-2-7b-chat-hf", 
                 prompt_file="kermit_prompt.md"):
        """
        Initializes the KermitResponder with optional defaults.
        
        Args:
        - model_name (str): Name of the model to load from Hugging Face.
        - prompt_file (str): Path to the Markdown file containing the prompt.
        """
        # configure quantization
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype="float16",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )

        # load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype="auto",
            quantization_config=quantization_config,
            token=True
        )

        # load prompt in init
        self.prompt = self._load_prompt(prompt_file)

    def _load_prompt(self, file_path):
        """Loads the text content of the prompt file."""
        try:
            with open(file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return ""

    def _remove_stage_directions_and_emojis(self, text):
        """
        Removes stage directions (stuff inb/n * and ()) and emojis from the text.
        """
        text = re.sub(r"(\*.*?\*|\(.*?\))", "", text)

        # unicode range
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F700-\U0001F77F"  # alchemical symbols
            u"\U0001F780-\U0001F7FF"  # geometric shapes extended
            u"\U0001F800-\U0001F8FF"  # supplemental arrows-c
            u"\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
            u"\U0001FA00-\U0001FA6F"  # chess symbols
            u"\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-a
            u"\U00002702-\U000027B0"  # dingbats
            u"\U000024C2-\U0001F251"  # enclosed characters
            "]+",
            flags=re.UNICODE
        )
        text = emoji_pattern.sub(r"", text)

        return text.strip()

    def get_response(self, user_input):
        """
        Generates a response to the user's input based on the loaded prompt.
        
        Args:
        - user_input (str): The user's message.

        Returns:
        - str: The generated response from the model.
        """
        prompt = (
            f"{self.prompt}\n\n"
            f"User: {user_input}\n"
            f"Kermit:"
        )

        # tokenize + generate response
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(**inputs, max_new_tokens=100)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # clean kermit's response
        kermit_response_start = response.find("Kermit:")
        if kermit_response_start != -1:
            response = response[kermit_response_start + len("Kermit:"):].strip()
        response = re.sub(r"User:.*", "", response)
        response = self._remove_stage_directions_and_emojis(response)
        print(f" >> KERMIT: '{response}'") # debug
        return response.strip()
