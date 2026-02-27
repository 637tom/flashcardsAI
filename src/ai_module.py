import ollama
import json
from pathlib import Path

class AiModule:
    def __init__(self, model_name: str = "deepseek-r1:1.5b"):
        self.model = model_name
        self.prompts_path = Path("prompts")
        self.load_prompts()

    def load_prompts(self):
        self.system_role = (self.prompts_path / "system_role.txt").read_text(encoding="utf-8")
        self.p_extract = (self.prompts_path / "extract_points.txt").read_text(encoding="utf-8")
        self.p_flashcards = (self.prompts_path / "flashcards.txt").read_text(encoding="utf-8")
    
    def ask_model(self, prompt: str) -> str:
        response = ollama.generate(
            model=self.model,
            system=self.system_role,
            prompt=prompt
        )
        return response["response"].strip()

    def extract_key_points(self, text: str) -> str: # using a chunk of text as a parameter
        full_prompt = f"{self.p_extract}\n\n{text}"
        return self.ask_model(full_prompt)

    def extract_to_flashcards(self, chunk: str) -> list[dict] | None:
        full_prompt = f"{self.p_flashcards}\n\n{chunk}"
        raw_response = self.ask_model(full_prompt)
        # Clean up in case the model wraps the output in markdown code blocks
        cleaned = raw_response.replace("```json", "").replace("```", "").strip()
        try:
            flashcards: list[dict] = json.loads(cleaned)
            return flashcards
        except json.JSONDecodeError:
            return None

