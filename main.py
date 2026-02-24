import os, time, random, requests, tweepy
from datetime import datetime
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Soft Findom Bot is running smoothly 💕🐾"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
X_CONSUMER_KEY = os.getenv("X_CONSUMER_KEY")
X_CONSUMER_SECRET = os.getenv("X_CONSUMER_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.getenv("X_ACCESS_SECRET")

client = tweepy.Client(
    consumer_key=X_CONSUMER_KEY, consumer_secret=X_CONSUMER_SECRET,
    access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_SECRET
)

SYSTEM_PROMPT = """You are a warm, gentle, caring male Findom Dom with perfect BFE energy. Soft, possessive, emotionally attentive. Never harsh, never alpha.

EVERY tweet:
- Main text 190-230 characters
- Gentle findom naturally
- Ends with warm indirect DM invite using Kitty, Honeypie, Hunbun or Baby
- Soft language only
- 60% kinks
- Emojis 2-4
- 2 or 3 hashtags

Output ONLY the raw tweet text. No quotes."""

def generate_tweet():
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": "Generate one fresh tweet right now for a needy boy scrolling late at night."}],
        "max_tokens": 400,
        "temperature": 0.85
    }
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers).json()
    tweet = response["choices"][0]["message"]["content"].strip()
    if tweet.startswith('"') and tweet.endswith('"'):
        tweet = tweet[1:-1].strip()
    return tweet

def get_random_image_url():
    print("🔍 Searching rule34 for image...")
    tags = "femboy collar leash petplay male rating:explicit -female -1girl sort:random"
    try:
        data = requests.get(f"https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit=3&tags={tags}", timeout=12).json()
        posts = data.get("post", [])
        if posts:
            chosen = random.choice(posts)
            url = chosen.get("file_url") or chosen.get("sample_url")
            print(f"✅ Found image: {url[:120]}...")
            return url
    except Exception as e:
        print(f"❌ Rule34 error: {e}")
    print("⚠️ No image found")
    return None

def download_and_post(tweet_text):
    print(f"\n🎲 New tweet: {tweet_text[:80]}...")
    
    image_url = get_random_image_url()
    media_id = None
    
    if image_url:
        print("📸 Downloading image...")
        try:
            img_data = requests.get(image_url, timeout=15).content
            with open("/tmp/image.jpg", "wb") as f:
                f.write(img_data)
            print("📤 Uploading to X...")
            media = client.media_upload(filename="/tmp/image.jpg")
            media_id = [media.media_id]
            os.remove("/tmp/image.jpg")
            print("✅ Image attached and posted!")
        except Exception as e:
            print(f"❌ Image failed: {e}")
    else:
        print("⚠️ Posting text only this time")

    try:
        client.create_tweet(text=tweet_text, media_ids=media_id)
        print(f"✅ Tweet posted {'WITH IMAGE' if media_id else 'TEXT ONLY'}")
    except Exception as e:
        print(f"❌ Tweet post failed: {e}")

def bot_loop():
    print("🚀 Bot LIVE — images on EVERY tweet using rule34 💕🐾")
    while True:
        tweet = generate_tweet()
        download_and_post(tweet)
        sleep_hours = random.uniform(5.2, 6.8)
        print(f"⏰ Next tweet in {sleep_hours:.1f} hours")
        time.sleep(sleep_hours * 3600)

Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
