import os
import asyncio
from rag.text_pipeline import retrieve_text
from rag.ocr_pipeline import retrieve_ocr

async def initialize_vector_store():
    print("--- Initializing Vector Database ---")

    text_dir = "knowledge/text"
    ocr_dir = "knowledge/ocr"

    os.makedirs(text_dir, exist_ok=True)
    os.makedirs(ocr_dir, exist_ok=True)

    for filename in os.listdir(text_dir):
        if filename.endswith(".txt"):
            print(f"Ingesting text: {filename}")

    for filename in os.listdir(ocr_dir):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            print(f"Ingesting OCR: {filename}")

    print("--- Database Initialization Complete ---")

if __name__ == "__main__":
    asyncio.run(initialize_vector_store())