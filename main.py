import os, time, random, requests, tweepy
from datetime import datetime
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Soft Findom Bot is running smoothly 💕🐾"

# === YOUR SECRETS ===
GROQ_API_KEY = os.getenv("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")
X_CONSUMER_KEY = os.getenv("Vk3HqKATuF77RKCgWCj0PxFEl")
X_CONSUMER_SECRET = os.getenv("ub3wGSzYNoKr62MqKK08cyFzp5Hd8BmCVxoNmzp97emZ9OqR7t")
X_ACCESS_TOKEN = os.getenv("1760590671487041536-Z3qVrcgb3lgNlQCVy7Ex8M3qQgdIhV")
X_ACCESS_SECRET = os.getenv("pMeIyEohQA3t6ja2LuNTYkB34tRerBVOOUetuNAFUE5r0")

client = tweepy.Client(
    consumer_key=X_CONSUMER_KEY, consumer_secret=X_CONSUMER_SECRET,
    access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_SECRET
)

SYSTEM_PROMPT = """You are a warm, gentle, caring male Findom Dom with perfect Boyfriend Experience (BFE) energy. Soft, possessive, emotionally attentive. Never harsh, never alpha.

Target: gay femboys, sissies, petboys who feel lost or need structure.

EVERY tweet:
- Main text exactly 190-230 characters
- Gentle findom naturally in every post
- ALWAYS ends with warm indirect DM invite using one of: Kitty, Honeypie, Hunbun, Baby
- Soft language only
- 60% kinks: pet play, sissy/feminization, crossdressing, hypno, light CBT/pain, gentle ownership
- Nicknames: sweetie, baby, my precious, good kitty, honeypie, hunbun
- Emojis: 💕🐾🌸🩷✨👑 (2-4)
- After main text, exactly 2 or 3 hashtags from: #GentleFindom #SoftFindom #MaleFindom #BFEFindom #Femboy #Sissy #PetPlay #SissyTraining #CashPup #NSFWFemboy #SoftDom #SissyHypno #GentleOwnership

Output ONLY the full tweet (main text + hashtags)."""

def generate_tweet():
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "Generate one fresh tweet right now for a needy boy scrolling late at night."}
        ],
        "max_tokens": 400,
        "temperature": 0.87
    }
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers).json()
    return response["choices"][0]["message"]["content"].strip()

def get_random_image_url():
    tag_sets = [
        "1boy femboy collar leash (pull OR tug OR master_hand) kneeling exposed panties rating:explicit -female",
        "1boy sissy crossdressing crawling owned domination collar leash rating:explicit -female",
        "1boy petboy weak submissive crawling master_hand collar rating:explicit -female",
        "1boy hypno sissy makeup exposed kneeling domination rating:explicit -female",
        "1boy light_cbt tease petplay collar owned rating:explicit -female"
    ]
    tags = random.choice(tag_sets) + " sort:random"
    try:
        data = requests.get(f"https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=1&tags={tags}", timeout=8).json()
        return data["post"][0]["file_url"] if data.get("post") else None
    except:
        return None

def download_and_post(tweet_text):
    image_url = get_random_image_url() if random.random() > 0.5 else None
    media_id = None
    if image_url:
        try:
            img_data = requests.get(image_url).content
            with open("/tmp/image.jpg", "wb") as f:
                f.write(img_data)
            media = client.media_upload(filename="/tmp/image.jpg")
            media_id = [media.media_id]
            os.remove("/tmp/image.jpg")
        except:
            pass
    try:
        client.create_tweet(text=tweet_text, media_ids=media_id)
        print(f"✅ Posted — {tweet_text[:70]}...")
    except Exception as e:
        print(f"Error: {e}")

def bot_loop():
    print("🚀 Soft Findom Bot LIVE on Render — free forever 💕🐾")
    while True:
        tweet = generate_tweet()
        download_and_post(tweet)
        sleep_hours = random.uniform(5.2, 6.8)
        print(f"⏰ Next post in {sleep_hours:.1f} hours")
        time.sleep(sleep_hours * 3600)

# Start bot in background
Thread(target=bot_loop, daemon=True).start()

# Run Flask (required for Render Web Service)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
