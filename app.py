import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import textwrap

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check API key
if not gemini_api_key:
    st.error("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=gemini_api_key)

# Custom Business Analyst Agent
class BusinessAnalystAgent:
    def __init__(self):
        # Using the latest Gemini model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Custom safety settings to allow business content
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
    
    def generate_report(self, prompt):
        response = self.model.generate_content(
            prompt,
            safety_settings=self.safety_settings,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192
            )
        )
        return response.text

# Format text with proper indentation
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Streamlit UI Configuration
st.set_page_config(
    page_title="Strategic Insights Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .header {
        font-size: 2.5em;
        color: #1f4172;
        text-align: center;
        padding: 20px 0;
        background: linear-gradient(90deg, #f5f7fa, #e4e5f1);
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .report-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #4361ee;
    }
    .stButton>button {
        background: linear-gradient(135deg, #4361ee, #3a0ca3);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-size: 1.1em;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(67, 97, 238, 0.3);
    }
    .stTextArea textarea {
        border-radius: 10px !important;
        padding: 15px !important;
        font-size: 1.1em !important;
    }
    .spinner {
        display: flex;
        justify-content: center;
        margin: 40px 0;
    }
    .success-message {
        text-align: center;
        color: #2ecc71;
        font-weight: bold;
        margin: 15px 0;
        font-size: 1.2em;
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        color: #6c757d;
        font-size: 0.9em;
    }
    .sidebar .block-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<div class="header">Strategic Insights Generator</div>', unsafe_allow_html=True)

# Sidebar for report customization
with st.sidebar:
    st.subheader("Report Configuration")
    report_type = st.selectbox(
        "Select Report Type",
        ["Business Analysis", "SWOT Analysis", "Market Research", 
         "Competitive Landscape", "Financial Projection", "Risk Assessment"],
        index=0
    )
    
    tone = st.selectbox(
        "Select Tone",
        ["Professional", "Executive Summary", "Technical", 
         "Persuasive", "Concise", "Data-Driven"],
        index=0
    )
    
    length = st.slider("Report Length (Words)", 200, 2000, 750)
    
    include_tables = st.checkbox("Include Data Tables", value=True)
    include_recommendations = st.checkbox("Include Strategic Recommendations", value=True)
    include_visualization = st.checkbox("Include Visualization Suggestions", value=True)
    
    st.markdown("---")
    st.info("Configure your business report using the options above. The AI analyst will generate professional insights based on your input.")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Business Context")
    company_name = st.text_input("Company/Organization Name", placeholder="Enter company name")
    industry = st.text_input("Industry/Sector", placeholder="Technology, Healthcare, Finance, etc.")
    business_context = st.text_area(
        "Describe Your Business Challenge or Topic", 
        height=250,
        placeholder="Example: We're launching a new SaaS product in the competitive project management space targeting mid-sized tech companies...",
        help="Provide detailed context for more accurate analysis"
    )
    
    # Create a more sophisticated prompt
    prompt = f"""
    **Act as:** Chief Business Analyst with 15+ years at McKinsey & Company
    **Task:** Generate a comprehensive {report_type} report
    **Company:** {company_name or "[Company Name]"}
    **Industry:** {industry or "[Industry/Sector]"}
    
    **Business Context:**
    {business_context}
    
    **Report Requirements:**
    1. Tone: {tone} with professional business terminology
    2. Length: Approximately {length} words
    3. Structure: Clear sections with headings, subheadings, and bullet points
    4. Data: {"Include relevant data tables" if include_tables else "No tables needed"}
    5. Recommendations: {"Provide actionable strategic recommendations" if include_recommendations else "Omit recommendations"}
    6. Visuals: {"Suggest data visualization types" if include_visualization else "No visualization suggestions"}
    7. Include: Market position, growth opportunities, challenges, strategic outlook
    8. Format: Executive summary, detailed analysis, conclusion
    """

with col2:
    st.subheader("Preview Prompt")
    st.markdown(f"**Report Type:** `{report_type}`")
    st.markdown(f"**Company:** `{company_name or 'Not specified'}`")
    st.markdown(f"**Industry:** `{industry or 'Not specified'}`")
    
    with st.expander("View Full Prompt"):
        st.code(prompt, language="markdown")
    
    st.markdown("---")
    generate_btn = st.button("Generate Strategic Report", use_container_width=True)

# Initialize agent
analyst = BusinessAnalystAgent()

# Report generation and display
if generate_btn:
    if not business_context:
        st.warning("Please provide business context before generating a report")
        st.stop()
    
    with st.spinner("🧠 Analyzing business context... Please wait"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate progress
        for percent in range(0, 101, 10):
            status_text.text(f"Processing: {percent}% complete")
            time.sleep(0.1)
            progress_bar.progress(percent)
        
        try:
            report = analyst.generate_report(prompt)
            progress_bar.empty()
            status_text.empty()
            
            st.markdown('<div class="success-message">✅ Analysis Complete! Strategic Report Generated</div>', unsafe_allow_html=True)
            
            with st.container():
                st.markdown('<div class="report-container">', unsafe_allow_html=True)
                st.subheader(f"{report_type} Report: {company_name}")
                st.markdown(to_markdown(report), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Export options
                st.download_button(
                    label="Download Report as PDF",
                    data=report,
                    file_name=f"{company_name}_{report_type.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")
            st.error("Please try again with more specific business context")

# Footer
st.markdown("---")
st.markdown('<div class="footer">© 2024 Strategic Insights Generator | AI-Powered Business Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; margin-top: 10px; font-size: 0.8em; color: #6c757d;">Powered by Google Gemini API</div>', unsafe_allow_html=True)