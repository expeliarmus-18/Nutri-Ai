from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

# Load the trained model with error handling
model_path = r'C:\Users\tanma\OneDrive\Desktop\apps\Personel\Projects\NutriAi\NutriAiMl\best_xgb_model.pkl'

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

try:
    model = pickle.load(open(model_path, "rb"))
    print("✅ Model loaded successfully!")
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

# Define diet plans
DIET_PLANS = {
    1: """**High-Protein Diet Plan:**
    - **Breakfast:** Scrambled eggs with spinach and whole-grain toast.
    - **Lunch:** Grilled chicken breast with quinoa and steamed broccoli.
    - **Dinner:** Baked salmon with roasted sweet potatoes and green beans.
    - **Snacks:** Greek yogurt, nuts, and protein shakes.""",

    2: """**Low-Carb Diet Plan:**
    - **Breakfast:** Omelette with cheese and avocado.
    - **Lunch:** Grilled chicken salad with olive oil dressing.
    - **Dinner:** Steak with sautéed mushrooms and zucchini noodles.
    - **Snacks:** Almonds, cheese sticks, and boiled eggs.""",

    3: """**Vegetarian Diet Plan:**
    - **Breakfast:** Oatmeal with nuts and berries.
    - **Lunch:** Chickpea salad with feta cheese and lemon dressing.
    - **Dinner:** Lentil soup with whole wheat bread.
    - **Snacks:** Hummus with carrots, peanut butter with apples.""",

    4: """**Balanced Diet Plan:**
    - **Breakfast:** Whole-grain cereal with milk and banana.
    - **Lunch:** Grilled fish with brown rice and mixed vegetables.
    - **Dinner:** Stir-fried tofu with quinoa and bell peppers.
    - **Snacks:** Handful of nuts, yogurt, or fresh fruit.""",

    5: """**Keto Diet Plan:**
    - **Breakfast:** Scrambled eggs with cheese and avocado.
    - **Lunch:** Grilled chicken with cauliflower rice and green beans.
    - **Dinner:** Beef steak with buttered asparagus.
    - **Snacks:** Nuts, cheese, and dark chocolate (85% cocoa)."""
}

# Create Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Log received request
        data = request.get_json()
        print("🔹 Received request:", data)

        # Validate input
        required_fields = ["age", "weight", "height", "region", "diet_preference"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Extract and convert input
        age = int(data['age'])
        weight = float(data['weight'])
        height = float(data['height'])
        region = data['region']
        diet_preference = data['diet_preference']

        # Encode categorical variables
        region_encoded = hash(region) % 100  
        diet_pref_encoded = hash(diet_preference) % 100  

        # Prepare input for model
        input_data = np.array([[age, weight, height, region_encoded, diet_pref_encoded]])
        print("🔹 Model input:", input_data)

        # Ensure input shape is correct
        if input_data.shape[1] != 5:
            return jsonify({"error": "Invalid input shape"}), 400

        # Predict diet plan
        prediction = model.predict(input_data)[0]
        print("🔹 Model Prediction:", prediction)

        # Convert prediction to integer if necessary
        prediction = int(prediction)

        # Map prediction to diet plan
        diet_plan = DIET_PLANS.get(prediction, "Diet plan not found")
        
        return jsonify({"diet_plan": diet_plan}), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Allow external access
