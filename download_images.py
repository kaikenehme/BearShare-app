import os
import time
from duckduckgo_search import DDGS

def download_images(search_term, save_dir, max_results=600):
    os.makedirs(save_dir, exist_ok=True)
    with DDGS() as ddgs:
        results = ddgs.images(search_term, max_results=max_results)
        for i, result in enumerate(results):
            url = result["image"]
            ext = os.path.splitext(url)[1].split("?")[0]
            ext = ext if ext.lower() in ['.jpg', '.jpeg', '.png'] else '.jpg'
            filepath = os.path.join(save_dir, f"{search_term.replace(' ', '_')}_{i}{ext}")
            if os.path.exists(filepath):
                continue
            try:
                import requests
                img_data = requests.get(url, timeout=5).content
                with open(filepath, "wb") as f:
                    f.write(img_data)
                print(f"✅ Downloaded: {filepath}")
            except Exception as e:
                print(f"⚠️ Failed to download {url}: {e}")
            time.sleep(1)  # avoid hitting rate limits


# Red Belly Snake prompts
snake_prompts = [
    "red belly snake close up",
    "red belly snake curled",
    "red belly snake on sand",
    "red belly snake head only",
    "red belly snake natural habitat"
]

save_folder_snake = "training_data/Red Belly Snake"
for prompt in snake_prompts:
    download_images(prompt, save_folder_snake, max_results=10)
    time.sleep(10)
