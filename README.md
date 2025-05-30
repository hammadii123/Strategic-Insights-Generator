
# 📊 Strategic Insights Generator

An AI-powered web app to generate professional business reports using Google Gemini models.

## 🔍 Overview
Strategic Insights Generator helps users create detailed business reports such as SWOT analysis, market research, financial projections, and more. It leverages Google's Gemini 1.5 Flash model and a customizable interface built with Streamlit.

## 🚀 Features
- Multiple report types: Business Analysis, SWOT, Market Research, etc.
- Tone customization: Professional, Executive Summary, Data-Driven, etc.
- Word length slider for controlling report size
- Options to include:
  - Data tables
  - Strategic recommendations
  - Visualization suggestions
- Live progress bar during report generation
- Downloadable output

## 🛠️ Tech Stack
- **Python**
- **Streamlit**
- **Google Generative AI (Gemini)**
- **dotenv**

## ⚙️ Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/strategic-insights-generator.git
   cd strategic-insights-generator
````

2. **Add your Gemini API key in a `.env` file**

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```
