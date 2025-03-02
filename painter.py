import PIL.ImagePath
import google.generativeai as genai
import PIL.Image
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
from datetime import datetime

load_dotenv()

my_key_openai = os.getenv("openai_apikey")

client = OpenAI(
    api_key=my_key_openai
)

def generate_image_with_dalle(prompt):

    AI_Response = client.images.generate(
        model="dall-e-3",
        size="1024x1024",
        quality="hd",
        n=1,
        response_format="url",
        prompt=prompt
    )

    image_url = AI_Response.data[0].url

    response = requests.get(image_url)
    image_bytes = BytesIO(response.content)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"./img/generated_image_{timestamp}.png"

    if not os.path.exists("./img"):
        os.makedirs("./img")
    
    with open(file_name, "wb") as file:
        file.write(image_bytes.getbuffer())

    return file_name

my_key_google = os.getenv("google_apikey")

genai.configure(
    api_key=my_key_google
    )

def gemini_vision_with_local_file(image_path, prompt):

    # multimodality_prompt = f"""Bu gönderdiğim resmi, bazı ek yönergelerle birlikte yeniden oluşturmanı istiyorum.
    # Bunun için ilk olarak resmi son derece ayrıntılı biçimde betimle. Resimdeki cisimlerin renklerini ve şekillerini 
    # iyi algıla ve renkleri ve şekilleri ayrıntılı açıkla, çünkü o resim üzerinde değişiklik yapmak istediğimde önceki resmin yapısı aynı kalsın.
    # Daha sonra sonucunda bana vereceğin metni, bir yapay zeka modelini kullanarak görsel oluşturmakta kullanacağım. O yüzden yanıtına son halini verirken 
    # bunun resim üretmek kullanılacak bir girdi yani prompt olduğunu dikkate al. İşte ek yönerge şöyle: {prompt}
    # """

    multimodality_prompt = f"""Analyze this image with extreme precision and convert it to a detailed, structured text description that can be used for regeneration. Follow these steps:

    1. Main Elements: List each distinct element in the image (people, objects, buildings, vehicles, etc.) with their exact positioning, scale, and relationship to other elements.

    2. Detailed Properties: For each element, describe:
    - Color: Specific color names (not just "blue" but "navy blue" or "cobalt blue")
    - Texture: Smooth, rough, metallic, matte, etc.
    - Shape: Precise geometric description
    - Lighting: How light interacts with the element
    - Position: Exact location using terms like foreground, background, left third, center, etc.

    3. Environment & Background: Describe the setting, time of day, weather, and background details.

    4. Composition: Explain the overall framing, perspective, and viewing angle.

    5. Style: Note the artistic style (photorealistic, cartoon, painting, etc.)

    After providing this detailed description, I will need to make the following specific modification: {prompt}

    Important: When implementing this change, maintain all other elements exactly as they appear in the original image (same positions, lighting, perspective, background details, etc.). Only modify what is explicitly requested in the modification instruction.
    """

    client = genai.GenerativeModel(model_name="gemini-2.0-flash")

    source_image = PIL.Image.open(image_path)

    AI_Response = client.generate_content(
        [
            multimodality_prompt,
            source_image
        ]
    )

    AI_Response.resolve()

    return AI_Response.text

def generate_image(image_path, prompt):
    image_based_prompt = gemini_vision_with_local_file(image_path=image_path, prompt=prompt)

    updated_image_file_name = generate_image_with_dalle(prompt=image_based_prompt)

    return updated_image_file_name