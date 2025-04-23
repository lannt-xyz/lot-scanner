import google.generativeai as genai

from config import settings

genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel(settings.gemini_model_id)

# res = model.generate_content('What is the capital of France?')
# print("Response from Gemini model:")
# print(res.text)

# # List available models
# models = genai.list_models()
# print("Available models:")
# for model in models:
#     print(f"Model ID: {model.name}, Supported Methods: {model.supported_generation_methods}")


def generate_gemini_response(prompt):
    """
    Generate a response from the Gemini model using the provided prompt.
    
    Args:
        prompt (str): The input prompt for the model.
        
    Returns:
        str: The generated response from the model.
    """

    print("Using prompt:")
    print(prompt)

    response = model.generate_content(prompt)
    structured_json = response.text

    print("Response from Gemini model:")
    print(structured_json)

    return structured_json
