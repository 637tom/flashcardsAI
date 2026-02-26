import ollama
from pathlib import Path

class AiModule:
    def __init__(self, model_name: str = "deepseek-r1:1.5b"):
        self.model = model_name
        self.prompts_path = Path("prompts")
        self.load_prompts()

    def load_prompts(self):
        self.system_role = (self.prompts_path / "system_role.txt").read_text(encoding="utf-8")
        self.p_extract = (self.prompts_path / "extract_points.txt").read_text(encoding="utf-8")
    
    def ask_model(self, prompt: str) -> str:
        response = ollama.generate(
            model=self.model,
            system=self.system_role,
            prompt=prompt
        )
        return response["response"].strip()

    def extract_key_points(self, text: str) -> str:
        full_prompt = f"{self.p_extract}\n\n{text}"
        return self.ask_model(full_prompt)

