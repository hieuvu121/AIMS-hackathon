import os
import zipfile
import io
from typing import List, Tuple

import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

# -----------------
# Page config FIRST
# -----------------
st.set_page_config(
    page_title="Modern Slavery Compliance - Lite Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------
# Light Carriers Style Theme Styling
# -----------------
st.markdown("""
<style>
/* Light Carriers Style Theme Variables */
:root {
    --primary-dark: #1e3a8a;
    --primary-slate: #1e40af;
    --primary-navy: #1e3a8a;
    --accent-orange: #f97316;
    --accent-bright-orange: #ea580c;
    --accent-gold: #fbb040;
    --accent-light-blue: #60a5fa;
    --accent-green: #10b981;
    --white: #ffffff;
    --light-gray: #f8fafc;
    --medium-gray: #e2e8f0;
    --dark-gray: #64748b;
    --text-dark: #0f172a;
    --text-light: #ffffff;
    --text-medium: #334155;
    --shadow-light: rgba(30, 58, 138, 0.1);
    --shadow-medium: rgba(30, 58, 138, 0.15);
    --shadow-orange: rgba(249, 115, 22, 0.2);
    --gradient-primary: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-slate) 100%);
    --gradient-orange: linear-gradient(135deg, var(--accent-orange) 0%, var(--accent-bright-orange) 100%);
    --gradient-gold: linear-gradient(135deg, var(--accent-gold) 0%, var(--accent-orange) 100%);
    --gradient-score: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #059669 100%);
    --border-dark: 3px solid var(--primary-dark);
    --border-orange: 3px solid var(--accent-orange);
}

/* Global App Styling */
.stApp {
    background: #0f172a;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Main content area styling */
.main .block-container {
    background: #0f172a;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.main .block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    background: transparent;
}

/* Professional Headers */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-dark) !important;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
}

h1 {
    font-size: 3rem;
    font-weight: 900;
    color: var(--white) !important;
    text-align: center;
    margin-bottom: 1.5rem;
    letter-spacing: -0.025em;
}

/* Override gradient text for hero section h1 */
.hero-section h1 {
    background: none !important;
    -webkit-background-clip: unset !important;
    -webkit-text-fill-color: #ffffff !important;
    background-clip: unset !important;
    color: #ffffff !important;
}

h2 {
    color: var(--white) !important;
    border-bottom: 2px solid var(--accent-orange);
    padding-bottom: 0.75rem;
    margin-bottom: 2rem;
    font-size: 2rem;
    font-weight: 700;
}

h3 {
    color: var(--white) !important;
    margin-bottom: 1.25rem;
    font-size: 1.5rem;
    font-weight: 600;
}

/* Light Carriers Style Section Frames */
.section-frame {
    background: #1A202C;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3), 0 0 20px rgba(135, 206, 235, 0.3);
    border: 2px solid #87CEEB;
    position: relative;
    overflow: hidden;
    color: var(--white);
}

.section-frame::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--gradient-primary);
}

.compliance-frame {
    background: #1A202C;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3), 0 0 20px rgba(135, 206, 235, 0.3);
    border: 2px solid #87CEEB;
    position: relative;
    overflow: hidden;
    color: var(--white);
}

.compliance-frame::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: var(--gradient-gold);
}

.compliance-frame h2, .compliance-frame h3, .compliance-frame h4, .compliance-frame h5, .compliance-frame h6 {
    color: var(--white) !important;
}

.compliance-frame p, .compliance-frame div {
    color: var(--white) !important;
}

/* Light Carriers Style Hero Section */
.hero-section {
    background: var(--primary-navy);
    padding: 4rem 3rem;
    border-radius: 16px;
    margin-bottom: 3rem;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 300px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    opacity: 0.1;
}

.hero-title {
    color: #ffffff !important;
    font-size: 4rem !important;
    font-weight: 900 !important;
    margin-bottom: 1.5rem;
    letter-spacing: 2px;
    position: relative;
    z-index: 1;
    text-transform: uppercase;
    text-align: center;
    text-shadow: none !important;
    width: 100%;
    max-width: 100%;
}

.hero-section h1 {
    color: #ffffff !important;
}

.hero-section .hero-title {
    color: #ffffff !important;
}

/* Override any Streamlit default h1 styling in hero section */
.hero-section h1.hero-title {
    color: #ffffff !important;
}

/* Force white color for all text in hero section */
.hero-section * {
    color: #ffffff !important;
}

/* Force white color for all text elements */
.stApp * {
    color: #ffffff !important;
}

/* Override specific Streamlit elements */
.stMarkdown, .stMarkdown * {
    color: #ffffff !important;
}

.stText, .stText * {
    color: #ffffff !important;
}

.stSelectbox label, .stSlider label, .stMultiselect label {
    color: #ffffff !important;
}

/* Professional Sidebar styling */
.stSidebar {
    background: #0f172a !important;
    padding: 1rem !important;
}

.stSidebar * {
    color: #ffffff !important;
}

.stSidebar .stSelectbox label,
.stSidebar .stSlider label,
.stSidebar .stMultiselect label {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.5rem !important;
}

/* Professional sidebar widget styling - matching index.py style */
.stSidebar .stSelectbox > div > div,
.stSidebar .stMultiSelect > div > div {
    background-color: var(--bg-secondary) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}

.stSidebar .stSelectbox > div > div:hover,
.stSidebar .stMultiSelect > div > div:hover {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
}

/* Slider styling - target the background track line only */
.stSidebar .stSlider > div {
    background-color: #f97316 !important;
    height: 2px !important;
    border-radius: 1px !important;
}

/* Remove styling from the filled range area */
.stSidebar .stSlider > div > div {
    background: transparent !important;
}

/* Target the track background specifically */
.stSidebar [data-testid="stSlider"] > div {
    background-color: #f97316 !important;
    height: 2px !important;
    border-radius: 1px !important;
}

/* Ensure the range fill doesn't override the track */
.stSidebar .stSlider > div > div[style*="background"] {
    background: transparent !important;
}

/* Sidebar warning styling - matching index.py style */
.stSidebar .stAlert {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1)) !important;
    border: 1px solid var(--warning-color) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    padding: 1rem !important;
    margin: 1rem 0 !important;
}

/* Streamlit widget labels */
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
[data-testid="stMultiselect"] label {
    color: #ffffff !important;
}

/* Selectbox dropdown options styling */
.stSelectbox > div > div {
    background-color: var(--primary-navy) !important;
    color: #ffffff !important;
}

.stSelectbox > div > div > div {
    background-color: var(--primary-navy) !important;
    color: #ffffff !important;
}

/* Selectbox dropdown menu items */
.stSelectbox [role="listbox"] {
    background-color: var(--primary-navy) !important;
}

.stSelectbox [role="option"] {
    background-color: var(--primary-navy) !important;
    color: #ffffff !important;
}

.stSelectbox [role="option"]:hover {
    background-color: var(--accent-orange) !important;
    color: #ffffff !important;
}

/* Override all selectbox text */
.stSelectbox * {
    color: #ffffff !important;
}

/* Additional selectbox styling for dropdown options */
div[data-baseweb="select"] {
    background-color: var(--primary-navy) !important;
}

div[data-baseweb="select"] * {
    color: #ffffff !important;
}

div[data-baseweb="select"] ul {
    background-color: var(--primary-navy) !important;
}

div[data-baseweb="select"] li {
    background-color: var(--primary-navy) !important;
    color: #ffffff !important;
}

div[data-baseweb="select"] li:hover {
    background-color: var(--accent-orange) !important;
    color: #ffffff !important;
}

/* Force white text on all dropdown elements */
[data-testid="stSelectbox"] div[data-baseweb="select"] * {
    color: #ffffff !important;
}

/* Download section selectbox styling - target by data-testid */
div[data-testid="stSelectbox"]:has([data-baseweb="select"][aria-label*="dataset"]) > div > div {
    background: #1e3a8a !important;
    border: 2px solid #f97316 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

div[data-testid="stSelectbox"]:has([data-baseweb="select"][aria-label*="dataset"]) label {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Alternative approach - target all selectboxes in download section */
.stSelectbox > div > div {
    background: #1e3a8a !important;
    border: 2px solid #f97316 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

.stSelectbox label {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Multiselect styling for download section */
.stMultiSelect > div > div {
    background: #1e3a8a !important;
    border: 2px solid #f97316 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

.stMultiSelect label {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Multiselect dropdown options */
.stMultiSelect [role="listbox"] {
    background: #ffffff !important;
    border: 2px solid #f97316 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

.stMultiSelect [role="option"] {
    background: #ffffff !important;
    color: #1e3a8a !important;
    border-radius: 4px !important;
    padding: 8px 12px !important;
}

.stMultiSelect [role="option"]:hover {
    background: #f97316 !important;
    color: #ffffff !important;
}

/* Multiselect selected items */
.stMultiSelect [data-baseweb="tag"] {
    background: #f97316 !important;
    color: #ffffff !important;
    border-radius: 4px !important;
    border: 1px solid #f97316 !important;
}

.stMultiSelect [data-baseweb="tag"]:hover {
    background: #ea580c !important;
    color: #ffffff !important;
}

/* Download section selectbox dropdown options */
.stSelectbox [role="listbox"] {
    background: #1e3a8a !important;
    border: 2px solid #f97316 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}

.stSelectbox [role="option"] {
    background: #1e3a8a !important;
    color: #ffffff !important;
    border-radius: 4px !important;
    padding: 8px 12px !important;
}

.stSelectbox [role="option"]:hover {
    background: #f97316 !important;
    color: #ffffff !important;
}

/* Target dropdown menu specifically */
div[data-baseweb="select"] ul {
    background: #1e3a8a !important;
    border: 2px solid #f97316 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}

div[data-baseweb="select"] li {
    background: #1e3a8a !important;
    color: #ffffff !important;
    border-radius: 4px !important;
    padding: 8px 12px !important;
    margin: 2px !important;
}

div[data-baseweb="select"] li:hover {
    background: #f97316 !important;
    color: #ffffff !important;
}

/* Additional targeting for dropdown menu */
.stSelectbox div[data-baseweb="select"] ul {
    background: #1e3a8a !important;
    border: 2px solid #f97316 !important;
    border-radius: 8px !important;
}

.stSelectbox div[data-baseweb="select"] li {
    background: #1e3a8a !important;
    color: #ffffff !important;
    border-radius: 4px !important;
    padding: 8px 12px !important;
}

.stSelectbox div[data-baseweb="select"] li:hover {
    background: #f97316 !important;
    color: #ffffff !important;
}

/* View Details expander styling with glow effect */
.streamlit-expander {
    background: #1A202C !important;
    border-radius: 16px !important;
    box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3), 0 0 20px rgba(135, 206, 235, 0.3) !important;
    border: 2px solid #87CEEB !important;
    margin: 1rem 0 !important;
    overflow: hidden !important;
}

.streamlit-expanderHeader {
    background: #1A202C !important;
    border: none !important;
    border-radius: 16px 16px 0 0 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    padding: 1rem !important;
    transition: all 0.3s ease !important;
}

.streamlit-expanderHeader:hover {
    background: #2D3748 !important;
    border-color: #87CEEB !important;
}

.streamlit-expanderContent {
    background: #1A202C !important;
    border: none !important;
    border-radius: 0 0 16px 16px !important;
    border-top: 1px solid rgba(135, 206, 235, 0.3) !important;
    padding: 1rem !important;
    color: #ffffff !important;
}

/* Chart container styling with glow effect */
.stPlotlyChart {
    background: #1A202C !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3), 0 0 20px rgba(135, 206, 235, 0.3) !important;
    border: 2px solid #87CEEB !important;
    margin: 1rem 0 !important;
}

/* Altair chart container styling */
.stAltairChart {
    background: #1A202C !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3), 0 0 20px rgba(135, 206, 235, 0.3) !important;
    border: 2px solid #87CEEB !important;
    margin: 1rem 0 !important;
}

/* General chart wrapper */
div[data-testid="stPlotlyChart"],
div[data-testid="stAltairChart"] {
    background: transparent !important;
    border-radius: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
    border: none !important;
    margin: 0 !important;
}

.hero-subtitle {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    opacity: 1;
    line-height: 1.6;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    position: relative;
    z-index: 1;
    color: #ffffff !important;
    font-weight: 700 !important;
    text-shadow: none !important;
    text-align: center;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Light Carriers Style Metrics Cards */
.metric-card {
    background: #1A202C;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3), 0 0 15px rgba(135, 206, 235, 0.2);
    border: 2px solid #87CEEB;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    color: var(--white);
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px var(--shadow-medium);
    border-color: var(--accent-orange);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradient-primary);
}

.metric-label {
    color: var(--white);
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.75rem;
}

.metric-value {
    color: var(--accent-orange);
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1;
    text-shadow: 0 2px 4px var(--shadow-orange);
}

/* Light Carriers Style Findings Cards */
.findings-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.findings-card {
    background: #1A202C;
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3), 0 0 10px rgba(135, 206, 235, 0.2);
    border: 2px solid #87CEEB;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    color: var(--white);
}

.findings-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px var(--shadow-medium);
    border-left-color: var(--primary-dark);
}

.findings-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradient-primary);
}

.findings-percentage {
    font-size: 2.5rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.75rem;
    color: var(--accent-orange);
    text-shadow: 0 2px 4px var(--shadow-orange);
}

.findings-description {
    font-size: 0.9rem;
    text-align: center;
    line-height: 1.4;
    margin-bottom: 0.75rem;
    color: var(--white);
    font-weight: 500;
}

.findings-tag {
    font-size: 0.75rem;
    font-weight: 700;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--white);
    background: rgba(255, 255, 255, 0.1);
    padding: 6px 12px;
    border-radius: 4px;
    display: inline-block;
    margin: 0 auto;
}

/* Criteria Description Styling */
.criteria-description-card {
    background: #1A202C;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3), 0 0 10px rgba(135, 206, 235, 0.2);
    border: 2px solid #87CEEB;
}

.criteria-title {
    color: #ffffff;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-align: center;
}

.criteria-item {
    background: rgba(135, 206, 235, 0.1);
    border-radius: 8px;
    padding: 1rem;
    border-left: 4px solid #87CEEB;
    margin-bottom: 1rem;
}

.criteria-name {
    color: #87CEEB;
    font-size: 1rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
}

.criteria-desc {
    color: #cbd5e1;
    font-size: 0.9rem;
    margin: 0;
    line-height: 1.4;
}

.criteria-info-box {
    background: linear-gradient(135deg, #5078E6 0%, #3250BE 100%);
    border: none;
    border-radius: 12px;
    padding: 15px 30px;
    margin: 1.5rem 0;
    color: #FFFFFF;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}

.criteria-info-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.criteria-info-text {
    color: #FFFFFF;
    font-size: 1.4rem;
    margin: 0;
    font-weight: 700;
    text-align: center;
    position: relative;
    z-index: 1;
}

/* Light Carriers Style Buttons */
.stButton > button {
    background: var(--gradient-orange);
    color: var(--white);
    border: none;
    border-radius: 10px;
    padding: 14px 28px;
    font-weight: 600;
    font-size: 14px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px var(--shadow-orange);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    background: var(--gradient-primary);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--shadow-light);
}

/* Light Carriers Style Sidebar */
.css-1d391kg {
    background: var(--white);
    border-right: 2px solid var(--medium-gray);
    box-shadow: 4px 0 15px var(--shadow-light);
}

.css-1d391kg .stSelectbox > div > div,
.css-1d391kg .stMultiSelect > div > div {
    background: var(--white);
    border: 2px solid var(--medium-gray);
    border-radius: 8px;
    transition: all 0.3s ease;
}

.css-1d391kg .stSelectbox > div > div:hover,
.css-1d391kg .stMultiSelect > div > div:hover {
    border-color: var(--accent-orange);
    box-shadow: 0 0 0 3px var(--shadow-orange);
}

/* Light Carriers Style Charts */
.stPlotlyChart, .vega-embed {
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    background: transparent !important;
    padding: 0 !important;
}

/* Remove white backgrounds and borders from chart elements */
.vega-embed .vega-actions {
    background: transparent !important;
    border: none !important;
}

.vega-embed summary {
    background: transparent !important;
    border: none !important;
    color: #ffffff !important;
}

/* Override Altair chart backgrounds */
.altair-chart,
.altair-chart svg,
.altair-chart .vega-embed {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* Remove black backgrounds from chart SVG elements */
.altair-chart svg {
    background: transparent !important;
    background-color: transparent !important;
}

/* Remove black backgrounds from chart containers */
.altair-chart .vega-embed {
    background: transparent !important;
    background-color: transparent !important;
}

/* Remove backgrounds from chart containers */
div[data-testid="stAltairChart"] .vega-embed,
div[data-testid="stAltairChart"] .vega-embed summary {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* Override any remaining backgrounds */
.vega-embed .vega-embed-wrapper {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* Force transparent background on all chart elements */
.vega-embed,
.vega-embed > div,
.vega-embed .vega-embed-wrapper,
.vega-embed .vega-embed-wrapper > div {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* Remove borders from chart SVG elements */
.vega-embed svg {
    background: transparent !important;
    border: none !important;
}

/* Override backgrounds in chart containers */
div[data-testid="stAltairChart"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

/* Remove black backgrounds from all chart elements */
.vega-embed .vega-embed-wrapper,
.vega-embed .vega-embed-wrapper > div,
.vega-embed .vega-embed-wrapper svg {
    background: transparent !important;
    background-color: transparent !important;
}

/* Force transparent backgrounds on chart SVG elements */
svg {
    background: transparent !important;
    background-color: transparent !important;
}

/* Remove black backgrounds from chart containers */
div[data-testid="stAltairChart"] > div,
div[data-testid="stAltairChart"] > div > div {
    background: transparent !important;
    background-color: transparent !important;
}

/* Remove black backgrounds from Plotly charts */
div[data-testid="stPlotlyChart"] > div,
div[data-testid="stPlotlyChart"] > div > div {
    background: transparent !important;
    background-color: transparent !important;
}

/* Force transparent backgrounds on all chart elements */
.plotly .plotly,
.plotly .main-svg {
    background: transparent !important;
    background-color: transparent !important;
}

/* Remove black backgrounds from chart SVG elements */
.plotly svg {
    background: transparent !important;
    background-color: transparent !important;
}

/* Light Carriers Style Info Boxes */
.stInfo {
    background: linear-gradient(135deg, var(--light-gray) 0%, rgba(74, 85, 104, 0.05) 100%);
    border: 1px solid var(--primary-dark);
    border-radius: 10px;
    border-left: var(--border-dark);
    color: var(--text-dark);
}

.stWarning {
    background: var(--gradient-gold);
    border: 1px solid var(--accent-orange);
    border-radius: 10px;
    border-left: var(--border-orange);
    color: var(--white);
}

.stError {
    background: linear-gradient(135deg, #fed7d7 0%, rgba(239, 68, 68, 0.1) 100%);
    border: 1px solid #e53e3e;
    border-radius: 10px;
    border-left: 3px solid #e53e3e;
    color: var(--text-dark);
}

.stSuccess {
    background: linear-gradient(135deg, #f0fff4 0%, rgba(72, 187, 120, 0.1) 100%);
    border: 1px solid #48bb78;
    border-radius: 10px;
    border-left: 3px solid #48bb78;
    color: var(--text-dark);
}

/* Light Carriers Style Expanders */
.streamlit-expanderHeader {
    background: var(--white);
    border: 2px solid var(--medium-gray);
    border-radius: 10px;
    color: var(--text-dark);
    font-weight: 600;
    transition: all 0.3s ease;
}

.streamlit-expanderHeader:hover {
    background: var(--light-gray);
    border-color: var(--accent-orange);
}

/* Custom styling for download buttons - matching main button style */
.stDownloadButton > button,
.stDownloadButton button,
div[data-testid="stDownloadButton"] > button {
    background: var(--gradient-orange) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 28px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px var(--shadow-orange) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    font-family: inherit !important;
}

.stDownloadButton > button:hover,
.stDownloadButton button:hover,
div[data-testid="stDownloadButton"] > button:hover {
    background: var(--gradient-primary) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px var(--shadow-light) !important;
    color: var(--white) !important;
    font-weight: 600 !important;
}

.streamlit-expanderContent {
    background: var(--white);
    border: 2px solid var(--medium-gray);
    border-top: none;
    border-radius: 0 0 10px 10px;
    padding: 1.5rem;
}

/* Light Carriers Style Download Button */
.stDownloadButton > button {
    background: var(--gradient-primary);
    color: var(--white);
    border: none;
    border-radius: 10px;
    padding: 14px 28px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px var(--shadow-light);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stDownloadButton > button:hover {
    background: var(--gradient-orange);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px var(--shadow-orange);
}

/* Light Carriers Style Metric Containers */
[data-testid="metric-container"] {
    background: var(--white);
    border: 2px solid var(--medium-gray);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 15px var(--shadow-light);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

[data-testid="metric-container"]:hover {
    border-color: var(--accent-orange);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px var(--shadow-medium);
}

[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradient-primary);
}

[data-testid="metric-container"] [data-testid="metric-value"] {
    color: var(--accent-orange);
    font-weight: 800;
    font-size: 2.5rem;
    text-shadow: 0 2px 4px var(--shadow-orange);
}

[data-testid="metric-container"] [data-testid="metric-label"] {
    color: var(--text-dark);
    font-weight: 600;
    font-size: 1rem;
}

/* Light Carriers Style Caption */
.stCaption {
    color: var(--text-medium);
    font-style: italic;
    background: var(--light-gray);
    padding: 12px 16px;
    border-radius: 8px;
    border-left: var(--border-orange);
    margin: 8px 0;
}

/* Light Carriers Style Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--light-gray);
}

::-webkit-scrollbar-thumb {
    background: var(--accent-orange);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary-dark);
}

/* Animation */
@keyframes fadeInUp {
    from { 
        opacity: 0; 
        transform: translateY(30px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}

.main .block-container {
    animation: fadeInUp 0.8s ease-out;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero-section {
        padding: 2rem 1rem;
    }
    
    .hero-title {
        font-size: 2.5rem !important;
    }
    
    .section-frame, .compliance-frame {
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        padding: 1.5rem;
    }
    
    .findings-card {
        padding: 1.5rem;
        min-height: 200px;
    }
}

/* Chart Color Customization */
.vega-embed .vega-actions a {
    color: var(--primary-dark);
}

/* Light Carriers Style Data Tables */
.stDataFrame {
    border: 2px solid var(--medium-gray);
    border-radius: 12px;
    box-shadow: 0 4px 15px var(--shadow-light);
    background: var(--white);
}

/* Text Colors */
p, div:not(.metric-value):not(.findings-percentage), span {
    color: var(--text-dark);
}

/* Light Carriers Style slider styling */
.stSlider > div > div > div {
    background: var(--gradient-primary);
}

.stSlider > div > div > div > div {
    background: var(--white);
    border: 2px solid var(--accent-orange);
}
</style>
""", unsafe_allow_html=True)

# -----------------
# Paths
# -----------------
HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, "au_uk_unified_sectors_merged.csv")
DERIVED_DIR = os.path.join(HERE, "derived")

# -----------------
# Data loading
# -----------------
@st.cache_data(show_spinner=True)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)

    # Normalize helpful columns - use reportdate instead of RegisterYear
    if "reportdate" in df.columns:
        df["RegisterYear"] = pd.to_numeric(df["reportdate"], errors="coerce").astype("Int64")
    elif "reporting_year" in df.columns:
        df["RegisterYear"] = pd.to_numeric(df["reporting_year"], errors="coerce").astype("Int64")
    elif "RegisterYear" in df.columns:
        df["RegisterYear"] = pd.to_numeric(df["RegisterYear"], errors="coerce").astype("Int64")
    else:
        df["RegisterYear"] = pd.NA

    if (df["RegisterYear"].isna().all() or df["RegisterYear"].isna().mean() > 0.5) and ("PeriodEnd" in df.columns):
        period_end_parsed = pd.to_datetime(df["PeriodEnd"], errors="coerce")
        derived_year = period_end_parsed.dt.year.astype("Int64")
        df["RegisterYear"] = df["RegisterYear"].fillna(derived_year)

    if "Entities" not in df.columns:
        df["Entities"] = pd.NA

    if "IndustrySectors" not in df.columns:
        df["IndustrySectors"] = pd.NA

    def yes_to_bool(series: pd.Series) -> pd.Series:
        return series.fillna("").astype(str).str.strip().str.lower().eq("yes")

    for col in [
        "Approval",
        "Signature",
        "c2_structure",
        "c2_operations",
        "c2_supply_chain",
        "c3_risk_description",
        "c4_risk_mitigation",
        "c4_ms_remediation",
        "c5_assess_effectiveness",
    ]:
        if col in df.columns:
            df[col + "__bool"] = yes_to_bool(df[col])
        else:
            df[col + "__bool"] = False

    # Use UnifiedSectors column for unified sectors
    if "UnifiedSectors" in df.columns:
        df["SectorOne"] = df["UnifiedSectors"]
    else:
        def first_sector(value: str) -> str:
            if not isinstance(value, str) or not value.strip():
                return "Unknown"
            return value.split(",")[0].strip()
        df["SectorOne"] = df["IndustrySectors"].apply(first_sector)
    return df

# Check if the data file exists before trying to load it
try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Data file not found at {DATA_PATH}. Please check the file path.")
    st.stop()

# -----------------
# Weights / helpers
# -----------------
WEIGHTS = {
    "Structure & Operation": (0.10, ["c2_structure__bool", "c2_operations__bool"]),
    "Supply Chain": (0.15, ["c2_supply_chain__bool"]),
    "Modern Slavery Risks": (0.30, ["c3_risk_description__bool"]),
    "Due Diligence & Remediation": (0.25, ["c4_risk_mitigation__bool", "c4_ms_remediation__bool"]),
    "Effective Assessment": (0.20, ["c5_assess_effectiveness__bool"]),
}

def compute_weighted_disclosure(df_in: pd.DataFrame) -> pd.DataFrame:
    """Return avg weighted score (%) per sector."""
    if df_in.empty:
        return pd.DataFrame(columns=["SectorOne", "score"])
    rows = []
    for sector, group in df_in.groupby("SectorOne", dropna=False):
        total = 0.0
        for _, (w, cols) in WEIGHTS.items():
            present = [c for c in cols if c in group.columns]
            if not present:
                continue
            category_mean = float(group[present].mean(axis=1).mean()) if len(group) else 0.0
            total += w * category_mean
        rows.append({"SectorOne": sector, "score": total * 100.0})
    return pd.DataFrame(rows)

def compute_weighted_overall(df_in: pd.DataFrame) -> float:
    tmp = compute_weighted_disclosure(df_in)
    return float(tmp["score"].mean()) if not tmp.empty else 0.0

@st.cache_data(show_spinner=True)
def preprocess_and_cache(_df: pd.DataFrame) -> dict:
    os.makedirs(DERIVED_DIR, exist_ok=True)
    out = {}

    # 1) Heatmap data (sector-year)
    rec_scores = []
    for _, row in _df.iterrows():
        total = 0.0
        for _, (w, cols) in WEIGHTS.items():
            present = [c for c in cols if c in _df.columns]
            vals = [bool(row[c]) for c in present] if present else []
            category_mean = (sum(vals) / len(vals)) if vals else 0.0
            total += w * category_mean
        rec_scores.append(total * 100.0)
    tmp = _df.assign(WeightedScore=rec_scores)

    heat = tmp.groupby(["SectorOne", "RegisterYear"], dropna=False)["WeightedScore"].mean().reset_index()
    heat_path = os.path.join(DERIVED_DIR, "sector_year_weighted_compliance.csv")
    heat.to_csv(heat_path, index=False)
    out["heatmap"] = heat_path

    # 2) Disclosure by sector
    disc_df = compute_weighted_disclosure(_df)
    disc_path = os.path.join(DERIVED_DIR, "disclosure_by_sector.csv")
    disc_df.to_csv(disc_path, index=False)
    out["disclosure"] = disc_path

    # 3) Policy vs Action by sector
    bool_cols = [c for c in _df.columns if c.endswith("__bool")]
    pol_cols = [c for c in ["c4_ms_remediation__bool"] if c in bool_cols]
    act_cols = [c for c in ["c4_risk_mitigation__bool"] if c in bool_cols]

    def any_cols_true(frame: pd.DataFrame, cols: list) -> pd.Series:
        if not cols:
            return pd.Series([False] * len(frame), index=frame.index)
        return frame[cols].any(axis=1)

    pa = (
        _df.assign(
            PolicyPresent=any_cols_true(_df, pol_cols),
            ActionTaken=any_cols_true(_df, act_cols),
        )
        .groupby("SectorOne", dropna=False)
        .apply(lambda g: 100.0 * ((g["PolicyPresent"] & ~g["ActionTaken"]).sum() / len(g)))
        .reset_index(name="pct_policy_no_action")
    )
    pa_path = os.path.join(DERIVED_DIR, "policy_vs_action_by_sector.csv")
    pa.to_csv(pa_path, index=False)
    out["policy_action"] = pa_path

    # 4) Level 1 not met trend
    if _df["RegisterYear"].notna().any():
        lev1 = (_df["Approval__bool"] & _df["Signature__bool"]).rename("level1_met")
        trend = (
            pd.concat([_df[["SectorOne", "RegisterYear"]].reset_index(drop=True), lev1.reset_index(drop=True)], axis=1)
            .groupby(["SectorOne", "RegisterYear"], dropna=False)["level1_met"]
            .apply(lambda s: 100.0 * (1.0 - float(s.mean())))
            .reset_index(name="pct_not_meeting_level1")
            .dropna(subset=["RegisterYear"])
        )
        trend_path = os.path.join(DERIVED_DIR, "level1_not_met_trend.csv")
        trend.to_csv(trend_path, index=False)
        out["trend"] = trend_path

    return out

derived_paths = preprocess_and_cache(df)

# -----------------
# Professional Filter Section
# -----------------
st.sidebar.markdown("""
<h3 style="
    color: #ffffff;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
">Data Filters</h3>
""", unsafe_allow_html=True)

# Set fixed year range from 2020 to 2025
year_min, year_max = 2020, 2025
year_range: Tuple[int, int] = st.sidebar.slider(
    "Register Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
    step=1,
    key="year_range"
)

# Check if required columns exist
if "SectorOne" in df.columns and len(df["SectorOne"].dropna()) > 0:
    top_sectors = df["SectorOne"].value_counts().head(5).index.tolist()
    selected_sectors: List[str] = st.sidebar.multiselect(
        "Sectors",
        options=top_sectors,
        default=top_sectors,
        key="sector_picker"
    )
else:
    st.sidebar.warning("No sector data available")
    selected_sectors = []

# Country filter
if "Country" in df.columns and len(df["Country"].dropna()) > 0:
    available_countries = sorted(df["Country"].dropna().unique().tolist())
    selected_countries: List[str] = st.sidebar.multiselect(
        "Countries",
        options=available_countries,
        default=available_countries,
        key="country_picker"
    )
else:
    st.sidebar.warning("No country data available")
    selected_countries = []

st.sidebar.markdown("""
<div style="
    background: #1A202C;
    border-radius: 16px;
    padding: 1rem;
    margin-top: 1.5rem;
    box-shadow: 0 4px 15px rgba(30, 58, 138, 0.2);
    border: 1px solid rgba(135, 206, 235, 0.3);
">
    <div style="
        display: flex;
        align-items: center;
        color: #87CEEB;
        font-size: 0.9rem;
        font-weight: 500;
    ">
        <span>Data source: AIMS-derived CSV</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Apply filters
filtered = df.copy()
if year_range and all(isinstance(v, int) for v in year_range):
    filtered = filtered[filtered["RegisterYear"].between(year_range[0], year_range[1])]

if selected_sectors:
    filtered = filtered[filtered["SectorOne"].isin(selected_sectors)]

if selected_countries:
    filtered = filtered[filtered["Country"].isin(selected_countries)]

# -----------------
# Professional Hero Section
# -----------------
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">LIGHT CARRIER</h1>
    <p class="hero-subtitle">A comprehensive data dashboard evaluating modern slavery reporting across business sectors. Discover insights that go beyond traditional compliance measures.</p>
</div>
""", unsafe_allow_html=True)

# -----------------
# Header
# -----------------

# -----------------
# Data Scope Summary
# -----------------
st.header("Data Scope Summary")

num_companies = filtered["Entities"].nunique(dropna=True) if "Entities" in filtered.columns else 0
num_sectors = filtered["SectorOne"].nunique(dropna=True) if "SectorOne" in filtered.columns else 0
num_countries = filtered["Country"].nunique(dropna=True) if "Country" in filtered.columns else 0
overall_rate = compute_weighted_overall(filtered)


if year_range[0] is not None and year_range[1] is not None:
    current_year_min = int(filtered["RegisterYear"].dropna().min()) if filtered["RegisterYear"].notna().any() else year_range[0]
    current_year_max = int(filtered["RegisterYear"].dropna().max()) if filtered["RegisterYear"].notna().any() else year_range[1]
else:
    current_year_min = current_year_max = None

# Initialize session state for visualization toggle
if 'show_detailed_compliance' not in st.session_state:
    st.session_state.show_detailed_compliance = False

# Create a styled metrics container using Streamlit columns
col_a, col_b, col_c, col_d = st.columns(4)

with col_a:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Companies</div>
        <div class="metric-value">{num_companies:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Sectors</div>
        <div class="metric-value">{num_sectors:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col_c:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Countries</div>
        <div class="metric-value">{num_countries:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col_d:
    year_display = f"{current_year_min}–{current_year_max}" if current_year_min and current_year_max else 'N/A'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Register Years</div>
        <div class="metric-value">{year_display}</div>
    </div>
    """, unsafe_allow_html=True)

# Compliance Distribution Section

st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
st.header("Compliance Rate")
st.markdown("</div>", unsafe_allow_html=True)
st.subheader("Overall Compliance Rate")


if not st.session_state.show_detailed_compliance:
    # Calculate compliance data
    compliant_companies = int(num_companies * overall_rate / 100) if num_companies > 0 else 0
    non_compliant_companies = num_companies - compliant_companies
    non_compliant_percentage = 100 - overall_rate
    
    # Create pie chart data with Light Carriers style colors
    pie_data = pd.DataFrame({
        'Status': ['Compliant', 'Non-Compliant'],
        'Count': [compliant_companies, non_compliant_companies],
        'Percentage': [overall_rate, 100 - overall_rate]
    })
    
    # Create donut chart with Light Carriers theme
    fig_pie = px.pie(pie_data, 
                     values='Count', 
                     names='Status',
                     color='Status',
                     color_discrete_map={'Compliant': '#1e3a8a', 'Non-Compliant': '#f97316'},
                     hole=0.4)
    
    fig_pie.update_traces(textposition='inside', textinfo='percent', textfont_size=14, textfont_color='white')
    fig_pie.update_layout(
        height=300,
        width=300,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    # Professional Light Carriers style frame with both elements
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Export entire Data Scope Summary frame as PNG
    
    # Create a combined figure with all elements
    try:
        # Create a figure that combines the pie chart with metrics
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        
        # Create subplot with 2 rows and 2 columns
        fig_combined = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Overall Compliance", "Data Scope Summary", "", ""),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "table"}, {"type": "table"}]],
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # Add pie chart
        fig_combined.add_trace(
            go.Pie(
                labels=['Compliant', 'Non-Compliant'],
                values=[overall_rate, 100-overall_rate],
                marker_colors=['#1e3a8a', '#f97316'],
                textinfo='percent',
                textfont_size=14,
                textfont_color='white'
            ),
            row=1, col=1
        )
        
        # Add metrics bar chart
        metrics_data = [num_companies, num_sectors, num_countries, 1]  # 1 for countries
        metrics_labels = ['Companies', 'Sectors', 'Countries', 'Years']
        
        fig_combined.add_trace(
            go.Bar(
                x=metrics_labels,
                y=metrics_data,
                marker_color=['#1e3a8a', '#f97316', '#60a5fa', '#10b981'],
                text=metrics_data,
                textposition='auto',
                textfont_color='white'
            ),
            row=1, col=2
        )
        
        # Add summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Companies', f"{num_companies:,}"],
            ['Sectors', f"{num_sectors:,}"],
            ['Countries', f"{num_countries:,}"],
            ['Years', f"{current_year_min}–{current_year_max}"],
            ['Compliance Rate', f"{overall_rate:.1f}%"]
        ]
        
        fig_combined.add_trace(
            go.Table(
                header=dict(
                    values=summary_data[0],
                    fill_color='#1e3a8a',
                    font_color='white',
                    font_size=14
                ),
                cells=dict(
                    values=list(zip(*summary_data[1:])),
                    fill_color='#1A202C',
                    font_color='white',
                    font_size=12
                )
            ),
            row=2, col=1
        )
        
        # Add compliance message
        message_data = [
            ['Key Finding'],
            [f"{100-overall_rate:.1f}% OF COMPANIES ARE FAILING TO EFFECTIVELY MEET THEIR REPORTING OBLIGATIONS"]
        ]
        
        fig_combined.add_trace(
            go.Table(
                header=dict(
                    values=message_data[0],
                    fill_color='#f97316',
                    font_color='white',
                    font_size=16
                ),
                cells=dict(
                    values=message_data[1],
                    fill_color='#1e3a8a',
                    font_color='white',
                    font_size=14
                )
            ),
            row=2, col=2
        )
        
        # Update layout
        fig_combined.update_layout(
            title="📈 Data Scope Summary",
            title_font_size=24,
            title_font_color='white',
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font_color='white',
            height=800,
            width=1200,
            showlegend=False
        )
        
        # Update subplot titles
        fig_combined.update_annotations(font_color='white', font_size=16)
        
        
    except Exception as e:
        st.warning(f"PNG export not available: {str(e)}")
        st.info("Please ensure kaleido is installed: pip install kaleido")
    
    with col_right:
        st.markdown("""
        <div style="
            text-align: left;
            height: 300px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding: 1rem;
            max-width: 300px;
            margin-left: -2rem;
        ">
            <h2 style="
                color: #1e3a8a;
                font-size: 1.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                line-height: 1.2;
            ">SEVERAL COMPANIES ARE FAILING TO EFFECTIVELY MEET THEIR REPORTING OBLIGATIONS</h2>
            <div style="
                width: 100%;
                height: 2px;
                background: #f97316;
                margin: 0.5rem 0;
            "></div>
            <p style="
                color: #1e3a8a;
                font-size: 1.1rem;
                font-weight: 700;
                margin: 0;
                line-height: 1.4;
            ">Nearly one-quarters of statements fail to satisfy all of the minimum requirements set by the MSA legislation.</p>
        </div>
        """, unsafe_allow_html=True)
    
# -----------------
# Year-over-Year Compliance Heatmap (Separate Section)
# -----------------
st.markdown("### Year-over-Year Compliance Heatmap")
st.markdown("Out of all 1,639 sample size we analyze the compliance rate by sectors over time (2020-2025)")

if len(filtered) and "RegisterYear" in filtered.columns:
        # per-record weighted score for heatmap
        rec_scores = []
        for _, row in filtered.iterrows():
            total = 0.0
            for _, (w, cols) in WEIGHTS.items():
                present = [c for c in cols if c in filtered.columns]
                vals = [bool(row[c]) for c in present] if present else []
                category_mean = (sum(vals) / len(vals)) if vals else 0.0
                total += w * category_mean
            rec_scores.append(total * 100.0)
        filtered_with_score = filtered.assign(WeightedScore=rec_scores)

        heat = (
            filtered_with_score.groupby(["SectorOne", "RegisterYear"], dropna=False)["WeightedScore"]
            .mean()
            .reset_index()
            .rename(columns={"WeightedScore": "rate"})
            .dropna(subset=["RegisterYear"])
        )

        if len(heat) > 0:
            # Updated Altair chart with Light Carriers color scheme
            chart = (
                alt.Chart(heat)
                .mark_rect()
                .encode(
                    x=alt.X("RegisterYear:O", title="Year"),
                    y=alt.Y("SectorOne:N", title="Sector"),
                    color=alt.Color("rate:Q", 
                                  scale=alt.Scale(range=["#ffffff", "#fff7ed", "#fed7aa", "#fdba74", "#fb923c", "#f97316", "#ea580c", "#dc2626", "#b45309", "#92400e", "#78350f", "#0f172a"]), 
                                  title="Compliance %"),
                    tooltip=["SectorOne", "RegisterYear", alt.Tooltip("rate:Q", format=".1f")],
                )
            .properties(height=400)
            )
            st.altair_chart(chart, use_container_width=True)
            
            # Export Compliance Rate section as PNG
            try:
                # Create a combined figure for the entire compliance rate section
                from plotly.subplots import make_subplots
                import plotly.graph_objects as go
                
                # Create subplot with 1 row and 2 columns
                fig_compliance = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=("Compliance Rate", "Key Finding"),
                    specs=[[{"type": "pie"}, {"type": "table"}]],
                    vertical_spacing=0.1,
                    horizontal_spacing=0.1
                )
                
                # Add pie chart
                fig_compliance.add_trace(
                    go.Pie(
                        labels=['Compliant', 'Non-Compliant'],
                        values=[overall_rate, 100-overall_rate],
                        marker_colors=['#1e3a8a', '#f97316'],
                        textinfo='percent',
                        textfont_size=14,
                        textfont_color='white',
                        hole=0.4
                    ),
                    row=1, col=1
                )
                
                # Add key finding table
                finding_data = [
                    ['Key Finding'],
                    ['SEVERAL COMPANIES ARE FAILING TO EFFECTIVELY MEET THEIR REPORTING OBLIGATIONS'],
                    ['Nearly one-quarters of statements fail to satisfy all of the minimum requirements set by the MSA legislation.']
                ]
                
                fig_compliance.add_trace(
                    go.Table(
                        header=dict(
                            values=finding_data[0],
                            fill_color='#f97316',
                            font_color='white',
                            font_size=16
                        ),
                        cells=dict(
                            values=finding_data[1:],
                            fill_color='#1e3a8a',
                            font_color='white',
                            font_size=12
                        )
                    ),
                    row=1, col=2
                )
                
                # Update layout
                fig_compliance.update_layout(
                    title="Compliance Rate Analysis",
                    title_font_size=24,
                    title_font_color='white',
                    plot_bgcolor='#0f172a',
                    paper_bgcolor='#0f172a',
                    font_color='white',
                    height=400,
                    width=1000,
                    showlegend=False
                )
                
                # Update subplot titles
                fig_compliance.update_annotations(font_color='white', font_size=16)
                
                # Create download button for PNG
                st.download_button(
                    label="Export Compliance Rate Section as PNG",
                    data=fig_compliance.to_image(format="png", width=1000, height=400),
                    file_name="compliance_rate_section.png",
                    mime="image/png",
                    type="primary"
                )
                
            except Exception as e:
                st.warning(f"PNG export not available: {str(e)}")
                st.info("Please ensure kaleido is installed: pip install kaleido")
        else:
            st.info("No year-over-year data available for heatmap with current filters.")
else:
    st.info("No data available for the selected filters.")


# Show detailed analysis if toggled
if st.session_state.show_detailed_compliance:
    # DETAILED COMPLIANCE ANALYSIS VIEW
    st.markdown('<div class="compliance-frame">', unsafe_allow_html=True)
    st.markdown("#### Detailed Compliance Analysis")
    
    if st.button("← Back to Overview", help="Return to overall compliance pie chart"):
        st.session_state.show_detailed_compliance = False
        st.rerun()

    # 1. Compliance Rate Matrix by Sector
    st.markdown("##### Compliance Rate Matrix by Sector")
    
    disclosure_df = compute_weighted_disclosure(filtered)
    if len(disclosure_df) > 0:
        # Create heatmap matrix with Light Carriers colors
        disclosure_df_sorted = disclosure_df.sort_values('score', ascending=False)
        
        # Create a matrix-style visualization
        fig_matrix = go.Figure(data=go.Heatmap(
            z=[disclosure_df_sorted['score'].values],
            x=disclosure_df_sorted['SectorOne'].values,
            y=['Compliance Rate'],
            colorscale=[[0, "#ffffff"], [0.1, "#fff7ed"], [0.2, "#fed7aa"], [0.3, "#fdba74"], [0.4, "#fb923c"], [0.5, "#f97316"], [0.6, "#ea580c"], [0.7, "#dc2626"], [0.8, "#b45309"], [0.9, "#92400e"], [0.95, "#78350f"], [1, "#0f172a"]],
            colorbar=dict(title="Compliance %"),
            hoverongaps=False,
            hovertemplate='<b>%{x}</b><br>Compliance: %{z:.1f}%<extra></extra>'
        ))
        
        fig_matrix.update_layout(
            title="Compliance Rate Matrix by Sector",
            xaxis_title="Sectors",
            yaxis_title="",
            height=200,
            xaxis={'side': 'bottom'},
            yaxis={'showticklabels': False}
        )
        
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        # Export PNG button for matrix chart
        try:
            st.download_button(
                label="Export Matrix Chart as PNG",
                data=fig_matrix.to_image(format="png"),
                file_name="compliance_matrix.png",
                mime="image/png",
                type="primary"
            )
        except Exception as e:
            st.warning(f"PNG export not available: {str(e)}")
        
        # Add sector details below the matrix
        st.markdown("**Sector Performance Summary**")
        
        # Create columns for sector details
        cols = st.columns(min(3, len(disclosure_df_sorted)))
        for i, (_, row) in enumerate(disclosure_df_sorted.iterrows()):
            with cols[i % len(cols)]:
                # Color code based on compliance level
                if row['score'] >= 80:
                    color = "🟢"
                elif row['score'] >= 60:
                    color = "🟡"
                else:
                    color = "🔴"
                
                st.metric(
                    f"{color} {row['SectorOne']}", 
                    f"{row['score']:.1f}%",
                    help=f"Compliance rate for {row['SectorOne']} sector"
                )
    else:
        st.info("No sector data available for the current filters.")
    



st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
st.header("Disclosure Rate")
st.markdown("</div>", unsafe_allow_html=True)

# -----------------
# MOVED: Average Disclosure Scores by Sector (NOW OUTSIDE THE BUTTON TOGGLE)
# -----------------
st.markdown("### Average Disclosure Scores by Sector")

disclosure_df = compute_weighted_disclosure(filtered)
if len(disclosure_df):
    # Updated chart with Light Carriers gradient colors
    disc_chart = (
        alt.Chart(disclosure_df)
        .mark_bar()
        .encode(
            x=alt.X("SectorOne:N", sort="-y", title="Sector", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("score:Q", title="Avg Disclosure Score (%)"),
            tooltip=["SectorOne", alt.Tooltip("score:Q", format=".1f")],
            color=alt.Color("score:Q", 
                          scale=alt.Scale(range=["#f97316", "#ea580c", "#dc2626", "#7c3aed", "#1e3a8a"]),
                          legend=None),
        )
        .properties(height=300)
    )
    st.altair_chart(disc_chart, use_container_width=True)
    
    # Export PNG button for disclosure chart
    disc_chart_json = disc_chart.to_json()
    st.download_button(
        label="Export Disclosure Chart as PNG",
        data=disc_chart_json,
        file_name="disclosure_scores_by_sector.png",
        mime="image/png",
        type="primary"
    )
else:
    st.info("No disclosure proxy data for current filters.")

# Calculate category-wise scores for filtered data
def calculate_category_scores(df_in: pd.DataFrame) -> pd.DataFrame:
    """Calculate average scores for each category across all companies in filtered data."""
    if df_in.empty:
        return pd.DataFrame()
    
    category_results = []
    for category_name, (weight, cols) in WEIGHTS.items():
        present_cols = [c for c in cols if c in df_in.columns]
        if present_cols:
            # Calculate average for this category across all companies
            category_avg = float(df_in[present_cols].mean(axis=1).mean()) * 100
        else:
            category_avg = 0.0
        
        category_results.append({
            'Category': category_name,
            'Score': category_avg,
            'Weight': weight * 100,
            'Weighted_Score': category_avg * weight
        })
    
    return pd.DataFrame(category_results)
    
# Generate category breakdown
category_df = calculate_category_scores(filtered)

if len(category_df) > 0:
    st.markdown("#### Average Disclosure Score Breakdown by Category")
    st.write("Visualization of average disclosure score out of 100% based on sector filter")
    
    # Create horizontal bar chart showing category scores with Light Carriers theme
    category_chart = alt.Chart(category_df).mark_bar().encode(
        y=alt.Y('Category:N', sort='-x', title='Category', 
                axis=alt.Axis(labelFontSize=11, titleFontSize=12)),
        x=alt.X('Score:Q', title='Average Score (%)', 
                scale=alt.Scale(domain=[0, 100]),
                axis=alt.Axis(labelFontSize=11, titleFontSize=12)),
        color=alt.Color('Score:Q', 
                       scale=alt.Scale(range=["#f97316", "#ea580c", "#dc2626", "#7c3aed", "#1e3a8a"]),
                       legend=None),
        tooltip=[
            alt.Tooltip('Category:N', title='Category'),
            alt.Tooltip('Score:Q', title='Score (%)', format='.1f'),
            alt.Tooltip('Weight:Q', title='Weight (%)', format='.0f')
        ]
    )
    
    st.altair_chart(category_chart, use_container_width=True)
    
    # Export PNG button for category chart
    category_chart_json = category_chart.to_json()
    st.download_button(
        label="Export Category Chart as PNG",
        data=category_chart_json,
        file_name="category_breakdown_chart.png",
        mime="image/png",
        type="primary"
            )
    
    # Summary statistics
    st.markdown("---")
    st.markdown("**Summary Statistics:**")
    
    # Create individual cards for each statistic
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="findings-card">
            <div class="findings-percentage">{category_df['Score'].max():.1f}%</div>
            <div class="findings-description">Highest Category: <strong>{category_df.loc[category_df['Score'].idxmax(), 'Category']}</strong></div>
            <div class="findings-tag">BEST PERFORMER</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="findings-card">
            <div class="findings-percentage">{category_df['Score'].min():.1f}%</div>
            <div class="findings-description">Lowest Category: <strong>{category_df.loc[category_df['Score'].idxmin(), 'Category']}</strong></div>
            <div class="findings-tag">NEEDS IMPROVEMENT</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="findings-card">
            <div class="findings-percentage">{category_df['Score'].mean():.1f}%</div>
            <div class="findings-description">Average Across All Categories</div>
            <div class="findings-tag">OVERALL AVERAGE</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("No data available for category breakdown with current filters.")

with st.expander("Data collection methodology (overview)"):
    st.write(
        "This dashboard reads a consolidated CSV derived from the AIMS dataset. "
        "Sectors are parsed from the first value in `IndustrySectors`. Register year uses `RegisterYear` with fallback to `PeriodEnd`. "
        "Compliance-related charts use proxy fields (e.g., `Approval`, `Signature`, `c2_*`, `c3_*`, `c4_*`, `c5_*`)."
    )


# -----------------
# Policy vs Action Analysis
# -----------------
st.markdown('<div class="compliance-frame">', unsafe_allow_html=True)
st.subheader("Remediation Policy vs Boilerplate Content")
st.markdown("***This section compares whether companies disclose remediation policies versus taking concrete actions. It highlights how often disclosures rely on boilerplate wording, making it harder to assess genuine implementation across sectors.***")

# Add data quality warning
st.warning("**Data Quality Note**: Analysis shows significant boilerplate content in compliance disclosures. "
          "Results should be interpreted with caution as many responses contain vague, generic language rather than specific policy details.")

if len(filtered):
    # Enhanced analysis that accounts for boilerplate content
    def analyze_policy_substance(row, pol_cols, act_cols):
        """Analyze if policies contain substantive content vs boilerplate"""
        present_pol = [c for c in pol_cols if c in filtered.columns]
        present_act = [c for c in act_cols if c in filtered.columns]
        
        has_policy = any(bool(row[c]) for c in present_pol) if present_pol else False
        has_action = any(bool(row[c]) for c in present_act) if present_act else False
        
        # Classify based on policy/action presence
        if has_policy and has_action:
            return "Policy + Action"
        elif has_policy and not has_action:
            return "Policy Only (Potential Boilerplate)"
        elif not has_policy and has_action:
            return "Action Only"
        else:
            return "Neither Policy nor Action"

    pol_cols = ["c4_ms_remediation__bool"]
    act_cols = ["c4_risk_mitigation__bool"]

    # Apply enhanced analysis
    policy_analysis = filtered.apply(
        lambda r: analyze_policy_substance(r, pol_cols, act_cols), axis=1
    )
    
    # Create sector-wise breakdown
    sector_policy_breakdown = (
        pd.DataFrame({
            'SectorOne': filtered['SectorOne'],
            'PolicyType': policy_analysis
        })
        .groupby(['SectorOne', 'PolicyType'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )
    
    # Calculate percentages for better interpretation
    if len(sector_policy_breakdown) > 0:
        # Melt for visualization
        sector_policy_melted = sector_policy_breakdown.melt(
            id_vars=['SectorOne'], 
            var_name='PolicyType', 
            value_name='Count'
        )
        
        # Calculate total per sector for percentage
        sector_totals = sector_policy_melted.groupby('SectorOne')['Count'].sum().reset_index()
        sector_totals.columns = ['SectorOne', 'Total']
        
        sector_policy_melted = sector_policy_melted.merge(sector_totals, on='SectorOne')
        sector_policy_melted['Percentage'] = (sector_policy_melted['Count'] / sector_policy_melted['Total']) * 100
        
        # Create horizontal stacked bar chart with Light Carriers colors
        policy_chart = alt.Chart(sector_policy_melted).mark_bar().encode(
            y=alt.Y('SectorOne:N', title='Sector'),
            x=alt.X('Percentage:Q', title='Percentage of Companies'),
            color=alt.Color('PolicyType:N', 
                          scale=alt.Scale(
                              domain=['Policy + Action', 'Policy Only (Potential Boilerplate)', 'Action Only', 'Neither Policy nor Action'],
                              range=['#1e3a8a', '#f97316', '#ea580c', '#7c3aed']
                          ),
                          title='Policy Implementation Type'),
            tooltip=['SectorOne:N', 'PolicyType:N', 
                    alt.Tooltip('Percentage:Q', format='.1f', title='Percentage'), 
                    alt.Tooltip('Count:Q', title='Count')]
        ).properties(
            height=400,
            title="Policy vs Action Implementation by Sector"
        )
        
        st.altair_chart(policy_chart, use_container_width=True)
        
        # Export PNG button for policy chart
        policy_chart_json = policy_chart.to_json()
        st.download_button(
            label="Export Policy Chart as PNG",
            data=policy_chart_json,
            file_name="policy_vs_action_chart.png",
            mime="image/png",
            type="primary"
        )
    
    else:
        st.info("Insufficient data for policy vs action analysis with current filters.")

else:
    st.info("No data available for policy vs action analysis with current filters.")


# -----------------
# Level 1 Compliance by Sector - MODIFIED TO USE HORIZONTAL BAR CHARTS
# -----------------
st.header("Statement Minimum Requirement")
st.markdown("""
<div style="font-style: italic; font-size: 1.1rem; color: #94a3b8; margin-bottom: 1rem; line-height: 1.5;">
This section evaluates whether companies meet the minimum Level 1 reporting requirement under the Modern Slavery Act. Alongside overall and sector-level compliance rates, the trend graph tracks changes over time, showing fluctuations in non-compliance across industries and highlighting which sectors have improved or lagged in meeting the baseline standard.
</div>
""", unsafe_allow_html=True)

if len(filtered):
    if ("Approval__bool" in filtered.columns) and ("Signature__bool" in filtered.columns):
        # Calculate Level 1 compliance (both Approval and Signature)
        level1_met = filtered[["Approval__bool", "Signature__bool"]].all(axis=1)
        
        compliant_count = level1_met.sum()
        non_compliant_count = len(level1_met) - compliant_count
        total_companies = len(level1_met)
        
        # Calculate sector-wise compliance
        sector_level1 = (
            filtered.assign(level1_met=level1_met)
            .groupby("SectorOne", dropna=False)["level1_met"]
            .agg(['mean', 'count'])
            .reset_index()
        )
        sector_level1['pct_meeting_level1'] = sector_level1['mean'] * 100
        sector_level1['company_count'] = sector_level1['count']
        
        if len(sector_level1) > 0:
            # Create two-column layout: pie chart on left, bar chart on right
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                # Overall Level 1 compliance pie chart with navy-orange colors
                st.subheader("Overall Minimum Statement Requirement")
                
                if total_companies > 0:
                    pie_data_level1 = pd.DataFrame({
                        'Status': ['Meets Level 1', 'Does Not Meet Level 1'],
                        'Count': [compliant_count, non_compliant_count],
                        'Percentage': [
                            (compliant_count / total_companies) * 100,
                            (non_compliant_count / total_companies) * 100
                        ]
                    })
                    
                    fig_pie_level1 = px.pie(
                        pie_data_level1,
                        values='Count',
                        names='Status',
                        color='Status',
                        color_discrete_map={
                            'Meets Level 1': '#1e3a8a',
                            'Does Not Meet Level 1': '#f97316'
                        },
                        title=f"Sample of ({total_companies:,} companies)"
                    )
                    fig_pie_level1.update_traces(textposition='inside', textinfo='percent+label')
                    fig_pie_level1.update_layout(height=400, showlegend=True)
                    st.plotly_chart(fig_pie_level1, use_container_width=True)
                    
                    
                    # Summary metric below pie chart
                    compliance_rate = (compliant_count / total_companies) * 100
                    st.metric(
                        "Overall Minimum Statement Requirement Rate",
                        f"{compliance_rate:.1f}%",
                        f"{compliant_count:,} of {total_companies:,} companies"
                    )
            
            with col_right:
                # Horizontal bar chart by sector
                st.subheader("Statement minimum requirement by sector")
                
                # Sort sectors by compliance rate for better visualization
                sector_level1_sorted = sector_level1.sort_values('pct_meeting_level1', ascending=True)
                
                # Create horizontal bar chart data
                bar_data = []
                for _, row in sector_level1_sorted.iterrows():
                    compliant_pct = row['pct_meeting_level1']
                    non_compliant_pct = 100 - compliant_pct
                    
                    bar_data.append({
                        'Sector': row['SectorOne'],
                        'Status': 'Compliant', 
                        'Percentage': compliant_pct,
                        'Count': int(row['company_count'] * compliant_pct / 100),
                        'Total_Companies': int(row['company_count'])
                    })
                    bar_data.append({
                        'Sector': row['SectorOne'],
                        'Status': 'Non-Compliant',
                        'Percentage': non_compliant_pct, 
                        'Count': int(row['company_count'] * non_compliant_pct / 100),
                        'Total_Companies': int(row['company_count'])
                    })
                
                bar_df = pd.DataFrame(bar_data)
                
                # Create horizontal stacked bar chart with Light Carriers colors
                level1_bar_chart = alt.Chart(bar_df).mark_bar().encode(
                    y=alt.Y('Sector:N', 
                           sort=alt.EncodingSortField(field='Percentage', op='mean', order='descending'),
                           title='Sector',
                           axis=alt.Axis(labelFontSize=11)),
                    x=alt.X('Percentage:Q', 
                           title='Percentage',
                           axis=alt.Axis(labelFontSize=10)),
                    color=alt.Color('Status:N',
                                  scale=alt.Scale(
                                      domain=['Compliant', 'Non-Compliant'],
                                      range=['#1e3a8a', '#f97316']
                                  ),
                                  legend=alt.Legend(title="Status")),
                    tooltip=[
                        alt.Tooltip('Sector:N', title='Sector'),
                        alt.Tooltip('Status:N', title='Status'),
                        alt.Tooltip('Percentage:Q', format='.1f', title='Percentage'),
                        alt.Tooltip('Count:Q', title='Companies'),
                        alt.Tooltip('Total_Companies:Q', title='Total Companies')
                    ]
                ).properties(
                    height=400,
                    title="Compliance by Sector"
                ).resolve_scale(
                    color='independent'
                )
                
                st.altair_chart(level1_bar_chart, use_container_width=True)
                
            
            # Add compliance rate labels on the right side of bars
            st.markdown("##### Sector Compliance Rates")
            
            # Create a more detailed breakdown
            cols = st.columns(min(3, len(sector_level1_sorted)))
            for i, (_, row) in enumerate(sector_level1_sorted.sort_values('pct_meeting_level1', ascending=False).iterrows()):
                with cols[i % len(cols)]:
                    # Color coding
                    if row['pct_meeting_level1'] >= 90:
                        color = "🟢"
                        status = "Excellent"
                    elif row['pct_meeting_level1'] >= 75:
                        color = "🟡"
                        status = "Good"
                    elif row['pct_meeting_level1'] >= 50:
                        color = "🟠"
                        status = "Needs Improvement"
                    else:
                        color = "🔴"
                        status = "Poor"
                    
                    st.metric(
                        f"{color} {row['SectorOne'][:20]}{'...' if len(row['SectorOne']) > 20 else ''}", 
                        f"{row['pct_meeting_level1']:.1f}%",
                        f"{int(row['company_count'])} companies",
                        help=f"{status} - {row['pct_meeting_level1']:.1f}% compliance rate"
                    )
            
            # Overall summary metrics
            st.markdown("##### Summary Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            if total_companies > 0:
                overall_compliance_rate = (compliant_count / total_companies) * 100
                best_sector = sector_level1.loc[sector_level1['pct_meeting_level1'].idxmax()]
                worst_sector = sector_level1.loc[sector_level1['pct_meeting_level1'].idxmin()]
                
                with col1:
                    st.metric(
                        "Overall Compliance Rate",
                        f"{overall_compliance_rate:.1f}%",
                        f"{compliant_count:,} of {total_companies:,}"
                    )
                with col2:
                    st.metric(
                        "Best Performing Sector", 
                        best_sector['SectorOne'][:15] + ('...' if len(best_sector['SectorOne']) > 15 else ''),
                        f"{best_sector['pct_meeting_level1']:.1f}%"
                    )
                with col3:
                    st.metric(
                        "Worst Performing Sector", 
                        worst_sector['SectorOne'][:15] + ('...' if len(worst_sector['SectorOne']) > 15 else ''),
                        f"{worst_sector['pct_meeting_level1']:.1f}%"
                    )
                with col4:
                    st.metric(
                        "Average Across Sectors", 
                        f"{sector_level1['pct_meeting_level1'].mean():.1f}%",
                        f"{len(sector_level1)} sectors"
                    )
                
        else:
            st.info("No Level 1 compliance data available for current filters.")
                
    else:
        st.warning("Approval and/or Signature columns not found in the dataset.")
else:
    st.info("No data available for Level 1 compliance analysis.")


# -----------------
# Minimum Requirement Trend
# -----------------
st.subheader("Minimum Requirement Trend")
st.caption("Level 1 minimum = both Approval and Signature marked Yes.")

if len(filtered) and filtered["RegisterYear"].notna().any():
    if ("Approval__bool" in filtered.columns) and ("Signature__bool" in filtered.columns):
        lev1_series = filtered[["Approval__bool", "Signature__bool"]].all(axis=1)
    else:
        lev1_series = pd.Series([False] * len(filtered), index=filtered.index)

    lev1 = lev1_series.rename("level1_met")
    trend = (
        pd.concat([filtered[["SectorOne", "RegisterYear"]].reset_index(drop=True), lev1.reset_index(drop=True)], axis=1)
        .groupby(["SectorOne", "RegisterYear"], dropna=False)["level1_met"]
        .apply(lambda s: 100.0 * (1.0 - float(s.mean())))
        .reset_index(name="pct_not_meeting_level1")
        .dropna(subset=["RegisterYear"])
    )

    # Create trend chart with Light Carriers color scheme
    trend_chart = (
        alt.Chart(trend)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("RegisterYear:O", title="Year"),
            y=alt.Y("pct_not_meeting_level1:Q", title="% Not Meeting Level 1"),
            color=alt.Color("SectorOne:N", 
                          scale=alt.Scale(range=["#1e3a8a", "#7c3aed", "#f97316", "#ea580c", "#dc2626"]),
                          title="Sector"),
            tooltip=["SectorOne", "RegisterYear", alt.Tooltip("pct_not_meeting_level1:Q", format=".1f")],
        )
        .properties(height=300)
    )
    st.altair_chart(trend_chart, use_container_width=True)
    
    # Export entire Statement Minimum Requirement section as PNG
    try:
        # Create a combined figure for the entire Statement Minimum Requirement section
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        
        # Create subplot with 2 rows and 2 columns
        fig_statement = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Level 1 Compliance by Sector", "Compliance Trend Over Time", "Sector Breakdown", "Summary"),
            specs=[[{"type": "pie"}, {"type": "scatter"}], [{"type": "bar"}, {"type": "table"}]],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # Add pie chart (Level 1 compliance)
        if len(filtered) and ("Approval__bool" in filtered.columns) and ("Signature__bool" in filtered.columns):
            level1_met = filtered[["Approval__bool", "Signature__bool"]].all(axis=1)
            compliant_count = level1_met.sum()
            total_companies = len(filtered)
            compliance_rate = (compliant_count / total_companies) * 100 if total_companies > 0 else 0
            
            fig_statement.add_trace(
                go.Pie(
                    labels=['Compliant', 'Non-Compliant'],
                    values=[compliance_rate, 100-compliance_rate],
                    marker_colors=['#1e3a8a', '#f97316'],
                    textinfo='percent',
                    textfont_size=12,
                    textfont_color='white',
                    hole=0.4
                ),
                row=1, col=1
            )
        
        # Add trend chart (simplified)
        if len(filtered) and "RegisterYear" in filtered.columns:
            yearly_data = filtered.groupby('RegisterYear').size().reset_index(name='count')
            fig_statement.add_trace(
                go.Scatter(
                    x=yearly_data['RegisterYear'],
                    y=yearly_data['count'],
                    mode='lines+markers',
                    line=dict(color='#f97316', width=3),
                    marker=dict(size=8, color='#1e3a8a')
                ),
                row=1, col=2
            )
        
        # Add sector breakdown (simplified bar chart)
        if len(filtered) and "SectorOne" in filtered.columns:
            sector_counts = filtered['SectorOne'].value_counts().head(5)
            fig_statement.add_trace(
                go.Bar(
                    x=sector_counts.index,
                    y=sector_counts.values,
                    marker_color='#1e3a8a'
                ),
                row=2, col=1
            )
        
        # Add summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Total Companies', f"{total_companies:,}"],
            ['Compliant Companies', f"{compliant_count:,}"],
            ['Compliance Rate', f"{compliance_rate:.1f}%"],
            ['Sectors Analyzed', f"{len(filtered['SectorOne'].unique()) if 'SectorOne' in filtered.columns else 0}"]
        ]
        
        fig_statement.add_trace(
            go.Table(
                header=dict(
                    values=summary_data[0],
                    fill_color='#f97316',
                    font_color='white',
                    font_size=14
                ),
                cells=dict(
                    values=list(zip(*summary_data[1:])),
                    fill_color='#1e3a8a',
                    font_color='white',
                    font_size=12
                )
            ),
            row=2, col=2
        )
        
        # Update layout
        fig_statement.update_layout(
            title="Statement Minimum Requirement Analysis",
            title_font_size=24,
            title_font_color='white',
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            font_color='white',
            height=800,
            width=1200,
            showlegend=False
        )
        
        # Update subplot titles
        fig_statement.update_annotations(font_color='white', font_size=14)
        
        # Create download button for PNG
        st.download_button(
            label="Export Statement Minimum Requirement Section as PNG",
            data=fig_statement.to_image(format="png", width=1200, height=800),
            file_name="statement_minimum_requirement_section.png",
            mime="image/png",
            type="primary"
        )
        
    except Exception as e:
        st.warning(f"PNG export not available: {str(e)}")
        st.info("Please ensure kaleido is installed: pip install kaleido")
else:
    st.info("No year data available for trend chart with current filters.")



# -----------------
# Key Findings
# -----------------
st.header("Company Performance On Key Criterias In Modern Slavery Report Template")

# FURTHER FINDINGS - 7 Dropdown Blocks in Grid Layout
st.markdown("This section displays a comprehensive overview of company performance across seven key criteria for modern slavery reporting, with each panel showing the overall achievement percentage and providing expandable details for deeper analysis. ")

# Add detailed description of the 7 international reporting criteria
st.markdown("""
<div class="criteria-description-card">
    <h3 class="criteria-title">The 7 International Reporting Criteria for Modern Slavery</h3>
</div>
""", unsafe_allow_html=True)

# Add the criteria descriptions using simpler approach
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="criteria-item">
        <h4 class="criteria-name">Criteria 1: Structure & Operation</h4>
        <p class="criteria-desc">Organizational structure, policies, and operational frameworks for addressing modern slavery risks.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="criteria-item">
        <h4 class="criteria-name">Criteria 2: Due Diligence & Remediation</h4>
        <p class="criteria-desc">Processes for identifying, assessing, and addressing modern slavery risks in operations and supply chains.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="criteria-item">
        <h4 class="criteria-name">Criteria 3: Risk Assessment</h4>
        <p class="criteria-desc">Comprehensive risk identification and assessment procedures for modern slavery vulnerabilities.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="criteria-item">
        <h4 class="criteria-name">Criteria 4: Training & Awareness</h4>
        <p class="criteria-desc">Employee training programs and awareness initiatives to recognize and prevent modern slavery.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="criteria-item">
        <h4 class="criteria-name">Criteria 5: Supply Chain Management</h4>
        <p class="criteria-desc">Policies and procedures for managing modern slavery risks throughout the supply chain.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="criteria-item">
        <h4 class="criteria-name">Criteria 6: Monitoring & Review</h4>
        <p class="criteria-desc">Ongoing monitoring systems and regular review processes to ensure effectiveness of anti-slavery measures.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="criteria-item">
        <h4 class="criteria-name">Criteria 7: Reporting & Transparency</h4>
        <p class="criteria-desc">Transparent reporting mechanisms and disclosure practices regarding modern slavery efforts and outcomes.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="criteria-info-box">
    <p class="criteria-info-text">Each criterion below shows the overall achievement percentage across all companies, with detailed breakdowns available by clicking "View Details"</p>
</div>
""", unsafe_allow_html=True)

# Create 2 columns for the first row
col1, col2 = st.columns(2, gap="medium")

# Create 2 columns for the second row
col3, col4 = st.columns(2, gap="medium")

# Create 3 columns for the third row
col5, col6, col7 = st.columns(3, gap="medium")

# Block 1: CRITERIA 1 ACHIEVEMENT
with col1:
    # Load criteria 1 data
    try:
        criteria1_df = pd.read_csv(os.path.join(HERE, 'criteria_1_final_summary.csv'))
        overall_achievement = criteria1_df[criteria1_df['Metric'] == 'Overall Criteria 1 Achievement']['Achievement_Percentage'].iloc[0]
        overall_notes = criteria1_df[criteria1_df['Metric'] == 'Overall Criteria 1 Achievement']['Notes'].iloc[0]
    except (FileNotFoundError, IndexError, KeyError):
        overall_achievement = 0.0
        overall_notes = "Data not available"
    
    # Custom styled card with navy-orange theme
    st.markdown(f"""
    <div class="findings-card" onclick="this.nextElementSibling.querySelector('button').click()">
        <div class="findings-percentage">{overall_achievement:.1f}%</div>
        <div class="findings-description">Overall <strong>Criteria 1 Achievement</strong> across all companies</div>
        <div class="findings-tag">CRITERIA 1 ></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Separate expander for detailed content
    with st.expander("View Details", expanded=False):
        st.markdown("#### Criteria 1 Detailed Breakdown")
        
        # Display detailed metrics from CSV
        if 'criteria1_df' in locals():
            # Filter out the overall achievement row for detailed breakdown
            detailed_metrics = criteria1_df[criteria1_df['Metric'] != 'Overall Criteria 1 Achievement'].copy()
            
            if not detailed_metrics.empty:
                # Create a horizontal bar chart for the detailed metrics with navy-orange colors
                chart_data = detailed_metrics[['Metric', 'Achievement_Percentage']].copy()
                chart_data = chart_data[chart_data['Achievement_Percentage'] > 0]  # Filter out zero values
                
                if not chart_data.empty:
                    criteria_chart = alt.Chart(chart_data).mark_bar().encode(
                        y=alt.Y('Metric:N', sort='-x', title='Criteria 1 Metrics'),
                        x=alt.X('Achievement_Percentage:Q', title='Achievement Percentage (%)', scale=alt.Scale(domain=[0, 100])),
                        color=alt.Color('Achievement_Percentage:Q', 
                                     scale=alt.Scale(range=["#f97316", "#ea580c", "#dc2626", "#7c3aed", "#1e3a8a"]),
                                     legend=None),
                        tooltip=['Metric:N', alt.Tooltip('Achievement_Percentage:Q', format='.1f', title='Achievement %')]
                    ).properties(
                        height=400,
                        title="Criteria 1 Achievement by Metric"
                    )
                    
                    st.altair_chart(criteria_chart, use_container_width=True)
            else:
                st.info("No detailed metrics available in the data.")
        else:
            st.error("Could not load criteria 1 data. Please ensure 'criteria_1_final_summary.csv' is available.")

# Block 2: CRITERIA 2 ACHIEVEMENT
with col2:
    # Load criteria 2 data
    try:
        criteria2_df = pd.read_csv(os.path.join(HERE, 'criteria2_final_summary.csv'))
        overall_achievement = criteria2_df[criteria2_df['Metric'] == 'Overall Criteria 2 Achievement']['Achievement_Percentage'].iloc[0]
        overall_notes = criteria2_df[criteria2_df['Metric'] == 'Overall Criteria 2 Achievement']['Notes'].iloc[0]
    except (FileNotFoundError, IndexError, KeyError):
        overall_achievement = 0.0
        overall_notes = "Data not available"
    
    # Custom styled card with navy-orange theme
    st.markdown(f"""
    <div class="findings-card" onclick="this.nextElementSibling.querySelector('button').click()">
        <div class="findings-percentage">{overall_achievement:.1f}%</div>
        <div class="findings-description">Overall <strong>Criteria 2 Achievement</strong> across all companies</div>
        <div class="findings-tag">CRITERIA 2 ></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Separate expander for detailed content
    with st.expander("View Details", expanded=False):
        st.markdown("#### Criteria 2 Detailed Breakdown")
        
        # Display detailed metrics from CSV
        if 'criteria2_df' in locals():
            # Filter out the overall achievement row for detailed breakdown
            detailed_metrics = criteria2_df[criteria2_df['Metric'] != 'Overall Criteria 2 Achievement'].copy()
            
            if not detailed_metrics.empty:
                # Create a horizontal bar chart for the detailed metrics with Light Carriers colors
                chart_data = detailed_metrics[['Metric', 'Achievement_Percentage']].copy()
                chart_data = chart_data[chart_data['Achievement_Percentage'] > 0]  # Filter out zero values
                
                if not chart_data.empty:
                    criteria_chart = alt.Chart(chart_data).mark_bar().encode(
                        y=alt.Y('Metric:N', sort='-x', title='Criteria 2 Metrics'),
                        x=alt.X('Achievement_Percentage:Q', title='Achievement Percentage (%)', scale=alt.Scale(domain=[0, 100])),
                        color=alt.Color('Achievement_Percentage:Q', 
                                     scale=alt.Scale(range=["#f97316", "#ea580c", "#dc2626", "#7c3aed", "#1e3a8a"]),
                                     legend=None),
                        tooltip=['Metric:N', alt.Tooltip('Achievement_Percentage:Q', format='.1f', title='Achievement %')]
                    ).properties(
                        height=400,
                        title="Criteria 2 Achievement by Metric"
                    )
                    
                    st.altair_chart(criteria_chart, use_container_width=True)
            else:
                st.info("No detailed metrics available in the data.")
        else:
            st.error("Could not load criteria 2 data. Please ensure 'criteria2_final_summary.csv' is available.")

# Block 3: CRITERIA 3 ACHIEVEMENT
with col3:
    # Load criteria 3 data
    try:
        criteria3_df = pd.read_csv(os.path.join(HERE, 'criteria3_final_summary.csv'))
        overall_achievement = criteria3_df[criteria3_df['Metric'] == 'Overall Criteria 3 Achievement']['Achievement_Percentage'].iloc[0]
        overall_notes = criteria3_df[criteria3_df['Metric'] == 'Overall Criteria 3 Achievement']['Notes'].iloc[0]
    except (FileNotFoundError, IndexError, KeyError):
        overall_achievement = 0.0
        overall_notes = "Data not available"
    
    # Custom styled card with navy-orange theme
    st.markdown(f"""
    <div class="findings-card" onclick="this.nextElementSibling.querySelector('button').click()">
        <div class="findings-percentage">{overall_achievement:.1f}%</div>
        <div class="findings-description">Overall <strong>Criteria 3 Achievement</strong> across all companies</div>
        <div class="findings-tag">CRITERIA 3 ></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Separate expander for detailed content
    with st.expander("View Details", expanded=False):
        st.markdown("#### Criteria 3 Detailed Breakdown")
        
        # Display detailed metrics from CSV
        if 'criteria3_df' in locals():
            # Filter out the overall achievement row for detailed breakdown
            detailed_metrics = criteria3_df[criteria3_df['Metric'] != 'Overall Criteria 3 Achievement'].copy()
            
            if not detailed_metrics.empty:
                # Create a horizontal bar chart for the detailed metrics with navy-orange colors
                chart_data = detailed_metrics[['Metric', 'Achievement_Percentage']].copy()
                chart_data = chart_data[chart_data['Achievement_Percentage'] > 0]  # Filter out zero values
                
                if not chart_data.empty:
                    criteria_chart = alt.Chart(chart_data).mark_bar().encode(
                        y=alt.Y('Metric:N', sort='-x', title='Criteria 3 Metrics'),
                        x=alt.X('Achievement_Percentage:Q', title='Achievement Percentage (%)', scale=alt.Scale(domain=[0, 100])),
                        color=alt.Color('Achievement_Percentage:Q', 
                                     scale=alt.Scale(range=["#f97316", "#ea580c", "#dc2626", "#7c3aed", "#1e3a8a"]),
                                     legend=None),
                        tooltip=['Metric:N', alt.Tooltip('Achievement_Percentage:Q', format='.1f', title='Achievement %')]
                    ).properties(
                        height=400,
                        title="Criteria 3 Achievement by Metric"
                    )
                    
                    st.altair_chart(criteria_chart, use_container_width=True)
            else:
                st.info("No detailed metrics available in the data.")
        else:
            st.error("Could not load criteria 3 data. Please ensure 'criteria3_final_summary.csv' is available.")

# Block 4: CRITERIA 4 ACHIEVEMENT
with col4:
    # Load criteria 4 data
    try:
        criteria4_df = pd.read_csv(os.path.join(HERE, 'criteria4_final_summary.csv'))
        overall_achievement = criteria4_df[criteria4_df['Metric'] == 'Overall Criteria 4 Achievement']['Achievement_Percentage'].iloc[0]
        overall_notes = criteria4_df[criteria4_df['Metric'] == 'Overall Criteria 4 Achievement']['Notes'].iloc[0]
    except (FileNotFoundError, IndexError, KeyError):
        overall_achievement = 0.0
        overall_notes = "Data not available"
    
    # Custom styled card with navy-orange theme
    st.markdown(f"""
    <div class="findings-card" onclick="this.nextElementSibling.querySelector('button').click()">
        <div class="findings-percentage">{overall_achievement:.1f}%</div>
        <div class="findings-description">Overall <strong>Criteria 4 Achievement</strong> across all companies</div>
        <div class="findings-tag">CRITERIA 4 ></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Separate expander for detailed content
    with st.expander("View Details", expanded=False):
        st.markdown("#### Criteria 4 Detailed Breakdown")
        
        # Display detailed metrics from CSV
        if 'criteria4_df' in locals():
            # Filter out the overall achievement row for detailed breakdown
            detailed_metrics = criteria4_df[criteria4_df['Metric'] != 'Overall Criteria 4 Achievement'].copy()
            
            if not detailed_metrics.empty:
                # Create a horizontal bar chart for the detailed metrics with navy-orange colors
                chart_data = detailed_metrics[['Metric', 'Achievement_Percentage']].copy()
                chart_data = chart_data[chart_data['Achievement_Percentage'] > 0]  # Filter out zero values
                
                if not chart_data.empty:
                    criteria_chart = alt.Chart(chart_data).mark_bar().encode(
                        y=alt.Y('Metric:N', sort='-x', title='Criteria 4 Metrics'),
                        x=alt.X('Achievement_Percentage:Q', title='Achievement Percentage (%)', scale=alt.Scale(domain=[0, 100])),
                        color=alt.Color('Achievement_Percentage:Q', 
                                     scale=alt.Scale(range=["#f97316", "#ea580c", "#dc2626", "#7c3aed", "#1e3a8a"]),
                                     legend=None),
                        tooltip=['Metric:N', alt.Tooltip('Achievement_Percentage:Q', format='.1f', title='Achievement %')]
                    ).properties(
                        height=400,
                        title="Criteria 4 Achievement by Metric"
                    )
                    
                    st.altair_chart(criteria_chart, use_container_width=True)
            else:
                st.info("No detailed metrics available in the data.")
        else:
            st.error("Could not load criteria 4 data. Please ensure 'criteria4_final_summary.csv' is available.")

# Block 5: CRITERIA 5 ACHIEVEMENT
with col5:
    # Load criteria 5 data
    try:
        criteria5_df = pd.read_csv(os.path.join(HERE, 'criteria5_final_summary.csv'))
        overall_achievement = criteria5_df[criteria5_df['Metric'] == 'Overall Criteria 5 Achievement']['Achievement_Percentage'].iloc[0]
        overall_notes = criteria5_df[criteria5_df['Metric'] == 'Overall Criteria 5 Achievement']['Notes'].iloc[0]
    except (FileNotFoundError, IndexError, KeyError):
        overall_achievement = 0.0
        overall_notes = "Data not available"
    
    # Custom styled card with navy-orange theme
    st.markdown(f"""
    <div class="findings-card" onclick="this.nextElementSibling.querySelector('button').click()">
        <div class="findings-percentage">{overall_achievement:.1f}%</div>
        <div class="findings-description">Overall <strong>Criteria 5 Achievement</strong> across all companies</div>
        <div class="findings-tag">CRITERIA 5 ></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Separate expander for detailed content
    with st.expander("View Details", expanded=False):
        st.markdown("#### Criteria 5 Detailed Breakdown")
        
        # Display detailed metrics from CSV
        if 'criteria5_df' in locals():
            # Filter out the overall achievement row for detailed breakdown
            detailed_metrics = criteria5_df[criteria5_df['Metric'] != 'Overall Criteria 5 Achievement'].copy()
            
            if not detailed_metrics.empty:
                # Create a horizontal bar chart for the detailed metrics with navy-orange colors
                chart_data = detailed_metrics[['Metric', 'Achievement_Percentage']].copy()
                chart_data = chart_data[chart_data['Achievement_Percentage'] > 0]  # Filter out zero values
                
                if not chart_data.empty:
                    criteria_chart = alt.Chart(chart_data).mark_bar().encode(
                        y=alt.Y('Metric:N', sort='-x', title='Criteria 5 Metrics'),
                        x=alt.X('Achievement_Percentage:Q', title='Achievement Percentage (%)', scale=alt.Scale(domain=[0, 100])),
                        color=alt.Color('Achievement_Percentage:Q', 
                                     scale=alt.Scale(range=["#f97316", "#ea580c", "#dc2626", "#7c3aed", "#1e3a8a"]),
                                     legend=None),
                        tooltip=['Metric:N', alt.Tooltip('Achievement_Percentage:Q', format='.1f', title='Achievement %')]
                    ).properties(
                        height=400,
                        title="Criteria 5 Achievement by Metric"
                    )
                    
                    st.altair_chart(criteria_chart, use_container_width=True)
            else:
                st.info("No detailed metrics available in the data.")
        else:
            st.error("Could not load criteria 5 data. Please ensure 'criteria5_final_summary.csv' is available.")

# Block 6: CRITERIA 6 ACHIEVEMENT
with col6:
    # Load criteria 6 data
    try:
        criteria6_df = pd.read_csv(os.path.join(HERE, 'criteria6_final_summary.csv'))
        overall_achievement = criteria6_df[criteria6_df['Metric'] == 'Overall Criteria 6 Achievement']['Achievement_Percentage'].iloc[0]
        overall_notes = criteria6_df[criteria6_df['Metric'] == 'Overall Criteria 6 Achievement']['Notes'].iloc[0]
    except (FileNotFoundError, IndexError, KeyError):
        overall_achievement = 0.0
        overall_notes = "Data not available"
    
    # Custom styled card with navy-orange theme
    st.markdown(f"""
    <div class="findings-card" onclick="this.nextElementSibling.querySelector('button').click()">
        <div class="findings-percentage">{overall_achievement:.1f}%</div>
        <div class="findings-description">Overall <strong>Criteria 6 Achievement</strong> across all companies</div>
        <div class="findings-tag">CRITERIA 6 ></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Separate expander for detailed content
    with st.expander("View Details", expanded=False):
        st.markdown("#### Criteria 6 Detailed Breakdown")
        
        # Display detailed metrics from CSV
        if 'criteria6_df' in locals():
            # Filter out the overall achievement row for detailed breakdown
            detailed_metrics = criteria6_df[criteria6_df['Metric'] != 'Overall Criteria 6 Achievement'].copy()
            
            if not detailed_metrics.empty:
                # Create a horizontal bar chart for the detailed metrics with navy-orange colors
                chart_data = detailed_metrics[['Metric', 'Achievement_Percentage']].copy()
                chart_data = chart_data[chart_data['Achievement_Percentage'] > 0]  # Filter out zero values
                
                if not chart_data.empty:
                    criteria_chart = alt.Chart(chart_data).mark_bar().encode(
                        y=alt.Y('Metric:N', sort='-x', title='Criteria 6 Metrics'),
                        x=alt.X('Achievement_Percentage:Q', title='Achievement Percentage (%)', scale=alt.Scale(domain=[0, 100])),
                        color=alt.Color('Achievement_Percentage:Q', 
                                     scale=alt.Scale(range=["#f97316", "#ea580c", "#dc2626", "#7c3aed", "#1e3a8a"]),
                                     legend=None),
                        tooltip=['Metric:N', alt.Tooltip('Achievement_Percentage:Q', format='.1f', title='Achievement %')]
                    ).properties(
                        height=400,
                        title="Criteria 6 Achievement by Metric"
                    )
                    
                    st.altair_chart(criteria_chart, use_container_width=True)
            else:
                st.info("No detailed metrics available in the data.")
        else:
            st.error("Could not load criteria 6 data. Please ensure 'criteria6_final_summary.csv' is available.")

# Block 7: CRITERIA 7 ACHIEVEMENT
with col7:
    # Load criteria 7 data
    try:
        criteria7_df = pd.read_csv(os.path.join(HERE, 'criteria7_final_summary.csv'))
        overall_achievement = criteria7_df[criteria7_df['Metric'] == 'Overall Criteria 7 Achievement']['Achievement_Percentage'].iloc[0]
        overall_notes = criteria7_df[criteria7_df['Metric'] == 'Overall Criteria 7 Achievement']['Notes'].iloc[0]
    except (FileNotFoundError, IndexError, KeyError):
        overall_achievement = 0.0
        overall_notes = "Data not available"
    
    # Custom styled card with navy-orange theme
    st.markdown(f"""
    <div class="findings-card" onclick="this.nextElementSibling.querySelector('button').click()">
        <div class="findings-percentage">{overall_achievement:.1f}%</div>
        <div class="findings-description">Overall <strong>Criteria 7 Achievement</strong> across all companies</div>
        <div class="findings-tag">CRITERIA 7 ></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Separate expander for detailed content
    with st.expander("View Details", expanded=False):
        st.markdown("#### Criteria 7 Detailed Breakdown")
        
        # Display detailed metrics from CSV
        if 'criteria7_df' in locals():
            # Filter out the overall achievement row for detailed breakdown
            detailed_metrics = criteria7_df[criteria7_df['Metric'] != 'Overall Criteria 7 Achievement'].copy()
            
            if not detailed_metrics.empty:
                # Create a horizontal bar chart for the detailed metrics with navy-orange colors
                chart_data = detailed_metrics[['Metric', 'Achievement_Percentage']].copy()
                chart_data = chart_data[chart_data['Achievement_Percentage'] > 0]  # Filter out zero values
                
                if not chart_data.empty:
                    criteria_chart = alt.Chart(chart_data).mark_bar().encode(
                        y=alt.Y('Metric:N', sort='-x', title='Criteria 7 Metrics'),
                        x=alt.X('Achievement_Percentage:Q', title='Achievement Percentage (%)', scale=alt.Scale(domain=[0, 100])),
                        color=alt.Color('Achievement_Percentage:Q', 
                                     scale=alt.Scale(range=["#f97316", "#ea580c", "#dc2626", "#7c3aed", "#1e3a8a"]),
                                     legend=None),
                        tooltip=['Metric:N', alt.Tooltip('Achievement_Percentage:Q', format='.1f', title='Achievement %')]
                    ).properties(
                        height=400,
                        title="Criteria 7 Achievement by Metric"
                    )
                    
                    st.altair_chart(criteria_chart, use_container_width=True)
            else:
                st.info("No detailed metrics available in the data.")
        else:
            st.error("Could not load criteria 7 data. Please ensure 'criteria7_final_summary.csv' is available.")

# Export button for criteria performance data
st.markdown("---")

with st.container():
    if st.button("Export Criteria Performance Data", type="primary", use_container_width=True):
        # Collect all criteria data for visualization
        criteria_summary = []
        
        for i in range(1, 8):
            try:
                df = pd.read_csv(os.path.join(HERE, f'criteria{i}_final_summary.csv'))
                overall_achievement = df[df['Metric'] == f'Overall Criteria {i} Achievement']['Achievement_Percentage'].iloc[0]
                criteria_summary.append({
                    'Criteria': f'Criteria {i}',
                    'Achievement_Percentage': overall_achievement
                })
            except (FileNotFoundError, IndexError, KeyError):
                criteria_summary.append({
                    'Criteria': f'Criteria {i}',
                    'Achievement_Percentage': 0.0
                })
        
        if criteria_summary:
            # Create summary dataframe
            summary_df = pd.DataFrame(criteria_summary)
            
            # Create visualization
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
            
            # Set up the figure with custom styling
            fig, ax = plt.subplots(figsize=(12, 8))
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')
            
            # Create horizontal bar chart
            bars = ax.barh(summary_df['Criteria'], summary_df['Achievement_Percentage'], 
                          color=['#1e3a8a', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe', '#f3f4f6'])
            
            # Customize the chart
            ax.set_xlabel('Achievement Percentage (%)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Criteria', fontsize=12, fontweight='bold')
            ax.set_title('Company Performance on Key Criteria\nModern Slavery Report Template', 
                        fontsize=16, fontweight='bold', pad=20)
            
            # Add percentage labels on bars
            for i, (bar, percentage) in enumerate(zip(bars, summary_df['Achievement_Percentage'])):
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                       f'{percentage:.1f}%', ha='left', va='center', fontweight='bold')
            
            # Set x-axis limits and styling
            ax.set_xlim(0, 100)
            ax.grid(axis='x', alpha=0.3, linestyle='--')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Adjust layout
            plt.tight_layout()
            
            # Convert to PNG bytes
            import io
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight', 
                       facecolor='white', edgecolor='none')
            img_buffer.seek(0)
            img_data = img_buffer.getvalue()
            
            # Create download button
            st.download_button(
                label="Download Criteria Performance Chart (PNG)",
                data=img_data,
                file_name="criteria_performance_chart.png",
                mime="image/png",
                use_container_width=True
            )
            
            st.success("✅ Criteria performance chart ready for download!")
            plt.close(fig)  # Clean up
        else:
            st.error("❌ No criteria data available for export.")

# -----------------
# Export & Print
# -----------------
st.subheader("Export & Print")

st.markdown("**Download All Available Data From Light Carrier**")

# Dropdown for all available datasets
available_datasets = {
    "Main Dataset": "au_uk_unified_sectors_merged.csv",
    "Criteria 1 Summary": "criteria_1_final_summary.csv", 
    "Criteria 2 Summary": "criteria2_final_summary.csv",
    "Criteria 3 Summary": "criteria3_final_summary.csv",
    "Criteria 4 Summary": "criteria4_final_summary.csv",
    "Criteria 5 Summary": "criteria5_final_summary.csv",
    "Criteria 6 Summary": "criteria6_final_summary.csv",
    "Criteria 7 Summary": "criteria7_final_summary.csv",
    "Disclosure by Sector": "derived/disclosure_by_sector.csv",
    "Level 1 Not Met Trend": "derived/level1_not_met_trend.csv",
    "Policy vs Action by Sector": "derived/policy_vs_action_by_sector.csv",
    "Sector Year Weighted Compliance": "derived/sector_year_weighted_compliance.csv"
}

selected_datasets = st.multiselect(
    "Select datasets to download:",
    options=list(available_datasets.keys()),
    default=list(available_datasets.keys())[:3],  # Default to first 3 datasets
    help="Choose which datasets you want to download (you can select multiple)",
    key="dataset_selector"
)

# Create single zip download button
if selected_datasets:
    st.markdown(f"**Selected Files ({len(selected_datasets)}):**")
    
    # Display selected files
    for dataset_name in selected_datasets:
        st.markdown(f"• {dataset_name}")
    
    # Create zip file with all selected datasets
    if st.button("📦 Download All Selected Files as ZIP", type="primary", use_container_width=True):
        try:
            # Create zip file in memory
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for dataset_name in selected_datasets:
                    selected_file = available_datasets[dataset_name]
                    file_path = os.path.join(os.path.dirname(__file__), selected_file)
                    
                    if os.path.exists(file_path):
                        # Read file content
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()
                        
                        # Add file to zip
                        zip_file.writestr(selected_file, file_content)
                    else:
                        st.warning(f"File not found: {selected_file}")
            
            # Prepare zip file for download
            zip_buffer.seek(0)
            zip_data = zip_buffer.getvalue()
            
            # Create download button
            st.download_button(
                label="📦 Download ZIP File",
                data=zip_data,
                file_name="modern_slavery_datasets.zip",
                mime="application/zip",
                type="primary",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error creating zip file: {str(e)}")
else:
    st.info("Please select at least one dataset to download.")

st.caption("Use your browser's print dialog to print or save as PDF. Charts are vector-based via Altair.")
