import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Breaking Chains: Modern Slavery Exposed",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS with original theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;700;900&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: white;
    }
    
    .main-header {
        background: linear-gradient(135deg, rgba(15,23,42,0.95) 0%, rgba(30,41,59,0.95) 100%);
        backdrop-filter: blur(20px);
        padding: 5rem 2rem;
        margin: -1rem -1rem 4rem -1rem;
        border-bottom: 6px solid #fbbf24;
        text-align: center;
        position: relative;
        overflow: hidden;
        border-radius: 0 0 50px 50px;
        box-shadow: 0 25px 80px rgba(0,0,0,0.4);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 300"><defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:rgba(251,191,36,0.1);stop-opacity:1" /><stop offset="100%" style="stop-color:rgba(245,158,11,0.1);stop-opacity:1" /></linearGradient></defs><path d="M0,100 Q250,50 500,100 T1000,100 L1000,300 L0,300 Z" fill="url(%23grad1)"/></svg>');
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 5rem;
        font-weight: 900;
        letter-spacing: -4px;
        position: relative;
        z-index: 1;
        font-family: 'Playfair Display', serif;
        text-shadow: 0 8px 30px rgba(0,0,0,0.7);
        line-height: 1.1;
    }
    
    .main-header p {
        color: #e2e8f0;
        margin: 2rem 0 0 0;
        font-size: 1.8rem;
        font-weight: 500;
        position: relative;
        z-index: 1;
        opacity: 0.95;
        letter-spacing: 1px;
    }
    
    .hero-stat {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        padding: 6rem 3rem;
        border-radius: 35px;
        text-align: center;
        color: #1a2332;
        margin: 5rem auto;
        box-shadow: 0 40px 120px rgba(251, 191, 36, 0.5);
        max-width: 900px;
        position: relative;
        overflow: hidden;
        transform: perspective(1200px) rotateX(8deg);
        transition: all 0.4s ease;
    }
    
    .hero-stat:hover {
        transform: perspective(1200px) rotateX(0deg) translateY(-15px);
        box-shadow: 0 50px 140px rgba(251, 191, 36, 0.6);
    }
    
    .hero-stat::before {
        content: '';
        position: absolute;
        top: -100%;
        left: -100%;
        width: 300%;
        height: 300%;
        background: conic-gradient(from 0deg, rgba(255,255,255,0.15), transparent, rgba(255,255,255,0.15));
        animation: rotate 6s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hero-stat h2 {
        font-size: 8rem;
        font-weight: 900;
        margin: 0;
        line-height: 0.9;
        position: relative;
        z-index: 1;
        text-shadow: 0 6px 25px rgba(0,0,0,0.3);
        font-family: 'Inter', sans-serif;
    }
    
    .hero-stat p {
        font-size: 2rem;
        font-weight: 700;
        margin: 2rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 4px;
        position: relative;
        z-index: 1;
    }
    
    .section-header {
        background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(30,41,59,0.9) 100%);
        backdrop-filter: blur(15px);
        color: white;
        padding: 4rem 3rem;
        margin: 8rem -1rem 5rem -1rem;
        font-size: 3.5rem;
        font-weight: 900;
        border-left: 12px solid #fbbf24;
        position: relative;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        border-radius: 0 30px 30px 0;
        font-family: 'Playfair Display', serif;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        width: 12px;
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        border-radius: 0 30px 30px 0;
    }
    
    .image-overlay {
        position: relative;
        margin: 4rem 0;
        border-radius: 25px;
        overflow: hidden;
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
        transition: all 0.4s ease;
    }
    
    .image-overlay:hover {
        transform: translateY(-5px);
        box-shadow: 0 40px 100px rgba(0, 0, 0, 0.6);
    }
    
    .image-overlay img {
        width: 100%;
        height: 500px;
        object-fit: cover;
        transition: transform 0.4s ease;
        filter: brightness(0.85) contrast(1.1);
    }
    
    .image-overlay:hover img {
        transform: scale(1.05);
        filter: brightness(0.9) contrast(1.2);
    }
    
    .image-overlay-text {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(transparent, rgba(0,0,0,0.9));
        color: white;
        padding: 4rem 3rem;
        font-size: 1.4rem;
        font-weight: 600;
        line-height: 1.7;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }
    
    .vulnerability-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 3rem;
        margin: 4rem 0;
    }
    
    .vulnerability-card {
        position: relative;
        border-radius: 25px;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        transition: all 0.4s ease;
    }
    
    .vulnerability-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 30px 80px rgba(0, 0, 0, 0.5);
    }
    
    .vulnerability-card img {
        width: 100%;
        height: 350px;
        object-fit: cover;
        filter: brightness(0.8) contrast(1.1);
        transition: all 0.4s ease;
    }
    
    .vulnerability-card:hover img {
        transform: scale(1.05);
        filter: brightness(0.85) contrast(1.2);
    }
    
    .vulnerability-card-text {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(transparent, rgba(0,0,0,0.95));
        color: white;
        padding: 3rem;
        font-size: 1.2rem;
        font-weight: 500;
        line-height: 1.6;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
    }
    
    .testimonial-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.12) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 3rem;
        margin: 3rem 0;
        border: 2px solid rgba(255,255,255,0.2);
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        position: relative;
        transition: all 0.4s ease;
    }
    
    .testimonial-card:hover {
        transform: translateY(-8px);
        border-color: rgba(251, 191, 36, 0.5);
        box-shadow: 0 30px 80px rgba(0,0,0,0.4);
    }
    
    .testimonial-card::before {
        content: '"';
        position: absolute;
        top: -15px;
        left: 25px;
        font-size: 6rem;
        color: #fbbf24;
        font-family: 'Playfair Display', serif;
        opacity: 0.6;
        text-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .testimonial-text {
        font-style: italic;
        font-size: 1.2rem;
        line-height: 1.7;
        margin-bottom: 1.5rem;
        color: #e2e8f0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    .testimonial-author {
        font-weight: 700;
        color: #fbbf24;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Enhanced metric cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.95) 100%);
        backdrop-filter: blur(25px);
        border: none;
        padding: 3.5rem;
        border-radius: 30px;
        box-shadow: 0 25px 80px rgba(0, 0, 0, 0.2);
        border-top: 10px solid #1a2332;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    [data-testid="metric-container"]::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255,255,255,0.8);
        border-radius: 30px;
        z-index: 1;
    }
    
    [data-testid="metric-container"] > div {
        position: relative;
        z-index: 2;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 35px 100px rgba(0, 0, 0, 0.25);
    }
    
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 10px;
        background: linear-gradient(90deg, #1a2332, #fbbf24, #1a2332);
        background-size: 200% 100%;
        animation: gradient-shift 4s ease-in-out infinite;
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 200% 0; }
        50% { background-position: -200% 0; }
    }
    
    [data-testid="metric-container"] > div {
        width: fit-content;
        margin: auto;
        text-align: center;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 4.5rem;
        font-weight: 900;
        color: #1a2332;
        text-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    [data-testid="metric-container"] [data-testid="metric-label"] {
        font-size: 1.4rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    [data-testid="metric-container"] [data-testid="metric-delta"] {
        font-size: 1rem;
        font-weight: 700;
        padding: 0.5rem 1rem;
        background: rgba(34, 197, 94, 0.1);
        border-radius: 25px;
        color: #22c55e;
        margin-top: 0.5rem;
    }
    
    .metric-card {
        background: black;
        border: 2px solid #e5e7eb;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        border-color: #fbbf24;
    }
    
    .metric-card h3 {
        font-size: 2.5rem;
        font-weight: 900;
        color: white;
        margin: 0 0 0.5rem 0;
    }
    
    .metric-card p {
        color: #e2e8f0;
        font-weight: 600;
        margin: 0;
    }
    
    .emergency-box {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        padding: 3rem;
        border-radius: 25px;
        margin-top: 3rem;
        box-shadow: 0 20px 60px rgba(220, 38, 38, 0.5);
        color: white;
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255,255,255,0.2);
        text-align: center;
    }
    
    .emergency-box h5 {
        margin: 0 0 1rem 0;
        font-size: 1.4rem;
        font-weight: 800;
    }
    
    .emergency-box p {
        margin: 0.5rem 0;
        font-weight: 700;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>UNDERSTANDING THE SCALE OF MODERN SLAVERY</h1>
    <p>Global Overview and Australia's Response</p>
</div>
""", unsafe_allow_html=True)

# Hero statistic section
st.markdown("""
<div class="hero-stat">
    <h2>49.6 MILLION</h2>
    <p>People in Modern Slavery Worldwide</p>
</div>
""", unsafe_allow_html=True)

# Add powerful opening testimonials
st.markdown("## Behind Every Number is a Human Story")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-text">
            They promised me good work in Australia. Instead, I worked 16 hours a day in construction with no pay, 
            sleeping in a shed with 8 other workers. My passport was taken, and they said if I complained, 
            I'd be deported. It took 3 years before someone helped me escape.
        </div>
        <div class="testimonial-author">— Ahmed, Construction Worker (Name Changed for Protection)</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="testimonial-card">
        <div class="testimonial-text">
            I was married at 16 to a man I'd never met. When I tried to refuse, my family said it would bring shame. 
            The abuse started immediately. I didn't know this was called modern slavery until I found help years later. 
            Breaking free was the hardest thing I ever did, but I'm not alone.
        </div>
        <div class="testimonial-author">— Fatima, Forced Marriage Survivor (Name Changed for Protection)</div>
    </div>
    """, unsafe_allow_html=True)

# Global Overview Section
st.markdown('<div class="section-header">GLOBAL OVERVIEW</div>', unsafe_allow_html=True)

# Hero image
st.markdown("""
<div class="image-overlay">
    <img src="https://images.unsplash.com/photo-1594736797933-d0d55ff4d8c7?w=800&h=500&fit=crop" alt="Hands breaking chains"/>
    <div class="image-overlay-text">
        Modern slavery is hidden in plain sight and deeply intertwined with life in every corner of the world. 
        49.6 million people trapped in exploitation, with women and children bearing the heaviest burden.
    </div>
</div>
""", unsafe_allow_html=True)

# What is Modern Slavery section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### What is Modern Slavery?
    
    Modern slavery takes many forms and is known by many names. Essentially, it refers to **situations of 
    exploitation that a person cannot refuse or leave because of threats, violence, coercion, or deception.**
    
    **Modern slavery includes:**
    
    • **Forced labour** - work extracted under threat of penalty  
    • **Forced or servile marriage** - marriages without free and full consent  
    • **Debt bondage** - labour as security for debt repayment  
    • **Forced commercial sexual exploitation** - sexual exploitation under coercion  
    • **Human trafficking** - recruitment and transport for exploitation  
    • **Slavery-like practices** - ownership-like control over people  
    • **Sale and exploitation of children** - treating children as commodities  
    
    In all its forms, modern slavery represents **the removal of a person's freedom** — their freedom to accept 
    or refuse a job, their freedom to leave one employer for another, or their freedom to decide if, when, 
    and whom to marry — in order to exploit them for personal or financial gain.
    """)

with col2:
    st.image("https://images.unsplash.com/photo-1532629345422-7515f3d16bb6?w=400&h=300&fit=crop", caption="Global Modern Slavery Breakdown (2022) - 49.6 Million Total Victims")

# Global Statistics using Streamlit metrics
st.markdown("### Global Statistics & Trends")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="In Forced Labour", value="27.6M", delta="86% in private sector")

with col2:
    st.metric(label="In Forced Marriage", value="22M", delta="85% family pressure")

with col3:
    st.metric(label="Children Affected", value="12M", delta="24% of all victims")

with col4:
    st.metric(label="Increase Since 2016", value="10M", delta="25% growth rate")

# Regional Distribution
st.markdown("### Regional Distribution")

regional_data = pd.DataFrame({
    'Region': ['Asia-Pacific', 'Europe & Central Asia', 'Africa', 'Arab States', 'Americas'],
    'Total_Modern_Slavery': [28.4, 5.5, 8.6, 2.7, 4.6],
    'Prevalence_per_1000': [3.5, 4.4, 2.9, 5.3, 2.8]
})

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(regional_data, x='Region', y='Total_Modern_Slavery', 
                 title='Total Modern Slavery by Region (Millions)',
                 color='Total_Modern_Slavery', 
                 color_continuous_scale=['#fee2e2', '#dc2626'])
    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(regional_data, x='Region', y='Prevalence_per_1000', 
                 title='Modern Slavery Prevalence (per 1000 people)',
                 color='Prevalence_per_1000', 
                 color_continuous_scale=['#fef3c7', '#fbbf24'])
    fig.update_layout(height=400, showlegend=False)
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Economic Sectors Analysis
st.markdown("### Economic Sectors Most Affected by Forced Labour")

sector_data = pd.DataFrame({
    'Sector': ['Agriculture', 'Commercial Sexual Exploitation', 'Manufacturing', 
               'Construction', 'Other Services', 'Domestic Work'],
    'Percentage': [27, 23, 15, 12, 13, 10]
})

fig = px.pie(sector_data, values='Percentage', names='Sector', 
             title='Forced Labour by Economic Sector (% of total)',
             color_discrete_sequence=['#dc2626', '#ef4444', '#f87171', '#fca5a5', '#fecaca', '#fee2e2'])
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# Women and Girls Section
st.markdown("### Women and Girls: A Gendered Crisis")

st.markdown("""
<div class="vulnerability-grid">
    <div class="vulnerability-card">
        <img src="https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=350&fit=crop" alt="Women supporting each other"/>
        <div class="vulnerability-card-text">
            <strong>Modern Slavery is a Gendered Issue</strong><br>
            Although modern slavery affects everyone, females account for 68% of all victims of forced marriage 
            and 43% of all victims of forced labour. Nearly 4 out of every 5 trapped in forced commercial sexual exploitation are girls and women.
        </div>
    </div>
    <div class="vulnerability-card">
        <img src="https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=400&h=350&fit=crop" alt="Child protection"/>
        <div class="vulnerability-card-text">
            <strong>Children Robbed of Their Futures</strong><br>
            12 million children are trapped in modern slavery, forced to work in mines, factories, 
            and fields instead of going to school. Their childhood stolen, their futures uncertain.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Australia Analysis Section
st.markdown('<div class="section-header">AUSTRALIA IN-DEPTH ANALYSIS</div>', unsafe_allow_html=True)

# Australia hero image
st.markdown("""
<div class="image-overlay">
    <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=500&fit=crop" alt="Australian construction site"/>
    <div class="image-overlay-text">
        Australia faces significant modern slavery challenges: 41,000 estimated victims, 
        with only 1 in 5 detected. Construction, agriculture, and service sectors hide exploitation in plain sight.
    </div>
</div>
""", unsafe_allow_html=True)

# Australia's Modern Slavery Landscape
st.markdown("### Australia's Modern Slavery Landscape")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Estimated Victims", value="41,000", delta="Walk Free estimate 2023")

with col2:
    st.metric(label="AFP Reports (2023-24)", value="382", delta="+12% increase")

with col3:
    st.metric(label="Detection Rate", value="1 in 5", delta="80% remain undetected")

with col4:
    st.metric(label="At-Risk Imports", value="$25B AUD", delta="Annual value")

# Modern Slavery Types in Australia
st.markdown("### Modern Slavery Types in Australia")

au_slavery_types = pd.DataFrame({
    'Type': ['Human Trafficking', 'Forced Marriage', 'Sexual Servitude', 'Forced Labour', 'Other Forms'],
    'Reports': [110, 91, 73, 43, 65],
    'Percentage': [28.8, 23.8, 19.1, 11.3, 17.0]
})

col1, col2 = st.columns([1, 1])

with col1:
    fig = px.bar(au_slavery_types, x='Type', y='Reports',
                 title='Distribution of Modern Slavery Reports in Australia',
                 color='Reports', 
                 color_continuous_scale=['#dbeafe', '#1e40af'])
    fig.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Key Insights by Type:**")
    st.markdown("**Human Trafficking (110 cases)**")
    st.markdown("Entry, exit & child trafficking - often cross-border operations")
    st.markdown("**Forced Marriage (91 cases)**") 
    st.markdown("51% involve minors, 70% overseas marriages - zero convictions since 2013")
    st.markdown("**Sexual Servitude (73 cases)**")
    st.markdown("Commercial sexual exploitation with coercion")
    st.markdown("**Forced Labour (43 cases)**")
    st.markdown("Agriculture, construction, domestic work - hidden in plain sight")
    st.markdown("**Other Forms (65 cases)**")
    st.markdown("Debt bondage, servitude, slavery-like practices")

# Forced Marriage Analysis
st.markdown("### Forced Marriage in Australia - Critical Statistics")

st.markdown("""
<div style="background: rgba(220, 38, 38, 0.1); border-left: 6px solid #dc2626; padding: 2rem; margin: 2rem 0; border-radius: 10px;">
    <h4 style="color: #dc2626; margin-bottom: 1rem;">Critical Forced Marriage Statistics:</h4>
    <ul style="color: #e2e8f0; font-size: 1.1rem; line-height: 1.8;">
        <li><strong>91 reports to AFP</strong> in 2023-24</li>
        <li><strong>70% involve overseas marriages</strong>, making intervention difficult</li>
        <li><strong>Zero convictions</strong> since criminalization in 2013</li>
        <li><strong>Family pressure</strong> drives 85%+ of cases</li>
        <li><strong>Women and girls</strong> disproportionately affected</li>
    </ul>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    forced_marriage_data = pd.DataFrame({
        'Age_Group': ['Under 18', '18-25', '26-35', 'Over 35'],
        'Percentage': [51, 30, 15, 4]
    })
    fig = px.pie(forced_marriage_data, values='Percentage', names='Age_Group',
                 title='Forced Marriage by Age Group',
                 color_discrete_sequence=['#dc2626', '#ef4444', '#f87171', '#fca5a5'])
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("**Key Challenges in Forced Marriage Cases:**")
    st.markdown("""
    - **Victims reluctant to report family members** - Complex family dynamics make reporting difficult
    - **Cross-jurisdictional complexity** - Federal vs state law creates prosecution challenges  
    - **Cultural sensitivity required** - Investigation must be respectful of cultural contexts
    - **Limited specialized support services** - Insufficient resources for comprehensive victim support
    - **Community awareness gaps** - Many don't recognize forced marriage as modern slavery
    - **Overseas marriage complications** - 70% occur overseas, limiting intervention options
    """)

# Vulnerability section
st.markdown("### Who is Most Vulnerable?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>68%</h3>
        <p>of forced marriage victims are female</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>79%</h3>
        <p>of sex trafficking victims are female</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>24%</h3>
        <p>of all victims are children</p>
    </div>
    """, unsafe_allow_html=True)

# Emergency contacts
st.markdown("""
<div class="emergency-box">
    <h5>Need Help or Want to Report Suspected Modern Slavery?</h5>
    <p><strong>AFP Human Trafficking Helpline:</strong> 131 AFP (131 237)</p>
    <p><strong>National Sexual Assault Helpline:</strong> 1800 737 732</p>
    <p><strong>Emergency Services:</strong> 000</p>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**Data Sources:** Walk Free Foundation Global Slavery Index, Australian Federal Police, International Labour Organization")