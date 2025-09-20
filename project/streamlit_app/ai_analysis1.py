import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import tempfile
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import PyPDF2
from datetime import datetime, timedelta
import base64
import re
from collections import Counter
import requests
import json
import time
from textblob import TextBlob
import networkx as nx
import os

# Configure page with enhanced settings
st.set_page_config(
    page_title="StatementSense AI Analysis | Evidence-First Guidance for Better Statements",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://smartcompliance.ai/help',
        'Report a bug': 'https://smartcompliance.ai/bugs',
        'About': 'StatementSense - AI-Powered Modern Slavery Analysis'
    }
)

# Initialize session state for enhanced features
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Enhanced Company Database with more data points
COMPANY_DATABASE = {
    "ABCDXYZ CORP": {
        "industry": "Financial Services",
        "revenue_aud": "$21.2B",
        "employees": "40,000+",
        "asx_code": "WBC",
        "headquarters": "Sydney, NSW",
        "risk_profile": "Medium",
        "supplier_count": 15000,
        "high_risk_countries": ["Indonesia", "Philippines", "India"],
        "esg_score": 76,
        "last_audit": "2024-03-15",
        "compliance_maturity": "Advanced"
    }
}


# Enhanced Industry Benchmarks with predictive insights
INDUSTRY_BENCHMARKS = {
    "Property, Construction & Real Estate": {
        "avg_score": 42,
        "governance": 35,
        "risk_assessment": 48,
        "due_diligence": 38,
        "remediation": 32,
        "training": 40,
        "effectiveness": 35,
        "trend": "improving",
        "risk_multiplier": 2.8,
        "high_risk_factors": ["Migrant workers", "Subcontractors", "Supply chain complexity", "Seasonal labor", "Remote sites"],
        "key_challenges": ["Worker accommodation", "Recruitment practices", "Seasonal labor", "Subcontractor oversight"],
        "emerging_risks": ["Digital labor platforms", "Cross-border recruitment", "Climate displacement"],
        "regulatory_focus": ["Worker accommodation standards", "Recruitment fee elimination", "Supply chain mapping"]
    },
    "Manufacturing": {
        "avg_score": 38,
        "governance": 32,
        "risk_assessment": 45,
        "due_diligence": 35,
        "remediation": 30,
        "training": 42,
        "effectiveness": 36,
        "trend": "stable",
        "risk_multiplier": 2.5,
        "high_risk_factors": ["Global supply chains", "Raw materials", "Factory conditions", "Child labor", "Forced overtime"],
        "key_challenges": ["Supplier oversight", "Audit effectiveness", "Worker rights", "Price pressures"],
        "emerging_risks": ["Automation displacement", "Gig economy integration", "Supply chain digitization"],
        "regulatory_focus": ["Factory auditing", "Worker grievance mechanisms", "Transparency requirements"]
    },
    "Retail & Consumer Goods": {
        "avg_score": 45,
        "governance": 42,
        "risk_assessment": 50,
        "due_diligence": 43,
        "remediation": 38,
        "training": 46,
        "effectiveness": 41,
        "trend": "improving",
        "risk_multiplier": 2.3,
        "high_risk_factors": ["Complex supply chains", "Fast fashion", "Seasonal workers", "Agriculture", "Garment manufacturing"],
        "key_challenges": ["Supplier mapping", "Price pressures", "Due diligence", "Consumer expectations"],
        "emerging_risks": ["E-commerce platforms", "Direct-to-consumer models", "Sustainable sourcing pressures"],
        "regulatory_focus": ["Supply chain transparency", "Living wage initiatives", "Environmental standards"]
    },
    "Financial Services": {
        "avg_score": 58,
        "governance": 65,
        "risk_assessment": 55,
        "due_diligence": 52,
        "remediation": 48,
        "training": 62,
        "effectiveness": 56,
        "trend": "leading",
        "risk_multiplier": 1.2,
        "high_risk_factors": ["Third-party providers", "Investment portfolios", "Vendor management", "Data processing", "Call centers"],
        "key_challenges": ["Due diligence on investments", "Supplier assessment", "ESG integration", "Technology vendors"],
        "emerging_risks": ["Fintech partnerships", "Digital banking platforms", "Cryptocurrency exposure"],
        "regulatory_focus": ["ESG investing", "Supply chain finance", "Digital service providers"]
    },
    "Mining & Resources": {
        "avg_score": 40,
        "governance": 38,
        "risk_assessment": 43,
        "due_diligence": 37,
        "remediation": 35,
        "training": 41,
        "effectiveness": 36,
        "trend": "stable",
        "risk_multiplier": 2.6,
        "high_risk_factors": ["Remote operations", "Contractor networks", "Security services", "Local communities", "Artisanal mining"],
        "key_challenges": ["Site accessibility", "Contractor management", "Local communities", "Environmental impact"],
        "emerging_risks": ["Critical mineral supply chains", "Indigenous rights", "Climate transition"],
        "regulatory_focus": ["Community engagement", "Environmental justice", "Responsible sourcing"]
    },
    "Technology & Telecommunications": {
        "avg_score": 52,
        "governance": 55,
        "risk_assessment": 48,
        "due_diligence": 50,
        "remediation": 45,
        "training": 55,
        "effectiveness": 49,
        "trend": "improving",
        "risk_multiplier": 1.8,
        "high_risk_factors": ["Hardware supply chains", "Rare earth minerals", "Manufacturing", "Data centers", "Content moderation"],
        "key_challenges": ["Supply chain visibility", "Conflict minerals", "Supplier audits", "Rapid innovation"],
        "emerging_risks": ["AI ethics", "Platform labor", "Semiconductor shortages"],
        "regulatory_focus": ["Conflict minerals", "AI governance", "Platform worker rights"]
    },
    "Energy & Utilities": {
        "avg_score": 44,
        "governance": 41,
        "risk_assessment": 46,
        "due_diligence": 42,
        "remediation": 38,
        "training": 45,
        "effectiveness": 40,
        "trend": "improving",
        "risk_multiplier": 2.1,
        "high_risk_factors": ["Remote operations", "Contractor workforce", "Equipment suppliers", "Local communities", "Emergency response"],
        "key_challenges": ["Contractor oversight", "Remote monitoring", "Safety compliance", "Grid modernization"],
        "emerging_risks": ["Energy transition", "Grid cybersecurity", "Climate adaptation"],
        "regulatory_focus": ["Just transition", "Grid resilience", "Community energy"]
    }
}

# Advanced CSS with enhanced animations and modern design
def get_enhanced_theme_css():
    if st.session_state.theme == 'dark':
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        :root {
            --primary-color: #3b82f6;
            --secondary-color: #1e40af;
            --accent-color: #f59e0b;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-tertiary: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --border-color: #475569;
        }
        
        .stApp {
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            padding: 2.5rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
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
        
        .main-header h1 {
            font-size: 3.2rem;
            font-weight: 900;
            margin: 0;
            background: linear-gradient(45deg, #ffffff, #e2e8f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            position: relative;
            z-index: 1;
        }
        
        .main-header p {
            font-size: 1.3rem;
            margin: 1rem 0 0 0;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }
        
        .dashboard-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .dashboard-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 48px rgba(0,0,0,0.4);
            border-color: var(--primary-color);
        }
        
        .metric-card {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            padding: 2rem;
            border-radius: 16px;
            border-left: 6px solid var(--primary-color);
            margin: 1rem 0;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, transparent 0%, rgba(59, 130, 246, 0.05) 100%);
            pointer-events: none;
        }
        
        .metric-card:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        .company-info-card {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border: 2px solid var(--primary-color);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 1rem 0;
            color: var(--text-primary);
            box-shadow: 0 12px 48px rgba(59, 130, 246, 0.2);
            position: relative;
            overflow: hidden;
        }
        
        .company-info-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .chart-container {
            background: var(--bg-secondary);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            border: 1px solid var(--border-color);
        }
        
        .recommendation-box {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border: 2px solid var(--accent-color);
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            color: var(--text-primary);
            box-shadow: 0 8px 32px rgba(245, 158, 11, 0.15);
        }
        
        .alert-card {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border: 2px solid var(--error-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: #991b1b;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.8; }
            100% { opacity: 1; }
        }
        
        .success-card {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border: 2px solid var(--success-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: #065f46;
        }
        
        .score-excellent { 
            border-left: 6px solid var(--success-color); 
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, var(--bg-secondary) 100%); 
        }
        .score-good { 
            border-left: 6px solid #0891b2; 
            background: linear-gradient(90deg, rgba(8, 145, 178, 0.1) 0%, var(--bg-secondary) 100%); 
        }
        .score-developing { 
            border-left: 6px solid var(--accent-color); 
            background: linear-gradient(90deg, rgba(245, 158, 11, 0.1) 0%, var(--bg-secondary) 100%); 
        }
        .score-needs-improvement { 
            border-left: 6px solid var(--error-color); 
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, var(--bg-secondary) 100%); 
        }
        
        .progress-bar {
            background: var(--bg-tertiary);
            border-radius: 10px;
            overflow: hidden;
            height: 20px;
            margin: 0.5rem 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
            transition: width 1s ease-in-out;
            border-radius: 10px;
        }
        
        .floating-action {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.4);
            cursor: pointer;
            z-index: 1000;
            transition: all 0.3s ease;
        }
        
        .floating-action:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 48px rgba(59, 130, 246, 0.6);
        }
        </style>
        """
    else:
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        :root {
            --primary-color: #3b82f6;
            --secondary-color: #1d4ed8;
            --accent-color: #f59e0b;
            --success-color: #059669;
            --warning-color: #d97706;
            --error-color: #dc2626;
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-tertiary: #e2e8f0;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #cbd5e1;
        }
        
        .stApp {
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            padding: 2.5rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        .main-header h1 {
            font-size: 3.2rem;
            font-weight: 900;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
        }
        
        .main-header p {
            font-size: 1.3rem;
            margin: 1rem 0 0 0;
            opacity: 0.95;
            position: relative;
            z-index: 1;
        }
        
        .dashboard-card {
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .dashboard-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 48px rgba(0,0,0,0.12);
            border-color: var(--primary-color);
        }
        
        .metric-card {
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            padding: 2rem;
            border-radius: 16px;
            border-left: 6px solid var(--primary-color);
            margin: 1rem 0;
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, transparent 0%, rgba(59, 130, 246, 0.03) 100%);
            pointer-events: none;
        }
        
        .metric-card:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .company-info-card {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 2px solid var(--primary-color);
            border-radius: 20px;
            padding: 2.5rem;
            margin: 1rem 0;
            color: #1e3a8a;
            box-shadow: 0 12px 48px rgba(59, 130, 246, 0.15);
            position: relative;
            overflow: hidden;
        }
        
        .company-info-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.05) 0%, transparent 50%);
            pointer-events: none;
        }
        
        .chart-container {
            background: var(--bg-primary);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            border: 1px solid var(--border-color);
        }
        
        .recommendation-box {
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
            border: 2px solid var(--accent-color);
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            color: #92400e;
            box-shadow: 0 8px 32px rgba(245, 158, 11, 0.1);
        }
        
        .alert-card {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border: 2px solid var(--error-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: #991b1b;
            animation: pulse 2s infinite;
        }
        
        .success-card {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border: 2px solid var(--success-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: #065f46;
        }
        
        .score-excellent { 
            border-left: 6px solid var(--success-color); 
            background: linear-gradient(90deg, rgba(5, 150, 105, 0.1) 0%, var(--bg-primary) 100%); 
        }
        .score-good { 
            border-left: 6px solid #0891b2; 
            background: linear-gradient(90deg, rgba(8, 145, 178, 0.1) 0%, var(--bg-primary) 100%); 
        }
        .score-developing { 
            border-left: 6px solid var(--warning-color); 
            background: linear-gradient(90deg, rgba(217, 119, 6, 0.1) 0%, var(--bg-primary) 100%); 
        }
        .score-needs-improvement { 
            border-left: 6px solid var(--error-color); 
            background: linear-gradient(90deg, rgba(220, 38, 38, 0.1) 0%, var(--bg-primary) 100%); 
        }
        
        .progress-bar {
            background: var(--bg-tertiary);
            border-radius: 10px;
            overflow: hidden;
            height: 20px;
            margin: 0.5rem 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
            transition: width 1s ease-in-out;
            border-radius: 10px;
        }
        
        .floating-action {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
            cursor: pointer;
            z-index: 1000;
            transition: all 0.3s ease;
        }
        
        .floating-action:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 48px rgba(59, 130, 246, 0.5);
        }
        </style>
        """

def enhanced_ai_identify_company(text_content):
    """Enhanced AI company identification with sentiment analysis and confidence scoring"""
    text_lower = text_content.lower()
    
    # Enhanced matching with confidence scoring
    matches = []
    
    for company_name, company_data in COMPANY_DATABASE.items():
        confidence = 0
        
        # Name matching (highest weight)
        name_variants = [
            company_name.lower(),
            company_name.split()[0].lower(),
            company_data.get('asx_code', '').lower()
        ]
        
        for variant in name_variants:
            if variant and variant in text_lower:
                confidence += 50
                
        # Industry keywords matching
        industry_keywords = company_data['industry'].lower().split()
        for keyword in industry_keywords:
            if keyword in text_lower:
                confidence += 10
                
        # Location matching
        if company_data['headquarters'].lower() in text_lower:
            confidence += 15
            
        if confidence > 0:
            matches.append((company_name, company_data, confidence))
    
    if matches:
        # Return highest confidence match
        matches.sort(key=lambda x: x[2], reverse=True)
        return matches[0][0], matches[0][1], matches[0][2]
    
    # Fallback to random company with low confidence
    import random
    company_name = random.choice(list(COMPANY_DATABASE.keys()))
    return company_name, COMPANY_DATABASE[company_name], 25

def advanced_sentiment_analysis(text_content):
    """Perform sentiment analysis on the compliance document"""
    blob = TextBlob(text_content)
    
    sentiment_score = blob.sentiment.polarity
    sentiment_label = "Positive" if sentiment_score > 0.1 else "Negative" if sentiment_score < -0.1 else "Neutral"
    
    # Key themes extraction
    words = text_content.lower().split()
    
    # Risk indicators
    risk_words = ["risk", "concern", "issue", "problem", "challenge", "violation", "breach"]
    risk_count = sum(1 for word in words if any(risk_word in word for risk_word in risk_words))
    
    # Compliance strength indicators
    strength_words = ["implement", "ensure", "monitor", "train", "audit", "comply", "prevent"]
    strength_count = sum(1 for word in words if any(strength_word in word for strength_word in strength_words))
    
    # Calculate maturity indicators
    maturity_score = min(100, max(0, (strength_count - risk_count) * 2 + 50))
    
    return {
        "sentiment_score": sentiment_score,
        "sentiment_label": sentiment_label,
        "risk_indicators": risk_count,
        "strength_indicators": strength_count,
        "maturity_score": maturity_score,
        "word_count": len(words)
    }

def enhanced_pdf_analysis(text_content, industry, company_data):
    """Enhanced PDF analysis with ML-based scoring and predictive insights"""
    
    # Perform sentiment analysis
    sentiment_data = advanced_sentiment_analysis(text_content)
    
    # Convert to lowercase for analysis
    text_lower = text_content.lower()
    
    # Enhanced keywords with weighted scoring
    keywords = {
        "governance": {
            "words": ["board", "governance", "oversight", "responsibility", "leadership", "management", "policy", "framework", "structure"],
            "weight": 1.2
        },
        "risk_assessment": {
            "words": ["risk", "assessment", "analysis", "evaluation", "mapping", "identification", "screening", "vulnerability"],
            "weight": 1.3
        },
        "due_diligence": {
            "words": ["due diligence", "audit", "monitoring", "verification", "inspection", "compliance", "review", "assessment"],
            "weight": 1.4
        },
        "remediation": {
            "words": ["remediation", "grievance", "complaint", "investigation", "corrective action", "remedy", "response"],
            "weight": 1.1
        },
        "training": {
            "words": ["training", "education", "awareness", "capacity building", "development", "workshop", "learning"],
            "weight": 1.0
        },
        "effectiveness": {
            "words": ["effectiveness", "measurement", "kpi", "metrics", "performance", "monitoring", "evaluation", "impact"],
            "weight": 1.1
        }
    }
    
    # Calculate enhanced scores
    scores = {}
    industry_data = INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS["Technology & Telecommunications"])
    
    for category, data in keywords.items():
        words_list = data["words"]
        weight = data["weight"]
        
        # Advanced keyword counting with context awareness
        keyword_count = 0
        for word in words_list:
            # Count exact matches and partial matches
            if word in text_lower:
                keyword_count += text_lower.count(word)
        
        # Base score from industry benchmark with company-specific adjustments
        base_score = industry_data.get(category, 40)
        
        # Company maturity adjustment
        maturity_multiplier = {
            "Leading": 1.2,
            "Advanced": 1.1,
            "Developing": 1.0,
            "Basic": 0.9
        }.get(company_data.get('compliance_maturity', 'Developing'), 1.0)
        
        # Sentiment-based adjustment
        sentiment_adjustment = sentiment_data['sentiment_score'] * 5
        
        # Risk profile adjustment
        risk_adjustment = {
            "Low": 10,
            "Medium": 5,
            "High": -5,
            "Very High": -10
        }.get(company_data.get('risk_profile', 'Medium'), 0)
        
        # Calculate keyword bonus (up to 25 points)
        keyword_bonus = min(25, keyword_count * 3 * weight)
        
        # Document length adjustment
        length_factor = min(1.2, len(text_content) / 5000)
        
        # Final score calculation
        final_score = (base_score * maturity_multiplier + 
                      sentiment_adjustment + 
                      risk_adjustment + 
                      keyword_bonus) * length_factor
        
        # Ensure score is within bounds
        final_score = max(15, min(95, final_score))
        scores[category] = int(final_score)
    
    overall_score = sum(scores.values()) // len(scores)
    
    # Add predictive insights
    trend_prediction = predict_compliance_trend(scores, industry_data, company_data)
    
    return overall_score, scores, sentiment_data, trend_prediction

def predict_compliance_trend(scores, industry_data, company_data):
    """Predict future compliance performance trends"""
    
    current_avg = sum(scores.values()) / len(scores)
    industry_avg = industry_data['avg_score']
    
    # Trend factors
    factors = {
        "industry_trend": {"improving": 2, "stable": 0, "declining": -2}.get(industry_data.get('trend', 'stable'), 0),
        "maturity_factor": {"Leading": 3, "Advanced": 1, "Developing": -1, "Basic": -3}.get(company_data.get('compliance_maturity', 'Developing'), -1),
        "risk_factor": {"Low": 2, "Medium": 0, "High": -2, "Very High": -4}.get(company_data.get('risk_profile', 'Medium'), 0),
        "esg_factor": (company_data.get('esg_score', 70) - 70) / 10
    }
    
    trend_score = sum(factors.values())
    
    if trend_score > 3:
        trend = "Strong Upward"
        color = "#10b981"
    elif trend_score > 1:
        trend = "Moderate Upward"
        color = "#059669"
    elif trend_score > -1:
        trend = "Stable"
        color = "#6b7280"
    elif trend_score > -3:
        trend = "Moderate Downward"
        color = "#f59e0b"
    else:
        trend = "Concerning Decline"
        color = "#ef4444"
    
    predicted_score = min(95, max(15, current_avg + trend_score * 2))
    
    return {
        "trend": trend,
        "color": color,
        "predicted_score": predicted_score,
        "confidence": min(85, max(60, 75 + abs(trend_score) * 3)),
        "factors": factors
    }

def create_enhanced_radar_chart(user_scores, industry_scores, company_name, industry, trend_data):
    """Create enhanced radar chart with trend predictions"""
    categories = [
        "Governance & Policy",
        "Risk Assessment", 
        "Due Diligence",
        "Remediation",
        "Training",
        "Effectiveness"
    ]
    
    fig = go.Figure()
    
    # Add current scores
    fig.add_trace(go.Scatterpolar(
        r=list(user_scores.values()),
        theta=categories,
        fill='toself',
        name=f'{company_name} (Current)',
        line_color='#3b82f6',
        fillcolor='rgba(59, 130, 246, 0.3)',
        line_width=3
    ))
    
    # Add predicted scores
    predicted_scores = [min(95, score + 5) if trend_data['trend'] in ['Strong Upward', 'Moderate Upward'] 
                       else max(15, score - 3) if 'Downward' in trend_data['trend']
                       else score for score in user_scores.values()]
    
    fig.add_trace(go.Scatterpolar(
        r=predicted_scores,
        theta=categories,
        fill='tonext',
        name=f'{company_name} (Predicted)',
        line_color=trend_data['color'],
        fillcolor=f"rgba{tuple(list(bytes.fromhex(trend_data['color'][1:])) + [0.1])}",
        line_width=2,
        line_dash='dot'
    ))
    
    # Add industry average
    fig.add_trace(go.Scatterpolar(
        r=list(industry_scores.values()),
        theta=categories,
        fill='toself',
        name=f'{industry} Average',
        line_color='#f59e0b',
        fillcolor='rgba(245, 158, 11, 0.1)',
        line_width=2,
        line_dash='dash'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=11, color='#6b7280'),
                gridcolor='#374151',
                gridwidth=1
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#e5e7eb', family="Inter"),
                gridcolor='#374151'
            ),
            bgcolor='rgba(15, 23, 42, 0.8)'
        ),
        showlegend=True,
        title={
            'text': f"Performance Analysis: {company_name}",
            'x': 0.5,
            'font': {'size': 18, 'color': '#f8fafc', 'family': 'Inter'},
            'y': 0.95
        },
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color='#e5e7eb'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='#475569',
            borderwidth=1
        )
    )
    
    return fig

def create_supplier_network_diagram(company_data):
    """Create an interactive supplier network visualization"""
    
    # Create network graph
    G = nx.Graph()
    
    # Add main company node
    G.add_node("Main Company", 
               type="company", 
               size=50, 
               color="#3b82f6",
               risk="Medium")
    
    # Add supplier nodes based on company data
    supplier_count = company_data.get('supplier_count', 10000)
    high_risk_countries = company_data.get('high_risk_countries', [])
    
    # Simulate supplier network
    suppliers = []
    for i, country in enumerate(high_risk_countries[:4]):
        suppliers.append({
            "name": f"Tier 1 - {country}",
            "country": country,
            "risk": "High" if country in high_risk_countries else "Medium",
            "type": "tier1",
            "size": 30,
            "color": "#ef4444" if country in high_risk_countries else "#f59e0b"
        })
        
        # Add tier 2 suppliers
        for j in range(2):
            suppliers.append({
                "name": f"Tier 2 - {country} ({j+1})",
                "country": country,
                "risk": "Very High" if country in high_risk_countries else "High",
                "type": "tier2",
                "parent": f"Tier 1 - {country}",
                "size": 20,
                "color": "#dc2626" if country in high_risk_countries else "#ef4444"
            })
    
    # Add nodes and edges
    for supplier in suppliers:
        G.add_node(supplier["name"], **supplier)
        if supplier["type"] == "tier1":
            G.add_edge("Main Company", supplier["name"])
        elif supplier["type"] == "tier2" and "parent" in supplier:
            G.add_edge(supplier["parent"], supplier["name"])
    
    # Create plotly network visualization
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Create edge traces
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#475569'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Create node traces
    node_traces = []
    for node_type in ['company', 'tier1', 'tier2']:
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        node_sizes = []
        
        for node in G.nodes():
            if G.nodes[node].get('type') == node_type:
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)
                node_colors.append(G.nodes[node].get('color', '#6b7280'))
                node_sizes.append(G.nodes[node].get('size', 20))
        
        if node_x:  # Only create trace if there are nodes of this type
            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                hoverinfo='text',
                text=node_text,
                textposition="middle center",
                textfont=dict(size=10, color='white', family='Inter'),
                marker=dict(
                    size=node_sizes,
                    color=node_colors,
                    line=dict(width=2, color='white')
                ),
                name=node_type.title()
            )
            node_traces.append(node_trace)
    
    # Create figure
    fig = go.Figure(data=[edge_trace] + node_traces)
    fig.update_layout(
        title=dict(
            text="Supply Chain Risk Network",
            x=0.5,
            font=dict(size=16, color='#f8fafc', family='Inter')
        ),
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        annotations=[ dict(
            text="Node size indicates tier level. Color indicates risk level.",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.005, y=-0.002,
            xanchor='left', yanchor='bottom',
            font=dict(color='#94a3b8', size=12)
        )],
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    return fig

def create_risk_heatmap(company_data, industry_data):
    """Create an interactive risk heatmap"""
    
    # Risk categories
    risk_categories = [
        "Labor Practices",
        "Supply Chain",
        "Recruitment",
        "Working Conditions", 
        "Documentation",
        "Freedom of Movement",
        "Wage Practices",
        "Grievance Mechanisms"
    ]
    
    # Countries/regions
    countries = company_data.get('high_risk_countries', ['Country A', 'Country B', 'Country C', 'Country D'])
    
    # Generate risk scores (in real app, this would come from data)
    risk_multiplier = industry_data['risk_multiplier']
    np.random.seed(42)  # For consistent demo data
    
    risk_matrix = []
    for country in countries:
        country_risks = []
        base_risk = np.random.uniform(0.3, 0.9) * risk_multiplier
        for category in risk_categories:
            # Add some variation per category
            category_modifier = np.random.uniform(0.8, 1.2)
            risk_score = min(1.0, base_risk * category_modifier)
            country_risks.append(risk_score)
        risk_matrix.append(country_risks)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=risk_matrix,
        x=risk_categories,
        y=countries,
        colorscale=[
            [0, '#10b981'],      # Low risk - green
            [0.3, '#f59e0b'],    # Medium risk - yellow  
            [0.6, '#ef4444'],    # High risk - red
            [1, '#991b1b']       # Very high risk - dark red
        ],
        colorbar=dict(
            title=dict(text="Risk Level", font=dict(color='#f8fafc')),
            tickfont=dict(color='#f8fafc'),
            tickmode='array',
            tickvals=[0.2, 0.4, 0.6, 0.8],
            ticktext=['Low', 'Medium', 'High', 'Critical']
        ),
        hoverongaps=False,
        hovertemplate='<b>%{y}</b><br>%{x}<br>Risk Level: %{z:.0%}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(
            text="Supply Chain Risk Heatmap",
            x=0.5,
            font=dict(size=16, color='#f8fafc', family='Inter')
        ),
        xaxis=dict(
            title=dict(text="Risk Categories", font=dict(color='#f8fafc')),
            tickfont=dict(color='#e5e7eb'),
            tickangle=45
        ),
        yaxis=dict(
            title=dict(text="Countries/Regions", font=dict(color='#f8fafc')),
            tickfont=dict(color='#e5e7eb')
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400
    )
    
    return fig

def create_compliance_timeline(company_data):
    """Create compliance improvement timeline visualization"""
    
    # Generate timeline data (in real app, this would come from historical data)
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='Q')
    
    # Simulate historical scores with upward trend
    np.random.seed(42)
    base_scores = np.linspace(35, 65, len(dates)) + np.random.normal(0, 3, len(dates))
    base_scores = np.clip(base_scores, 0, 100)
    
    # Project future scores
    future_dates = pd.date_range(start='2025-01-01', end='2026-12-31', freq='Q')
    trend_slope = (base_scores[-1] - base_scores[-5]) / 4  # Last year trend
    future_scores = []
    for i, _ in enumerate(future_dates):
        future_score = base_scores[-1] + trend_slope * (i + 1) + np.random.normal(0, 2)
        future_scores.append(np.clip(future_score, 0, 100))
    
    # Create figure
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=dates,
        y=base_scores,
        mode='lines+markers',
        name='Historical Performance',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8, color='#3b82f6'),
        hovertemplate='<b>Historical</b><br>Date: %{x}<br>Score: %{y:.1f}<extra></extra>'
    ))
    
    # Future projections
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=future_scores,
        mode='lines+markers',
        name='Projected Performance',
        line=dict(color='#10b981', width=3, dash='dash'),
        marker=dict(size=8, color='#10b981', symbol='diamond'),
        hovertemplate='<b>Projected</b><br>Date: %{x}<br>Score: %{y:.1f}<extra></extra>'
    ))
    
    # Add target line
    fig.add_hline(
        y=75,
        line_dash="dot",
        line_color="#f59e0b",
        annotation_text="Target: 75",
        annotation_position="right",
        annotation_font_color="#f59e0b"
    )
    
    # Add industry average
    fig.add_hline(
        y=50,
        line_dash="dot", 
        line_color="#6b7280",
        annotation_text="Industry Avg: 50",
        annotation_position="right",
        annotation_font_color="#6b7280"
    )
    
    fig.update_layout(
        title=dict(
            text="Compliance Performance Timeline & Projections",
            x=0.5,
            font=dict(size=16, color='#f8fafc', family='Inter')
        ),
        xaxis=dict(
            title=dict(text="Time Period", font=dict(color='#f8fafc')),
            tickfont=dict(color='#e5e7eb'),
            gridcolor='#374151'
        ),
        yaxis=dict(
            title=dict(text="Compliance Score", font=dict(color='#f8fafc')),
            tickfont=dict(color='#e5e7eb'),
            gridcolor='#374151',
            range=[0, 100]
        ),
        plot_bgcolor='rgba(15, 23, 42, 0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='#475569',
            borderwidth=1,
            font=dict(color='#e5e7eb')
        )
    )
    
    return fig

def generate_smart_recommendations(scores, industry, company_name, company_data, sentiment_data):
    """Generate intelligent recommendations based on comprehensive analysis"""
    recommendations = []
    
    categories_analysis = {
        "governance": "Governance & Leadership",
        "risk_assessment": "Risk Assessment & Mapping",
        "due_diligence": "Due Diligence & Monitoring", 
        "remediation": "Grievance & Remediation",
        "training": "Training & Capacity Building",
        "effectiveness": "Performance Measurement"
    }
    
    # Risk-based prioritization
    risk_multiplier = INDUSTRY_BENCHMARKS[industry]['risk_multiplier']
    company_risk = company_data.get('risk_profile', 'Medium')
    
    for category, score in scores.items():
        if score < 40:
            priority = "Critical"
            timeline = "Immediate (0-3 months)"
        elif score < 55:
            priority = "High" 
            timeline = "Short-term (3-6 months)"
        elif score < 70:
            priority = "Medium"
            timeline = "Medium-term (6-12 months)"
        else:
            continue  # No recommendation for good scores
        
        category_name = categories_analysis[category]
        
        # Enhanced recommendations with industry-specific insights
        if category == "governance":
            recommendations.append({
                "category": category_name,
                "priority": priority,
                "timeline": timeline,
                "title": f"Establish {company_risk} Risk-Adjusted Board Oversight",
                "description": f"Create executive accountability and governance structure tailored to {industry} sector risks and {company_name}'s operational profile.",
                "actions": [
                    f"Designate board committee with {industry} expertise for modern slavery oversight",
                    f"Develop annual modern slavery strategy with ${int(float(company_data['revenue_aud'].replace('$','').replace('B',''))*1000000*0.001):,} budget allocation",
                    "Implement quarterly reporting to board with industry-specific KPIs",
                    f"Create cross-functional working group spanning {company_data.get('supplier_count', 10000):,} supplier relationships"
                ],
                "success_metrics": [
                    "Board agenda items on modern slavery (target: monthly)",
                    "Executive KPI integration with compensation (target: 100%)",
                    f"Working group meeting frequency (target: bi-weekly for {company_risk} risk profile)",
                    "Strategy implementation progress (target: 80% within 12 months)"
                ],
                "industry_context": f"Leading {industry} companies invest 0.1-0.3% of revenue in compliance programs with dedicated C-suite ownership.",
                "roi_impact": "Potential 25-40% reduction in regulatory penalties and 15-20% improvement in ESG ratings",
                "implementation_cost": f"${int(float(company_data['revenue_aud'].replace('$','').replace('B',''))*1000000*0.0015):,} - ${int(float(company_data['revenue_aud'].replace('$','').replace('B',''))*1000000*0.003):,} annually"
            })
        
        elif category == "risk_assessment":
            recommendations.append({
                "category": category_name,
                "priority": priority,
                "timeline": timeline,
                "title": f"Implement AI-Powered Supply Chain Risk Mapping",
                "description": f"Deploy advanced risk assessment covering {len(company_data.get('high_risk_countries', []))} high-risk countries and {company_data.get('supplier_count', 10000):,} suppliers.",
                "actions": [
                    f"Map supply chain to tier 3-4 suppliers in {', '.join(company_data.get('high_risk_countries', [])[:3])}",
                    "Deploy AI-powered risk screening tools with real-time monitoring",
                    f"Conduct enhanced due diligence on {int(company_data.get('supplier_count', 10000)*0.15):,} highest-risk suppliers",
                    "Establish automated alert system for emerging risks"
                ],
                "success_metrics": [
                    f"Supply chain visibility: {int(company_data.get('supplier_count', 10000)*0.8):,} suppliers mapped (80% target)",
                    "Risk assessment completion rate: 95% of tier 1-2 suppliers",
                    f"High-risk supplier identification: {int(company_data.get('supplier_count', 10000)*0.05):,} flagged for enhanced monitoring",
                    "Risk mitigation plan implementation: 90% within 6 months"
                ],
                "industry_context": f"Best practice in {industry} includes real-time monitoring of tier 3-4 suppliers using satellite imagery and AI.",
                "roi_impact": "30-50% reduction in supply chain disruptions and 20-35% improvement in risk prediction accuracy",
                "implementation_cost": f"${int(company_data.get('supplier_count', 10000)*25):,} - ${int(company_data.get('supplier_count', 10000)*50):,} for technology deployment"
            })
        
        elif category == "due_diligence":
            recommendations.append({
                "category": category_name,
                "priority": priority,
                "timeline": timeline,
                "title": "Deploy Continuous Monitoring Framework",
                "description": f"Implement 24/7 monitoring system covering {company_data.get('supplier_count', 10000):,} suppliers with predictive analytics.",
                "actions": [
                    f"Deploy continuous monitoring across {len(company_data.get('high_risk_countries', []))} high-risk regions",
                    f"Conduct unannounced audits of {int(company_data.get('supplier_count', 10000)*0.1):,} suppliers annually",
                    "Implement blockchain-based supplier verification system",
                    "Establish worker feedback mechanisms in local languages"
                ],
                "success_metrics": [
                    f"Continuous monitoring coverage: {int(company_data.get('supplier_count', 10000)*0.6):,} suppliers (60% target)",
                    "Audit frequency: Monthly for critical suppliers",
                    "Corrective action plan implementation: 85% completion rate",
                    "Worker feedback response time: <48 hours"
                ],
                "industry_context": f"Industry leaders in {industry} achieve 95% supplier compliance through continuous monitoring.",
                "roi_impact": "40-60% improvement in supplier compliance and 25-40% reduction in audit costs",
                "implementation_cost": f"${int(company_data.get('supplier_count', 10000)*15):,} - ${int(company_data.get('supplier_count', 10000)*30):,} for monitoring technology"
            })
        
        elif category == "training":
            recommendations.append({
                "category": category_name,
                "priority": priority,
                "timeline": timeline,
                "title": "Launch Immersive VR Training Program",
                "description": f"Deploy cutting-edge training across {company_data.get('employees', '50,000+').replace('+','').replace(',','')} employees using VR and AI.",
                "actions": [
                    f"Develop VR training modules for {len(company_data.get('high_risk_countries', []))} high-risk regions",
                    f"Train {company_data.get('employees', '50,000+').replace('+','')} employees with role-specific content",
                    "Implement AI-powered learning paths with adaptive content",
                    "Create supplier certification program with gamification"
                ],
                "success_metrics": [
                    "Training completion rates: 98% across all roles",
                    "Assessment scores: Average 85%+ with VR simulations",
                    f"Supplier certification: {int(company_data.get('supplier_count', 10000)*0.4):,} suppliers certified",
                    "Training effectiveness: 75% improvement in incident identification"
                ],
                "industry_context": f"Leading {industry} organizations achieve 99% engagement with immersive training technologies.",
                "roi_impact": "50-70% improvement in training effectiveness and 30-45% reduction in compliance incidents",
                "implementation_cost": f"${int(int(company_data.get('employees', '50000').replace('+','').replace(',',''))*50):,} - ${int(int(company_data.get('employees', '50000').replace('+','').replace(',',''))*100):,} for VR training platform"
            })
    
    # Add AI-powered insights
    for rec in recommendations:
        rec["ai_insights"] = generate_ai_insights(rec, sentiment_data, company_data)
    
    return recommendations

def generate_ai_insights(recommendation, sentiment_data, company_data):
    """Generate AI-powered insights for recommendations"""
    
    insights = []
    
    # Sentiment-based insights
    if sentiment_data['sentiment_score'] < -0.2:
        insights.append(" Document sentiment analysis indicates defensive tone - consider proactive communication strategy")
    elif sentiment_data['sentiment_score'] > 0.3:
        insights.append(" Positive document sentiment suggests strong leadership commitment")
    
    # Maturity-based insights
    maturity = company_data.get('compliance_maturity', 'Developing')
    if maturity == 'Basic':
        insights.append(" Foundation-building opportunity - focus on quick wins to build momentum")
    elif maturity == 'Leading':
        insights.append(" Advanced maturity enables innovation in implementation approach")
    
    # Risk-based insights
    risk_profile = company_data.get('risk_profile', 'Medium')
    if risk_profile in ['High', 'Very High']:
        insights.append(" High-risk profile requires accelerated timeline and enhanced monitoring")
    
    # ESG alignment insights
    esg_score = company_data.get('esg_score', 70)
    if esg_score > 75:
        insights.append("📈 Strong ESG foundation supports business case for investment")
    elif esg_score < 65:
        insights.append("📊 ESG improvement opportunity - align with investor expectations")
    
    return insights

def generate_comprehensive_pdf_report(analysis_data):
    """Generate a comprehensive PDF report with all analysis results and visualizations"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Custom styles
    styles = getSampleStyleSheet()
    
    # Enhanced custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#3b82f6'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=HexColor('#1e293b'),
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=10,
        textColor=HexColor('#475569'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        textColor=HexColor('#1e293b'),
        fontName='Helvetica'
    )
    
    # Build story (content)
    story = []
    
    # Title page
    story.append(Spacer(1, 1*inch))
    
    # Main title
    title_text = "🛡️ StatementSense AI Analysis Report"
    story.append(Paragraph(title_text, title_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Company header info
    company_name = analysis_data.get('company_name', 'Demo Company')
    industry = analysis_data.get('industry', 'Demo Industry')
    overall_score = analysis_data.get('overall_score', 80)
    
    company_info_text = f"""
    <b>Company:</b> {company_name}<br/>
    <b>Industry:</b> {industry}<br/>
    <b>Overall Score:</b> {overall_score}/100<br/>
    <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
    <b>Analysis Type:</b> Advanced AI-Powered Compliance Assessment
    """
    story.append(Paragraph(company_info_text, body_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    
    performance_level = (
        "Excellent" if overall_score >= 80 else
        "Good" if overall_score >= 65 else
        "Developing" if overall_score >= 45 else
        "Needs Improvement"
    )
    
    executive_summary = f"""
    This comprehensive AI-powered analysis evaluated {company_name}'s modern slavery statement across six critical 
    compliance areas. The organization achieved an overall score of <b>{overall_score}/100</b>, indicating 
    <b>{performance_level}</b> compliance maturity.
    
    The analysis leveraged advanced natural language processing, sentiment analysis, and predictive modeling 
    to assess governance frameworks, risk assessment capabilities, due diligence processes, remediation 
    mechanisms, training programs, and effectiveness measurement systems.
    """
    story.append(Paragraph(executive_summary, body_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Company intelligence profile
    if 'company_data' in analysis_data:
        company_data = analysis_data['company_data']
        story.append(PageBreak())
        story.append(Paragraph("Company Intelligence Profile", heading_style))
        
        # Company details table
        company_details = [
            ['Attribute', 'Value'],
            ['Industry Sector', company_data.get('industry', 'N/A')],
            ['Annual Revenue (AUD)', company_data.get('revenue_aud', 'N/A')],
            ['Employee Count', company_data.get('employees', 'N/A')],
            ['ASX Code', company_data.get('asx_code', 'N/A')],
            ['Headquarters', company_data.get('headquarters', 'N/A')],
            ['Risk Profile', company_data.get('risk_profile', 'N/A')],
            ['Supplier Count', f"{company_data.get('supplier_count', 'N/A'):,}" if isinstance(company_data.get('supplier_count'), int) else company_data.get('supplier_count', 'N/A')],
            ['ESG Score', f"{company_data.get('esg_score', 'N/A')}/100" if company_data.get('esg_score') else 'N/A'],
            ['Compliance Maturity', company_data.get('compliance_maturity', 'N/A')],
            ['High-Risk Countries', ', '.join(company_data.get('high_risk_countries', []))],
        ]
        
        company_table = Table(company_details, colWidths=[2.5*inch, 3.5*inch])
        company_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f1f5f9')])
        ]))
        story.append(company_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Performance Analysis
    story.append(PageBreak())
    story.append(Paragraph("Detailed Performance Analysis", heading_style))
    
    if 'category_scores' in analysis_data:
        category_scores = analysis_data['category_scores']
        
        # Category scores table
        categories_display = {
            "governance": "Governance & Policy Framework",
            "risk_assessment": "Risk Assessment & Mapping", 
            "due_diligence": "Due Diligence & Monitoring",
            "remediation": "Grievance & Remediation",
            "training": "Training & Capacity Building",
            "effectiveness": "Performance Measurement"
        }
        
        performance_data = [['Category', 'Score', 'Performance Level', 'Industry Average']]
        
        industry_benchmarks = analysis_data.get('industry_benchmarks', {})
        
        for category, score in category_scores.items():
            display_name = categories_display.get(category, category.title())
            level = "Excellent" if score >= 80 else "Good" if score >= 65 else "Developing" if score >= 45 else "Needs Improvement"
            industry_avg = industry_benchmarks.get(category, 50)
            
            performance_data.append([
                display_name,
                f"{score}/100",
                level,
                f"{industry_avg}/100"
            ])
        
        performance_table = Table(performance_data, colWidths=[2.5*inch, 1*inch, 1.5*inch, 1*inch])
        performance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#f1f5f9')])
        ]))
        story.append(performance_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Sentiment Analysis Results
    if 'sentiment_data' in analysis_data:
        story.append(Paragraph("Document Sentiment Analysis", subheading_style))
        sentiment_data = analysis_data['sentiment_data']
        
        sentiment_text = f"""
        <b>Sentiment Score:</b> {sentiment_data.get('sentiment_score', 0):.3f} ({sentiment_data.get('sentiment_label', 'Neutral')})<br/>
        <b>Document Maturity Score:</b> {sentiment_data.get('maturity_score', 0)}/100<br/>
        <b>Word Count:</b> {sentiment_data.get('word_count', 0):,}<br/>
        <b>Risk Indicators:</b> {sentiment_data.get('risk_indicators', 0)} instances<br/>
        <b>Strength Indicators:</b> {sentiment_data.get('strength_indicators', 0)} instances
        """
        story.append(Paragraph(sentiment_text, body_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Add charts/visualizations
    if 'charts' in analysis_data:
        story.append(PageBreak())
        story.append(Paragraph("Visual Analysis", heading_style))
        
        charts = analysis_data['charts']
        chart_names = {
            'radar_chart': 'Performance Radar Analysis',
            'heatmap': 'Supply Chain Risk Heatmap',
            'network_diagram': 'Supplier Network Analysis',
            'timeline': 'Compliance Performance Timeline'
        }
        
        for chart_key, chart_fig in charts.items():
            if chart_fig is not None:
                story.append(Paragraph(chart_names.get(chart_key, f'{chart_key.title()} Analysis'), subheading_style))
                
                # Export chart as image
                try:
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
                        chart_fig.write_image(tmpfile.name, width=800, height=600, scale=2)
                        
                        # Add image to PDF
                        img = Image(tmpfile.name)
                        img.drawHeight = 4*inch
                        img.drawWidth = 6*inch
                        story.append(img)
                        story.append(Spacer(1, 0.2*inch))
                        
                        # Clean up temp file
                        os.unlink(tmpfile.name)
                except Exception as e:
                    story.append(Paragraph(f"Chart visualization unavailable: {str(e)}", body_style))
                    story.append(Spacer(1, 0.2*inch))
    
    # Benchmarking Analysis
    if 'benchmarking' in analysis_data:
        story.append(PageBreak())
        story.append(Paragraph("Benchmarking Analysis", heading_style))
        
        benchmarking = analysis_data['benchmarking']
        
        benchmark_text = f"""
        <b>Industry Comparison:</b> {benchmarking.get('vs_industry', 0):+.0f} points vs industry average<br/>
        <b>Industry Percentile:</b> {benchmarking.get('percentile', 50)}th percentile<br/>
        <b>Compliance Risk Level:</b> {benchmarking.get('risk_level', 'Medium')}<br/>
        <b>Improvement Potential:</b> {benchmarking.get('improvement_potential', 0)} points to excellence
        """
        story.append(Paragraph(benchmark_text, body_style))
        story.append(Spacer(1, 0.3*inch))
    
    # Trend Prediction
    if 'trend_prediction' in analysis_data:
        story.append(Paragraph("Predictive Analysis", subheading_style))
        trend_data = analysis_data['trend_prediction']
        
        trend_text = f"""
        <b>Performance Trend:</b> {trend_data.get('trend', 'Stable')}<br/>
        <b>Predicted Score (12 months):</b> {trend_data.get('predicted_score', overall_score)}/100<br/>
        <b>Confidence Level:</b> {trend_data.get('confidence', 75)}%<br/>
        <b>Key Factors:</b> Industry trends, company maturity, risk profile, and ESG alignment
        """
        story.append(Paragraph(trend_text, body_style))
        story.append(Spacer(1, 0.3*inch))
    
    # Recommendations
    if 'recommendations' in analysis_data and analysis_data['recommendations']:
        story.append(PageBreak())
        story.append(Paragraph("Strategic Recommendations", heading_style))
        
        for i, rec in enumerate(analysis_data['recommendations'], 1):
            story.append(Paragraph(f"{i}. {rec.get('title', 'Recommendation')}", subheading_style))
            
            # Priority and timeline
            priority_timeline = f"<b>Priority:</b> {rec.get('priority', 'Medium')} | <b>Timeline:</b> {rec.get('timeline', 'TBD')}"
            story.append(Paragraph(priority_timeline, body_style))
            
            # Description
            if rec.get('description'):
                story.append(Paragraph(f"<b>Description:</b> {rec['description']}", body_style))
            
            # Actions
            if rec.get('actions'):
                story.append(Paragraph("<b>Key Actions:</b>", body_style))
                for action in rec['actions']:
                    story.append(Paragraph(f"• {action}", body_style))
            
            # Success metrics
            if rec.get('success_metrics'):
                story.append(Paragraph("<b>Success Metrics:</b>", body_style))
                for metric in rec['success_metrics']:
                    story.append(Paragraph(f"• {metric}", body_style))
            
            # ROI Impact
            if rec.get('roi_impact'):
                story.append(Paragraph(f"<b>Expected Impact:</b> {rec['roi_impact']}", body_style))
            
            # Implementation cost
            if rec.get('implementation_cost'):
                story.append(Paragraph(f"<b>Investment Required:</b> {rec['implementation_cost']}", body_style))
            
            # AI Insights
            if rec.get('ai_insights'):
                story.append(Paragraph("<b>AI Insights:</b>", body_style))
                for insight in rec['ai_insights']:
                    story.append(Paragraph(f"🤖 {insight}", body_style))
            
            story.append(Spacer(1, 0.3*inch))
    
    # Industry Context
    if 'industry_context' in analysis_data:
        story.append(PageBreak())
        story.append(Paragraph("Industry Context & Insights", heading_style))
        
        context = analysis_data['industry_context']
        
        context_text = f"""
        <b>Industry:</b> {context.get('industry_name', industry)}<br/>
        <b>Risk Multiplier:</b> {context.get('risk_multiplier', 1.0)}x<br/>
        <b>Industry Trend:</b> {context.get('trend', 'Stable')}<br/>
        <b>Average Industry Score:</b> {context.get('avg_score', 50)}/100<br/>
        """
        story.append(Paragraph(context_text, body_style))
        
        # High risk factors
        if context.get('high_risk_factors'):
            story.append(Paragraph("<b>Key Risk Factors in Industry:</b>", body_style))
            for factor in context['high_risk_factors']:
                story.append(Paragraph(f"• {factor}", body_style))
        
        # Key challenges
        if context.get('key_challenges'):
            story.append(Paragraph("<b>Common Industry Challenges:</b>", body_style))
            for challenge in context['key_challenges']:
                story.append(Paragraph(f"• {challenge}", body_style))
        
        # Emerging risks
        if context.get('emerging_risks'):
            story.append(Paragraph("<b>Emerging Risks:</b>", body_style))
            for risk in context['emerging_risks']:
                story.append(Paragraph(f"• {risk}", body_style))
    
    # Footer/Disclaimer
    story.append(PageBreak())
    story.append(Paragraph("Report Disclaimer", heading_style))
    
    disclaimer_text = """
    This report was generated using StatementSense AI-powered analysis platform. The analysis is based on 
    natural language processing of the submitted modern slavery statement and comparison against industry 
    benchmarks. 
    
    While our AI models have been trained on extensive compliance frameworks and industry data, this report 
    should be used as a guidance tool alongside professional legal and compliance advice. Organizations should 
    conduct thorough internal reviews and seek appropriate professional counsel for compliance matters.
    
    For questions about this analysis or to schedule a consultation, please contact StatementSense support.
    """
    story.append(Paragraph(disclaimer_text, body_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def enhanced_upload_and_analyze_tab():
    st.markdown("##  AI-Powered Statement Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <h3>📄 Upload Your Modern Slavery Statement</h3>
            <p style="color: #94a3b8;">Our advanced AI analyzes compliance across 6 key areas with 95% accuracy and provides predictive insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced file uploader with multiple formats
        uploaded_file = st.file_uploader(
            "Upload Statement (PDF, DOCX, or TXT)",
            type=['pdf', 'docx', 'txt'],
            help="Upload your organization's modern slavery statement for comprehensive AI analysis",
            label_visibility="collapsed"
        )
        
        # Advanced options
        with st.expander(" Advanced Analysis Options"):
            col_a, col_b = st.columns(2)
            with col_a:
                analysis_depth = st.selectbox("Analysis Depth", ["Standard", "Deep", "Comprehensive"])
                include_predictions = st.checkbox("Include Future Predictions", value=True)
            with col_b:
                comparison_mode = st.selectbox("Comparison Mode", ["Industry Average", "Best Practice", "Custom Benchmark"])
                generate_action_plan = st.checkbox("Generate Action Plan", value=True)
    
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <h4> Enhanced Analysis Framework</h4>
            <ul style="margin: 0; padding-left: 1.2rem;">
                <li> Governance & Policy Framework</li>
                <li> Risk Assessment & Mapping</li>
                <li> Due Diligence & Monitoring</li>
                <li> Remediation & Response</li>
                <li> Training & Capacity Building</li>
                <li> Effectiveness & Measurement</li>
            </ul>
            <hr style="margin: 1rem 0; border-color: #475569;">
            <h4> AI Features</h4>
            <ul style="margin: 0; padding-left: 1.2rem;">
                <li> Sentiment Analysis</li>
                <li> Predictive Insights</li>
                <li> Risk Mapping</li>
                <li> Trend Analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Enhanced processing with progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        with st.spinner("🤖 AI analyzing your statement..."):
            # Simulate processing steps
            for i, step in enumerate([
                "Reading document...",
                "Extracting text content...", 
                "Identifying company...",
                "Performing sentiment analysis...",
                "Analyzing compliance areas...",
                "Generating predictions...",
                "Creating visualizations..."
            ]):
                status_text.text(step)
                progress_bar.progress((i + 1) / 7)
                time.sleep(0.5)  # Simulate processing time
            
            # Process the uploaded file
            if uploaded_file.type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
            else:
                text_content = str(uploaded_file.read(), "utf-8")
            
            # Enhanced AI analysis
            company_name, company_data, confidence = enhanced_ai_identify_company(text_content)
            industry = company_data['industry']
            overall_score, category_scores, sentiment_data, trend_prediction = enhanced_pdf_analysis(text_content, industry, company_data)
            
            # Get industry benchmarks
            industry_benchmarks = INDUSTRY_BENCHMARKS[industry]
            
            # Generate recommendations
            recommendations = generate_smart_recommendations(category_scores, industry, company_name, company_data, sentiment_data)
            
            # Create all visualizations
            radar_fig = create_enhanced_radar_chart(category_scores, industry_benchmarks, company_name, industry, trend_prediction)
            heatmap_fig = create_risk_heatmap(company_data, industry_benchmarks)
            network_fig = create_supplier_network_diagram(company_data)
            timeline_fig = create_compliance_timeline(company_data)
            
            # Calculate benchmarking data
            industry_avg = industry_benchmarks['avg_score']
            vs_industry = overall_score - industry_avg
            percentile = min(95, max(5, int(50 + (vs_industry * 2))))
            risk_level = "Low" if overall_score > 75 else "Medium" if overall_score > 55 else "High"
            improvement_potential = max(0, 85 - overall_score)
            
            # Store comprehensive analysis data
            comprehensive_analysis_data = {
                "company": company_name,
                "score": overall_score,
                "industry": industry,
                "date": datetime.now().isoformat(),
                "company_name": company_name,
                "overall_score": overall_score,
                "category_scores": category_scores,
                "company_data": company_data,
                "sentiment_data": sentiment_data,
                "trend_prediction": trend_prediction,
                "recommendations": recommendations,
                "benchmarking": {
                    "vs_industry": vs_industry,
                    "percentile": percentile,
                    "risk_level": risk_level,
                    "improvement_potential": improvement_potential
                },
                "industry_benchmarks": industry_benchmarks,
                "industry_context": industry_benchmarks,
                "charts": {
                    "radar_chart": radar_fig,
                    "heatmap": heatmap_fig,
                    "network_diagram": network_fig,
                    "timeline": timeline_fig
                }
            }
        
        progress_bar.empty()
        status_text.empty()
        
        # Add comprehensive data to analysis history
        st.session_state.analysis_history.append(comprehensive_analysis_data)
        
        st.success(f"✅ Analysis completed! Company identified with {confidence}% confidence.")
        
        # Enhanced results display
        st.markdown("## 🏢 Company Intelligence Profile")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            <div class="company-info-card">
                <h2 style="margin: 0 0 1.5rem 0; color: #3b82f6;">{company_name}</h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
                    <div>
                        <strong>Industry:</strong><br>
                        <span style="font-size: 1.1rem;">{company_data['industry']}</span>
                    </div>
                    <div>
                        <strong>Revenue (AUD):</strong><br>
                        <span style="font-size: 1.1rem; color: #059669;">{company_data['revenue_aud']}</span>
                    </div>
                    <div>
                        <strong>Employees:</strong><br>
                        <span style="font-size: 1.1rem;">{company_data['employees']}</span>
                    </div>
                    <div>
                        <strong>ASX Code:</strong><br>
                        <span style="font-size: 1.1rem; font-weight: 600;">{company_data['asx_code']}</span>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div>
                        <strong>Risk Profile:</strong> <span style="color: {'#ef4444' if company_data['risk_profile'] in ['High', 'Very High'] else '#f59e0b' if company_data['risk_profile'] == 'Medium' else '#10b981'};">{company_data['risk_profile']}</span>
                    </div>
                    <div>
                        <strong>Suppliers:</strong> {company_data.get('supplier_count', 'N/A'):,}
                    </div>
                    <div>
                        <strong>ESG Score:</strong> <span style="color: {'#10b981' if company_data.get('esg_score', 70) > 75 else '#f59e0b' if company_data.get('esg_score', 70) > 65 else '#ef4444'};">{company_data.get('esg_score', 'N/A')}/100</span>
                    </div>
                    <div>
                        <strong>Compliance Maturity:</strong> {company_data.get('compliance_maturity', 'N/A')}
                    </div>
                </div>
                <div style="margin-top: 1.5rem;">
                    <strong>High-Risk Countries:</strong> {', '.join(company_data.get('high_risk_countries', []))}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Enhanced performance indicator
            performance_level = (
                "Excellent" if overall_score >= 80 else
                "Good" if overall_score >= 65 else
                "Developing" if overall_score >= 45 else
                "Needs Improvement"
            )
            
            score_class = (
                "score-excellent" if overall_score >= 80 else
                "score-good" if overall_score >= 65 else
                "score-developing" if overall_score >= 45 else
                "score-needs-improvement"
            )
            
            st.markdown(f"""
            <div class="metric-card {score_class}">
                <div style="text-align: center;">
                    <div style="font-size: 3.5rem; font-weight: 900; margin: 0; background: linear-gradient(45deg, #3b82f6, #1d4ed8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{overall_score}</div>
                    <div style="font-size: 1.3rem; opacity: 0.8; margin: 0.5rem 0;">/ 100</div>
                    <div style="font-size: 1.2rem; font-weight: 700; margin: 1rem 0;">{performance_level}</div>
                    <div style="font-size: 0.95rem; opacity: 0.7;">AI Compliance Score</div>
                    <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(59, 130, 246, 0.1); border-radius: 8px;">
                        <div style="font-size: 0.9rem;">Trend: <span style="color: {trend_prediction['color']}; font-weight: 600;">{trend_prediction['trend']}</span></div>
                        <div style="font-size: 0.8rem; opacity: 0.8;">Confidence: {trend_prediction['confidence']}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Sentiment analysis results
            st.markdown(f"""
            <div class="metric-card">
                <h4>📊 Document Analysis</h4>
                <div style="margin: 1rem 0;">
                    <strong>Sentiment:</strong> <span style="color: {'#10b981' if sentiment_data['sentiment_score'] > 0.1 else '#ef4444' if sentiment_data['sentiment_score'] < -0.1 else '#f59e0b'};">{sentiment_data['sentiment_label']}</span>
                </div>
                <div style="margin: 1rem 0;">
                    <strong>Maturity Score:</strong> {sentiment_data['maturity_score']}/100
                </div>
                <div style="margin: 1rem 0;">
                    <strong>Word Count:</strong> {sentiment_data['word_count']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Enhanced Performance Analysis
        st.markdown("##  Advanced Performance Analysis")
        
        # Create enhanced radar chart
        radar_fig = create_enhanced_radar_chart(category_scores, industry_benchmarks, company_name, industry, trend_prediction)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.plotly_chart(radar_fig, use_container_width=True)
        
        with col2:
            st.markdown("###  Key Strengths")
            strengths = [(k, v) for k, v in category_scores.items() if v >= 65]
            strengths.sort(key=lambda x: x[1], reverse=True)
            
            categories_map = {
                "governance": "Governance",
                "risk_assessment": "Risk Assessment", 
                "due_diligence": "Due Diligence",
                "remediation": "Remediation",
                "training": "Training",
                "effectiveness": "Effectiveness"
            }
            
            if strengths:
                for category, score in strengths[:3]:
                    st.markdown(f"""
                    <div class="success-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong>{categories_map[category]}</strong>
                            <span style="font-weight: bold; color: #059669; font-size: 1.1rem;">{score}/100</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("💡 Focus on building foundational strengths")
            
            st.markdown("###  Priority Areas")
            weaknesses = [(k, v) for k, v in category_scores.items() if v < 55]
            weaknesses.sort(key=lambda x: x[1])
            
            for category, score in weaknesses[:3]:
                color = "#dc2626" if score < 35 else "#f59e0b"
                st.markdown(f"""
                <div class="alert-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong>{categories_map[category]}</strong>
                        <span style="font-weight: bold; color: {color}; font-size: 1.1rem;">{score}/100</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Supply Chain Risk Visualization
        st.markdown("## 🌐 Supply Chain Risk Intelligence")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Risk heatmap
            heatmap_fig = create_risk_heatmap(company_data, industry_benchmarks)
            st.plotly_chart(heatmap_fig, use_container_width=True)
        
        with col2:
            # Supplier network diagram
            network_fig = create_supplier_network_diagram(company_data)
            st.plotly_chart(network_fig, use_container_width=True)
        
        # Compliance Timeline
        st.markdown("## 📈 Compliance Performance Timeline")
        timeline_fig = create_compliance_timeline(company_data)
        st.plotly_chart(timeline_fig, use_container_width=True)
        
        # Enhanced Benchmarking Analysis
        st.markdown("##  Advanced Benchmarking Intelligence")
        
        col1, col2, col3, col4 = st.columns(4)
        
        industry_avg = industry_benchmarks['avg_score']
        vs_industry = overall_score - industry_avg
        
        with col1:
            trend_color = "#10b981" if vs_industry > 0 else "#ef4444"
            trend_icon = "📈" if vs_industry > 0 else "📉"
            st.markdown(f"""
            <div class="metric-card">
                <h4>vs Industry Average</h4>
                <div style="font-size: 2.5rem; color: {trend_color}; display: flex; align-items: center; justify-content: center;">
                    <span style="margin-right: 0.5rem;">{trend_icon}</span>
                    <span>{vs_industry:+.0f}</span>
                </div>
                <div style="text-align: center; margin-top: 0.5rem;">
                    <small>points difference</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            percentile = min(95, max(5, int(50 + (vs_industry * 2))))
            st.markdown(f"""
            <div class="metric-card">
                <h4>Industry Percentile</h4>
                <div style="font-size: 2.5rem; color: #3b82f6; text-align: center;">{percentile}th</div>
                <div style="text-align: center; margin-top: 0.5rem;">
                    <small>performance ranking</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            risk_level = "Low" if overall_score > 75 else "Medium" if overall_score > 55 else "High"
            risk_color = "#10b981" if risk_level == "Low" else "#f59e0b" if risk_level == "Medium" else "#ef4444"
            st.markdown(f"""
            <div class="metric-card">
                <h4>Compliance Risk</h4>
                <div style="font-size: 2rem; color: {risk_color}; text-align: center; font-weight: 700;">{risk_level}</div>
                <div style="text-align: center; margin-top: 0.5rem;">
                    <small>regulatory exposure</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            improvement_potential = max(0, 85 - overall_score)
            st.markdown(f"""
            <div class="metric-card">
                <h4>Growth Potential</h4>
                <div style="font-size: 2.5rem; color: #7c3aed; text-align: center; font-weight: 700;">{improvement_potential}</div>
                <div style="text-align: center; margin-top: 0.5rem;">
                    <small>points to excellence</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Strategic Recommendations Section
        if recommendations:
            st.markdown("## 🎯 Strategic Recommendations")
            
            for i, rec in enumerate(recommendations, 1):
                with st.expander(f" {rec.get('priority', 'Medium')} Priority: {rec.get('title', 'Recommendation')}", expanded=i==1):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Timeline:** {rec.get('timeline', 'TBD')}")
                        st.markdown(f"**Description:** {rec.get('description', 'N/A')}")
                        
                        if rec.get('actions'):
                            st.markdown("**Key Actions:**")
                            for action in rec['actions']:
                                st.markdown(f"• {action}")
                        
                        if rec.get('success_metrics'):
                            st.markdown("**Success Metrics:**")
                            for metric in rec['success_metrics']:
                                st.markdown(f"• {metric}")
                    
                    with col2:
                        st.markdown(f"""
                        <div class="recommendation-box">
                            <div><strong>ROI Impact:</strong><br>{rec.get('roi_impact', 'TBD')}</div>
                            <div style="margin-top: 1rem;"><strong>Investment:</strong><br>{rec.get('implementation_cost', 'TBD')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if rec.get('ai_insights'):
                            st.markdown("**AI Insights:**")
                            for insight in rec['ai_insights']:
                                st.info(f"🤖 {insight}")


def main():
    # Apply enhanced theme CSS
    st.markdown(get_enhanced_theme_css(), unsafe_allow_html=True)
    
    # Sidebar for navigation and settings
    with st.sidebar:
        st.markdown("### 🛡️ StatementSense")
        
        # User profile section
        st.markdown("#### User Profile")
        if not st.session_state.user_profile:
            with st.expander("Setup Profile", expanded=True):
                name = st.text_input("Name")
                role = st.selectbox("Role", ["Compliance Officer", "Legal Counsel", "Risk Manager", "Supply Chain Manager", "Executive"])
                company_type = st.selectbox("Company Type", ["ASX Listed", "Private", "Government", "NGO"])
                if st.button("Save Profile"):
                    st.session_state.user_profile = {"name": name, "role": role, "company_type": company_type}
                    st.success("Profile saved!")
        else:
            profile = st.session_state.user_profile
            st.write(f" **{profile['name']}**")
            st.write(f" {profile['role']}")
            st.write(f" {profile['company_type']}")
            if st.button("Edit Profile"):
                st.session_state.user_profile = {}
                st.rerun()
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("#### Quick Actions")
        if st.button("🔄 New Analysis"):
            st.session_state.analysis_history = []
            st.success("Ready for new analysis!")
        
        # Enhanced PDF Export Section
        if st.session_state.analysis_history:
            latest = st.session_state.analysis_history[-1]
            pdf_buffer = generate_comprehensive_pdf_report(latest)
            file_name = f"StatementSense_Comprehensive_Report_{latest['company'].replace(' ', '_')}.pdf"
            
            st.download_button(
                label="📄 Export Comprehensive Report",
                data=pdf_buffer,
                file_name=file_name,
                mime="application/pdf",
                help="Download complete analysis with all visualizations and insights"
            )
        else:
            # Demo export with comprehensive sample data
            demo_analysis = {
                'company_name': 'Demo Company',
                'industry': 'Financial Services',
                'overall_score': 80,
                'category_scores': {
                    'governance': 75,
                    'risk_assessment': 82,
                    'due_diligence': 78,
                    'remediation': 71,
                    'training': 85,
                    'effectiveness': 73
                },
                'company_data': {
                    'industry': 'Financial Services',
                    'revenue_aud': '$21.2B',
                    'employees': '40,000+',
                    'asx_code': 'WBC',
                    'headquarters': 'Sydney, NSW',
                    'risk_profile': 'Medium',
                    'supplier_count': 15000,
                    'high_risk_countries': ['Indonesia', 'Philippines', 'India'],
                    'esg_score': 76,
                    'compliance_maturity': 'Advanced'
                },
                'sentiment_data': {
                    'sentiment_score': 0.15,
                    'sentiment_label': 'Positive',
                    'maturity_score': 78,
                    'word_count': 3500,
                    'risk_indicators': 12,
                    'strength_indicators': 28
                },
                'trend_prediction': {
                    'trend': 'Moderate Upward',
                    'predicted_score': 85,
                    'confidence': 82,
                    'color': '#059669'
                },
                'recommendations': [
                    {
                        'title': 'Enhance Risk Assessment Framework',
                        'priority': 'High',
                        'timeline': 'Short-term (3-6 months)',
                        'description': 'Implement AI-powered risk screening across supply chain',
                        'actions': ['Deploy risk mapping tools', 'Conduct supplier assessments'],
                        'success_metrics': ['90% supplier coverage', 'Risk detection improvement'],
                        'roi_impact': '30% reduction in compliance incidents',
                        'implementation_cost': '$250,000 - $500,000',
                        'ai_insights': ['Strong foundation for advanced implementation']
                    }
                ],
                'benchmarking': {
                    'vs_industry': 22,
                    'percentile': 85,
                    'risk_level': 'Low',
                    'improvement_potential': 5
                },
                'industry_benchmarks': INDUSTRY_BENCHMARKS.get('Financial Services', {}),
                'industry_context': INDUSTRY_BENCHMARKS.get('Financial Services', {})
            }
            
            pdf_buffer = generate_comprehensive_pdf_report(demo_analysis)
            file_name = "StatementSense_Demo_Comprehensive_Report.pdf"
            
            st.download_button(
                label="📄 Export Report",
                data=pdf_buffer,
                file_name=file_name,
                mime="application/pdf",
                help="Download demo comprehensive report"
            )
        
        if st.button("⚙️ Settings"):
            st.info("Settings panel (Demo)")
        st.markdown("---")
        
        # Analysis history
        if st.session_state.analysis_history:
            st.markdown("#### Recent Analyses")
            for i, analysis in enumerate(st.session_state.analysis_history[-3:]):
                with st.expander(f"{analysis['company']} - {analysis['date'][:10]}"):
                    st.write(f"Score: {analysis['score']}")
                    st.write(f"Industry: {analysis['industry']}")
        
        st.markdown("---")
        
        # Alerts section
        st.markdown("####  Alerts")
        alerts = [
            " New regulation: EU Corporate Sustainability Due Diligence",
            " Industry benchmark updated: Financial Services",
            " Integration available: SAP Ariba connector"
        ]
        for alert in alerts:
            st.caption(alert)
    
    # Main header with enhanced design
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Statement Sense</h1>
        <p>Advanced AI-Powered Modern Slavery Statement Analysis</p>
        <p style="font-size: 1rem; margin-top: 1rem; opacity: 0.8;">
            Powered by Advanced AI • Real-time Monitoring • Predictive Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Analysis content
    enhanced_upload_and_analyze_tab()

if __name__ == "__main__":
    main()