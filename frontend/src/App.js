import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { analyzeContent } from './api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

// --- PRELOADED SAMPLES ---
const SAMPLES = [
  {
    id: "SAMPLE-01",
    label: "Medical Miracle Claim (Fake)",
    headline: "SHOCKING secret cure exposed by anonymous doctors",
    article: "A viral post claims that anonymous sources have revealed a secret cure that doctors hate. The article does not identify the study, the institution, the sample size, or any peer-reviewed publication. It also asks readers to share the story before it is banned.",
    source: "unknownviralnews.example",
    claim: "Anonymous doctors revealed a secret cure that mainstream medicine is hiding.",
    evidence: [
      "Trusted medical guidance requires peer-reviewed evidence, named institutions, and reproducible clinical trial results.",
      "Public health agencies warn that miracle cure claims without transparent studies should be treated with skepticism."
    ]
  },
  {
    id: "SAMPLE-02",
    label: "Climate Science Report (Real)",
    headline: "Global temperature analysis shows warming trends in tropical reefs",
    article: "National oceanographers published a study indicating tropical coral reefs show elevated thermal resistance under specific current shifts. The study compiled 15 years of daily satellite readings and was vetted by 4 independent research labs.",
    source: "sciencejournal.nature.example",
    claim: "Tropical coral reefs show thermal resistance anomalies under current shifts.",
    evidence: [
      "A peer-reviewed publication in Nature Coral confirms ocean currents can buffer local temperature rises.",
      "National oceanographic databases verify satellite dataset accuracy and calibration logs."
    ]
  },
  {
    id: "SAMPLE-03",
    label: "Deepfake Video Scam (Fake)",
    headline: "Secret recording shows prime minister announcing emergency curfew starting tonight",
    article: "A leaked video shared on messaging platforms shows the Prime Minister announcing a nationwide lock-down and immediate asset freeze starting at midnight. Authorities have denied any such orders and warn of voice cloning.",
    source: "leaks2026.social.example",
    claim: "The Prime Minister announced a midnight emergency curfew and bank lockdown.",
    evidence: [
      "The official government gazette confirms banking services remain fully operational and no curfew has been declared.",
      "Audio forensic experts identified robotic voice artifacts and lip-sync alignment anomalies indicative of deepfake synthesis."
    ]
  }
];

function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [activeTab, setActiveTab] = useState('workspace');
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [error, setError] = useState(null);

  // Form inputs
  const [headline, setHeadline] = useState('');
  const [article, setArticle] = useState('');
  const [source, setSource] = useState('');
  const [claim, setClaim] = useState('');
  const [evidenceText, setEvidenceText] = useState('');
  const [imageBase64, setImageBase64] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  // Analysis result
  const [result, setResult] = useState(null);

  // Apply dark mode class to HTML element
  useEffect(() => {
    if (darkMode) document.documentElement.classList.add('dark');
    else document.documentElement.classList.remove('dark');
  }, [darkMode]);

  // Loading screen text cycle animation
  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setLoadingStep(prev => (prev + 1) % 4);
      }, 1500);
    }
    return () => clearInterval(interval);
  }, [loading]);

  // Preload first sample on start
  useEffect(() => {
    loadSample(SAMPLES[0]);
  }, []);

  const loadSample = (sample) => {
    setHeadline(sample.headline);
    setArticle(sample.article);
    setSource(sample.source);
    setClaim(sample.claim);
    setEvidenceText(sample.evidence.join('\n'));
    setImageBase64(null);
    setImagePreview(null);
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
        setImageBase64(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const clearImage = () => {
    setImagePreview(null);
    setImageBase64(null);
  };

  const triggerAnalysis = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setLoadingStep(0);
    setError(null);

    const payload = {
      headline,
      article,
      source,
      claim,
      evidence: evidenceText.split('\n').map(l => l.trim()).filter(l => l !== ''),
      image_base64: imageBase64
    };

    try {
      const res = await analyzeContent(payload);
      setResult(res);
      setActiveTab('fusion'); // Switch to fusion results upon successful analysis
    } catch (err) {
      console.error(err);
      setError(err.message || "Something went wrong while connecting to the model backend.");
    } finally {
      setLoading(false);
    }
  };

  const formatPercentage = (val) => `${(val * 100).toFixed(1)}%`;

  // Components for results
  const StatCard = ({ title, value, icon, gradientLight, gradientDark, live }) => (
    <div className="glass-panel p-6 rounded-2xl flex items-center space-x-6 hover:scale-[1.02] transition-transform duration-300">
      <div className={`p-4 rounded-xl bg-gradient-to-br ${darkMode ? gradientDark : gradientLight} shadow-lg text-white text-2xl`}>{icon}</div>
      <div>
        <div className="flex items-center gap-2 mb-1">
           <p className="text-xs text-ocean-dark dark:text-orange-200/70 font-bold uppercase tracking-wider">{title}</p>
           {live && <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse shadow-[0_0_8px_rgba(239,68,68,0.8)]"></span>}
        </div>
        <p className="text-3xl font-display font-bold text-cyan-950 dark:text-orange-50 tracking-tight">{value}</p>
      </div>
    </div>
  );

  const NavItem = ({ id, label, icon }) => (
    <button onClick={() => setActiveTab(id)} className={`relative flex items-center gap-2 px-5 py-3 text-sm font-semibold transition-all duration-300 rounded-lg overflow-hidden ${activeTab === id ? 'text-ocean-DEFAULT dark:text-flame-light bg-sky-100 dark:bg-orange-900/40' : 'text-cyan-800 dark:text-orange-200/60 hover:text-cyan-950 dark:hover:text-white hover:bg-sky-200/50 dark:hover:bg-orange-800/30'}`}>
      <span className="text-lg z-10">{icon}</span><span className="z-10">{label}</span>
      {activeTab === id && <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-8 h-1 bg-ocean-DEFAULT dark:bg-flame-DEFAULT rounded-t-full"></span>}
    </button>
  );

  const loadingTexts = [
    "Encoding textual semantics via NLP transformers...",
    "Running computer vision models for image ELA artifacts...",
    "Verifying claiming statements against source reputations...",
    "Executing weighted late-fusion calculations..."
  ];

  // Modality configurations
  const getModalityColor = (name) => {
    switch (name) {
      case "Text credibility": return { light: "from-sky-400 to-blue-500", dark: "from-orange-500 to-red-600" };
      case "Image manipulation": return { light: "from-cyan-400 to-indigo-500", dark: "from-yellow-500 to-orange-600" };
      case "Source reliability": return { light: "from-teal-400 to-emerald-500", dark: "from-amber-400 to-yellow-600" };
      case "Claim verification": return { light: "from-purple-400 to-pink-500", dark: "from-rose-500 to-red-600" };
      default: return { light: "from-cyan-400 to-blue-500", dark: "from-orange-500 to-red-600" };
    }
  };

  const getModalityIcon = (name) => {
    switch (name) {
      case "Text credibility": return "📄";
      case "Image manipulation": return "🖼️";
      case "Source reliability": return "🌐";
      case "Claim verification": return "🔍";
      default: return "📊";
    }
  };

  // Chart configurations
  const chartData = result ? {
    labels: result.modality_scores.map(s => s.name),
    datasets: [
      {
        label: 'Modality Fake Probability',
        data: result.modality_scores.map(s => s.fake_probability * 100),
        backgroundColor: darkMode ? 'rgba(249, 115, 22, 0.8)' : 'rgba(14, 165, 233, 0.8)',
        borderColor: darkMode ? '#ea580c' : '#0284c7',
        borderWidth: 2,
        borderRadius: 8,
      }
    ]
  } : null;

  return (
    <div className="min-h-screen relative flex justify-center p-4 overflow-x-hidden bg-sky-50 dark:bg-[#110805] font-sans transition-colors duration-500">
      {/* GLOBAL BACKGROUNDS */}
      <div className="fixed inset-0 w-full h-full pointer-events-none z-0 overflow-hidden">
        {/* Light Theme Tech/Matrix GIF */}
        <div className="absolute inset-0 w-full h-full opacity-30 dark:opacity-0 transition-opacity duration-1000 mix-blend-multiply saturate-50" style={{ backgroundImage: "url('https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTllbmg0dWRxYTUyenB2NHowZTY2d2Q5cjRtaW9yZnQ4M29jYmhybSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1zgzISaYrnMAYRJJEr/giphy.gif')", backgroundSize: "cover", backgroundPosition: "center" }}></div>
        {/* Dark Theme Matrix/Tech GIF */}
        <div className="absolute inset-0 w-full h-full opacity-0 dark:opacity-20 transition-opacity duration-1000 mix-blend-screen" style={{ backgroundImage: "url('https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTllbmg0dWRxYTUyenB2NHowZTY2d2Q5cjRtaW9yZnQ4M29jYmhybSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1zgzISaYrnMAYRJJEr/giphy.gif')", backgroundSize: "cover", backgroundPosition: "center", filter: "contrast(1.5) brightness(0.8)" }}></div>

        {/* Glowing Blobs */}
        <div className="absolute top-[-10%] left-[-10%] w-[40vw] h-[40vw] bg-ocean-light/20 dark:bg-flame-DEFAULT/15 rounded-full blur-[120px] animate-morph pointer-events-none mix-blend-multiply dark:mix-blend-screen"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40vw] h-[40vw] bg-cyan-400/20 dark:bg-red-600/10 rounded-full blur-[120px] animate-morph pointer-events-none mix-blend-multiply dark:mix-blend-screen" style={{ animationDelay: '1.2s' }}></div>
      </div>

      {/* DARK MODE TOGGLE */}
      <button onClick={() => setDarkMode(!darkMode)} className="fixed top-6 right-6 p-3 rounded-full glass-panel text-2xl hover:scale-110 active:scale-95 transition-all z-50 shadow-lg" title="Toggle Visual Mode">
        {darkMode ? '☀️' : '🌙'}
      </button>

      {/* CORE PORTAL LAYOUT */}
      <div className="relative z-10 w-full max-w-7xl flex flex-col min-h-screen">
        
        {/* TOP HEADER */}
        <header className="glass-panel sticky top-4 z-40 shadow-md rounded-2xl mx-2 mt-4 border border-white/20">
          <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-gradient-to-br from-ocean-DEFAULT to-blue-500 dark:from-flame-DEFAULT dark:to-red-600 rounded-xl flex items-center justify-center text-white text-xl shadow-lg">🛡️</div>
              <div>
                <h2 className="text-xl font-display font-extrabold text-cyan-950 dark:text-white">VERITAS FUSION</h2>
                <p className="text-xs text-ocean-DEFAULT dark:text-flame-light font-bold">Multi-Modal Misinformation Pipeline</p>
              </div>
            </div>

            <div className="flex space-x-1 overflow-x-auto max-w-full">
              <NavItem id="workspace" label="Workspace" icon="🛠️" />
              <NavItem id="fusion" label="Fusion Engine" icon="📊" />
              <NavItem id="explain" label="Explanations" icon="🧠" />
              <NavItem id="sandbox" label="Device Sandbox" icon="📱" />
              <NavItem id="architecture" label="Architecture" icon="⚙️" />
            </div>

            <div className="hidden lg:flex items-center gap-4">
              <span className="text-xs font-bold text-emerald-500 dark:text-emerald-400 tracking-wider uppercase flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                Inference Node Active
              </span>
            </div>
          </div>
        </header>

        {/* HERO TITLE AREA */}
        <div className="text-center mt-10 mb-8 animate-fade-in">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-display font-extrabold text-cyan-950 dark:text-white tracking-tight">
            Multi-Modal Fake News <span className="bg-gradient-to-r from-ocean-DEFAULT to-blue-600 dark:from-flame-DEFAULT dark:to-red-500 bg-clip-text text-transparent">& Deepfake Scanner</span>
          </h1>
          <p className="text-cyan-700 dark:text-orange-200/60 mt-3 font-semibold text-lg max-w-2xl mx-auto">
            A state-of-the-art weighted late-fusion framework ensembling textual, source, claim, and visual manipulation signals.
          </p>
        </div>

        {/* MAIN DISPLAY CONTAINER */}
        <main className="flex-1 w-full py-6 pb-20">
          
          {/* 1. WORKSPACE TAB */}
          {activeTab === 'workspace' && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 animate-slide-up">
              
              {/* Left Column: Input Form */}
              <div className="lg:col-span-8 space-y-6">
                <div className="glass-panel p-8 rounded-3xl border border-white/20">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-2xl font-display font-extrabold text-cyan-950 dark:text-orange-50">Scan Workspace</h3>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-cyan-700 dark:text-orange-200/60">Load Sample:</span>
                      <select 
                        onChange={(e) => {
                          const sample = SAMPLES.find(s => s.id === e.target.value);
                          if (sample) loadSample(sample);
                        }} 
                        className="text-xs bg-sky-100 dark:bg-orange-950 text-cyan-900 dark:text-orange-200 px-3 py-1.5 rounded-lg font-bold outline-none border border-cyan-200 dark:border-orange-950"
                      >
                        {SAMPLES.map(s => <option key={s.id} value={s.id}>{s.label}</option>)}
                      </select>
                    </div>
                  </div>

                  <form onSubmit={triggerAnalysis} className="space-y-6">
                    <div className="relative group">
                      <input 
                        type="text" 
                        id="headline" 
                        required
                        placeholder=" " 
                        className="peer w-full px-4 pt-6 pb-2 rounded-xl border-2 border-cyan-200 dark:border-orange-900/50 bg-white/50 dark:bg-[#1f0d06]/50 text-cyan-950 dark:text-orange-50 focus:border-ocean-DEFAULT dark:focus:border-flame-DEFAULT outline-none transition-colors backdrop-blur-sm" 
                        value={headline} 
                        onChange={(e) => setHeadline(e.target.value)} 
                      />
                      <label htmlFor="headline" className="absolute text-sm text-cyan-600 dark:text-orange-300/60 duration-300 transform -translate-y-3 scale-75 top-4 z-10 origin-[0] left-4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-3 peer-focus:text-ocean-DEFAULT dark:peer-focus:text-flame-DEFAULT font-semibold">News Headline</label>
                    </div>

                    <div className="relative group">
                      <textarea 
                        id="article" 
                        required
                        rows="6"
                        placeholder=" " 
                        className="peer w-full px-4 pt-6 pb-2 rounded-xl border-2 border-cyan-200 dark:border-orange-900/50 bg-white/50 dark:bg-[#1f0d06]/50 text-cyan-950 dark:text-orange-50 focus:border-ocean-DEFAULT dark:focus:border-flame-DEFAULT outline-none transition-colors backdrop-blur-sm" 
                        value={article} 
                        onChange={(e) => setArticle(e.target.value)} 
                      />
                      <label htmlFor="article" className="absolute text-sm text-cyan-600 dark:text-orange-300/60 duration-300 transform -translate-y-3 scale-75 top-4 z-10 origin-[0] left-4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-3 peer-focus:text-ocean-DEFAULT dark:peer-focus:text-flame-DEFAULT font-semibold">Article Body Text</label>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="relative group">
                        <input 
                          type="text" 
                          id="source" 
                          placeholder=" " 
                          className="peer w-full px-4 pt-6 pb-2 rounded-xl border-2 border-cyan-200 dark:border-orange-900/50 bg-white/50 dark:bg-[#1f0d06]/50 text-cyan-950 dark:text-orange-50 focus:border-ocean-DEFAULT dark:focus:border-flame-DEFAULT outline-none transition-colors backdrop-blur-sm" 
                          value={source} 
                          onChange={(e) => setSource(e.target.value)} 
                        />
                        <label htmlFor="source" className="absolute text-sm text-cyan-600 dark:text-orange-300/60 duration-300 transform -translate-y-3 scale-75 top-4 z-10 origin-[0] left-4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-3 peer-focus:text-ocean-DEFAULT dark:peer-focus:text-flame-DEFAULT font-semibold">Publisher Domain (e.g. site.com)</label>
                      </div>

                      <div className="relative group">
                        <input 
                          type="text" 
                          id="claim" 
                          placeholder=" " 
                          className="peer w-full px-4 pt-6 pb-2 rounded-xl border-2 border-cyan-200 dark:border-orange-900/50 bg-white/50 dark:bg-[#1f0d06]/50 text-cyan-950 dark:text-orange-50 focus:border-ocean-DEFAULT dark:focus:border-flame-DEFAULT outline-none transition-colors backdrop-blur-sm" 
                          value={claim} 
                          onChange={(e) => setClaim(e.target.value)} 
                        />
                        <label htmlFor="claim" className="absolute text-sm text-cyan-600 dark:text-orange-300/60 duration-300 transform -translate-y-3 scale-75 top-4 z-10 origin-[0] left-4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-3 peer-focus:text-ocean-DEFAULT dark:peer-focus:text-flame-DEFAULT font-semibold">Claim Statement to Verify</label>
                      </div>
                    </div>

                    <div className="relative group">
                      <textarea 
                        id="evidence" 
                        rows="3"
                        placeholder=" " 
                        className="peer w-full px-4 pt-6 pb-2 rounded-xl border-2 border-cyan-200 dark:border-orange-900/50 bg-white/50 dark:bg-[#1f0d06]/50 text-cyan-950 dark:text-orange-50 focus:border-ocean-DEFAULT dark:focus:border-flame-DEFAULT outline-none transition-colors backdrop-blur-sm" 
                        value={evidenceText} 
                        onChange={(e) => setEvidenceText(e.target.value)} 
                      />
                      <label htmlFor="evidence" className="absolute text-sm text-cyan-600 dark:text-orange-300/60 duration-300 transform -translate-y-3 scale-75 top-4 z-10 origin-[0] left-4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-3 peer-focus:text-ocean-DEFAULT dark:peer-focus:text-flame-DEFAULT font-semibold">Trusted Evidence Snippets (One per line)</label>
                    </div>

                    <button 
                      type="submit" 
                      disabled={loading}
                      className="w-full py-4 bg-gradient-to-r from-blue-500 to-blue-700 dark:from-orange-600 dark:to-red-700 text-white rounded-xl font-bold text-lg hover:shadow-[0_10px_20px_rgba(37,99,235,0.3)] dark:hover:shadow-[0_10px_20px_rgba(249,115,22,0.3)] transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center justify-center gap-2"
                    >
                      🛡️ Analyze Modalities & Fuse
                    </button>
                  </form>
                </div>
              </div>

              {/* Right Column: Image Uploader & Help */}
              <div className="lg:col-span-4 space-y-6">
                
                {/* Image Uploader */}
                <div className="glass-panel p-8 rounded-3xl border border-white/20 text-center">
                  <h3 className="text-xl font-display font-extrabold text-cyan-950 dark:text-orange-50 mb-4">Verification Media</h3>
                  
                  {imagePreview ? (
                    <div className="relative group rounded-2xl overflow-hidden border border-cyan-200 dark:border-orange-900/50">
                      <img src={imagePreview} alt="News scan preview" className="w-full h-48 object-cover" />
                      <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <button 
                          onClick={clearImage} 
                          className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg transition-colors"
                        >
                          Remove Image
                        </button>
                      </div>
                    </div>
                  ) : (
                    <label className="border-2 border-dashed border-cyan-300 dark:border-orange-900/60 rounded-2xl p-8 flex flex-col items-center justify-center cursor-pointer hover:border-ocean-DEFAULT dark:hover:border-flame-DEFAULT transition-colors bg-white/30 dark:bg-black/10">
                      <span className="text-4xl mb-3">🖼️</span>
                      <span className="text-sm font-semibold text-cyan-800 dark:text-orange-200/80">Upload news image</span>
                      <span className="text-xs text-cyan-600 dark:text-orange-300/40 mt-1">PNG, JPG, JPEG, WEBP</span>
                      <input type="file" accept="image/*" onChange={handleImageChange} className="hidden" />
                    </label>
                  )}
                  <p className="text-xs text-cyan-600 dark:text-orange-300/60 mt-4 leading-relaxed">
                    Uploading an image triggers active JPEG Error Level Analysis (ELA) and CNN feature forensic signal extractors.
                  </p>
                </div>

                {/* Status Log / Error Panel */}
                {error && (
                  <div className="p-5 rounded-2xl bg-red-500/10 border border-red-500/30 text-red-700 dark:text-red-400 font-medium text-sm flex gap-3">
                    <span className="text-lg">⚠️</span>
                    <div>
                      <span className="font-bold block">Analysis Failed</span>
                      {error}
                    </div>
                  </div>
                )}

                {/* Informational Guidelines */}
                <div className="glass-panel p-6 rounded-3xl border border-white/20 space-y-4">
                  <h4 className="font-bold text-cyan-950 dark:text-orange-200">How Late Fusion Works</h4>
                  <ul className="text-xs text-cyan-800 dark:text-orange-200/70 space-y-2 leading-relaxed list-disc list-inside">
                    <li>The <b>NLP Model</b> analyzes articles for loaded language and structural patterns.</li>
                    <li>The <b>Vision Model</b> detects compression discrepancies and forensic splices.</li>
                    <li>The <b>Source Model</b> verifies domain history and publisher reputation score.</li>
                    <li>The <b>Claim Model</b> cross-references statements against evidence embeddings.</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* LOADING / SCANNING ANIMATION PAGE */}
          {loading && (
            <div className="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex flex-col items-center justify-center text-white">
              <div className="relative w-80 h-80 flex items-center justify-center">
                {/* Glowing Morphing Scan Orb */}
                <div className="absolute w-64 h-64 bg-gradient-to-tr from-ocean-DEFAULT to-blue-600 dark:from-flame-DEFAULT dark:to-red-600 rounded-full blur-[40px] opacity-40 animate-pulse-glow"></div>
                
                {/* Scan Grid Frame */}
                <div className="w-56 h-56 border-2 border-cyan-400 dark:border-orange-500 rounded-3xl flex flex-col items-center justify-center relative overflow-hidden bg-black/40">
                  {/* Neon laser scan line */}
                  <div className="absolute w-full h-1 bg-cyan-400 dark:bg-orange-500 shadow-[0_0_15px_rgba(34,211,238,1)] dark:shadow-[0_0_15px_rgba(249,115,22,1)] top-0 left-0 animate-bounce" style={{ animationDuration: '3s' }}></div>
                  
                  <span className="text-5xl animate-float">🛡️</span>
                  <span className="text-xs font-bold tracking-widest text-cyan-400 dark:text-orange-400 uppercase mt-4">Scanning Content</span>
                </div>
              </div>
              
              <div className="mt-8 text-center px-4 max-w-md">
                <p className="text-xl font-display font-bold text-cyan-100 dark:text-orange-100 animate-pulse">{loadingTexts[loadingStep]}</p>
                <p className="text-sm text-cyan-400/70 dark:text-orange-300/50 mt-2">Connecting to parallel inference GPU node...</p>
              </div>
            </div>
          )}

          {/* 2. FUSION ENGINE RESULTS TAB */}
          {activeTab === 'fusion' && (
            <div className="space-y-10 animate-slide-up">
              {result ? (
                <>
                  {/* Top Dashboard Overview Card */}
                  <div className="relative rounded-3xl overflow-hidden shadow-2xl glass-panel p-8 md:p-12 border border-white/20">
                    <div className="absolute inset-0 bg-gradient-to-r from-cyan-400/5 to-blue-500/5 dark:from-orange-500/5 dark:to-red-600/5 pointer-events-none"></div>
                    <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-8 relative z-10">
                      <div>
                        <span className="text-xs font-bold uppercase tracking-widest px-3 py-1 bg-sky-200 dark:bg-orange-950 text-cyan-800 dark:text-orange-300 rounded-md mb-3 inline-block">Fused Verification Outcome</span>
                        <h2 className="text-3xl md:text-5xl font-display font-extrabold text-cyan-950 dark:text-white mb-2">
                          Status: <span className={result.label === "Fake" ? "text-rose-600 dark:text-rose-500" : "text-emerald-600 dark:text-emerald-500"}>{result.label === "Fake" ? "Unreliable / Misinformation" : "Credible / Real News"}</span>
                        </h2>
                        <p className="text-cyan-800 dark:text-orange-200/70 font-medium text-lg max-w-xl">
                          The system ensembled four distinct data streams. A calibrated risk band of <b>{result.risk_band}</b> was assigned.
                        </p>
                      </div>

                      <div className="flex flex-col md:flex-row gap-6 w-full lg:w-auto">
                        <StatCard title="Fused Fake Index" value={formatPercentage(result.fake_probability)} icon="⚖️" gradientLight="from-sky-400 to-blue-600" gradientDark="from-orange-500 to-red-600" live={result.fake_probability >= 0.5} />
                        <StatCard title="Calibration Confidence" value={formatPercentage(result.confidence)} icon="🔐" gradientLight="from-cyan-400 to-emerald-500" gradientDark="from-amber-400 to-orange-600" />
                      </div>
                    </div>
                  </div>

                  {/* Modality Breakdowns */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {result.modality_scores.map((score, idx) => {
                      const prob = score.fake_probability;
                      const colors = getModalityColor(score.name);
                      return (
                        <div key={score.name} className="glass-panel p-6 rounded-2xl hover:scale-[1.02] transition-transform duration-300 border border-white/10 flex flex-col justify-between">
                          <div>
                            <div className="flex justify-between items-start mb-4">
                              <span className="text-3xl">{getModalityIcon(score.name)}</span>
                              <span className="text-xs font-bold bg-sky-100 dark:bg-black/30 px-2 py-1 rounded text-cyan-800 dark:text-orange-300">Modality #{idx+1}</span>
                            </div>
                            <h4 className="font-display font-bold text-lg text-cyan-950 dark:text-orange-50 mb-1">{score.name}</h4>
                            <p className="text-xs text-cyan-600 dark:text-orange-300/50 uppercase tracking-widest font-extrabold mb-4">Fake Index: {formatPercentage(prob)}</p>
                          </div>
                          
                          <div>
                            {/* Glow bar */}
                            <div className="w-full h-2.5 bg-sky-200/50 dark:bg-black/40 rounded-full overflow-hidden mb-3">
                              <div 
                                className={`h-full bg-gradient-to-r ${darkMode ? colors.dark : colors.light} rounded-full`} 
                                style={{ width: `${prob * 100}%` }}
                              ></div>
                            </div>
                            <p className="text-xs font-bold text-cyan-800 dark:text-orange-100/70 italic">
                              "{score.signals[0] || 'No dominant signal recorded.'}"
                            </p>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {/* Chart and Details Grid */}
                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* Visual Bar Chart */}
                    <div className="lg:col-span-8 glass-panel p-8 rounded-3xl border border-white/20">
                      <h3 className="text-xl font-display font-extrabold text-cyan-950 dark:text-orange-50 mb-6">Inference Model Breakdown</h3>
                      <div className="h-72 flex items-center justify-center">
                        <Bar 
                          data={chartData} 
                          options={{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                              legend: { display: false }
                            },
                            scales: {
                              y: {
                                min: 0,
                                max: 100,
                                ticks: {
                                  color: darkMode ? '#fed7aa' : '#0f172a'
                                },
                                grid: {
                                  color: darkMode ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)'
                                }
                              },
                              x: {
                                ticks: {
                                  color: darkMode ? '#fed7aa' : '#0f172a'
                                },
                                grid: { display: false }
                              }
                            }
                          }} 
                        />
                      </div>
                    </div>

                    {/* Weight Matrix */}
                    <div className="lg:col-span-4 glass-panel p-8 rounded-3xl border border-white/20">
                      <h3 className="text-xl font-display font-extrabold text-cyan-950 dark:text-orange-50 mb-6">Late Fusion Weights</h3>
                      <div className="space-y-4">
                        <div className="flex justify-between items-center text-sm font-semibold">
                          <span className="text-cyan-800 dark:text-orange-200/70">Text semantical weights</span>
                          <span className="text-cyan-950 dark:text-white font-mono">35%</span>
                        </div>
                        <div className="flex justify-between items-center text-sm font-semibold">
                          <span className="text-cyan-800 dark:text-orange-200/70">Vision forensic weights</span>
                          <span className="text-cyan-950 dark:text-white font-mono">25%</span>
                        </div>
                        <div className="flex justify-between items-center text-sm font-semibold">
                          <span className="text-cyan-800 dark:text-orange-200/70">Source reputation priors</span>
                          <span className="text-cyan-950 dark:text-white font-mono">20%</span>
                        </div>
                        <div className="flex justify-between items-center text-sm font-semibold">
                          <span className="text-cyan-800 dark:text-orange-200/70">Claim cross-match weights</span>
                          <span className="text-cyan-950 dark:text-white font-mono">20%</span>
                        </div>
                        <div className="pt-4 border-t border-cyan-200 dark:border-orange-950/60 flex justify-between items-center text-sm font-bold">
                          <span>Total model weights</span>
                          <span className="text-ocean-DEFAULT dark:text-flame-light font-mono">100%</span>
                        </div>
                      </div>
                      <p className="text-xs text-cyan-600 dark:text-orange-300/40 mt-6 leading-relaxed">
                        These weights define the mathematical coefficients used during linear late fusion. Calibration maps raw sums to logistic likelihood.
                      </p>
                    </div>
                  </div>
                </>
              ) : (
                <div className="glass-panel p-16 rounded-3xl text-center border-2 border-dashed border-cyan-200 dark:border-orange-950/60 bg-white/40 dark:bg-black/10">
                  <span className="text-6xl block mb-4">🧪</span>
                  <h3 className="text-2xl font-display font-bold text-cyan-900 dark:text-orange-200 mb-2">No active scan results loaded</h3>
                  <p className="text-cyan-800 dark:text-orange-300/60 max-w-md mx-auto mb-6">
                    Run the Late Fusion pipeline by entering news data on the <b>Workspace</b> tab first.
                  </p>
                  <button onClick={() => setActiveTab('workspace')} className="px-6 py-3 bg-ocean-DEFAULT dark:bg-flame-DEFAULT text-white font-bold rounded-xl shadow-lg hover:-translate-y-0.5 transition-all">
                    Go to Workspace
                  </button>
                </div>
              )}
            </div>
          )}

          {/* 3. EXPLANATIONS TAB */}
          {activeTab === 'explain' && (
            <div className="space-y-8 animate-slide-up max-w-5xl mx-auto">
              {result ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  {/* Left panel: Top Contributing Signals */}
                  <div className="glass-panel p-8 rounded-3xl border border-white/20 space-y-6">
                    <h3 className="text-2xl font-display font-extrabold text-cyan-950 dark:text-orange-50 border-b border-cyan-100 dark:border-orange-950/60 pb-3 flex items-center gap-2">
                      <span>🧠</span> Model Explainability (XAI)
                    </h3>
                    <div className="space-y-4">
                      {result.explanations.map((exp, idx) => (
                        <div key={idx} className="p-4 rounded-xl bg-sky-100/50 dark:bg-black/20 border-l-4 border-ocean-DEFAULT dark:border-flame-DEFAULT text-cyan-950 dark:text-orange-200/80 text-sm leading-relaxed">
                          {exp}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Right panel: Reviewer Actions */}
                  <div className="glass-panel p-8 rounded-3xl border border-white/20 space-y-6">
                    <h3 className="text-2xl font-display font-extrabold text-cyan-950 dark:text-orange-50 border-b border-cyan-100 dark:border-orange-950/60 pb-3 flex items-center gap-2">
                      <span>📝</span> Reviewer Actions Required
                    </h3>
                    <div className="space-y-4">
                      {result.reviewer_actions.map((act, idx) => (
                        <div key={idx} className="p-4 rounded-xl bg-emerald-500/10 dark:bg-emerald-500/5 border-l-4 border-emerald-500 text-cyan-950 dark:text-orange-200/80 text-sm leading-relaxed">
                          {act}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="glass-panel p-16 rounded-3xl text-center border-2 border-dashed border-cyan-200 dark:border-orange-950/60 bg-white/40 dark:bg-black/10">
                  <span className="text-6xl block mb-4">🧠</span>
                  <h3 className="text-2xl font-display font-bold text-cyan-900 dark:text-orange-200 mb-2">No explainability logs</h3>
                  <p className="text-cyan-800 dark:text-orange-300/60 max-w-md mx-auto mb-6">
                    Explainability (SHAP/LIME style logs) generates automatically when you run the pipeline.
                  </p>
                  <button onClick={() => setActiveTab('workspace')} className="px-6 py-3 bg-ocean-DEFAULT dark:bg-flame-DEFAULT text-white font-bold rounded-xl shadow-lg hover:-translate-y-0.5 transition-all">
                    Analyze content first
                  </button>
                </div>
              )}
            </div>
          )}

          {/* 4. INTERACTIVE SANDBOX TAB */}
          {activeTab === 'sandbox' && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center animate-slide-up">
              
              {/* Left Column: Device Sandbox Mockup */}
              <div className="lg:col-span-7 flex justify-center">
                <div className="relative w-full max-w-[480px] p-6 bg-cyan-950 dark:bg-[#1a0b07] rounded-[50px] border-[12px] border-cyan-900 dark:border-orange-950 shadow-2xl overflow-hidden aspect-[9/18]">
                  
                  {/* Phone Header Speaker / Camera */}
                  <div className="absolute top-2 left-1/2 -translate-x-1/2 w-28 h-5 bg-cyan-900 dark:bg-orange-950 rounded-full z-30"></div>
                  
                  {/* Inner Phone Content Area */}
                  <div className="relative w-full h-full bg-[#fafafa] dark:bg-[#120704] rounded-[36px] overflow-hidden flex flex-col p-4">
                    
                    {/* Device Top Status Bar */}
                    <div className="flex justify-between items-center text-[10px] text-cyan-600 dark:text-orange-400 font-bold mb-3 px-2">
                      <span>09:41 📶</span>
                      <span>VeritasNode v1.0</span>
                    </div>

                    {/* Scanned Browser / Webpage View */}
                    <div className="flex-1 bg-white dark:bg-[#1f0f0a] rounded-2xl p-4 border border-cyan-100 dark:border-orange-950 overflow-y-auto space-y-3">
                      <div className="flex items-center gap-1.5 text-[8px] font-bold text-cyan-500 dark:text-orange-400 uppercase">
                        <span>🌐 {source || 'unknownpublisher.com'}</span>
                      </div>
                      <h5 className="text-xs font-bold text-cyan-950 dark:text-white leading-tight">
                        {headline || 'Headline placeholder...'}
                      </h5>
                      <div className="w-full h-1 bg-cyan-100 dark:bg-orange-950 my-1"></div>
                      <p className="text-[10px] text-cyan-800 dark:text-orange-200/70 leading-normal line-clamp-6">
                        {article || 'Article body text will load here. The system scans linguistic and layout sequences...'}
                      </p>

                      {imagePreview && (
                        <div className="relative rounded-lg overflow-hidden border border-cyan-100 dark:border-orange-900/40">
                          <img src={imagePreview} alt="News scan thumbnail" className="w-full h-20 object-cover" />
                        </div>
                      )}
                    </div>

                    {/* Scanning laser glow on the device */}
                    <div className="absolute inset-x-0 h-40 bg-gradient-to-b from-transparent via-cyan-400/20 to-transparent pointer-events-none z-10 animate-bounce" style={{ animationDuration: '4s' }}></div>

                    {/* Device Bottom Button Indicator */}
                    <div className="h-4 flex items-center justify-center mt-3">
                      <div className="w-20 h-1 bg-cyan-800 dark:bg-orange-800 rounded-full"></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column: Rotating Orbit Animation */}
              <div className="lg:col-span-5 flex flex-col items-center justify-center text-center space-y-6">
                <h3 className="text-2xl font-display font-extrabold text-cyan-950 dark:text-orange-50">Interactive Late Fusion Orbit</h3>
                <p className="text-sm text-cyan-800 dark:text-orange-200/70 max-w-sm leading-relaxed">
                  Modality encoders run independently in parallel pipelines. A centralized weighted combiner fuses text, image, source, and claim scores.
                </p>

                {/* Rotating Orbit Container */}
                <div className="relative w-80 h-80 bg-white/30 dark:bg-black/20 rounded-full border border-cyan-200/50 dark:border-orange-950/50 flex items-center justify-center overflow-hidden">
                  
                  {/* Rotating Inner Ring */}
                  <div className="absolute w-60 h-60 border border-dashed border-cyan-300 dark:border-orange-900/40 rounded-full animate-spin" style={{ animationDuration: '24s' }}></div>
                  {/* Rotating Outer Ring */}
                  <div className="absolute w-72 h-72 border border-dashed border-cyan-400/20 dark:border-orange-800/20 rounded-full animate-spin" style={{ animationDuration: '32s', animationDirection: 'reverse' }}></div>

                  {/* Center Node representing output */}
                  <div className="relative z-20 w-24 h-24 rounded-full bg-gradient-to-br from-ocean-DEFAULT to-blue-600 dark:from-flame-DEFAULT to-red-600 text-white flex flex-col items-center justify-center shadow-xl border border-white/20">
                    <span className="text-[10px] font-bold tracking-wider uppercase opacity-70">Fused</span>
                    <span className="text-xl font-bold font-mono">{result ? formatPercentage(result.fake_probability) : '0.0%'}</span>
                  </div>

                  {/* Orbit nodes */}
                  <div className="absolute w-8 h-8 rounded-lg bg-sky-100 dark:bg-orange-950 border border-cyan-200 dark:border-orange-900 flex items-center justify-center text-sm shadow-md animate-float top-8 left-1/2 -translate-x-1/2" title="Text Modality">📄</div>
                  <div className="absolute w-8 h-8 rounded-lg bg-sky-100 dark:bg-orange-950 border border-cyan-200 dark:border-orange-900 flex items-center justify-center text-sm shadow-md animate-float bottom-8 left-1/2 -translate-x-1/2" style={{ animationDelay: '0.5s' }} title="Image Modality">🖼️</div>
                  <div className="absolute w-8 h-8 rounded-lg bg-sky-100 dark:bg-orange-950 border border-cyan-200 dark:border-orange-900 flex items-center justify-center text-sm shadow-md animate-float left-8 top-1/2 -translate-y-1/2" style={{ animationDelay: '1s' }} title="Source Modality">🌐</div>
                  <div className="absolute w-8 h-8 rounded-lg bg-sky-100 dark:bg-orange-950 border border-cyan-200 dark:border-orange-900 flex items-center justify-center text-sm shadow-md animate-float right-8 top-1/2 -translate-y-1/2" style={{ animationDelay: '1.5s' }} title="Claim Modality">🔍</div>
                </div>

                <div className="flex flex-wrap gap-2 justify-center">
                  <span className="px-2.5 py-1 rounded-full bg-sky-100 dark:bg-orange-950/60 text-[10px] font-bold text-cyan-800 dark:text-orange-300">📄 Text Encoders</span>
                  <span className="px-2.5 py-1 rounded-full bg-sky-100 dark:bg-orange-950/60 text-[10px] font-bold text-cyan-800 dark:text-orange-300">🖼️ CV Forensics</span>
                  <span className="px-2.5 py-1 rounded-full bg-sky-100 dark:bg-orange-950/60 text-[10px] font-bold text-cyan-800 dark:text-orange-300">🌐 Domain Prior</span>
                  <span className="px-2.5 py-1 rounded-full bg-sky-100 dark:bg-orange-950/60 text-[10px] font-bold text-cyan-800 dark:text-orange-300">🔍 Claim Verification</span>
                </div>
              </div>
            </div>
          )}

          {/* 5. ARCHITECTURE TAB */}
          {activeTab === 'architecture' && (
            <div className="space-y-10 animate-slide-up">
              <div>
                <h3 className="text-2xl font-display font-extrabold text-cyan-950 dark:text-orange-50 mb-2">Inference Model Architecture</h3>
                <p className="text-sm text-cyan-800 dark:text-orange-200/60 leading-relaxed max-w-2xl">
                  Each feature representation maps to distinct neural models (or baselines) and feeds into a downstream calibrated weights assembler.
                </p>
              </div>

              {/* Architecture Steps grid */}
              <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
                <div className="glass-panel p-6 rounded-2xl border border-white/20 flex flex-col justify-between min-h-[200px]">
                  <div>
                    <span className="text-3xl mb-3 block">📥</span>
                    <h4 className="font-bold text-cyan-950 dark:text-orange-100 mb-2">1. Ingestion</h4>
                    <p className="text-xs text-cyan-800 dark:text-orange-200/60 leading-relaxed">
                      Extract headline, body, domain, claims, evidence list, and optional news images.
                    </p>
                  </div>
                  <span className="text-xs font-bold text-ocean-DEFAULT dark:text-flame-light mt-4">API schema validated</span>
                </div>

                <div className="glass-panel p-6 rounded-2xl border border-white/20 flex flex-col justify-between min-h-[200px]">
                  <div>
                    <span className="text-3xl mb-3 block">📄</span>
                    <h4 className="font-bold text-cyan-950 dark:text-orange-100 mb-2">2. Text Encoder</h4>
                    <p className="text-xs text-cyan-800 dark:text-orange-200/60 leading-relaxed">
                      Baseline linguistic and vocabulary checkers (DistilBERT / RoBERTa compatible).
                    </p>
                  </div>
                  <span className="text-xs font-bold text-ocean-DEFAULT dark:text-flame-light mt-4">NLP pipeline ready</span>
                </div>

                <div className="glass-panel p-6 rounded-2xl border border-white/20 flex flex-col justify-between min-h-[200px]">
                  <div>
                    <span className="text-3xl mb-3 block">🖼️</span>
                    <h4 className="font-bold text-cyan-950 dark:text-orange-100 mb-2">3. Vision Encoder</h4>
                    <p className="text-xs text-cyan-800 dark:text-orange-200/60 leading-relaxed">
                      ELA metadata scanners (CNN/ViT deepfake feature extraction ready).
                    </p>
                  </div>
                  <span className="text-xs font-bold text-ocean-DEFAULT dark:text-flame-light mt-4">Image ELA verified</span>
                </div>

                <div className="glass-panel p-6 rounded-2xl border border-white/20 flex flex-col justify-between min-h-[200px]">
                  <div>
                    <span className="text-3xl mb-3 block">🔍</span>
                    <h4 className="font-bold text-cyan-950 dark:text-orange-100 mb-2">4. Claim Verification</h4>
                    <p className="text-xs text-cyan-800 dark:text-orange-200/60 leading-relaxed">
                      Cosine distance calculation against trusted external evidence database.
                    </p>
                  </div>
                  <span className="text-xs font-bold text-ocean-DEFAULT dark:text-flame-light mt-4">NLI entailment bound</span>
                </div>

                <div className="glass-panel p-6 rounded-2xl border border-white/20 flex flex-col justify-between min-h-[200px]">
                  <div>
                    <span className="text-3xl mb-3 block">⚖️</span>
                    <h4 className="font-bold text-cyan-950 dark:text-orange-100 mb-2">5. Late Fusion</h4>
                    <p className="text-xs text-cyan-800 dark:text-orange-200/60 leading-relaxed">
                      Weighted ensemble combiner with calibrating thresholds to output final risk bounds.
                    </p>
                  </div>
                  <span className="text-xs font-bold text-ocean-DEFAULT dark:text-flame-light mt-4">Weights calibrated</span>
                </div>
              </div>

              {/* Research Datasets Section */}
              <div className="pt-10 border-t border-cyan-200 dark:border-orange-950/60 space-y-6">
                <h4 className="text-xl font-display font-bold text-cyan-950 dark:text-orange-100">Research & Training Datasets</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-2">
                    <h5 className="font-bold text-cyan-900 dark:text-orange-300">FakeNewsNet</h5>
                    <p className="text-xs text-cyan-800 dark:text-orange-200/60 leading-relaxed">
                      Linguistic article text body files combined with social tweets, publisher reputation lists, and verified labels.
                    </p>
                  </div>
                  <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-2">
                    <h5 className="font-bold text-cyan-900 dark:text-orange-300">DFDC & FaceForensics++</h5>
                    <p className="text-xs text-cyan-800 dark:text-orange-200/60 leading-relaxed">
                      Gold-standard benchmark datasets containing original and synthetically generated facial deepfakes.
                    </p>
                  </div>
                  <div className="glass-panel p-6 rounded-2xl border border-white/10 space-y-2">
                    <h5 className="font-bold text-cyan-900 dark:text-orange-300">LIAR Dataset</h5>
                    <p className="text-xs text-cyan-800 dark:text-orange-200/60 leading-relaxed">
                      12,000+ short political claims fact-checked by PolitiFact, ideal for statement-evidence alignment models.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

        </main>
      </div>
    </div>
  );
}

export default App;