import streamlit as st
import pandas as pd
import requests

# ==============================
# CONFIGURATION
# ==============================
PPLX_API_KEY='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'
PPLX_API_URL = "https://api.perplexity.ai/chat/completions"
MODEL_NAME = "sonar-pro"

# ==============================
# STREAMLIT PAGE SETUP
# ==============================
st.set_page_config(page_title="NSE Equities Smart News", layout="centered")

# Load NSE scrips
scripname = pd.read_csv('newsymbol.csv')

# ==============================
# CSS Styling
# ==============================
st.markdown("""
    <style>
    .center-title {
        text-align: center;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title & Subtitle
st.markdown('<h1 class="center-title">NSE Equities Smart News</h1>', unsafe_allow_html=True)
st.markdown('<p class="center-title" style="font-size:20px;">Made NSE Equities News to be Smart</p>', unsafe_allow_html=True)

# ==============================
# NSE Scrip Selection
# ==============================
text = st.selectbox("📌 Select any NSE Scrip", scripname)

# ==============================
# Prompt Template
# ==============================
prompt = f"""
You are a strict financial analyst. A user has typed a stock or commodity name: {text}

Return an analysis in this order:
1. Current Market Condition
2. Sector/Macro Trends
3. Institutional Holdings & Actions 
4. Quarterly Results Summary
5. Analyst Expectations 
6. News Sentiment Summary 
7. Expert/Firm Opinions 
8. Influencer Tweets or Articles 
9. Actionable Insights
10. Important News (Last Week).
   
    
Constraints:
- Use real tone.
- No "As an AI" or explanation about yourself.
- Prefer bullet points.
- Use human-like commentary for influencers.
- Do NOT include direct links (URLs) or citations.
- Use simple english 
"""

# ==============================
# Sonar Pro API Function
# ==============================
def analyze_with_sonar(prompt):
    headers = {
        "Authorization": f"Bearer {PPLX_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a highly skilled financial analyst specializing in NSE market analysis."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1500
    }

    try:
        response = requests.post(PPLX_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ Request Error: {e}"

# ==============================
# Run Analysis
# ==============================
if st.button("Analyze Now"):
    with st.spinner(f"📊 Analyzing {text}..."):
        result = analyze_with_sonar(prompt)
        st.markdown("### 🧾 Analysis Result:")
        st.markdown(result)
        st.snow()
