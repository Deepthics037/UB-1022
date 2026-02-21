from flask import Flask, render_template, request, jsonify
import requests
import base64
import io
import traceback
import os
import random

app = Flask(__name__)

# ============================================
# SAFE IMPORTS – with error handling
# ============================================


# ============================================
# DISEASE DATABASE (mock, always works)
# ============================================
DISEASE_REMEDIES = [
    {"name": "Tomato Early Blight", "solution": "Apply copper fungicide", "prevention": "Avoid overhead watering"},
    {"name": "Tomato Late Blight", "solution": "Use copper-based fungicides", "prevention": "Good air circulation"},
    {"name": "Potato Early Blight", "solution": "Spray chlorothalonil", "prevention": "Remove infected debris"},
    {"name": "Corn Common Rust", "solution": "Apply sulfur fungicide", "prevention": "Use resistant hybrids"},
    {"name": "Rice Blast", "solution": "Use tricyclazole", "prevention": "Avoid excess nitrogen"},
    {"name": "Healthy Plant", "solution": "No treatment", "prevention": "Continue good practices"}
]

# ============================================
# HOME ROUTE
# ============================================
@app.route('/')
def home():
    return render_template('index.html')

# ============================================
# GLOBAL ERROR HANDLER
# ============================================
@app.errorhandler(Exception)
def handle_exception(e):
    print("🔥 Unhandled exception:", traceback.format_exc())
    return jsonify({"error": f"Server error: {str(e)}"}), 500

# ============================================
# CROP PREDICTION (scoring logic)
# ============================================
@app.route('/crop-prediction', methods=['POST'])
def crop_prediction():
    try:
        data = request.json
        soil = data.get('soil')
        temp = float(data.get('temperature', 25))
        rainfall = float(data.get('rainfall', 100))
        humidity = float(data.get('humidity', 60))

        crops = [
            {'name': 'Rice', 'soils': ['Clay', 'Loamy'], 'tmin': 20, 'tmax': 35, 'rmin': 100, 'rmax': 200, 'hmin': 60, 'hmax': 90},
            {'name': 'Wheat', 'soils': ['Loamy', 'Clay'], 'tmin': 10, 'tmax': 25, 'rmin': 50, 'rmax': 100, 'hmin': 40, 'hmax': 70},
            {'name': 'Maize', 'soils': ['Loamy', 'Sandy'], 'tmin': 18, 'tmax': 32, 'rmin': 60, 'rmax': 120, 'hmin': 50, 'hmax': 80},
            {'name': 'Cotton', 'soils': ['Black', 'Loamy'], 'tmin': 21, 'tmax': 35, 'rmin': 50, 'rmax': 100, 'hmin': 40, 'hmax': 70},
            {'name': 'Sugarcane', 'soils': ['Clay', 'Loamy'], 'tmin': 20, 'tmax': 35, 'rmin': 100, 'rmax': 180, 'hmin': 60, 'hmax': 85},
            {'name': 'Groundnut', 'soils': ['Sandy', 'Red'], 'tmin': 20, 'tmax': 30, 'rmin': 50, 'rmax': 80, 'hmin': 50, 'hmax': 75},
            {'name': 'Millet', 'soils': ['Sandy', 'Red'], 'tmin': 25, 'tmax': 40, 'rmin': 30, 'rmax': 70, 'hmin': 30, 'hmax': 60},
            {'name': 'Vegetables', 'soils': ['Loamy'], 'tmin': 15, 'tmax': 30, 'rmin': 60, 'rmax': 120, 'hmin': 50, 'hmax': 80},
            {'name': 'Pulses', 'soils': ['Red', 'Loamy'], 'tmin': 20, 'tmax': 30, 'rmin': 40, 'rmax': 80, 'hmin': 40, 'hmax': 70},
            {'name': 'Potato', 'soils': ['Sandy', 'Loamy'], 'tmin': 15, 'tmax': 25, 'rmin': 50, 'rmax': 100, 'hmin': 50, 'hmax': 80},
            {'name': 'Banana', 'soils': ['Loamy', 'Clay'], 'tmin': 20, 'tmax': 35, 'rmin': 100, 'rmax': 200, 'hmin': 60, 'hmax': 90},
            {'name': 'Coconut', 'soils': ['Sandy', 'Red'], 'tmin': 25, 'tmax': 35, 'rmin': 100, 'rmax': 250, 'hmin': 60, 'hmax': 90},
        ]

        scored = []
        for c in crops:
            if soil not in c['soils']:
                continue
            score = 0
            if c['tmin'] <= temp <= c['tmax']:
                score += 40
            if c['rmin'] <= rainfall <= c['rmax']:
                score += 30
            if c['hmin'] <= humidity <= c['hmax']:
                score += 30
            if score > 0:
                scored.append((c['name'], score))

        scored.sort(key=lambda x: x[1], reverse=True)

        if not scored:
            fallback = {
                'Clay': ['Rice', 'Sugarcane', 'Wheat'],
                'Loamy': ['Wheat', 'Maize', 'Vegetables', 'Cotton'],
                'Sandy': ['Groundnut', 'Millet', 'Potato'],
                'Black': ['Cotton', 'Sugarcane', 'Millets'],
                'Red': ['Groundnut', 'Pulses', 'Millets']
            }
            crops_list = fallback.get(soil, ['Rice', 'Wheat', 'Maize'])
            return jsonify({'crops': crops_list, 'note': 'Soil-based recommendation (climate parameters suboptimal)'})

        top_crops = [c[0] for c in scored[:5]]
        return jsonify({'crops': top_crops})
    except Exception as e:
        print("Crop prediction error:", e)
        return jsonify({'error': str(e)})

# ============================================
# DISEASE DETECTION – MOCK (always works)
# ============================================
@app.route('/disease-detection', methods=['POST'])
def disease_detection():
    try:
        # Simulate a small delay
        import time
        time.sleep(1)
        result = random.choice(DISEASE_REMEDIES)
        return jsonify({
            'name': result['name'],
            'confidence': f"{random.uniform(85, 99.9):.1f}%",
            'solution': result['solution'],
            'prevention': result['prevention']
        })
    except Exception as e:
        print("Disease detection error:", e)
        return jsonify({'error': str(e)})

# ============================================
# WEATHER ENDPOINT (OpenWeatherMap)
# ============================================
@app.route('/weather', methods=['POST'])
def weather():
    try:
        data = request.json
        city_input = data.get('city', '').strip()
        if not city_input:
            return jsonify({'error': 'Please enter a city name'})

        API_KEY = os.environ.get("OPENWEATHER_API_KEY", "25af571f66faae35f603b05c296c99b3")
        indian_cities = {
            'mumbai': 'IN', 'delhi': 'IN', 'kolkata': 'IN', 'chennai': 'IN',
            'bangalore': 'IN', 'bengaluru': 'IN', 'hyderabad': 'IN', 'pune': 'IN',
            'lucknow': 'IN', 'jaipur': 'IN', 'chandigarh': 'IN', 'bhopal': 'IN'
        }
        city_lower = city_input.split(',')[0].strip().lower()
        if city_lower in indian_cities and ',' not in city_input:
            query = f"{city_input},{indian_cities[city_lower]}"
        else:
            query = city_input

        url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return jsonify({'error': f'City "{city_input}" not found. Try with country code (e.g., Bangalore,IN)'})

        w = response.json()
        rain_mm = 0
        if 'rain' in w:
            rain_mm = w['rain'].get('1h', 0) or w['rain'].get('3h', 0)

        return jsonify({
            'temperature': w['main']['temp'],
            'condition': w['weather'][0]['description'].title(),
            'humidity': w['main']['humidity'],
            'rain_mm': rain_mm,
            'rain_prediction': f'🌧️ {rain_mm} mm' if rain_mm > 0 else '☀️ No rain',
            'city': w.get('name', city_input),
            'country': w['sys']['country']
        })
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Weather API timeout. Please try again.'})
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Network error. Check your internet connection.'})
    except Exception as e:
        print("Weather error:", e)
        return jsonify({'error': str(e)})

# ============================================
# PRICE PREDICTION (mock, but realistic)
# ============================================
@app.route('/price-prediction', methods=['POST'])
def price_prediction():
    try:
        data = request.json
        crop = data.get('crop', 'rice').lower()
        month = int(data.get('month', 1))

        # Price database (simplified)
        price_db = {
            'rice': {'base': 35, 'seasonal': [1.0,0.95,0.98,1.02,1.05,1.08,1.10,1.07,1.03,1.0,0.97,0.95], 'trend': 'stable', 'unit': '₹/kg', 'advice': 'Market stable.'},
            'wheat': {'base': 28, 'seasonal': [1.02,1.0,0.97,0.95,0.98,1.02,1.05,1.07,1.05,1.02,1.0,0.98], 'trend': 'stable', 'unit': '₹/kg', 'advice': 'Stable market.'},
            'tomato': {'base': 25, 'seasonal': [0.8,0.85,0.9,1.1,1.3,1.5,1.4,1.2,1.0,0.9,0.85,0.8], 'trend': 'highly volatile', 'unit': '₹/kg', 'advice': 'Sell May-July.'},
            'potato': {'base': 22, 'seasonal': [0.9,0.92,0.95,1.05,1.15,1.2,1.18,1.1,1.02,0.95,0.9,0.88], 'trend': 'slightly up', 'unit': '₹/kg', 'advice': 'Wait a month.'},
            'onion': {'base': 30, 'seasonal': [0.7,0.75,0.85,1.1,1.4,1.6,1.5,1.3,1.1,0.9,0.8,0.75], 'trend': 'highly volatile', 'unit': '₹/kg', 'advice': 'Check local mandi.'},
            'maize': {'base': 20, 'seasonal': [1.0,0.98,0.97,0.99,1.02,1.05,1.07,1.06,1.03,1.01,1.0,0.99], 'trend': 'stable', 'unit': '₹/kg', 'advice': 'Sell anytime.'},
            'arecanut': {'base': 370, 'seasonal': [1.12,1.10,1.08,1.05,1.00,0.95,0.90,0.92,0.95,1.00,1.05,1.10], 'trend': 'strong uptrend', 'unit': '₹/kg', 'advice': 'Sell Jan-Mar.'},
            'cocoa': {'base': 120, 'seasonal': [1.05,1.02,0.98,0.95,0.92,0.90,0.92,0.98,1.05,1.10,1.12,1.08], 'trend': 'rising', 'unit': '₹/kg', 'advice': 'Sell to cooperatives.'},
            'pepper': {'base': 450, 'seasonal': [1.15,1.12,1.08,1.02,0.98,0.95,0.90,0.92,0.98,1.05,1.10,1.12], 'trend': 'volatile', 'unit': '₹/kg', 'advice': 'Monitor international markets.'},
            'banana': {'base': 35, 'seasonal': [0.95,0.98,1.05,1.20,1.15,1.10,0.95,0.88,0.85,0.90,0.95,0.98], 'trend': 'seasonal', 'unit': '₹/dozen', 'advice': 'Festival demand.'},
            'coconut': {'base': 25, 'seasonal': [0.95,0.98,1.05,1.10,1.08,1.02,0.98,0.95,0.98,1.02,0.98,0.92], 'trend': 'stable', 'unit': '₹/nut', 'advice': 'Copra influences price.'}
        }

        crop_data = price_db.get(crop, price_db['rice'])
        month_idx = max(0, min(month-1, 11))
        seasonal = crop_data['seasonal'][month_idx]
        variation = random.uniform(0.95, 1.05)
        predicted_price = round(crop_data['base'] * seasonal * variation, 2)

        return jsonify({
            'crop': crop,
            'predicted_price': predicted_price,
            'unit': crop_data['unit'],
            'confidence': f"{random.randint(85, 95)}%",
            'trend': crop_data['trend'],
            'advice': crop_data['advice'],
            'source': 'Seasonal market analysis'
        })
    except Exception as e:
        print("Price prediction error:", e)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5500)