from __future__ import annotations

import html
import json
import base64
from pathlib import Path

import streamlit as st
from PIL import Image

from src.multimodal_detector import MultiModalFakeNewsDetector
from src.schemas import ModalityScore, NewsInput, PredictionResult


@st.cache_data
def get_base64_gif(gif_path: str) -> str:
    with open(gif_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()



st.set_page_config(
    page_title="Multi-Modal Fake News & Deepfake Detection System",
    page_icon="📊",
    layout="wide",
)


@st.cache_resource
def load_detector() -> MultiModalFakeNewsDetector:
    return MultiModalFakeNewsDetector()


def load_sample() -> dict:
    sample_path = Path("samples/sample_article.json")
    if sample_path.exists():
        return json.loads(sample_path.read_text(encoding="utf-8"))
    return {
        "headline": "Scientists confirm local lake turns magnetic overnight",
        "article": "A viral article claims that a lake became magnetic after a secret experiment.",
        "source": "unknownviralnews.example",
        "claim": "A lake became magnetic overnight after a secret experiment.",
        "evidence": [],
    }


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def theme_tokens(mode: str) -> dict[str, str]:
    if mode == "Light":
        return {
            "bg": "rgba(248, 250, 252, 0.9)",
            "bg2": "rgba(241, 245, 249, 0.95)",
            "overlay": "radial-gradient(circle at 18% 8%, rgba(29, 78, 216, 0.06), transparent 45%), radial-gradient(circle at 86% 20%, rgba(30, 64, 175, 0.04), transparent 45%), linear-gradient(135deg, #f8fafc, #f1f5f9)",
            "surface": "rgba(255, 255, 255, 0.7)",
            "surface2": "rgba(241, 245, 249, 0.85)",
            "ink": "#0f172a",
            "muted": "#475569",
            "line": "rgba(14, 89, 199, 0.12)",
            "accent": "#0f59c7",
            "accent2": "#0284c7",
            "accent3": "#0891b2",
            "danger": "#dc2626",
            "shadow": "0 10px 30px rgba(15, 23, 42, 0.06)",
            "field": "rgba(255, 255, 255, 0.9)",
            "device": "#0f172a",
            "device2": "#1e293b",
            "border_highlight": "rgba(255, 255, 255, 0.5)",
        }
    return {
        "bg": "rgba(15, 10, 5, 0.95)",
        "bg2": "rgba(36, 24, 13, 0.98)",
        "overlay": "radial-gradient(circle at 18% 8%, rgba(217, 119, 6, 0.22), transparent 45%), radial-gradient(circle at 86% 20%, rgba(245, 158, 11, 0.15), transparent 45%), linear-gradient(135deg, rgba(15, 10, 5, 0.82), rgba(36, 24, 13, 0.76) 50%, rgba(15, 10, 5, 0.82))",
        "surface": "rgba(36, 24, 13, 0.65)",
        "surface2": "rgba(54, 36, 20, 0.8)",
        "ink": "#f8fafc",
        "muted": "#94a3b8",
        "line": "rgba(245, 158, 11, 0.16)",
        "accent": "#d97706",
        "accent2": "#f59e0b",
        "accent3": "#ea580c",
        "danger": "#ef4444",
        "shadow": "0 10px 30px rgba(0, 0, 0, 0.4)",
        "field": "rgba(15, 10, 5, 0.85)",
        "device": "#1c120c",
        "device2": "#2e1f14",
        "border_highlight": "rgba(255, 255, 255, 0.06)",
    }


def inject_css(mode: str) -> None:
    t = theme_tokens(mode)
    try:
        gif_base64 = get_base64_gif("line-noise-loop.gif")
        bg_url = f"data:image/gif;base64,{gif_base64}"
    except Exception:
        bg_url = "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExampmeXpvdGJnZTZkYWI4YWQ5N2dqajNtNW8xOXliaW5la2hwem45cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7btOfPKQb7mCLxBu/giphy.gif"

    st.markdown(
        f"""
        <style>
        :root {{
          --bg: {t["bg"]};
          --bg2: {t["bg2"]};
          --overlay: {t["overlay"]};
          --surface: {t["surface"]};
          --surface2: {t["surface2"]};
          --ink: {t["ink"]};
          --muted: {t["muted"]};
          --line: {t["line"]};
          --accent: {t["accent"]};
          --accent2: {t["accent2"]};
          --accent3: {t["accent3"]};
          --danger: {t["danger"]};
          --shadow: {t["shadow"]};
          --field: {t["field"]};
          --device: {t["device"]};
          --device2: {t["device2"]};
          --border-highlight: {t["border_highlight"]};
        }}

        [data-testid="stAppViewContainer"] {{
          background: transparent !important;
        }}
        [data-testid="stHeader"] {{
          background: transparent !important;
        }}

        .stApp {{
          color: var(--ink);
          background:
            var(--overlay),
            url("{bg_url}") no-repeat center center fixed;
          background-size: cover !important;
        }}

        .block-container {{
          max-width: 1280px;
          padding: 1.25rem 2rem 4rem;
        }}

        header, footer, #MainMenu {{
          visibility: hidden;
        }}

        h1, h2, h3, h4, p, span, label {{
          color: var(--ink);
          letter-spacing: 0;
        }}

        div[data-testid="stTabs"] {{
          background: transparent !important;
        }}

        div[data-testid="stTabs"] button {{
          border-radius: 999px;
          padding: 0.72rem 1.1rem;
          color: var(--muted);
          transition: background 180ms ease, transform 180ms ease, color 180ms ease;
        }}

        div[data-testid="stTabs"] button:hover {{
          transform: translateY(-1px);
          background: color-mix(in srgb, var(--surface2) 72%, transparent);
        }}

        div[data-testid="stTabs"] button[aria-selected="true"] {{
          color: var(--ink);
          background: var(--surface2);
          box-shadow: 0 12px 30px rgba(0,0,0,0.12);
        }}

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stFileUploader"] section {{
          background: var(--field);
          color: var(--ink);
          border: 1px solid var(--line);
          border-radius: 16px;
          box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
          transition: transform 170ms ease, border-color 170ms ease, box-shadow 170ms ease;
        }}

        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {{
          border-color: var(--accent);
          box-shadow: 0 0 0 4px color-mix(in srgb, var(--accent) 18%, transparent);
        }}

        [data-testid="stTextInput"] input:hover,
        [data-testid="stTextArea"] textarea:hover,
        [data-testid="stFileUploader"] section:hover {{
          transform: translateY(-1px);
        }}

        .stButton > button {{
          min-height: 3.2rem;
          border: 0;
          border-radius: 16px;
          color: #fff;
          font-weight: 850;
          background: linear-gradient(135deg, var(--accent), var(--accent2));
          box-shadow: 0 18px 42px color-mix(in srgb, var(--accent) 34%, transparent);
          transition: transform 170ms ease, box-shadow 170ms ease, filter 170ms ease;
        }}

        .stButton > button:hover {{
          transform: translateY(-2px) scale(1.01);
          filter: saturate(1.08);
          box-shadow: 0 24px 56px color-mix(in srgb, var(--accent) 38%, transparent);
        }}

        .topbar {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 18px;
          margin: 4px 0 18px;
        }}

        .brand {{
          display: flex;
          align-items: center;
          gap: 12px;
          font-weight: 900;
        }}

        .brand-mark {{
          width: 42px;
          height: 42px;
          display: grid;
          place-items: center;
          border-radius: 50%;
          color: #fff;
          background: conic-gradient(from 0deg, var(--accent), var(--accent2), var(--accent3), var(--accent));
          box-shadow: 0 10px 24px color-mix(in srgb, var(--accent) 20%, transparent);
        }}

        .nav-note {{
          color: var(--muted);
          font-size: 0.92rem;
        }}

        .hero {{
          min-height: auto;
          padding: 24px 0 34px;
          animation: riseIn 650ms cubic-bezier(.2,.8,.2,1) both;
        }}

        .eyebrow {{
          width: fit-content;
          padding: 8px 12px;
          border: 1px solid color-mix(in srgb, var(--accent2) 34%, transparent);
          border-radius: 999px;
          background: color-mix(in srgb, var(--accent2) 12%, transparent);
          color: var(--accent2);
          font-size: 0.84rem;
          font-weight: 850;
          margin-bottom: 18px;
        }}

        .hero-title {{
          margin: 0;
          font-size: clamp(2.2rem, 4.5vw, 3.5rem);
          line-height: 1.15;
          font-weight: 800;
          letter-spacing: -0.02em;
        }}

        .hero-title span {{
          color: var(--accent);
        }}

        .hero-desc {{
          margin: 20px 0 0;
          max-width: 900px;
          color: var(--muted);
          font-size: 1.12rem;
          line-height: 1.65;
        }}

        .hero-actions {{
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          margin-top: 24px;
        }}

        .pill {{
          padding: 12px 15px;
          border-radius: 999px;
          border: 1px solid var(--line);
          background: var(--surface);
          color: var(--muted);
          backdrop-filter: blur(18px);
        }}

        .pill strong {{
          color: var(--ink);
        }}

        .device-stage {{
          position: relative;
          min-height: 560px;
          display: grid;
          place-items: center;
          animation: riseIn 760ms cubic-bezier(.2,.8,.2,1) 90ms both;
        }}

        .device-stage::before {{
          content: "";
          position: absolute;
          inset: 28px 0 0 26px;
          border-radius: 44px;
          background: linear-gradient(135deg, color-mix(in srgb, var(--accent2) 28%, transparent), color-mix(in srgb, var(--accent3) 20%, transparent));
          filter: blur(2px);
          opacity: 0.72;
          transform: rotate(-3deg);
        }}

        .device {{
          position: relative;
          width: min(100%, 720px);
          min-height: 520px;
          padding: 26px;
          border: 14px solid var(--device);
          border-radius: 42px;
          background: linear-gradient(145deg, var(--device2), var(--device));
          box-shadow: var(--shadow);
          overflow: hidden;
          animation: deviceFloat 7s ease-in-out infinite, morphFrame 10s ease-in-out infinite;
        }}

        .device::after {{
          content: "";
          position: absolute;
          inset: 0;
          background: linear-gradient(115deg, transparent 0%, rgba(255,255,255,0.12) 42%, transparent 68%);
          transform: translateX(-110%);
          animation: glassSheen 6s ease-in-out infinite;
          pointer-events: none;
        }}

        .device-nav {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 10px;
          padding: 11px 13px;
          border: 1px solid rgba(255,255,255,0.12);
          border-radius: 18px;
          background: rgba(255,255,255,0.08);
          color: #f5f5ee;
          font-size: 0.85rem;
        }}

        .device-main {{
          display: grid;
          grid-template-columns: 0.82fr 1.18fr;
          gap: 16px;
          margin-top: 18px;
        }}

        .device-panel {{
          min-height: 388px;
          padding: 22px;
          border-radius: 26px;
          background: rgba(255,255,255,0.09);
          border: 1px solid rgba(255,255,255,0.1);
          color: #f5f5ee;
        }}

        .scan-card {{
          height: 98px;
          border-radius: 20px;
          background:
            linear-gradient(90deg, color-mix(in srgb, var(--accent) 75%, transparent), color-mix(in srgb, var(--accent2) 56%, transparent)),
            repeating-linear-gradient(0deg, transparent 0 12px, rgba(255,255,255,0.1) 12px 13px);
          margin: 16px 0;
          animation: pulseGlow 3.2s ease-in-out infinite;
        }}

        .stack-row {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
          border-bottom: 1px solid var(--line);
          padding: 15px 0;
          color: var(--muted);
        }}

        .stack-row strong {{
          color: var(--ink);
        }}

        .fusion-orbit {{
          position: relative;
          height: 388px;
          border-radius: 26px;
          background:
            radial-gradient(circle at center, color-mix(in srgb, var(--accent) 34%, transparent), transparent 28%),
            radial-gradient(circle at 68% 28%, color-mix(in srgb, var(--accent3) 26%, transparent), transparent 24%),
            var(--surface2);
          border: 1px solid var(--line);
          overflow: hidden;
        }}

        .ring {{
          position: absolute;
          inset: 60px;
          border: 1px solid var(--line);
          border-radius: 50%;
          animation: slowSpin 16s linear infinite;
        }}

        .ring.two {{
          inset: 94px;
          animation-direction: reverse;
          animation-duration: 20s;
        }}

        .node {{
          position: absolute;
          padding: 10px 12px;
          border-radius: 14px;
          color: var(--ink);
          background: var(--surface);
          border: 1px solid var(--line);
          backdrop-filter: blur(12px);
          box-shadow: var(--shadow);
          font-size: 0.82rem;
        }}

        .node.a {{ left: 26px; top: 44px; }}
        .node.b {{ right: 24px; top: 84px; }}
        .node.c {{ left: 44px; bottom: 74px; }}
        .node.d {{ right: 42px; bottom: 42px; }}

        .center-score {{
          position: absolute;
          inset: 0;
          display: grid;
          place-items: center;
          text-align: center;
          color: var(--ink);
        }}

        .center-score strong {{
          display: block;
          font-size: 3.4rem;
          line-height: 1;
          color: var(--ink);
        }}

        .section-title {{
          margin: 28px 0 14px;
          font-size: clamp(1.9rem, 3vw, 3rem);
          line-height: 1.05;
        }}

        .section-copy {{
          color: var(--muted);
          max-width: 860px;
          line-height: 1.68;
          margin-bottom: 24px;
        }}

        .glass-grid {{
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 16px;
        }}

        .glass-grid.two {{
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }}

        .glass-card,
        .wide-panel,
        .result-panel,
        .metric-card,
        .score-card {{
          position: relative;
          overflow: hidden;
          border: 1px solid var(--line);
          background: var(--surface);
          backdrop-filter: blur(22px) saturate(130%);
          -webkit-backdrop-filter: blur(22px) saturate(130%);
          box-shadow: var(--shadow), inset 0 1px 0 0 var(--border-highlight);
          animation: riseIn 520ms cubic-bezier(.2,.8,.2,1) both;
        }}

        .glass-card {{
          min-height: 188px;
          border-radius: 26px;
          padding: 22px;
          transition: transform 180ms ease, border-color 180ms ease;
        }}

        .glass-card:hover {{
          transform: translateY(-5px);
          border-color: color-mix(in srgb, var(--accent) 42%, var(--line));
        }}

        .glass-card .kicker {{
          color: var(--accent2);
          font-weight: 850;
          font-size: 0.82rem;
          margin-bottom: 14px;
        }}

        .glass-card h3 {{
          margin: 0 0 10px;
          font-size: 1.32rem;
        }}

        .glass-card p {{
          color: var(--muted);
          line-height: 1.58;
          margin: 0;
        }}

        .wide-panel {{
          border-radius: 30px;
          padding: 26px;
          margin: 14px 0;
        }}

        .architecture {{
          display: grid;
          grid-template-columns: repeat(5, minmax(0, 1fr));
          gap: 12px;
          align-items: stretch;
        }}

        .arch-step {{
          padding: 18px;
          border-radius: 22px;
          background: var(--surface2);
          border: 1px solid var(--line);
          min-height: 170px;
        }}

        .arch-step b {{
          display: block;
          font-size: 1.04rem;
          margin-bottom: 8px;
        }}

        .arch-step span {{
          color: var(--muted);
          line-height: 1.45;
          font-size: 0.9rem;
        }}

        .detector-shell {{
          padding: 22px;
          border: 1px solid var(--line);
          border-radius: 30px;
          background: var(--surface);
          backdrop-filter: blur(22px);
          box-shadow: var(--shadow);
          margin-top: 18px;
        }}

        .result-panel {{
          border-radius: 30px;
          padding: 26px;
          margin-top: 22px;
          --result-color: var(--accent2);
        }}

        .result-head {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 16px;
          margin-bottom: 18px;
        }}

        .prediction-label {{
          color: var(--result-color);
          font-size: clamp(2.6rem, 5vw, 5.2rem);
          line-height: 0.94;
          font-weight: 950;
        }}

        .risk-badge {{
          padding: 11px 15px;
          border-radius: 999px;
          color: var(--result-color);
          background: color-mix(in srgb, var(--result-color) 15%, transparent);
          border: 1px solid color-mix(in srgb, var(--result-color) 36%, transparent);
          font-weight: 850;
        }}

        .metrics-grid {{
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 14px;
          margin-bottom: 16px;
        }}

        .metric-card,
        .score-card {{
          border-radius: 22px;
          padding: 18px;
          background: var(--surface2);
        }}

        .metric-label {{
          color: var(--muted);
          font-size: 0.86rem;
          margin-bottom: 8px;
        }}

        .metric-value {{
          font-size: 2rem;
          font-weight: 950;
        }}

        .bar {{
          height: 9px;
          border-radius: 999px;
          margin-top: 13px;
          background: color-mix(in srgb, var(--ink) 10%, transparent);
          overflow: hidden;
        }}

        .bar > span {{
          display: block;
          width: var(--value);
          height: 100%;
          border-radius: inherit;
          background: linear-gradient(90deg, var(--accent), var(--accent2), var(--result-color));
          animation: growBar 760ms cubic-bezier(.2,.8,.2,1) both;
        }}

        .score-grid {{
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 14px;
        }}

        .score-top {{
          display: flex;
          justify-content: space-between;
          gap: 14px;
          margin-bottom: 9px;
        }}

        .score-name {{
          font-weight: 850;
        }}

        .score-value {{
          color: var(--accent2);
          font-weight: 950;
        }}

        .score-signal,
        .note {{
          color: var(--muted);
          line-height: 1.55;
        }}

        .timeline {{
          display: grid;
          gap: 12px;
        }}

        .timeline-item {{
          display: grid;
          grid-template-columns: 120px minmax(0, 1fr);
          gap: 16px;
          align-items: start;
          padding: 16px;
          border-radius: 22px;
          background: var(--surface2);
          border: 1px solid var(--line);
        }}

        .timeline-item b {{
          color: var(--accent);
        }}

        @keyframes riseIn {{
          from {{ opacity: 0; transform: translateY(22px) scale(0.985); }}
          to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        @keyframes growBar {{
          from {{ width: 0; }}
          to {{ width: var(--value); }}
        }}

        @keyframes slowSpin {{
          to {{ transform: rotate(360deg); }}
        }}

        @keyframes deviceFloat {{
          0%, 100% {{ transform: translateY(0) rotate(0deg); }}
          50% {{ transform: translateY(-12px) rotate(0.6deg); }}
        }}

        @keyframes morphFrame {{
          0%, 100% {{ border-radius: 42px; }}
          33% {{ border-radius: 52px 34px 46px 38px; }}
          66% {{ border-radius: 34px 52px 38px 46px; }}
        }}

        @keyframes glassSheen {{
          0%, 45% {{ transform: translateX(-110%); opacity: 0; }}
          55% {{ opacity: 1; }}
          100% {{ transform: translateX(110%); opacity: 0; }}
        }}

        @keyframes pulseGlow {{
          0%, 100% {{ filter: brightness(1); }}
          50% {{ filter: brightness(1.18); }}
        }}

        @media (max-width: 980px) {{
          .hero,
          .device-main {{
            grid-template-columns: 1fr;
          }}
          .hero {{
            min-height: auto;
          }}
          .device-stage {{
            min-height: auto;
          }}
          .glass-grid,
          .glass-grid.two,
          .architecture,
          .metrics-grid,
          .score-grid {{
            grid-template-columns: 1fr;
          }}
          .timeline-item {{
            grid-template-columns: 1fr;
          }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero">
          <div class="hero-copy-wrap">
            <h1 class="hero-title">Multi-Modal Misinformation & Deepfake <span>Detection Pipeline</span></h1>
            <p class="hero-desc">
              A scientific Machine Learning framework evaluating news credibility through
              independent modality encoders. Text semantics (NLP), image manipulation artifacts (CV),
              source reputation priors, and factual claim-evidence alignment are processed independently 
              and fused into a threshold-calibrated prediction.
            </p>
            <div class="hero-actions">
              <div class="pill"><strong>4</strong> Fused Modalities</div>
              <div class="pill"><strong>Late Fusion</strong> Strategy</div>
              <div class="pill"><strong>Interpretability</strong> Layer</div>
              <div class="pill"><strong>Metrics-Driven</strong> Calibration</div>
            </div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def card(kicker: str, title: str, body: str) -> str:
    return f'<div class="glass-card"><div class="kicker">{esc(kicker)}</div><h3>{esc(title)}</h3><p>{esc(body)}</p></div>'


def render_overview() -> None:
    st.markdown(
        """
<h2 class="section-title">Pipeline Overview</h2>
<p class="section-copy">
  This system is designed as a modular misinformation classification pipeline, transitioning from 
  heuristic baseline encoders to trained transformer-based NLP and deepfake image forensics models.
</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class="glass-grid">
{card("Problem", "Misinformation classification", "Classify suspicious news items into credibility categories with calibrated probabilities instead of a binary label.")}
{card("Input Modalities", "Text, metadata, and images", "Accepts article headline, body text, publisher source domain, primary claim, evidence snippets, and news image.")}
{card("Output Metrics", "Calibrated confidence & risk bands", "Computes modality-specific risk scores, fused fake probability, class label, and model explanations.")}
{card("NLP Encoder", "Transformer text classifier", "The text processing pipeline is ready for fine-tuning pre-trained models such as DistilBERT, RoBERTa, or DeBERTa.")}
{card("Vision Encoder", "Image manipulation forensics", "The image processing pipeline uses feature extraction suitable for deepfake and image forgery classifiers (e.g., EfficientNet, ViT).")}
{card("Late Fusion", "Modular ensemble architecture", "Ensembles predictions from individual encoders using weighted averaging, with a path to logistic regression or MLP fusion.")}
</div>
        """,
        unsafe_allow_html=True,
    )


def score_card(score: ModalityScore) -> str:
    probability = max(0, min(100, score.fake_probability * 100))
    signal = score.signals[0] if score.signals else "No dominant signal."
    return f'<div class="score-card"><div class="score-top"><div class="score-name">{esc(score.name)}</div><div class="score-value">{probability:.1f}%</div></div><div class="bar" style="--value:{probability:.1f}%"><span></span></div><p class="score-signal">{esc(signal)}</p></div>'


def render_result(result: PredictionResult) -> None:
    result_color = "var(--danger)" if result.label == "Fake" else "var(--accent2)"
    fake_probability = result.fake_probability * 100
    confidence = result.confidence * 100
    risk_value = {"Low": 25, "Medium": 52, "High": 78, "Critical": 96}.get(result.risk_band, 50)
    st.markdown(
        f"""
        <section class="result-panel" style="--result-color:{result_color};">
          <div class="result-head">
            <div>
              <div class="metric-label">Prediction</div>
              <div class="prediction-label">{esc(result.label)}</div>
            </div>
            <div class="risk-badge">{esc(result.risk_band)} risk</div>
          </div>
          <div class="metrics-grid">
            <div class="metric-card">
              <div class="metric-label">Fake probability</div>
              <div class="metric-value">{fake_probability:.1f}%</div>
              <div class="bar" style="--value:{fake_probability:.1f}%"><span></span></div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Confidence</div>
              <div class="metric-value">{confidence:.1f}%</div>
              <div class="bar" style="--value:{confidence:.1f}%"><span></span></div>
            </div>
            <div class="metric-card">
              <div class="metric-label">Risk band</div>
              <div class="metric-value">{esc(result.risk_band)}</div>
              <div class="bar" style="--value:{risk_value}%"><span></span></div>
            </div>
          </div>
          <div class="score-grid">
            {"".join(score_card(score) for score in result.modality_scores)}
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown('<div class="wide-panel"><h3>Explanation</h3>', unsafe_allow_html=True)
        for explanation in result.explanations:
            st.markdown(f'<p class="note">{esc(explanation)}</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="wide-panel"><h3>Reviewer Actions</h3>', unsafe_allow_html=True)
        for action in result.reviewer_actions:
            st.markdown(f'<p class="note">{esc(action)}</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with st.expander("Raw prediction JSON"):
        st.json(result.to_dict())


def render_detector(detector: MultiModalFakeNewsDetector, sample: dict) -> None:
    st.markdown(
        """
        <h2 class="section-title">Live Detector</h2>
        <p class="section-copy">
          Run the current baseline model through the same interface you would use for a trained
          transformer/CV deployment. The baseline is transparent and fast, so it is ideal for demos.
        </p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="detector-shell">', unsafe_allow_html=True)
    left, right = st.columns([0.62, 0.38], gap="large")
    with left:
        headline = st.text_input("Headline", value=sample["headline"])
        article = st.text_area("News article", value=sample["article"], height=270)
        source = st.text_input("Source / publisher domain", value=sample["source"])
        claim = st.text_input("Primary claim", value=sample["claim"])
        uploaded_image = st.file_uploader("News image", type=["jpg", "jpeg", "png", "webp"])
    with right:
        default_evidence = "\n".join(sample.get("evidence", []))
        evidence_text = st.text_area("Trusted evidence snippets", value=default_evidence, height=230)
        evidence = [line.strip() for line in evidence_text.splitlines() if line.strip()]
        image = None
        if uploaded_image is not None:
            image = Image.open(uploaded_image).convert("RGB")
            st.image(image, caption="Uploaded image", use_container_width=True)
        else:
            st.markdown(
                """
                <div class="glass-card" style="min-height:auto;">
                  <div class="kicker">Optional image</div>
                  <p>Upload a news image to activate manipulation-artifact scoring.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    run = st.button("Analyze Content", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if run:
        with st.spinner("Fusing NLP, vision, source, and claim signals..."):
            result = detector.predict(
                NewsInput(
                    headline=headline,
                    article=article,
                    source=source,
                    claim=claim,
                    evidence=evidence,
                    image=image,
                )
            )
        render_result(result)


def render_architecture() -> None:
    st.markdown(
        """
        <h2 class="section-title">System Architecture</h2>
        <p class="section-copy">
          The design uses modular late fusion so every component can be trained, evaluated,
          replaced, and ablated independently.
        </p>
        <div class="wide-panel">
          <div class="architecture">
            <div class="arch-step"><b>1. Ingestion</b><span>Collect headline, article body, source, primary claim, evidence snippets, and optional media.</span></div>
            <div class="arch-step"><b>2. Text Encoder</b><span>Baseline linguistic scoring now; DistilBERT, RoBERTa, or DeBERTa after training.</span></div>
            <div class="arch-step"><b>3. Vision Encoder</b><span>Artifact checks now; CNN, XceptionNet, EfficientNet, or ViT for trained deepfake detection.</span></div>
            <div class="arch-step"><b>4. Verification</b><span>Claim-evidence similarity now; retrieval plus NLI entailment for the advanced version.</span></div>
            <div class="arch-step"><b>5. Fusion</b><span>Weighted ensemble now; calibrated logistic regression, XGBoost, or MLP fusion later.</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_datasets() -> None:
    st.markdown(
        """
<h2 class="section-title">Datasets & Training Roadmap</h2>
<p class="section-copy">
  These datasets make the project credible in interviews because they map directly to the
  modalities and evaluation plan.
</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class="glass-grid">
{card("Text", "FakeNewsNet", "News content, social context, publisher information, and labels for real-world misinformation research.")}
{card("Claims", "LIAR Dataset", "Short political claims with fine-grained truthfulness labels for claim classification.")}
{card("Articles", "Kaggle Fake/Real News", "Large article-level baseline dataset for quick text classifier experiments.")}
{card("Deepfake", "DFDC", "Large-scale deepfake challenge data for video and face manipulation detection.")}
{card("Deepfake", "FaceForensics++", "Common benchmark for manipulated facial media and compression robustness.")}
{card("Deepfake", "Celeb-DF", "Harder celebrity deepfake dataset for stronger generalization testing.")}
</div>
        """,
        unsafe_allow_html=True,
    )


def render_evaluation() -> None:
    st.markdown(
        """
<h2 class="section-title">Evaluation & Metrics</h2>
<p class="section-copy">
  A strong ML project is not just a model; it includes calibration, ablations, error analysis,
  and a metric story that explains false-positive and false-negative tradeoffs.
</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class="glass-grid two">
{card("Classification", "Accuracy, Precision, Recall, F1", "Use F1 and recall heavily because missing harmful fake content can be costly.")}
{card("Ranking", "ROC-AUC and PR-AUC", "Evaluate probability quality across thresholds rather than only one hard decision boundary.")}
{card("Calibration", "Reliability curve and ECE", "Show whether a 70% fake probability really behaves like 70% historical risk.")}
{card("Ablation", "Text vs image vs source vs claim", "Measure each modality independently to prove fusion improves the final system.")}
</div>
        """,
        unsafe_allow_html=True,
    )


def render_explainability() -> None:
    st.markdown(
        """
<h2 class="section-title">Model Interpretability (XAI)</h2>
<p class="section-copy">
  The inference pipeline outputs class probabilities along with textual explanations. In the production pipeline, formal
  eXplainable ML (XAI) methods are integrated into each feature extraction layer.
</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="wide-panel">
<div class="timeline">
<div class="timeline-item"><b>Text</b><span>Use LIME, SHAP, integrated gradients, or attention rollout to identify phrases that pushed the prediction.</span></div>
<div class="timeline-item"><b>Image</b><span>Use Grad-CAM or attention maps to highlight image regions that look manipulated.</span></div>
<div class="timeline-item"><b>Claim</b><span>Return top evidence snippets, similarity scores, and contradiction/entailment labels.</span></div>
<div class="timeline-item"><b>Fusion</b><span>Use SHAP over modality scores and metadata features to explain the final ensemble decision.</span></div>
</div>
</div>
        """,
        unsafe_allow_html=True,
    )


def render_roadmap() -> None:
    st.markdown(
        """
<h2 class="section-title">Development Roadmap</h2>
<p class="section-copy">
  The development schedule outlines the transition from a heuristic baseline to trained 
  deep learning models and deployed inference microservices.
</p>
<div class="wide-panel">
<div class="timeline">
<div class="timeline-item"><b>Phase 1</b><span>Transparent baseline, Streamlit interface, sample inference, and model card.</span></div>
<div class="timeline-item"><b>Phase 2</b><span>Train DistilBERT on FakeNewsNet/Kaggle text and compare with TF-IDF logistic regression.</span></div>
<div class="timeline-item"><b>Phase 3</b><span>Train image/deepfake model with EfficientNet or ViT on DFDC or FaceForensics++ samples.</span></div>
<div class="timeline-item"><b>Phase 4</b><span>Add sentence-transformer retrieval, NLI claim verification, and SHAP/LIME explanations.</span></div>
<div class="timeline-item"><b>Phase 5</b><span>Deploy with FastAPI, Streamlit Cloud or Docker, CI tests, experiment tracking, and ablation report.</span></div>
</div>
</div>
        """,
        unsafe_allow_html=True,
    )


detector = load_detector()
sample = load_sample()

st.session_state.theme_mode = "Dark"

inject_css(st.session_state.theme_mode)
render_hero()

tabs = st.tabs(
    [
        "System Overview",
        "Model Inference",
        "Pipeline Architecture",
        "Datasets",
        "Evaluation Metrics",
        "Interpretability (XAI)",
        "Development Roadmap",
    ]
)

with tabs[0]:
    render_overview()
with tabs[1]:
    render_detector(detector, sample)
with tabs[2]:
    render_architecture()
with tabs[3]:
    render_datasets()
with tabs[4]:
    render_evaluation()
with tabs[5]:
    render_explainability()
with tabs[6]:
    render_roadmap()
