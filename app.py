
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Emissions per compute hour (kg CO2e/hour) based on Google TPU LCA study
emission_factors = {
    "a100": 0.050,     # Approx. estimate
    "v100": 0.040,
    "t4": 0.030,
    "tpu-v4": 0.0526,
    "tpu-v5e": 0.0579,
    "tpu-v5p": 0.0663
}

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    epochs = float(data.get("epochs", 0))
    compute_hours = float(data.get("computeHours", 0))
    gpu_type = data.get("gpuType", "a100").lower()
    region = data.get("region", "us").lower()
    freq = float(data.get("inferenceFreq", 0))
    duration = float(data.get("duration", 0))

    # Use static region intensity for now (real-time API to be integrated later)
    region_intensity = {
        "us": 0.6,
        "eu": 0.4,
        "nordics": 0.1
    }

    intensity = region_intensity.get(region, 0.6)
    factor = emission_factors.get(gpu_type, 0.05)

    training_emissions = compute_hours * factor
    inference_emissions = freq * 0.00005 * 30 * duration * intensity
    hardware_emissions = factor * 50  # Approximation placeholder

    total = training_emissions + inference_emissions + hardware_emissions

    return jsonify({
        "training": round(training_emissions, 2),
        "inference": round(inference_emissions, 2),
        "hardware": round(hardware_emissions, 2),
        "total": round(total, 2)
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
