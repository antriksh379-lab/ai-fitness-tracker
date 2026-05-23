import streamlit as st
import httpx
import os

# 1. Global Viewport Frame & Architecture Configurations
st.set_page_config(
    page_title="APEX // AI Performance Coach", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dynamic Target Routing Vector (Localhost dev / Production Render cluster)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

# 2. Advanced Premium CSS Injection Matrix
st.markdown("""
    <style>
    /* Global Background and Typography Overrides */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b0f19 !important;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }
    
    /* Premium Header Glow Layout */
    .header-container {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.7);
    }
    
    /* Modern Glassmorphic Training Cards */
    .athlete-card {
        background: rgba(23, 30, 46, 0.6) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .athlete-card:hover {
        border-color: rgba(34, 197, 94, 0.3);
        box-shadow: 0 12px 20px -10px rgba(34, 197, 94, 0.15);
        transform: translateY(-2px);
    }
    
    /* Workout Output Extracted Schema Visuals */
    .exercise-badge {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        padding: 16px;
        border-radius: 8px;
        margin-top: 12px;
    }
    
    /* Streamlit Input Component Tuning */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
    }
    
    .stTextArea textarea, .stTextInput input {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        color: #f3f4f6 !important;
        border-radius: 10px !important;
        transition: all 0.2s;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #22c55e !important;
        box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2) !important;
    }
    
    /* Button Premium Tuning */
    .stButton>button {
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3) !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4) !important;
    }
    
    /* Secondary Action Buttons (Reset/Session Init) */
    div.element-container button[aria-label*="Initialize"], 
    div.element-container button[aria-label*="Reset"] {
        background: #1f2937 !important;
        border: 1px solid #374151 !important;
        color: #e5e7eb !important;
        box-shadow: none !important;
    }
    
    /* Custom Scrollbar for Chat Panel */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track { background: #0b0f19; }
    ::-webkit-scrollbar-thumb { background: #374151; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #4b5563; }
    </style>
""", unsafe_allow_html=True)

# 3. Dynamic Animated Header Panel
st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; color:#ffffff; font-size:2.2rem;">⚡ APEX ENGINE // TERMINAL DEPLOY</h1>
        <p style="margin:5px 0 0 0; color:#9ca3af; font-size:1rem;">Production-ready data synchronization & real-time predictive coaching stream.</p>
    </div>
""", unsafe_allow_html=True)

# Orchestrate Screen Grid Canvas Split
col1, col2 = st.columns([1, 1], gap="large")

# =====================================================================
# LEFT CANVASS: LOG PIPELINE WINDOW (WORKOUT LOGGER)
# =====================================================================
with col1:
    st.markdown("<h2 style='color:#ffffff; margin-bottom:5px;'>📝 Analytics Intake Matrix</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280; margin-bottom:20px;'>Parse raw kinetic metrics directly into your cloud logging array.</p>", unsafe_allow_html=True)
    
    with st.container(border=False):
        st.markdown('<div class="athlete-card">', unsafe_allow_html=True)
        athlete_id = st.text_input("👤 Athlete System Profile Key", value="athlete_test_99", key="global_athlete_id")
        
        raw_input_text = st.text_area(
            "🏋️‍♂️ Post-Workout Shorthand Stream",
            height=160,
            placeholder="e.g., Squat day. Managed 3x5 at 315 lbs, then hit RDLs 3x10 with 225. Energy was a solid 4/5. Lockout felt incredibly powerful."
        )
        
        process_trigger = st.button("🚀 Push Performance Stream", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if process_trigger:
        if not raw_input_text.strip():
            st.warning("Cannot parse empty stream entry vector.")
        else:
            with st.spinner("Decoding metrics... Updating your Atlas collection clusters..."):
                try:
                    payload = {"user_id": athlete_id, "raw_input_text": raw_input_text}
                    response = httpx.post(f"{BACKEND_URL}/api/workouts/log", json=payload, timeout=30.0)
                    
                    if response.status_code in [200, 201]:
                        data = response.json()
                        st.success("✔️ Document integrated successfully with MongoDB cluster.")
                        
                        # Render Dynamic Metric Display Badge for Inferred Energy State
                        energy = data.get("energy_rating")
                        if energy:
                            st.metric(label="📊 Computed Athlete Energy Level", value=f"{energy} / 5")
                        
                        # AI Feedback Block Layout
                        st.markdown("### 🤖 Coach Apex Critique")
                        st.info(data.get('coach_notes'))
                        
                        # Schema Node Layout Render
                        st.markdown("### 🧬 Isolated Kinetic Schema Objects")
                        for exercise in data.get("exercises", []):
                            st.markdown(f"""
                            <div class="exercise-badge">
                                <h4 style="margin:0 0 5px 0; color:#ffffff;">{exercise['name']}</h4>
                                <span style="color:#9ca3af; font-size:0.95rem;">
                                    <b>Sets:</b> {exercise['sets']} &nbsp;|&nbsp; 
                                    <b>Rep Array:</b> {exercise['reps']} &nbsp;|&nbsp; 
                                    <b>Loading Parameter:</b> {exercise['weight_lbs']} lbs
                                </span>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ Backend Intake Fault. Status Code: {response.status_code} | Payload: {response.text}")
                except Exception as e:
                    st.error(f"❌ Gateway Communication Failure: Unable to reach backend API framework: {e}")

# =====================================================================
# RIGHT CANVASS: THE LIVE STREAM MATRIX CONSOLE (COACH CHAT)
# =====================================================================
with col2:
    st.markdown("<h2 style='color:#ffffff; margin-bottom:5px;'>💬 Predictive Coach Stream</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#6b7280; margin-bottom:20px;'>Query kinetic trends or compute optimization logic models dynamically.</p>", unsafe_allow_html=True)
    
    # State Memory Array Cache Checks
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Dynamic Context Controls Card Panel
    st.markdown('<div class="athlete-card">', unsafe_allow_html=True)
    if not st.session_state.session_id:
        st.markdown("<p style='color:#9ca3af; margin:0 0 10px 0;'>Memory pipeline offline. Initialize a session tracking frame to begin context tracking.</p>", unsafe_allow_html=True)
        if st.button("🏁 Initialize Coach Memory Gateway"):
            with st.spinner("Spawning cloud socket tracking variables..."):
                try:
                    payload = {"user_id": athlete_id, "session_name": "Premium Dashboard Stream"}
                    res = httpx.post(f"{BACKEND_URL}/api/coach/sessions", json=payload)
                    
                    if res.status_code in [200, 201]:
                        st.session_state.session_id = res.json()["_id"]
                        st.success("✔ Session pipeline generated successfully!")
                        st.rerun()
                    else:
                        st.error(f"❌ Session Generation Failure. Status: {res.status_code} | Server Says: {res.text}")
                except Exception as e:
                    st.error(f"❌ Connectivity Failure: Unable to resolve route target {BACKEND_URL}. Error: {e}")
    else:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"""
                <div style="padding-top:8px;">
                    <span style="color:#22c55e; font-weight:600;">● STREAM TUNNEL ACTIVE</span><br>
                    <span style="color:#6b7280; font-size:0.85rem;">ID: {st.session_state.session_id}</span>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            if st.button("🗑️ Reset Engine"):
                st.session_state.session_id = None
                st.session_state.chat_history = []
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Scroll Box Render Mapping Framework
    chat_container = st.container(height=400)
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("<p style='color:#4b5563; text-align:center; padding-top:150px; font-style:italic;'>Awaiting prompt sequence inputs... Query target metrics below.</p>", unsafe_allow_html=True)
        else:
            for role, text in st.session_state.chat_history:
                with st.chat_message(role):
                    st.write(text)

    # Input capture bar setup
    if chat_prompt := st.chat_input("Ask Coach Apex a strategic question..."):
        if not st.session_state.session_id:
            st.error("Cannot broadcast prompt vector across empty system memory layers. Open the gateway above.")
        else:
            # Render user text vector block immediately
            st.session_state.chat_history.append(("user", chat_prompt))
            with chat_container:
                with st.chat_message("user"):
                    st.write(chat_prompt)

            # Fire request to streaming context channels
            with chat_container:
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    with st.spinner("Coach Apex is breaking down the mechanics..."):
                        try:
                            payload = {"message": chat_prompt}
                            
                            # 🟢 CONNECT VIA STREAM: Read chunked data blocks incrementally
                            with httpx.Client(timeout=httpx.Timeout(60.0, connect=10.0)) as client:
                                with client.stream(
                                    "POST", 
                                    f"{BACKEND_URL}/api/coach/sessions/{st.session_state.session_id}/stream", 
                                    json=payload
                                ) as response:
                                    
                                    if response.status_code in [200, 201]:
                                        # Parse text tokens as they leave Render's platform router
                                        for chunk in response.iter_text():
                                            full_response += chunk
                                            # Update the visual canvas stream with a typing block marker
                                            response_placeholder.markdown(full_response + "▌")
                                        
                                        # Lock in the clean response and save to persistent cache state
                                        response_placeholder.markdown(full_response)
                                        st.session_state.chat_history.append(("assistant", full_response))
                                    else:
                                        st.error(f"❌ Streaming Error. Code: {response.status_code}")
                        except Exception as e:
                            st.error(f"❌ Error communicating with backend stream loop: {e}")