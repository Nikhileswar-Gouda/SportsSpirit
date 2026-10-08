from flask import Flask, jsonify, render_template, request
import os
import requests

app = Flask(__name__)

SPORT_ALIASES = {
    "cricket": ["cricket", "cricket bat", "cricket gear"],
    "football": ["football", "soccer", "football shoes", "soccer ball"],
    "tennis": ["tennis", "tennis racket", "tennis gear"],
    "badminton": ["badminton", "shuttle", "badminton racket"],
    "boxing": ["boxing", "boxing gloves", "mma"],
    "gym": ["gym", "fitness", "workout", "gym accessories"],
    "swimming": ["swimming", "swim", "swim gear"]
}

PRODUCTS = [
    {
        "id": 1,
        "name": "Cricket Bat Elite",
        "sport": "cricket",
        "category": "Cricket",
        "price": 1899,
        "rating": 4.9,
        "reviews": 341,
        "image": "https://images.unsplash.com/photo-1531415074968-036ba1b575da?auto=format&fit=crop&w=900&q=80",
        "description": "Premium willow bat designed for power and balance on match-day performance.",
        "badge": "Best Seller"
    },
    {
        "id": 2,
        "name": "Cricket Gloves Pro",
        "sport": "cricket",
        "category": "Cricket",
        "price": 1399,
        "rating": 4.8,
        "reviews": 280,
        "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=900&q=80",
        "description": "Shock-absorbing gloves with superior grip and wrist protection.",
        "badge": "Popular"
    },
    {
        "id": 3,
        "name": "Pro Football Kit",
        "sport": "football",
        "category": "Football",
        "price": 2499,
        "rating": 4.9,
        "reviews": 412,
        "image": "https://images.unsplash.com/photo-1547347298-4074fc3086f0?auto=format&fit=crop&w=900&q=80",
        "description": "Official match-ready football kit with breathable fabric and comfort fit.",
        "badge": "Top Rated"
    },
    {
        "id": 4,
        "name": "Football Boots X9",
        "sport": "football",
        "category": "Football",
        "price": 3299,
        "rating": 4.7,
        "reviews": 236,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
        "description": "AG-grip boots made for quick turns, control, and all-weather traction.",
        "badge": "New"
    },
    {
        "id": 5,
        "name": "Tennis Racket Ace",
        "sport": "tennis",
        "category": "Tennis",
        "price": 4599,
        "rating": 4.9,
        "reviews": 201,
        "image": "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?auto=format&fit=crop&w=900&q=80",
        "description": "Lightweight racket optimized for spin, control, and powerful serves.",
        "badge": "Best Seller"
    },
    {
        "id": 6,
        "name": "Badminton Set Prime",
        "sport": "badminton",
        "category": "Badminton",
        "price": 2199,
        "rating": 4.8,
        "reviews": 194,
        "image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?auto=format&fit=crop&w=900&q=80",
        "description": "Complete badminton set includes rackets, shuttlecocks, and carrying bag.",
        "badge": "Popular"
    },
    {
        "id": 7,
        "name": "Boxing Gloves Titan",
        "sport": "boxing",
        "category": "Boxing",
        "price": 2699,
        "rating": 4.8,
        "reviews": 139,
        "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80",
        "description": "Professional training gloves with shock protection and wrist support.",
        "badge": "Elite"
    },
    {
        "id": 8,
        "name": "Power Gym Kit",
        "sport": "gym",
        "category": "Gym",
        "price": 3499,
        "rating": 4.9,
        "reviews": 453,
        "image": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=900&q=80",
        "description": "Complete body-strength kit with dumbbells, mat, and resistance accessories.",
        "badge": "Trainer Pick"
    },
    {
        "id": 9,
        "name": "Swim Pro Kit",
        "sport": "swimming",
        "category": "Swimming",
        "price": 2999,
        "rating": 4.7,
        "reviews": 175,
        "image": "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?auto=format&fit=crop&w=900&q=80",
        "description": "Performance swimming gear with goggles, cap, and training essentials.",
        "badge": "Frequent Pick"
    }
]


def get_sport_key(message):
    text = message.lower()
    for sport, keywords in SPORT_ALIASES.items():
        if any(keyword in text for keyword in keywords):
            return sport
    return None


def get_recommended_products(message):
    sport = get_sport_key(message)
    if not sport:
        return []
    return [p for p in PRODUCTS if p["sport"] == sport]


def answer_question(message):
    text = message.lower().strip()
    if not text:
        return "Please type a sport name or question about a product."

    if any(word in text for word in ["hi", "hello", "hey"]):
        return "Hello! Type a sport like cricket, football, tennis, or badminton, and I will show the required gear and product price."

    sport = get_sport_key(text)
    recommended = get_recommended_products(text)

    if sport and recommended and any(word in text for word in ["need", "required", "gear", "tool", "buy", "order", "show", "recommend", "best"]):
        names = ", ".join(f"{p['name']} (₹{p['price']})" for p in recommended)
        return f"For {sport.title()}, the required gear is: {names}. You can order these products from our store."

    for product in PRODUCTS:
        product_name = product["name"].lower()
        if product_name in text or any(word in text for word in ["price of", "cost of", "how much", "what is the price", "price"]):
            if any(word in text for word in ["price", "cost", "how much"]):
                return f"{product['name']} costs ₹{product['price']}."
            if "rating" in text or "reviews" in text:
                return f"{product['name']} has a rating of {product['rating']} out of 5 from {product['reviews']} reviews."

    if sport and recommended:
        top = recommended[0]
        return f"For {sport.title()}, the best option is {top['name']} at ₹{top['price']} because it is popular and highly rated."

    if "price" in text:
        return "Please mention the sport or product name, for example: 'price of cricket bat' or 'football gear'."

    if sport:
        return f"I found {sport.title()}. The most useful products are: " + ", ".join(p["name"] for p in recommended[:3]) + "."

    return "I can help with sports like cricket, football, tennis, badminton, boxing, gym, and swimming. Please type one of these sports names to see the required products."


def call_local_qwen(message):
    model = os.getenv("QWEN_MODEL", "qwen2.5:3b")
    ollama_url = os.getenv("QWEN_BASE_URL", "http://localhost:11434/api/generate")

    payload = {
        "model": model,
        "prompt": message,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 220
        }
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "").strip()
        if text:
            return text
    except Exception:
        pass

    try:
        base_url = os.getenv("QWEN_OPENAI_BASE_URL", "http://localhost:11434/v1")
        openai_payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful sports equipment assistant."},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 220
        }
        response = requests.post(
            f"{base_url}/chat/completions",
            json=openai_payload,
            timeout=20,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"].strip()
        if text:
            return text
    except Exception:
        pass

    return answer_question(message)


@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)


@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    message = (payload.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Please type a sport name or ask a product question."})

    recommended = get_recommended_products(message)
    reply = call_local_qwen(message)

    return jsonify({"reply": reply, "recommended": recommended})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
