import streamlit as st
import requests
import time
import json
import pandas as pd
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION & THEMING
# ==========================================
st.set_page_config(
    page_title="Pipio AI Studio Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f0f2f6;
    }

    /* Card styling */
    .st-emotion-cache-1r6slb0 {
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }

    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E1E1E;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }

    /* Badge styling */
    .badge {
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .badge-pending { background-color: #FFF3CD; color: #856404; }
    .badge-completed { background-color: #D4EDDA; color: #155724; }
    .badge-failed { background-color: #F8D7DA; color: #721C24; }

    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Custom Sidebar */
    .sidebar-content {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# CONSTANTS & API HELPERS
# ==========================================
API_ENDPOINTS = {
    "AVATAR_LIST": "https://avatar.pipio.ai/actor",
    "VOICE_LIST": "https://avatar.pipio.ai/voice",
    "GENERATE_CLIP": "https://generate.pipio.ai/single-clip",
    "DUBBING": "https://project.pipio.ai/project/generate/dubbingV2",
    "LIPSYNC": "https://project.pipio.ai/project/generate/lipsync",
    "TEMPLATE": "https://project.pipio.ai/project/{project_id}/template"
}

def get_headers():
    return {
        "Authorization": f"Key {st.session_state.api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def safe_api_call(method, url, **kwargs):
    try:
        if method == "GET":
            response = requests.get(url, headers=get_headers(), **kwargs)
        else:
            response = requests.post(url, headers=get_headers(), **kwargs)
        
        if response.status_code in [200, 201]:
            return response.json(), None
        else:
            return None, f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"Connection Error: {str(e)}"

# ==========================================
# SESSION STATE MANAGEMENT
# ==========================================
def init_session_state():
    defaults = {
        "api_key": "",
        "avatars": [],
        "voices": [],
        "history": [],
        "active_tab": "Avatar Video",
        "sync_time": None
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# ==========================================
# SIDEBAR COMPONENTS
# ==========================================
with st.sidebar:
    st.image("https://pipio.ai/wp-content/uploads/2022/10/Pipio-Logo-1.png", width=120)
    st.markdown("### 🔑 Authentication")
    st.session_state.api_key = st.text_input("API Key", value=st.session_state.api_key, type="password", help="Get your key from Pipio Dashboard")
    
    if st.button("🔄 Sync Global Data", use_container_width=True):
        if not st.session_state.api_key:
            st.error("Please enter an API Key first!")
        else:
            with st.spinner("Fetching assets..."):
                avatars, a_err = safe_api_call("GET", API_ENDPOINTS["AVATAR_LIST"])
                voices, v_err = safe_api_call("GET", API_ENDPOINTS["VOICE_LIST"])
                history, h_err = safe_api_call("GET", f"{API_ENDPOINTS['GENERATE_CLIP']}?pageSize=20")
                
                if not a_err: st.session_state.avatars = avatars.get('items', [])
                if not v_err: st.session_state.voices = voices.get('items', [])
                if not h_err: st.session_state.history = history.get('items', [])
                
                st.session_state.sync_time = datetime.now().strftime("%H:%M:%S")
                st.success(f"Synced at {st.session_state.sync_time}")

    st.markdown("---")
    st.markdown("### 📊 Statistics")
    if st.session_state.avatars:
        st.write(f"🎭 Avatars: **{len(st.session_state.avatars)}**")
        st.write(f"🗣️ Voices: **{len(st.session_state.voices)}**")
    
    st.markdown("---")
    st.markdown("### 🛠️ Resources")
    st.markdown("[API Documentation](https://docs.pipio.ai/)")
    st.markdown("[Pipio Dashboard](https://app.pipio.ai/)")

# ==========================================
# MAIN CONTENT AREA
# ==========================================
st.markdown('<div class="main-header">Pipio AI Studio Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Create, Dub, and Sync high-quality AI avatar videos in seconds.</div>', unsafe_allow_html=True)

if not st.session_state.api_key:
    st.warning("👋 Welcome! Please enter your API Key in the sidebar to unlock the studio features.")
    st.stop()

tabs = st.tabs(["🎭 Avatar Video", "🌍 Dubbing", "👄 Lip Sync", "📁 Library"])

# ------------------------------------------
# TAB 1: AVATAR VIDEO GENERATION
# ------------------------------------------
with tabs[0]:
    if not st.session_state.avatars:
        st.info("💡 Tip: Click 'Sync Global Data' in the sidebar to load available avatars and voices.")
    else:
        col_setup, col_prev = st.columns([3, 2])
        
        with col_setup:
            st.subheader("1. Configure Actor")
            
            # Avatar Selection with Filters
            a_col1, a_col2 = st.columns(2)
            ethnicities = ["All"] + sorted(list(set([a.get('ethnicity', 'Other') for a in st.session_state.avatars])))
            sel_eth = a_col1.selectbox("Filter Ethnicity", ethnicities)
            
            filtered_avatars = st.session_state.avatars
            if sel_eth != "All":
                filtered_avatars = [a for a in st.session_state.avatars if a.get('ethnicity') == sel_eth]
            
            avatar_map = {a['name']: a for a in filtered_avatars}
            sel_avatar_name = st.selectbox("Select Avatar", list(avatar_map.keys()))
            sel_avatar = avatar_map[sel_avatar_name]
            
            # Voice Selection with Language Filter
            st.subheader("2. Configure Voice")
            v_col1, v_col2 = st.columns(2)
            all_langs = sorted(list(set([lang for v in st.session_state.voices for lang in v.get('languages', [])])))
            sel_lang = v_col1.selectbox("Filter Language", ["All"] + all_langs)
            
            filtered_voices = st.session_state.voices
            if sel_lang != "All":
                filtered_voices = [v for v in st.session_state.voices if sel_lang in v.get('languages', [])]
            
            voice_labels = {f"{v['name']} ({'/'.join(v.get('languages', []))})": v for v in filtered_voices}
            sel_voice_label = st.selectbox("Select Voice", list(voice_labels.keys()))
            sel_voice = voice_labels[sel_voice_label]
            
            st.subheader("3. Script")
            script = st.text_area("What should the avatar say?", height=250, placeholder="Enter your script here (max 5000 characters)...")
            st.caption(f"Character count: {len(script)} / 5000")
            
            if st.button("🚀 Generate Avatar Video", use_container_width=True, type="primary"):
                if not script.strip():
                    st.error("Please enter a script.")
                else:
                    with st.spinner("Processing request..."):
                        payload = {
                            "actorId": sel_avatar['id'],
                            "voiceId": sel_voice['id'],
                            "script": script
                        }
                        res, err = safe_api_call("POST", API_ENDPOINTS["GENERATE_CLIP"], json=payload)
                        if res:
                            st.success(f"Video queued! ID: {res.get('id')}")
                            # Refresh history
                            history, _ = safe_api_call("GET", f"{API_ENDPOINTS['GENERATE_CLIP']}?pageSize=20")
                            if history: st.session_state.history = history.get('items', [])
                        else:
                            st.error(err)

        with col_prev:
            st.subheader("Preview")
            with st.container():
                if 'thumbnailImagePath' in sel_avatar:
                    st.image(sel_avatar['thumbnailImagePath'], use_container_width=True)
                
                st.markdown(f"**Actor:** {sel_avatar['name']} | **Ethnicity:** {sel_avatar.get('ethnicity', 'N/A')}")
                
                if 'previewAudioPath' in sel_voice:
                    st.audio(sel_voice['previewAudioPath'])
                st.markdown(f"**Voice:** {sel_voice['name']} | **Type:** {sel_voice.get('voiceType', 'N/A')}")

# ------------------------------------------
# TAB 2: DUBBING
# ------------------------------------------
with tabs[1]:
    st.subheader("🌍 Video Dubbing (v2)")
    st.write("Translate and dub your videos into multiple languages automatically.")
    
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        source_url = st.text_input("Source Video URL", placeholder="https://example.com/video.mp4")
        s_lang = st.text_input("Source Language Code", value="auto", help="Use 'auto' or e.g., 'en'")
        t_lang = st.text_input("Target Language Code", placeholder="e.g., es, fr, de")
        
        if st.button("⚡ Start Dubbing", type="primary"):
            if not source_url or not t_lang:
                st.error("URL and Target Language are required.")
            else:
                with st.spinner("Initiating dubbing..."):
                    payload = {
                        "sourceUrl": source_url,
                        "targetLanguage": t_lang,
                        "sourceLanguage": s_lang
                    }
                    res, err = safe_api_call("POST", API_ENDPOINTS["DUBBING"], json=payload)
                    if res:
                        st.success("Dubbing process started!")
                    else:
                        st.error(err)
    
    with d_col2:
        st.info("""
        **How it works:**
        1. Ingests your source video.
        2. Automatically translates the audio.
        3. Regenerates audio in the target language.
        4. Produces a lip-synced result.
        """)

# ------------------------------------------
# TAB 3: LIP SYNC
# ------------------------------------------
with tabs[2]:
    st.subheader("👄 Lip Sync (v1)")
    st.write("Sync any audio file to any video file with natural lip movement.")
    
    l_col1, l_col2 = st.columns(2)
    with l_col1:
        ls_video_url = st.text_input("Source Video URL ", placeholder="https://example.com/video.mp4")
        ls_audio_url = st.text_input("Target Audio URL", placeholder="https://example.com/audio.mp3")
        
        if st.button("🔗 Sync Audio & Video", type="primary"):
            if not ls_video_url or not ls_audio_url:
                st.error("Both Video and Audio URLs are required.")
            else:
                with st.spinner("Processing lip sync..."):
                    payload = {
                        "sourceUrl": ls_video_url,
                        "targetAudioUrl": ls_audio_url
                    }
                    res, err = safe_api_call("POST", API_ENDPOINTS["LIPSYNC"], json=payload)
                    if res:
                        st.success("Lip sync process started!")
                    else:
                        st.error(err)
    
    with l_col2:
        st.info("""
        **Best for:**
        - A/B testing ads with different actors but same audio.
        - Using high-quality pre-recorded voiceovers.
        - Fixing sync issues in existing videos.
        """)

# ------------------------------------------
# TAB 4: LIBRARY & HISTORY
# ------------------------------------------
with tabs[3]:
    st.subheader("📁 Project Library")
    
    if st.button("🔄 Refresh Library"):
        history, _ = safe_api_call("GET", f"{API_ENDPOINTS['GENERATE_CLIP']}?pageSize=20")
        if history: st.session_state.history = history.get('items', [])
        st.rerun()

    if not st.session_state.history:
        st.info("No projects found yet. Start by generating a video!")
    else:
        for item in st.session_state.history:
            status = item.get('status', 'Pending')
            badge_class = f"badge badge-{status.lower()}"
            
            with st.expander(f"Project: {item['id']} | Status: {status}"):
                c1, c2 = st.columns([1, 2])
                
                with c1:
                    st.markdown(f"**Created:** {item.get('createdDate', 'N/A')}")
                    st.markdown(f'<span class="{badge_class}">{status}</span>', unsafe_allow_html=True)
                    
                    if status != "Completed":
                        if st.button("🔍 Check Status", key=f"check_{item['id']}"):
                            res, err = safe_api_call("GET", f"{API_ENDPOINTS['GENERATE_CLIP']}/{item['id']}")
                            if res:
                                # Update local state if completed
                                if res.get('status') == "Completed":
                                    st.success("Project is ready!")
                                    st.rerun()
                                else:
                                    st.info(f"Current Status: {res.get('status')}")
                            else:
                                st.error(err)
                    
                    if status == "Completed" and 'videoUrl' in item:
                        st.download_button("📥 Download MP4", item['videoUrl'], file_name=f"pipio_{item['id']}.mp4", key=f"dl_{item['id']}")

                with c2:
                    if status == "Completed" and 'videoUrl' in item:
                        st.video(item['videoUrl'])
                    else:
                        st.markdown(f"**Script Snippet:**\n> {item.get('script', 'N/A')[:200]}...")

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
f_col1, f_col2 = st.columns(2)
with f_col1:
    st.caption("© 2026 Pipio AI Studio Pro | Powered by Pipio API")
with f_col2:
    st.markdown('<div style="text-align: right;"><small>Built with Streamlit & ❤️</small></div>', unsafe_allow_html=True)
