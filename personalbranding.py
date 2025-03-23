import streamlit as st
import google.generativeai as genai
import pandas as pd

st.set_page_config(page_title="🚀 AI Personal Branding Assistant", layout="wide")

# Sidebar for API Key Upload
st.sidebar.title("🔑 Upload API Key")
st.sidebar.markdown("""
- [Get Google Gemini API Key](https://aistudio.google.com/app/apikey)  
""")

# API Key Input
gemini_api_key = st.sidebar.text_input("Google Gemini API Key", type="password")

# Ensure API key is provided
if not gemini_api_key:
    st.sidebar.warning("Please enter your API key to proceed.")
    st.stop()

# Initialize Gemini API
genai.configure(api_key=gemini_api_key)

# Streamlit App Main Interface
st.title("🚀 AI-Powered Personal Branding Assistant")
st.subheader("Enhance your online presence and build your personal brand with AI insights!")

# User Inputs
name = st.text_input("Your Name:", "John Doe")
industry = st.selectbox("Industry/Niche:", ["Technology", "Finance", "Healthcare", "Marketing", "Education", "Other"])
platform = st.multiselect("Select Platforms:", ["LinkedIn", "Twitter", "Instagram", "YouTube", "Blog"])
target_audience = st.text_area("Describe Your Target Audience:", "Tech enthusiasts, startup founders, and AI researchers.")
content_frequency = st.selectbox("Content Posting Frequency:", ["Daily", "Weekly", "Bi-Weekly", "Monthly"])

# Placeholder for strategy data
if "branding_data" not in st.session_state:
    st.session_state.branding_data = []

# Function to generate branding strategy
def generate_branding_strategy(name, industry, platforms, audience, frequency):
    prompt = f"""
    Create a personal branding strategy for {name}, a professional in {industry}.
    Platforms: {', '.join(platforms)}
    Target Audience: {audience}
    Content Posting Frequency: {frequency}
    Provide:
    - Content strategy (topics, engagement methods)
    - Posting schedule recommendations
    - Hashtag and SEO tips for visibility
    - Best practices for audience engagement
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text if response else "Sorry, I couldn't generate a branding strategy."

# Generate Branding Strategy
if st.button("Generate Branding Strategy"):
    with st.spinner("Generating personalized branding strategy..."):
        branding_strategy = generate_branding_strategy(name, industry, platform, target_audience, content_frequency)
        st.session_state.branding_data.append([name, industry, platform, target_audience, content_frequency, branding_strategy])
    
    # Display Branding Strategy
    st.subheader("📢 AI-Generated Personal Branding Strategy")
    st.write(branding_strategy)

    # Convert to DataFrame and Display Table
    df = pd.DataFrame(st.session_state.branding_data, columns=["Name", "Industry", "Platforms", "Target Audience", "Frequency", "Branding Strategy"])
    st.dataframe(df)

    # Download Branding Strategy Data
    st.download_button(
        label="📥 Download Branding Strategy",
        data=df.to_csv(index=False),
        file_name="personal_branding_strategy.csv",
        mime="text/csv",
    )

# Run the app using:
# streamlit run personal_branding_assistant.py
