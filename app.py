
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Emissions per compute hour (kg CO2e/hour)
emission_factors = {
    "a100": 0.050,
    "v100": 0.040,
    "t4": 0.030,
    "tpu-v4": 0.0526,
    "tpu-v5e": 0.0579,
    "tpu-v5p": 0.0663
}

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    # Core parameters
    epochs = float(data.get("epochs", 0))
    compute_hours = float(data.get("computeHours", 0))
    gpu_type = data.get("gpuType", "a100").lower()
    region = data.get("region", "us").lower()
    freq = float(data.get("inferenceFreq", 0))
    duration = float(data.get("duration", 0))

    # New parameters
    flops = float(data.get("modelSize", 100))  # in billions
    pue = float(data.get("pue", 1.3))
    reuse = data.get("reuse", False)
    intensity = float(data.get("gridIntensity", 0.6))

    factor = emission_factors.get(gpu_type, 0.05)

    # Adjust compute hours based on model size
    flops_base = 100
    flops_factor = flops / flops_base
    adjusted_compute = compute_hours * flops_factor

    # Calculate emissions
    training_emissions = adjusted_compute * factor * pue
    inference_emissions = freq * 0.00005 * 30 * duration * intensity * pue
    hardware_emissions = factor * 50  # Placeholder for embodied emissions

    if reuse:
        training_emissions /= 5
        hardware_emissions /= 5

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
