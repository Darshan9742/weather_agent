# ⚡ AI Energy Agent

An AI-powered energy assistant that analyzes household appliance usage and provides energy-saving tips using real-time weather data and large language models.

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-energy-agent.git
cd ai-energy-agent
```

### 2. (Optional) Create and activate a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
If `requirements.txt` is not present, install manually:
```bash
pip install flask python-dotenv requests langchain-google-genai langchain pydantic
```

### 4. Set up environment variables

Create a `.env` file in the root directory and add the following:
```
GOOGLE_API_KEY=your_google_gemini_api_key
WEATHERAPI_KEY=your_weatherapi_key
```

## ▶️ Running the Application

### Start the Flask server
```bash
flask run
```

### Access the web application

Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

Built with ❤️ by Hexagents 
