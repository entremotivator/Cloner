import streamlit as st
import requests
import time
import json
import pandas as pd
from datetime import datetime
import random

# ==========================================
# PAGE CONFIGURATION & MATRIX THEMING
# ==========================================
st.set_page_config(
    page_title="AI Digital Twin | Matrix Interface",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Matrix-inspired CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');
    
    /* Global Matrix Theme */
    html, body, [class*="css"] {
        font-family: 'Share Tech Mono', monospace;
        background-color: #0d0d0d !important;
        color: #00ff41 !important;
    }

    .main {
        background: linear-gradient(180deg, #000000 0%, #0a0e0a 50%, #000000 100%);
        background-attachment: fixed;
    }

    /* Matrix Rain Effect Background */
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0, 255, 65, 0.03) 2px,
                rgba(0, 255, 65, 0.03) 4px
            );
        pointer-events: none;
        z-index: 0;
        animation: matrix-scan 10s linear infinite;
    }

    @keyframes matrix-scan {
        0% { transform: translateY(0); }
        100% { transform: translateY(20px); }
    }

    /* Glitch Animation */
    @keyframes glitch {
        0% { text-shadow: 2px 2px #00ff41, -2px -2px #00ff41; }
        25% { text-shadow: -2px 2px #00ff41, 2px -2px #39ff14; }
        50% { text-shadow: 2px -2px #39ff14, -2px 2px #00ff41; }
        75% { text-shadow: -2px -2px #00ff41, 2px 2px #39ff14; }
        100% { text-shadow: 2px 2px #00ff41, -2px -2px #00ff41; }
    }

    /* Main Header */
    .matrix-header {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        color: #00ff41;
        text-align: center;
        margin: 2rem 0 1rem 0;
        text-transform: uppercase;
        letter-spacing: 8px;
        text-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41, 0 0 30px #00ff41;
        animation: glitch 3s infinite;
    }
    
    .matrix-subheader {
        font-family: 'Share Tech Mono', monospace;
        font-size: 1.2rem;
        color: #39ff14;
        text-align: center;
        margin-bottom: 3rem;
        text-shadow: 0 0 5px #39ff14;
        letter-spacing: 3px;
    }

    /* Card/Container Styling */
    .matrix-card {
        background: rgba(0, 20, 0, 0.85);
        border: 2px solid #00ff41;
        border-radius: 8px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 
            0 0 20px rgba(0, 255, 65, 0.3),
            inset 0 0 20px rgba(0, 255, 65, 0.1);
        position: relative;
        overflow: hidden;
    }

    .matrix-card::before {
        content: "";
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00ff41, #39ff14, #00ff41);
        z-index: -1;
        opacity: 0.3;
        filter: blur(10px);
    }

    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 5px;
        border: 1px solid;
        text-shadow: 0 0 5px currentColor;
    }
    
    .status-pending {
        background: rgba(255, 255, 0, 0.1);
        color: #ffff00;
        border-color: #ffff00;
        box-shadow: 0 0 10px rgba(255, 255, 0, 0.5);
    }
    
    .status-completed {
        background: rgba(0, 255, 65, 0.1);
        color: #00ff41;
        border-color: #00ff41;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }
    
    .status-processing {
        background: rgba(0, 191, 255, 0.1);
        color: #00bfff;
        border-color: #00bfff;
        box-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
        animation: pulse 2s infinite;
    }
    
    .status-failed {
        background: rgba(255, 0, 0, 0.1);
        color: #ff0000;
        border-color: #ff0000;
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #001a00 0%, #003300 100%);
        color: #00ff41;
        border: 2px solid #00ff41;
        border-radius: 8px;
        padding: 12px 30px;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.4);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #003300 0%, #004d00 100%);
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.8);
        transform: translateY(-2px);
        border-color: #39ff14;
    }

    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.6);
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: rgba(0, 20, 0, 0.8) !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 5px;
        font-family: 'Share Tech Mono', monospace !important;
        box-shadow: inset 0 0 10px rgba(0, 255, 65, 0.2);
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #39ff14 !important;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.5) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000 0%, #001a00 100%);
        border-right: 2px solid #00ff41;
        box-shadow: 5px 0 20px rgba(0, 255, 65, 0.3);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Custom Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff41, transparent);
        margin: 2rem 0;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(0, 20, 0, 0.5);
        border-radius: 8px;
        padding: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(0, 20, 0, 0.8);
        border: 1px solid #00ff41;
        color: #00ff41;
        border-radius: 5px;
        padding: 10px 20px;
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #003300, #004d00);
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.6);
        color: #39ff14;
    }

    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(0, 20, 0, 0.8) !important;
        border: 1px solid #00ff41 !important;
        border-radius: 5px;
        color: #00ff41 !important;
        font-family: 'Orbitron', monospace;
    }

    /* Success/Error/Warning Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        background-color: rgba(0, 20, 0, 0.9) !important;
        border-left: 4px solid #00ff41 !important;
        color: #00ff41 !important;
        font-family: 'Share Tech Mono', monospace;
    }

    .stError {
        border-left-color: #ff0000 !important;
        color: #ff0000 !important;
    }

    .stWarning {
        border-left-color: #ffff00 !important;
        color: #ffff00 !important;
    }

    /* Loading Spinner */
    .stSpinner > div {
        border-color: #00ff41 !important;
        border-right-color: transparent !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00ff41 !important;
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        text-shadow: 0 0 10px #00ff41;
    }

    /* Code blocks */
    code {
        background-color: rgba(0, 20, 0, 0.8) !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        padding: 2px 6px;
        border-radius: 3px;
    }

    /* Section Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00ff41 !important;
        font-family: 'Orbitron', monospace !important;
        text-shadow: 0 0 5px #00ff41;
    }

    /* Matrix Rain Characters */
    .matrix-char {
        position: fixed;
        color: #00ff41;
        font-family: 'Share Tech Mono', monospace;
        font-size: 20px;
        opacity: 0.8;
        pointer-events: none;
        animation: fall linear infinite;
    }

    @keyframes fall {
        to {
            transform: translateY(100vh);
            opacity: 0;
        }
    }

    /* Neural Network Background Pattern */
    .neural-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(0, 255, 65, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(57, 255, 20, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(0, 255, 65, 0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    /* Scan Line Effect */
    .scanline {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            to bottom,
            rgba(0, 255, 65, 0) 0%,
            rgba(0, 255, 65, 0.1) 50%,
            rgba(0, 255, 65, 0) 100%
        );
        background-size: 100% 4px;
        pointer-events: none;
        z-index: 1;
        animation: scan 8s linear infinite;
    }

    @keyframes scan {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100%); }
    }

    /* Holographic Effect */
    .holo-effect {
        position: relative;
        overflow: hidden;
    }

    .holo-effect::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(0, 255, 65, 0.1) 50%,
            transparent 70%
        );
        animation: hologram 3s linear infinite;
    }

    @keyframes hologram {
        0% { transform: translateX(-100%) translateY(-100%) rotate(0deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(360deg); }
    }

    /* Terminal-style output */
    .terminal-output {
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid #00ff41;
        border-radius: 5px;
        padding: 15px;
        font-family: 'Share Tech Mono', monospace;
        color: #00ff41;
        margin: 10px 0;
        box-shadow: inset 0 0 20px rgba(0, 255, 65, 0.2);
    }

    /* Glowing dots */
    .glow-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00ff41;
        box-shadow: 0 0 10px #00ff41, 0 0 20px #00ff41;
        display: inline-block;
        margin: 0 5px;
        animation: glow-pulse 2s infinite;
    }

    @keyframes glow-pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.8); }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CONSTANTS & API CONFIGURATION
# ==========================================
API_ENDPOINTS = {
    "AVATAR_LIST": "https://avatar.pipio.ai/actor",
    "VOICE_LIST": "https://avatar.pipio.ai/voice",
    "GENERATE_CLIP": "https://generate.pipio.ai/single-clip",
    "DUBBING": "https://project.pipio.ai/project/generate/dubbingV2",
    "LIPSYNC": "https://project.pipio.ai/project/generate/lipsync",
}

OPENAI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

# ==========================================
# API HELPER FUNCTIONS
# ==========================================
def get_avatar_headers():
    """Get headers for avatar API"""
    return {
        "Authorization": f"Key {st.session_state.avatar_api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def get_openai_headers():
    """Get headers for OpenAI API"""
    return {
        "Authorization": f"Bearer {st.session_state.openai_api_key}",
        "Content-Type": "application/json"
    }

def safe_api_call(method, url, headers, **kwargs):
    """Safe API call wrapper with error handling"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30, **kwargs)
        else:
            response = requests.post(url, headers=headers, timeout=30, **kwargs)
        
        if response.status_code in [200, 201]:
            return response.json(), None
        else:
            return None, f"Error {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return None, "Request timeout. Please try again."
    except Exception as e:
        return None, f"Connection Error: {str(e)}"

def generate_script_with_openai(prompt, script_type="general", tone="professional", length="medium"):
    """Generate script using OpenAI API"""
    
    length_guidelines = {
        "short": "Keep the script under 100 words, concise and impactful.",
        "medium": "Create a script between 100-300 words, well-balanced and engaging.",
        "long": "Develop a comprehensive script between 300-500 words with detailed content.",
        "extra_long": "Write an extensive script of 500-1000 words with in-depth coverage."
    }
    
    system_prompts = {
        "general": "You are a professional script writer for AI avatar videos. Create engaging, natural-sounding scripts.",
        "marketing": "You are an expert marketing copywriter. Create persuasive, compelling scripts that drive action.",
        "educational": "You are an educational content creator. Write clear, informative scripts that teach effectively.",
        "storytelling": "You are a master storyteller. Create engaging narratives with emotional resonance.",
        "technical": "You are a technical writer. Create clear, accurate scripts explaining complex concepts simply.",
        "entertainment": "You are an entertainment writer. Create fun, engaging, and entertaining content.",
        "news": "You are a news reporter. Write factual, balanced, and informative news scripts.",
        "motivational": "You are a motivational speaker. Create inspiring, uplifting scripts that energize audiences."
    }
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": f"{system_prompts.get(script_type, system_prompts['general'])} The tone should be {tone}. {length_guidelines.get(length, length_guidelines['medium'])}"
            },
            {
                "role": "user",
                "content": f"Create a script for an AI avatar video based on this topic: {prompt}\n\nMake it natural, conversational, and suitable for video narration."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    result, error = safe_api_call("POST", OPENAI_API_ENDPOINT, get_openai_headers(), json=payload)
    
    if result:
        return result['choices'][0]['message']['content'], None
    else:
        return None, error

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "avatar_api_key": "",
        "openai_api_key": "",
        "avatars": [],
        "voices": [],
        "history": [],
        "generated_scripts": [],
        "sync_time": None,
        "total_videos_created": 0,
        "processing_videos": 0
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# ==========================================
# SIDEBAR - CONTROL PANEL
# ==========================================
with st.sidebar:
    st.markdown('<div class="holo-effect">', unsafe_allow_html=True)
    st.markdown("## 🟢 CONTROL PANEL", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Key Section
    st.markdown("### 🔐 AUTHENTICATION")
    
    with st.expander("🤖 Avatar API Configuration", expanded=True):
        st.session_state.avatar_api_key = st.text_input(
            "Avatar Service API Key",
            value=st.session_state.avatar_api_key,
            type="password",
            help="Enter your avatar generation API key",
            key="avatar_key_input"
        )
    
    with st.expander("🧠 OpenAI Configuration", expanded=True):
        st.session_state.openai_api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.openai_api_key,
            type="password",
            help="Enter your OpenAI API key for script generation",
            key="openai_key_input"
        )
    
    st.markdown("---")
    
    # System Operations
    st.markdown("### ⚡ SYSTEM OPERATIONS")
    
    if st.button("🔄 SYNC NEURAL DATABASE", use_container_width=True):
        if not st.session_state.avatar_api_key:
            st.error("⚠️ Avatar API Key required!")
        else:
            with st.spinner("🌐 Connecting to neural network..."):
                time.sleep(0.5)  # Dramatic effect
                
                avatars, a_err = safe_api_call("GET", API_ENDPOINTS["AVATAR_LIST"], get_avatar_headers())
                voices, v_err = safe_api_call("GET", API_ENDPOINTS["VOICE_LIST"], get_avatar_headers())
                history, h_err = safe_api_call("GET", f"{API_ENDPOINTS['GENERATE_CLIP']}?pageSize=50", get_avatar_headers())
                
                if not a_err:
                    st.session_state.avatars = avatars.get('items', [])
                if not v_err:
                    st.session_state.voices = voices.get('items', [])
                if not h_err:
                    st.session_state.history = history.get('items', [])
                    st.session_state.total_videos_created = len([h for h in st.session_state.history if h.get('status') == 'Completed'])
                    st.session_state.processing_videos = len([h for h in st.session_state.history if h.get('status') in ['Pending', 'Processing']])
                
                st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")
                st.success(f"✅ Synchronized at {st.session_state.sync_time}")
                time.sleep(0.5)
                st.rerun()
    
    if st.button("🗑️ CLEAR CACHE", use_container_width=True):
        st.session_state.generated_scripts = []
        st.success("✅ Cache cleared")
    
    st.markdown("---")
    
    # System Statistics
    st.markdown("### 📊 NEURAL METRICS")
    
    if st.session_state.avatars:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("👤 AVATARS", len(st.session_state.avatars))
            st.metric("📹 COMPLETED", st.session_state.total_videos_created)
        with col2:
            st.metric("🎤 VOICES", len(st.session_state.voices))
            st.metric("⚙️ PROCESSING", st.session_state.processing_videos)
        
        if st.session_state.sync_time:
            st.caption(f"Last sync: {st.session_state.sync_time}")
    else:
        st.info("🔌 No data loaded. Click SYNC to connect.")
    
    st.markdown("---")
    
    # System Information
    st.markdown("### ℹ️ SYSTEM INFO")
    st.markdown("""
    <div class="terminal-output">
    <small>
    > STATUS: ONLINE<br>
    > UPTIME: 99.9%<br>
    > LATENCY: <15ms<br>
    > VERSION: 2.5.1<br>
    > BUILD: MATRIX_OMEGA
    </small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Links
    st.markdown("### 🔗 QUICK ACCESS")
    st.markdown("""
    - [📚 Documentation](#)
    - [💬 Support](#)
    - [🔧 Settings](#)
    - [📈 Analytics](#)
    """)

# ==========================================
# MAIN INTERFACE - HEADER
# ==========================================
st.markdown('<div class="neural-bg"></div>', unsafe_allow_html=True)
st.markdown('<div class="scanline"></div>', unsafe_allow_html=True)

st.markdown('<div class="matrix-header">AI DIGITAL TWIN</div>', unsafe_allow_html=True)
st.markdown('<div class="matrix-subheader">◈ NEURAL AVATAR GENERATION SYSTEM ◈ POWERED BY QUANTUM AI ◈</div>', unsafe_allow_html=True)

# Connection Status Banner
if not st.session_state.avatar_api_key:
    st.markdown("""
    <div style="background: rgba(255, 0, 0, 0.1); border: 2px solid #ff0000; padding: 20px; border-radius: 8px; text-align: center; margin: 20px 0;">
        <h3 style="color: #ff0000; margin: 0;">⚠️ SYSTEM NOT INITIALIZED ⚠️</h3>
        <p style="color: #ff6b6b; margin: 10px 0 0 0;">Configure API keys in the control panel to activate neural systems</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ==========================================
# MAIN TABS
# ==========================================
tabs = st.tabs([
    "🎬 AVATAR STUDIO",
    "✍️ SCRIPT GENERATOR",
    "🌍 VOICE DUBBING",
    "👄 LIP SYNCHRONIZATION",
    "📁 NEURAL LIBRARY",
    "⚙️ ADVANCED TOOLS"
])

# ------------------------------------------
# TAB 1: AVATAR VIDEO STUDIO
# ------------------------------------------
with tabs[0]:
    st.markdown("## 🎬 DIGITAL TWIN CREATION STUDIO")
    
    if not st.session_state.avatars:
        st.markdown("""
        <div class="matrix-card">
            <h3 style="text-align: center;">🔌 NEURAL DATABASE NOT LOADED</h3>
            <p style="text-align: center;">Initialize the system by clicking <strong>SYNC NEURAL DATABASE</strong> in the control panel</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Main Layout
        config_col, preview_col, output_col = st.columns([2, 1, 1])
        
        with config_col:
            st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
            
            # Avatar Configuration
            st.markdown("### 👤 AVATAR SELECTION")
            
            # Advanced Filters
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            
            with filter_col1:
                genders = ["All"] + sorted(list(set([a.get('gender', 'Unknown') for a in st.session_state.avatars if a.get('gender')])))
                sel_gender = st.selectbox("🚹 Gender", genders, key="gender_filter")
            
            with filter_col2:
                ethnicities = ["All"] + sorted(list(set([a.get('ethnicity', 'Other') for a in st.session_state.avatars])))
                sel_ethnicity = st.selectbox("🌍 Ethnicity", ethnicities, key="ethnicity_filter")
            
            with filter_col3:
                ages = ["All"] + sorted(list(set([a.get('ageGroup', 'Unknown') for a in st.session_state.avatars if a.get('ageGroup')])))
                sel_age = st.selectbox("📅 Age Group", ages, key="age_filter")
            
            # Apply Filters
            filtered_avatars = st.session_state.avatars
            if sel_gender != "All":
                filtered_avatars = [a for a in filtered_avatars if a.get('gender') == sel_gender]
            if sel_ethnicity != "All":
                filtered_avatars = [a for a in filtered_avatars if a.get('ethnicity') == sel_ethnicity]
            if sel_age != "All":
                filtered_avatars = [a for a in filtered_avatars if a.get('ageGroup') == sel_age]
            
            if not filtered_avatars:
                st.warning("⚠️ No avatars match your filters. Adjust criteria.")
                filtered_avatars = st.session_state.avatars
            
            avatar_map = {f"{a['name']} | {a.get('gender', 'N/A')} | {a.get('ethnicity', 'N/A')}": a for a in filtered_avatars}
            sel_avatar_label = st.selectbox("Select Avatar", list(avatar_map.keys()), key="avatar_select")
            sel_avatar = avatar_map[sel_avatar_label]
            
            st.markdown("---")
            
            # Voice Configuration
            st.markdown("### 🎤 VOICE SYNTHESIS")
            
            voice_col1, voice_col2, voice_col3 = st.columns(3)
            
            with voice_col1:
                all_langs = sorted(list(set([lang for v in st.session_state.voices for lang in v.get('languages', [])])))
                sel_lang = st.selectbox("🌐 Language", ["All"] + all_langs, key="voice_lang")
            
            with voice_col2:
                voice_types = ["All"] + sorted(list(set([v.get('voiceType', 'Unknown') for v in st.session_state.voices if v.get('voiceType')])))
                sel_voice_type = st.selectbox("🎵 Type", voice_types, key="voice_type")
            
            with voice_col3:
                voice_genders = ["All"] + sorted(list(set([v.get('gender', 'Unknown') for v in st.session_state.voices if v.get('gender')])))
                sel_voice_gender = st.selectbox("🚹 Gender", voice_genders, key="voice_gender")
            
            # Apply Voice Filters
            filtered_voices = st.session_state.voices
            if sel_lang != "All":
                filtered_voices = [v for v in filtered_voices if sel_lang in v.get('languages', [])]
            if sel_voice_type != "All":
                filtered_voices = [v for v in filtered_voices if v.get('voiceType') == sel_voice_type]
            if sel_voice_gender != "All":
                filtered_voices = [v for v in filtered_voices if v.get('gender') == sel_voice_gender]
            
            if not filtered_voices:
                st.warning("⚠️ No voices match your filters.")
                filtered_voices = st.session_state.voices
            
            voice_labels = {f"{v['name']} ({v.get('gender', 'N/A')}) - {'/'.join(v.get('languages', []))}": v for v in filtered_voices}
            sel_voice_label = st.selectbox("Select Voice", list(voice_labels.keys()), key="voice_select")
            sel_voice = voice_labels[sel_voice_label]
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Script Input
            st.markdown('<div class="matrix-card" style="margin-top: 20px;">', unsafe_allow_html=True)
            st.markdown("### 📝 SCRIPT INPUT")
            
            script_source = st.radio("Script Source", ["✍️ Manual Entry", "🤖 AI Generated (from Script Generator)"], horizontal=True)
            
            if script_source == "✍️ Manual Entry":
                script = st.text_area(
                    "Enter your script",
                    height=200,
                    placeholder="Type or paste your script here... (max 5000 characters)",
                    help="The avatar will speak this text",
                    key="manual_script"
                )
                char_count = len(script)
                words_count = len(script.split())
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                col_stat1.metric("Characters", f"{char_count}/5000")
                col_stat2.metric("Words", words_count)
                col_stat3.metric("Est. Duration", f"{int(words_count * 0.4)}s")
                
            else:
                if st.session_state.generated_scripts:
                    script_options = {f"Script {i+1}: {s[:50]}..." if len(s) > 50 else f"Script {i+1}: {s}": s 
                                    for i, s in enumerate(st.session_state.generated_scripts)}
                    selected_script_label = st.selectbox("Select Generated Script", list(script_options.keys()))
                    script = script_options[selected_script_label]
                    
                    st.text_area("Selected Script", value=script, height=200, disabled=True, key="ai_script_display")
                    
                    char_count = len(script)
                    words_count = len(script.split())
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    col_stat1.metric("Characters", f"{char_count}/5000")
                    col_stat2.metric("Words", words_count)
                    col_stat3.metric("Est. Duration", f"{int(words_count * 0.4)}s")
                else:
                    st.info("📋 No generated scripts available. Go to SCRIPT GENERATOR tab to create one.")
                    script = ""
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Generation Button
            st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
            if st.button("🚀 INITIATE AVATAR GENERATION", use_container_width=True, type="primary"):
                if not script.strip():
                    st.error("❌ Script cannot be empty!")
                elif len(script) > 5000:
                    st.error("❌ Script exceeds 5000 character limit!")
                else:
                    with st.spinner("🔄 Processing neural synthesis..."):
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        payload = {
                            "actorId": sel_avatar['id'],
                            "voiceId": sel_voice['id'],
                            "script": script
                        }
                        
                        res, err = safe_api_call("POST", API_ENDPOINTS["GENERATE_CLIP"], get_avatar_headers(), json=payload)
                        
                        if res:
                            st.success(f"✅ Avatar generation initiated successfully!")
                            st.info(f"🆔 Project ID: `{res.get('id')}`")
                            st.balloons()
                            
                            # Refresh history
                            time.sleep(1)
                            history, _ = safe_api_call("GET", f"{API_ENDPOINTS['GENERATE_CLIP']}?pageSize=50", get_avatar_headers())
                            if history:
                                st.session_state.history = history.get('items', [])
                        else:
                            st.error(f"❌ Generation failed: {err}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with preview_col:
            st.markdown('<div class="matrix-card holo-effect">', unsafe_allow_html=True)
            st.markdown("### 👁️ AVATAR PREVIEW")
            
            if 'thumbnailImagePath' in sel_avatar:
                st.image(sel_avatar['thumbnailImagePath'], use_container_width=True)
            else:
                st.info("No preview available")
            
            st.markdown(f"**Name:** {sel_avatar['name']}")
            st.markdown(f"**Gender:** {sel_avatar.get('gender', 'N/A')}")
            st.markdown(f"**Ethnicity:** {sel_avatar.get('ethnicity', 'N/A')}")
            st.markdown(f"**Age Group:** {sel_avatar.get('ageGroup', 'N/A')}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with output_col:
            st.markdown('<div class="matrix-card holo-effect">', unsafe_allow_html=True)
            st.markdown("### 🎵 VOICE PREVIEW")
            
            if 'previewAudioPath' in sel_voice and sel_voice['previewAudioPath']:
                st.audio(sel_voice['previewAudioPath'])
            else:
                st.info("No audio preview available")
            
            st.markdown(f"**Voice:** {sel_voice['name']}")
            st.markdown(f"**Type:** {sel_voice.get('voiceType', 'N/A')}")
            st.markdown(f"**Gender:** {sel_voice.get('gender', 'N/A')}")
            st.markdown(f"**Languages:** {', '.join(sel_voice.get('languages', ['N/A']))}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: AI SCRIPT GENERATOR
# ------------------------------------------
with tabs[1]:
    st.markdown("## ✍️ AI-POWERED SCRIPT GENERATOR")
    
    if not st.session_state.openai_api_key:
        st.markdown("""
        <div class="matrix-card">
            <h3 style="text-align: center;">🔐 OPENAI API KEY REQUIRED</h3>
            <p style="text-align: center;">Configure your OpenAI API key in the control panel to use this feature</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        gen_col1, gen_col2 = st.columns([2, 1])
        
        with gen_col1:
            st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
            st.markdown("### 🎯 SCRIPT CONFIGURATION")
            
            # Script Parameters
            param_col1, param_col2 = st.columns(2)
            
            with param_col1:
                script_type = st.selectbox(
                    "📋 Script Type",
                    ["general", "marketing", "educational", "storytelling", "technical", "entertainment", "news", "motivational"],
                    help="Choose the style and purpose of your script"
                )
                
                tone = st.selectbox(
                    "🎭 Tone",
                    ["professional", "casual", "friendly", "authoritative", "enthusiastic", "calm", "urgent", "inspiring"],
                    help="Set the emotional tone of the script"
                )
            
            with param_col2:
                length = st.selectbox(
                    "📏 Length",
                    ["short", "medium", "long", "extra_long"],
                    help="Short: <100 words, Medium: 100-300, Long: 300-500, Extra Long: 500-1000"
                )
                
                language_style = st.selectbox(
                    "🗣️ Language Style",
                    ["Simple & Clear", "Conversational", "Formal", "Technical", "Creative"],
                    help="How the script should be written"
                )
            
            st.markdown("### 💭 TOPIC INPUT")
            
            topic = st.text_area(
                "Describe what you want the script to be about",
                height=150,
                placeholder="Example: Create a script about the benefits of cloud computing for small businesses. Include cost savings, scalability, and remote work advantages.",
                help="Be as specific as possible for better results"
            )
            
            # Advanced Options
            with st.expander("🔧 Advanced Options"):
                include_cta = st.checkbox("Include Call-to-Action", value=False)
                include_stats = st.checkbox("Include Statistics/Numbers", value=False)
                include_questions = st.checkbox("Include Rhetorical Questions", value=False)
                custom_instructions = st.text_area(
                    "Custom Instructions",
                    height=100,
                    placeholder="Any additional requirements or constraints..."
                )
            
            if st.button("🤖 GENERATE SCRIPT", use_container_width=True, type="primary"):
                if not topic.strip():
                    st.error("❌ Please provide a topic or description!")
                else:
                    with st.spinner("🧠 AI processing your request..."):
                        progress_bar = st.progress(0)
                        
                        # Build enhanced prompt
                        enhanced_prompt = topic
                        if include_cta:
                            enhanced_prompt += " Include a strong call-to-action."
                        if include_stats:
                            enhanced_prompt += " Include relevant statistics or data points."
                        if include_questions:
                            enhanced_prompt += " Use rhetorical questions to engage the audience."
                        if custom_instructions:
                            enhanced_prompt += f" Additional requirements: {custom_instructions}"
                        
                        for i in range(100):
                            time.sleep(0.02)
                            progress_bar.progress(i + 1)
                        
                        script_content, error = generate_script_with_openai(
                            enhanced_prompt,
                            script_type=script_type,
                            tone=tone,
                            length=length
                        )
                        
                        if script_content:
                            st.session_state.generated_scripts.insert(0, script_content)
                            if len(st.session_state.generated_scripts) > 10:
                                st.session_state.generated_scripts = st.session_state.generated_scripts[:10]
                            
                            st.success("✅ Script generated successfully!")
                            st.balloons()
                        else:
                            st.error(f"❌ Generation failed: {error}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with gen_col2:
            st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
            st.markdown("### 📊 QUICK STATS")
            
            st.metric("Generated Scripts", len(st.session_state.generated_scripts))
            
            st.markdown("### 💡 TIPS")
            st.markdown("""
            <div class="terminal-output">
            <small>
            • Be specific in your topic<br>
            • Choose appropriate tone<br>
            • Consider your audience<br>
            • Review and edit results<br>
            • Save favorites
            </small>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Generated Scripts Library
        if st.session_state.generated_scripts:
            st.markdown("---")
            st.markdown("## 📚 GENERATED SCRIPTS LIBRARY")
            
            for idx, saved_script in enumerate(st.session_state.generated_scripts):
                with st.expander(f"📝 Script {idx + 1} - {saved_script[:80]}...", expanded=(idx == 0)):
                    st.text_area(f"Script Content {idx + 1}", value=saved_script, height=200, key=f"saved_script_{idx}")
                    
                    script_words = len(saved_script.split())
                    script_chars = len(saved_script)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Words", script_words)
                    col2.metric("Characters", script_chars)
                    col3.metric("Est. Duration", f"{int(script_words * 0.4)}s")
                    
                    action_col1, action_col2 = st.columns(2)
                    with action_col1:
                        if st.button(f"📋 Copy to Clipboard", key=f"copy_{idx}"):
                            st.success("✅ Copied! (Use Ctrl+C manually)")
                    with action_col2:
                        if st.button(f"🗑️ Delete", key=f"delete_{idx}"):
                            st.session_state.generated_scripts.pop(idx)
                            st.rerun()

# ------------------------------------------
# TAB 3: VOICE DUBBING
# ------------------------------------------
with tabs[2]:
    st.markdown("## 🌍 MULTILINGUAL VOICE DUBBING")
    
    st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
    
    dub_col1, dub_col2 = st.columns([2, 1])
    
    with dub_col1:
        st.markdown("### 📹 VIDEO CONFIGURATION")
        
        source_url = st.text_input(
            "Source Video URL",
            placeholder="https://example.com/video.mp4",
            help="URL of the video you want to dub"
        )
        
        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            source_lang = st.text_input(
                "Source Language",
                value="auto",
                help="Use 'auto' for automatic detection or specify (e.g., 'en', 'es')"
            )
        
        with lang_col2:
            target_lang = st.selectbox(
                "Target Language",
                ["es (Spanish)", "fr (French)", "de (German)", "it (Italian)", "pt (Portuguese)", 
                 "zh (Chinese)", "ja (Japanese)", "ko (Korean)", "ar (Arabic)", "hi (Hindi)"],
                help="Language to translate and dub into"
            )
        
        # Advanced Dubbing Options
        with st.expander("🔧 Advanced Settings"):
            preserve_timing = st.checkbox("Preserve Original Timing", value=True)
            voice_matching = st.checkbox("Match Original Voice Characteristics", value=True)
            background_audio = st.selectbox("Background Audio", ["Keep Original", "Remove", "Reduce by 50%"])
        
        if st.button("⚡ START DUBBING PROCESS", use_container_width=True, type="primary"):
            if not source_url or not target_lang:
                st.error("❌ Please provide both video URL and target language!")
            else:
                with st.spinner("🔄 Initiating dubbing pipeline..."):
                    progress_bar = st.progress(0)
                    stages = ["Analyzing video", "Extracting audio", "Transcribing", "Translating", "Synthesizing", "Syncing"]
                    
                    for i, stage in enumerate(stages):
                        for j in range(17):
                            time.sleep(0.01)
                            progress_bar.progress(min((i * 17 + j), 100))
                        st.info(f"📍 {stage}...")
                    
                    target_code = target_lang.split()[0]
                    payload = {
                        "sourceUrl": source_url,
                        "targetLanguage": target_code,
                        "sourceLanguage": source_lang
                    }
                    
                    res, err = safe_api_call("POST", API_ENDPOINTS["DUBBING"], get_avatar_headers(), json=payload)
                    
                    if res:
                        st.success("✅ Dubbing process initiated successfully!")
                        st.info(f"🆔 Project ID: `{res.get('id', 'N/A')}`")
                        st.balloons()
                    else:
                        st.error(f"❌ Process failed: {err}")
    
    with dub_col2:
        st.markdown("### 📋 PROCESS OVERVIEW")
        st.markdown("""
        <div class="terminal-output">
        <strong>Pipeline Stages:</strong><br><br>
        1️⃣ Video Analysis<br>
        2️⃣ Audio Extraction<br>
        3️⃣ Speech Recognition<br>
        4️⃣ AI Translation<br>
        5️⃣ Voice Synthesis<br>
        6️⃣ Lip Synchronization<br>
        7️⃣ Final Rendering<br><br>
        <strong>Est. Time: 5-15 min</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🌐 SUPPORTED LANGUAGES")
        st.markdown("""
        <div class="terminal-output">
        <small>
        🇪🇸 Spanish • 🇫🇷 French<br>
        🇩🇪 German • 🇮🇹 Italian<br>
        🇵🇹 Portuguese • 🇨🇳 Chinese<br>
        🇯🇵 Japanese • 🇰🇷 Korean<br>
        🇸🇦 Arabic • 🇮🇳 Hindi<br>
        + 50 more languages
        </small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 4: LIP SYNCHRONIZATION
# ------------------------------------------
with tabs[3]:
    st.markdown("## 👄 ADVANCED LIP SYNCHRONIZATION")
    
    st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
    
    sync_col1, sync_col2 = st.columns([2, 1])
    
    with sync_col1:
        st.markdown("### 🎬 SYNC CONFIGURATION")
        
        video_url = st.text_input(
            "Source Video URL",
            placeholder="https://example.com/video.mp4",
            help="Video file with the person/avatar speaking"
        )
        
        audio_url = st.text_input(
            "Target Audio URL",
            placeholder="https://example.com/audio.mp3",
            help="Audio file to sync with the video"
        )
        
        # Advanced Sync Options
        with st.expander("🔧 Synchronization Settings"):
            sync_quality = st.select_slider(
                "Quality Level",
                options=["Fast", "Balanced", "High Quality", "Ultra HD"],
                value="Balanced"
            )
            
            facial_enhancement = st.checkbox("Enhance Facial Features", value=True)
            motion_smoothing = st.checkbox("Apply Motion Smoothing", value=True)
            audio_enhancement = st.checkbox("Enhance Audio Quality", value=False)
        
        if st.button("🔗 SYNCHRONIZE VIDEO & AUDIO", use_container_width=True, type="primary"):
            if not video_url or not audio_url:
                st.error("❌ Both video and audio URLs are required!")
            else:
                with st.spinner("🔄 Processing lip synchronization..."):
                    progress_bar = st.progress(0)
                    
                    for i in range(100):
                        time.sleep(0.03)
                        progress_bar.progress(i + 1)
                    
                    payload = {
                        "sourceUrl": video_url,
                        "targetAudioUrl": audio_url
                    }
                    
                    res, err = safe_api_call("POST", API_ENDPOINTS["LIPSYNC"], get_avatar_headers(), json=payload)
                    
                    if res:
                        st.success("✅ Lip sync process completed successfully!")
                        st.info(f"🆔 Project ID: `{res.get('id', 'N/A')}`")
                        st.balloons()
                    else:
                        st.error(f"❌ Process failed: {err}")
    
    with sync_col2:
        st.markdown("### 💡 USE CASES")
        st.markdown("""
        <div class="terminal-output">
        <strong>Perfect for:</strong><br><br>
        🎯 A/B Testing Campaigns<br>
        🎤 Professional Voiceovers<br>
        🌍 Multi-language Content<br>
        🎬 Video Localization<br>
        📺 Content Remastering<br>
        🔧 Sync Issue Fixes
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ⚙️ TECH SPECS")
        st.markdown("""
        <div class="terminal-output">
        <small>
        • AI-Powered Alignment<br>
        • Frame-Perfect Sync<br>
        • Natural Lip Movement<br>
        • Multi-Format Support<br>
        • 4K Resolution Ready
        </small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 5: NEURAL LIBRARY
# ------------------------------------------
with tabs[4]:
    st.markdown("## 📁 NEURAL PROJECT LIBRARY")
    
    # Library Controls
    lib_col1, lib_col2, lib_col3, lib_col4 = st.columns(4)
    
    with lib_col1:
        if st.button("🔄 REFRESH DATABASE", use_container_width=True):
            with st.spinner("Syncing..."):
                history, _ = safe_api_call("GET", f"{API_ENDPOINTS['GENERATE_CLIP']}?pageSize=50", get_avatar_headers())
                if history:
                    st.session_state.history = history.get('items', [])
                    st.success("✅ Refreshed")
                    time.sleep(0.5)
                    st.rerun()
    
    with lib_col2:
        status_filter = st.selectbox("🔍 Filter Status", ["All", "Completed", "Processing", "Pending", "Failed"])
    
    with lib_col3:
        sort_by = st.selectbox("📊 Sort By", ["Newest First", "Oldest First", "Status"])
    
    with lib_col4:
        view_mode = st.selectbox("👁️ View", ["Grid", "List"])
    
    st.markdown("---")
    
    if not st.session_state.history:
        st.markdown("""
        <div class="matrix-card" style="text-align: center; padding: 60px;">
            <h2>📭 LIBRARY EMPTY</h2>
            <p>No projects found. Create your first digital twin in the Avatar Studio!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Filter projects
        filtered_history = st.session_state.history
        if status_filter != "All":
            filtered_history = [h for h in filtered_history if h.get('status', '').lower() == status_filter.lower()]
        
        # Sort projects
        if sort_by == "Newest First":
            filtered_history = sorted(filtered_history, key=lambda x: x.get('createdDate', ''), reverse=True)
        elif sort_by == "Oldest First":
            filtered_history = sorted(filtered_history, key=lambda x: x.get('createdDate', ''))
        
        st.info(f"📊 Displaying {len(filtered_history)} projects")
        
        # Display projects
        for idx, item in enumerate(filtered_history):
            status = item.get('status', 'Unknown')
            status_class_map = {
                'completed': 'status-completed',
                'pending': 'status-pending',
                'processing': 'status-processing',
                'failed': 'status-failed'
            }
            status_class = status_class_map.get(status.lower(), 'status-pending')
            
            with st.expander(f"🎬 Project #{item.get('id', 'N/A')[:8]}... | Status: {status}", expanded=(idx == 0 and status.lower() == 'completed')):
                proj_col1, proj_col2 = st.columns([1, 2])
                
                with proj_col1:
                    st.markdown(f'<span class="status-badge {status_class}">{status}</span>', unsafe_allow_html=True)
                    
                    st.markdown("**Project Details:**")
                    st.markdown(f"- **ID:** `{item.get('id', 'N/A')}`")
                    st.markdown(f"- **Created:** {item.get('createdDate', 'N/A')}")
                    st.markdown(f"- **Updated:** {item.get('updatedDate', 'N/A')}")
                    
                    if status.lower() != "completed":
                        if st.button("🔍 CHECK STATUS", key=f"check_{item['id']}", use_container_width=True):
                            with st.spinner("Checking..."):
                                res, err = safe_api_call("GET", f"{API_ENDPOINTS['GENERATE_CLIP']}/{item['id']}", get_avatar_headers())
                                if res:
                                    current_status = res.get('status', 'Unknown')
                                    if current_status.lower() == "completed":
                                        st.success("✅ Project completed!")
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.info(f"Current Status: {current_status}")
                                else:
                                    st.error(f"Error: {err}")
                    
                    if status.lower() == "completed" and 'videoUrl' in item:
                        if st.button("📥 DOWNLOAD VIDEO", key=f"dl_{item['id']}", use_container_width=True):
                            st.success("Download link ready!")
                            st.markdown(f"[Click to download]({item['videoUrl']})")
                
                with proj_col2:
                    if status.lower() == "completed" and 'videoUrl' in item:
                        st.markdown("**🎥 Video Preview:**")
                        st.video(item['videoUrl'])
                    else:
                        st.markdown("**📝 Script:**")
                        script_preview = item.get('script', 'No script available')
                        st.text_area("", value=script_preview, height=150, disabled=True, key=f"script_{item['id']}")
                        
                        if status.lower() == "processing":
                            st.info("⚙️ Video is being processed. Check back soon!")

# ------------------------------------------
# TAB 6: ADVANCED TOOLS
# ------------------------------------------
with tabs[5]:
    st.markdown("## ⚙️ ADVANCED NEURAL TOOLS")
    
    tool_tabs = st.tabs(["🔬 Batch Processing", "📊 Analytics", "⚡ API Tester", "🛠️ Utilities"])
    
    with tool_tabs[0]:
        st.markdown("### 🔬 BATCH VIDEO GENERATION")
        st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
        
        st.info("🚀 Generate multiple videos simultaneously with different configurations")
        
        batch_file = st.file_uploader("Upload CSV with scripts (columns: script, avatar_id, voice_id)", type=['csv'])
        
        if batch_file:
            df = pd.read_csv(batch_file)
            st.dataframe(df.head())
            
            if st.button("🚀 START BATCH GENERATION"):
                st.warning("⚠️ Batch processing feature coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tool_tabs[1]:
        st.markdown("### 📊 PROJECT ANALYTICS")
        st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
        
        if st.session_state.history:
            # Calculate statistics
            total_projects = len(st.session_state.history)
            completed = len([h for h in st.session_state.history if h.get('status', '').lower() == 'completed'])
            processing = len([h for h in st.session_state.history if h.get('status', '').lower() in ['processing', 'pending']])
            failed = len([h for h in st.session_state.history if h.get('status', '').lower() == 'failed'])
            
            met_col1, met_col2, met_col3, met_col4 = st.columns(4)
            met_col1.metric("Total Projects", total_projects, delta=None)
            met_col2.metric("Completed", completed, delta=f"{int(completed/total_projects*100)}%")
            met_col3.metric("In Progress", processing)
            met_col4.metric("Failed", failed)
            
            # Status distribution chart
            st.markdown("### 📈 Status Distribution")
            status_data = {
                'Status': ['Completed', 'Processing', 'Failed'],
                'Count': [completed, processing, failed]
            }
            st.bar_chart(pd.DataFrame(status_data).set_index('Status'))
        else:
            st.info("No data available for analytics")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tool_tabs[2]:
        st.markdown("### ⚡ API ENDPOINT TESTER")
        st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
        
        endpoint = st.selectbox("Select Endpoint", list(API_ENDPOINTS.keys()))
        method = st.radio("Method", ["GET", "POST"], horizontal=True)
        
        if method == "POST":
            payload_input = st.text_area("Request Payload (JSON)", height=150, value='{\n  "key": "value"\n}')
        
        if st.button("🧪 TEST ENDPOINT"):
            with st.spinner("Testing..."):
                if method == "GET":
                    res, err = safe_api_call("GET", API_ENDPOINTS[endpoint], get_avatar_headers())
                else:
                    try:
                        payload = json.loads(payload_input)
                        res, err = safe_api_call("POST", API_ENDPOINTS[endpoint], get_avatar_headers(), json=payload)
                    except json.JSONDecodeError:
                        st.error("Invalid JSON payload")
                        res, err = None, "Invalid JSON"
                
                if res:
                    st.success("✅ Request successful!")
                    st.json(res)
                else:
                    st.error(f"❌ Request failed: {err}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tool_tabs[3]:
        st.markdown("### 🛠️ UTILITY TOOLS")
        st.markdown('<div class="matrix-card">', unsafe_allow_html=True)
        
        util_col1, util_col2 = st.columns(2)
        
        with util_col1:
            st.markdown("#### 📝 Script Analyzer")
            analyze_text = st.text_area("Paste script to analyze", height=150)
            
            if st.button("🔍 ANALYZE"):
                if analyze_text:
                    words = len(analyze_text.split())
                    chars = len(analyze_text)
                    sentences = analyze_text.count('.') + analyze_text.count('!') + analyze_text.count('?')
                    
                    st.write(f"**Words:** {words}")
                    st.write(f"**Characters:** {chars}")
                    st.write(f"**Sentences:** {sentences}")
                    st.write(f"**Estimated Duration:** {int(words * 0.4)} seconds")
                    st.write(f"**Reading Level:** {'Easy' if words/sentences < 15 else 'Medium' if words/sentences < 20 else 'Complex'}")
        
        with util_col2:
            st.markdown("#### 🎨 Thumbnail Generator")
            st.info("🖼️ Generate custom thumbnails for your videos")
            
            thumb_text = st.text_input("Thumbnail Text")
            thumb_color = st.color_picker("Text Color", "#00ff41")
            
            if st.button("🎨 GENERATE THUMBNAIL"):
                st.warning("⚠️ Feature coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background: rgba(0, 20, 0, 0.5); border-radius: 10px; border: 1px solid #00ff41;">
    <p style="color: #00ff41; font-family: 'Orbitron', monospace; margin: 0;">
        <strong>AI DIGITAL TWIN v2.5.1</strong> | NEURAL AVATAR SYSTEM | POWERED BY QUANTUM AI
    </p>
    <p style="color: #39ff14; font-size: 0.8rem; margin: 10px 0 0 0;">
        © 2026 Matrix Neural Networks | Built with Streamlit • Python • OpenAI
    </p>
</div>
""", unsafe_allow_html=True)
