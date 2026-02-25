import ollama
from pathlib import Path
from pypdf import PdfReader

class PdfMaterial:
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def is_file_valid(self) -> bool:# firstly check if file exists, then if it's pdf format
        if(self.file_path.exists()):
            if(self.file_path.suffix == ".pdf"):
                return True
            else:
                print("This file is not a .pdf file")
                return False
        else:
            print("This file does not exist")
            return False

    def parsing_to_text(self) -> str | None:# parsing from pdf file to a str
        if(self.is_file_valid() == True):
            reader = PdfReader(self.file_path)
            full_text: str = ""

            for page in reader.pages:
                full_text += page.extract_text() + " "
            return full_text
        return None
    
    def parsing_to_chunk(self, chunk_size: int) -> list[str] | None:# slicing to chunks of "chunk_size" length
        full_text = self.parsing_to_text()

        if full_text is not None:
            chunks: list[str] = []

            for i in range(0, len(full_text), chunk_size):
                slice_of_text = full_text[i:i+chunk_size]
                chunks.append(slice_of_text)
            return chunks
        return None



my_pdf_file = PdfMaterial("materials/englishvocab.pdf")

#parasing to chunks
chunks: list[str] | None = my_pdf_file.parsing_to_chunk(200)
#output some chunks of size 200 for example
print("First chunk of the text:")
print(chunks[0])
print("\nSecond chunk of the text:")
print(chunks[1])