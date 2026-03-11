import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400&display=swap');

        html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

        .stApp {
            background: #080b12;
            background-image:
                radial-gradient(ellipse 80% 50% at 20% 10%, rgba(56,189,248,0.07) 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 80%, rgba(139,92,246,0.07) 0%, transparent 60%);
        }

        [data-testid="stSidebar"] {
            background: #0d111c !important;
            border-right: 1px solid rgba(56,189,248,0.12);
        }
        [data-testid="stSidebar"] * { font-family: 'Syne', sans-serif !important; }

        #MainMenu, footer, header { visibility: hidden; }

        .pm-header {
            display: flex; align-items: center; gap: 14px;
            padding: 8px 0 24px 0;
            border-bottom: 1px solid rgba(56,189,248,0.12);
            margin-bottom: 24px;
        }
        .pm-logo { font-size: 2rem; line-height: 1; }
        .pm-title { font-size: 1.6rem; font-weight: 800; color: #f0f6ff; letter-spacing: -0.5px; margin: 0; }
        .pm-subtitle { font-size: 0.75rem; color: #38bdf8; letter-spacing: 2px; text-transform: uppercase; font-weight: 600; margin: 0; font-family: 'JetBrains Mono', monospace !important; }

        .section-label {
            font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase;
            color: #38bdf8; font-weight: 700; font-family: 'JetBrains Mono', monospace;
            margin-bottom: 10px; margin-top: 20px;
        }

        .paper-tag {
            display: flex; align-items: center; gap: 8px;
            background: rgba(56,189,248,0.06); border: 1px solid rgba(56,189,248,0.2);
            border-radius: 8px; padding: 8px 12px; margin: 6px 0;
            font-size: 0.78rem; color: #94d8f8; font-family: 'JetBrains Mono', monospace;
            word-break: break-all;
        }
        .paper-dot { width:7px; height:7px; border-radius:50%; background:#38bdf8; flex-shrink:0; box-shadow:0 0 6px #38bdf8; }

        .summary-card {
            background: linear-gradient(135deg, rgba(56,189,248,0.06), rgba(139,92,246,0.06));
            border: 1px solid rgba(139,92,246,0.25); border-radius: 12px;
            padding: 16px 18px; margin: 12px 0;
            font-size: 0.82rem; color: #c4d4e8; line-height: 1.7;
            font-family: 'JetBrains Mono', monospace;
        }
        .summary-title {
            font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase;
            color: #a78bfa; font-weight: 700; margin-bottom: 10px;
            font-family: 'JetBrains Mono', monospace;
        }

        .stButton > button {
            background: rgba(56,189,248,0.08) !important;
            border: 1px solid rgba(56,189,248,0.25) !important;
            color: #38bdf8 !important; border-radius: 8px !important;
            font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
            font-size: 0.8rem !important; letter-spacing: 0.5px !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background: rgba(56,189,248,0.15) !important;
            border-color: rgba(56,189,248,0.5) !important;
            transform: translateY(-1px) !important;
        }

        [data-testid="stFileUploader"] {
            background: rgba(56,189,248,0.03) !important;
            border: 1px dashed rgba(56,189,248,0.25) !important;
            border-radius: 12px !important; padding: 8px !important;
        }

        .source-badge {
            display: inline-block;
            background: rgba(139,92,246,0.12); border: 1px solid rgba(139,92,246,0.25);
            color: #a78bfa; border-radius: 6px; padding: 2px 10px;
            font-size: 0.72rem; font-family: 'JetBrains Mono', monospace; margin-right: 4px;
            margin-top: 6px;
        }

        .empty-state { text-align: center; padding: 60px 20px; color: #2a3a52; }
        .empty-state h3 { color: #2a3a52; font-size: 1.1rem; font-weight: 600; }
        .empty-state p  { color: #1e2d40; font-size: 0.82rem; }

        .stats-bar { display: flex; gap: 16px; padding: 10px 0; margin-bottom: 8px; }
        .stat-item {
            background: rgba(56,189,248,0.05); border: 1px solid rgba(56,189,248,0.1);
            border-radius: 8px; padding: 6px 14px; font-size: 0.72rem;
            font-family: 'JetBrains Mono', monospace; color: #4a7a9b;
        }
        .stat-item span { color: #38bdf8; font-weight: 700; }

        hr { border-color: rgba(56,189,248,0.08) !important; }
    </style>
    """, unsafe_allow_html=True)