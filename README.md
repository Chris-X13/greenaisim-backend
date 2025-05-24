
# GreenAISim Backend

This is a simple Flask backend that receives AI simulation parameters via POST and returns estimated CO₂ emissions.

## 🚀 How to Deploy (Free) with Render

1. Go to [https://render.com](https://render.com)
2. Create an account and click "New Web Service" → "Deploy from GitHub"
3. Link your GitHub and select this repository (after pushing it)
4. For runtime, choose:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
5. Once deployed, note the URL. Example: `https://greenaisim-backend.onrender.com`

## 🔁 Endpoint

- **POST** `/calculate`
- JSON body fields: `epochs`, `computeHours`, `gpuType`, `region`, `inferenceFreq`, `duration`
