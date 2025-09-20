from openai import OpenAI
import google.generativeai as genai

kimi_api = "Your key"
openai_api = "Your key"
deep_seek_api = "Your key"
GEMINI_API_KEY="AIzaSyAFyuaNpK079lDvnLvF32w4uiabV6Z8IUA"

# Configure the API and key (using DeepSeek as an example)
def generate(message, gpt="gemini", temperature=0):

    if gpt == "deepseek":
        MODEL = "deepseek-chat"
        OPENAI_API_BASE = "https://api.deepseek.com"
        # Set your API key here
        OPENAI_API_KEY = deep_seek_api
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    elif gpt == "openai":
        MODEL = "gpt-4o"
        OPENAI_API_BASE = "https://api.gptapi.us/v1"
        OPENAI_API_KEY = openai_api
        client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_BASE)

    elif gpt =="gemini":
            genai.configure(api_key=GEMINI_API_KEY)
            MODEL ="gemini-2.5-pro"

    else:                   
        raise ValueError(f"Unsupported API provider: {gpt}")

    print('start generating')
    if gpt == "gemini":
        model = genai.GenerativeModel(MODEL)
        generation_config = genai.GenerationConfig(
            temperature=temperature
        )
        #prompt = message[-1]["content"]
        prompt = message
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            stream=False
        )
        print('end generating')

        return response.text
    else:
        response = client.chat.completions.create(
            model=MODEL,
            messages=message,
            stream=False,
            temperature=temperature,
        )
        print('end generating')

        return response.choices[0].message.content
    


