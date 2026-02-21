🌾 AI-Powered Smart Farmer Assistance System
https://img.shields.io/badge/Flask-2.3.3-green?style=flat
https://img.shields.io/badge/Python-3.11-blue
https://img.shields.io/badge/license-MIT-orange

A comprehensive web‑based platform that empowers farmers with AI‑driven insights and essential agricultural information. The system provides crop recommendations, disease detection, weather forecasts, price predictions, and government scheme information in a user‑friendly, responsive interface.

📖 Table of Contents

Problem Statement

Proposed Solution

Features

Tech Stack

System Architecture

Implementation Details

Installation

Usage

Contributing

License

Problem Statement

Small and marginal farmers in India and other developing regions often lack access to timely, accurate agricultural information. They face challenges such as:

Selecting the right crop for their soil and climate conditions.

Identifying crop diseases early and applying appropriate treatments.

Accessing reliable weather forecasts to plan irrigation and harvest.

Knowing fair market prices for their produce.

Being unaware of government schemes that can provide financial and technical support.

These information gaps lead to reduced yields, increased losses, and lower income. Existing solutions are often too complex, expensive, or not tailored to the needs of smallholder farmers.

Proposed Solution

The AI-Powered Smart Farmer Assistance System is a web‑based platform designed to empower farmers with AI‑driven insights and essential agricultural information. It provides five core modules:

🌱 Crop Prediction – Recommends suitable crops based on soil type, temperature, rainfall, and humidity.

🦠 Disease Detection – Allows farmers to upload a photo of a diseased leaf and receive a diagnosis, treatment suggestion, and prevention tips.

⛅ Weather Forecast – Fetches real‑time weather data (temperature, humidity, rainfall) for any city using a public API.

💰 Price Prediction – Forecasts crop prices based on seasonal patterns and market trends.

📋 Government Schemes – Lists active welfare schemes with descriptions, benefits, helpline numbers, and direct links to official application portals.

The system is built with a user‑friendly, responsive interface and runs entirely in the browser with a Python Flask backend.

Features

Module	Description

Crop Prediction	Input soil type, temperature, rainfall, humidity → get top 5 suitable crops with a scoring system.
Disease Detection	Upload leaf image → receive mock diagnosis, confidence, solution & prevention (can be replaced with real ML).
Weather Forecast	Enter city name → real‑time data from OpenWeatherMap (temp, condition, humidity, rainfall).
Price Prediction	Select crop and month → forecast price based on seasonal factors (mock data, extensible).
Government Schemes	Browse active schemes with details, helpline numbers, and direct official links.
Tech Stack
Component	Technology Used
Backend Framework	Python Flask
Frontend	HTML5, CSS3, JavaScript (vanilla)
Icons & Fonts	Font Awesome, Google Fonts (Inter)
Weather API	OpenWeatherMap (free tier)
Machine Learning	(Mock implementation for demo) – can be replaced with TensorFlow/PyTorch
Version Control	Git, GitHub
System Architecture
The application follows a client‑server model:

The frontend is a single‑page application built with HTML, CSS, and JavaScript. It dynamically loads content based on user navigation.

The backend is a Flask server that exposes RESTful API endpoints for each module.

Data is exchanged in JSON format.

Implementation Details

3.1 Crop Prediction
Endpoint: /crop-prediction (POST)

The user inputs soil type, temperature, rainfall, and humidity. The backend compares these values against a database of 12 crops with optimal ranges. Each crop gets a score based on how many parameters fall within its ideal range. The top 5 crops are returned. If no crop scores >0, a soil‑based fallback list is provided.

3.2 Disease Detection (Mock)

Endpoint: /disease-detection (POST)

The user uploads an image (base64 encoded). For demo purposes, the system randomly selects a disease from a predefined list of 6 entries (e.g., "Tomato Early Blight", "Rice Blast") and returns the disease name, a confidence percentage, and a recommended solution and prevention tip. This mimics an AI model; in a production version, it would call a real Vision Transformer model.

3.3 Weather Forecast

Endpoint: /weather (POST)

The user enters a city name. The backend calls the OpenWeatherMap API with the city and a free API key. It returns temperature, weather condition, humidity, and rainfall in millimeters. For Indian cities, the code automatically appends ,IN to improve accuracy.

3.4 Price Prediction

Endpoint: /price-prediction (POST)

The user selects a crop and a month. A built‑in price database contains base prices and monthly seasonal factors for 11 crops (rice, wheat, tomato, potato, onion, maize, arecanut, cocoa, pepper, banana, coconut). The predicted price is calculated as base × seasonal_factor[month] × random_variation. The result includes a trend label and market advice.

3.5 Government Schemes

Frontend‑only Module

The renderSchemes() function displays a curated list of 9 central and state‑level agricultural schemes. Each card shows the scheme name, description, benefits, launch year, helpline, and a clickable link to the official website. The data is stored in a JavaScript array and grouped by category (Income Support, Insurance, Credit, etc.).

3.6 Frontend Routing

A lightweight JavaScript router handles navigation without page reloads. Clicking on any navigation link calls navigateTo(section), which injects the corresponding HTML content into the main container and attaches the necessary event listeners.

Installation

Prerequisites
Python 3.11 or higher (download)

pip (Python package manager)

Git

Steps
Clone the repository

bash
git clone https://github.com/yourusername/smart-farmer-ai.git
cd smart-farmer-ai
Create a virtual environment (recommended)

bash
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on macOS/Linux
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Set up environment variables (optional)

OPENWEATHER_API_KEY – Get a free key from OpenWeatherMap. If not set, a demo key is used (may have limited usage).

Run the application

bash
python app.py
Open your browser at http://localhost:5500

Usage

For Crop Prediction, fill in the form and click "Predict Crop".

For Disease Detection, upload a leaf image and click "Analyze Disease".

For Weather, enter a city name (e.g., "Bangalore,IN") and click "Get Weather".

For Price Prediction, select a crop and month, then click "Predict Price".

For Government Schemes, browse the cards and click the "Visit Official Website" button for more details.


TEAM MEMBERS :
Deepthi Y V
Ashitha C U
Bhoomika A
Isiri 
