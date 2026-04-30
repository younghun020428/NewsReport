import google.generativeai as genai
import os

api_key = "AIzaSyB9ehSF0s8zXFzGPrIdQkwU_dMbtcjOmaY"
genai.configure(api_key=api_key)

try:
    print("Available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
