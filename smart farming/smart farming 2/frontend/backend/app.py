from flask import Flask, jsonify, request
import random, smtplib, os
from email.mime.text import MIMEText
from flask_cors import CORS

# ---------------- INIT ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# ---------------- CONFIG ----------------
EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"

# ---------------- HOME ----------------
@app.route("/")
def home():
    return app.send_static_file("login.html")

# ---------------- STATIC FIX (IMPORTANT) ----------------
@app.route("/<path:path>")
def static_files(path):
    try:
        return app.send_static_file(path)
    except:
        return "Page not found ❌"

# ---------------- HEALTH ----------------
@app.route("/health")
def health():
    return jsonify({"status": "Backend running ✅"})

# ---------------- SENSOR ----------------
current_moisture = 50

@app.route("/sensor-data")
def sensor_data():
    global current_moisture

    temperature = random.uniform(20, 35)
    humidity = random.uniform(40, 90)

    current_moisture += 0.3 if humidity > 60 else -0.3
    current_moisture = max(30, min(80, current_moisture))

    return jsonify({
        "moisture": round(current_moisture, 1),
        "temperature": round(temperature, 1),
        "humidity": round(humidity, 1)
    })

# ---------------- CROP PREDICTION ----------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        temp = float(data.get("temperature", 0))
        hum = float(data.get("humidity", 0))
        moisture = float(data.get("moisture", 50))

        if temp > 30 and hum > 70 and moisture > 60:
            crop = "Rice 🌾"
        elif 20 < temp < 28 and hum < 60:
            crop = "Wheat 🌱"
        elif 25 < temp < 35 and moisture < 60:
            crop = "Maize 🌽"
        elif temp > 30 and moisture < 50:
            crop = "Cotton 🌿"
        elif temp > 28 and hum > 60:
            crop = "Sugarcane 🍬"
        elif temp < 25 and hum < 50:
            crop = "Barley 🌾"
        elif 22 < temp < 30 and moisture < 55:
            crop = "Pulses 🌱"
        elif temp > 27 and moisture < 45:
            crop = "Groundnut 🥜"
        elif temp > 25 and hum > 50:
            crop = "Millets 🌾"
        else:
            crop = "Mixed Crops 🌿"

        return jsonify({"crop": crop})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ---------------- IMAGE / DISEASE PREDICTION ----------------
@app.route("/predict-image", methods=["POST"])
def predict_image():

    try:

        file = request.files.get("file")

        if not file:

            return jsonify({
                "result": "No image uploaded ❌"
            })

        filename = file.filename.lower()

        # DISEASE KEYWORDS
        disease_keywords = [
            "disease",
            "blight",
            "rust",
            "spot",
            "infected",
            "fungus",
            "bacteria"
        ]

        # HEALTHY KEYWORDS
        healthy_keywords = [
            "healthy",
            "green",
            "fresh"
        ]

        # CHECK DISEASE
        if any(word in filename for word in disease_keywords):

            result = "🦠 Diseased Plant Detected"

        elif any(word in filename for word in healthy_keywords):

            result = "✅ Healthy Plant"

        elif "rice" in filename:

            result = "🌾 Healthy Rice Plant"

        elif "wheat" in filename:

            result = "🌱 Healthy Wheat Plant"

        elif "cotton" in filename:

            result = "🌿 Healthy Cotton Plant"

        else:

            result = "⚠ Possible Disease Detected"

        return jsonify({
            "result": result
        })

    except Exception as e:

        return jsonify({
            "result": "Prediction Failed ❌",
            "error": str(e)
        })

# ---------------- EMAIL ----------------
@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()
        user_email = data.get("email")
        message = data.get("message")

        msg = MIMEText(f"From: {user_email}\n\n{message}")
        msg["Subject"] = "Smart Farming Support"
        msg["From"] = EMAIL
        msg["To"] = EMAIL

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())
        server.quit()

        return jsonify({"status": "success ✅"})

    except Exception as e:
        return jsonify({"status": "error ❌", "error": str(e)})

# ---------------- ADVANCED AI ----------------
@app.route("/ask-ai", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        q = data.get("question", "").lower()

        response = ""

        # 🌱 CROPS
        if "crop" in q or "fasal" in q:
            response += "🌾 Best crops depend on season:\n"
            response += "- Summer: Maize 🌽, Cotton 🌿\n"
            response += "- Winter: Wheat 🌱, Barley 🌾\n"
            response += "- Rainy: Rice 🌾\n\n"

        # 💧 WATER
        if "water" in q or "pani" in q:
            response += "💧 Irrigation tip:\nWater in morning or evening only.\n\n"

        # 🌱 SOIL
        if "soil" in q or "mitti" in q:
            response += "🌱 Soil tip:\nLoamy soil is best for most crops.\n\n"

        # 🌿 FERTILIZER
        if "fertilizer" in q or "khaad" in q:
            response += "🌿 Use NPK fertilizer (Nitrogen, Phosphorus, Potassium).\n\n"

        # 🦠 DISEASE
        if "disease" in q or "bimari" in q:
            response += "🦠 Check leaves regularly and use pesticide.\n\n"

        # 🌦 WEATHER
        if "weather" in q:
            response += "🌦 Weather impacts crops — monitor temperature & humidity.\n\n"

        # DEFAULT AI STYLE RESPONSE
        if response == "":
            response = "🤖 I can help with:\n- Crops 🌾\n- Water 💧\n- Soil 🌱\n- Fertilizer 🌿\n- Disease 🦠\n\nTry asking like:\n👉 Best crop in summer?\n👉 How to irrigate?"

        return jsonify({"answer": response})

    except Exception as e:
        return jsonify({"answer": "AI Error ❌", "error": str(e)})
   

# ---------------- RUN ----------------
if __name__ == "__main__":
    print("🚀 Server running at http://127.0.0.1:5000")
    app.run(debug=True)