import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    organization=os.getenv('OPENAI_ORG_ID'),
    project=os.getenv('OPENAI_PROJECT_ID'),
)

def analyze_images(diagnosis_type: str, image_paths: List[str]) -> str:
    msgInstructions = f"Analiza estas imágenes para: {diagnosis_type}, devuelve si hay alguna enfermedad o plaga, que tipo de enfermedad o plaga es y si es necesario aplicar algún tratamiento. Determina si es necesario realizar un análisis más profundo y qué tipo de análisis sería. Especifica si es necesario realizar un análisis más profundo y qué tipo de análisis sería."
    messages = [
        {
            "role": "user",
            "content": [
                # Pending: define the instructions to send to the model
                {"type": "text", "text": msgInstructions}
            ]
        }
    ]

    # Adding each image URL to the messages list
    for path in image_paths:
        messages[0]["content"].append({"type": "image_url", "image_url": path})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=300,
    )
    
    return response.choices[0].message['content'].strip()