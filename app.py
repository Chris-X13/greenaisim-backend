
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from your GitHub Pages site

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    epochs = float(data.get('epochs', 0))
    compute_hours = float(data.get('computeHours', 0))
    gpu = data.get('gpuType', 'a100')
    region = data.get('region', 'us')
    freq = float(data.get('inferenceFreq', 0))
    duration = float(data.get('duration', 0))

    emission_factors = {'a100': 1.0, 'v100': 0.8, 't4': 0.6}
    region_intensity = {'us': 0.6, 'eu': 0.4, 'nordics': 0.1}

    training = compute_hours * emission_factors[gpu] * region_intensity[region]
    inference = freq * 0.00005 * 30 * duration * region_intensity[region]
    hardware = 50 * emission_factors[gpu]
    total = training + inference + hardware

    return jsonify({
        'training': round(training, 2),
        'inference': round(inference, 2),
        'hardware': round(hardware, 2),
        'total': round(total, 2)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

