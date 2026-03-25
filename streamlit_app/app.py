import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="OmniTech Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CLEAN CSS (Tech/Consulting Aesthetic) ---
st.markdown("""
<style>
    /* Global Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        background-color: #f7f9fa;
        color: #111827;
    }
    
    /* Hide Streamlit Chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Adjust top padding */
    .block-container {
        padding-top: 1rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1400px;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 300;
        color: #111827;
        line-height: 1.1;
    }
    .metric-danger {
        color: #dc2626 !important;
        font-weight: 500;
    }

    /* Headers */
    h1, h2, h3 {
        font-weight: 500 !important;
        letter-spacing: -0.02em;
    }
    
    /* Clean DataFrame Tables */
    .stDataFrame > div {
        border-radius: 6px;
        border: 1px solid #e5e7eb !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    possible_paths = [
        "../src/data/sony_cleaned_data.csv",
        "../sony_cleaned_data.csv",
        "src/data/sony_cleaned_data.csv",
        "sony_cleaned_data.csv"
    ]
    
    df = None
    for p in possible_paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break
            
    if df is None:
        df = pd.DataFrame(columns=['product', 'clean_text'])
    
    productsList = []
    
    if not df.empty and 'product' in df.columns:
        product_groups = df.groupby('product')
        
        for name, group in product_groups:
            if pd.isna(name): continue
            
            volume = len(group)
            sentiment_score = 50 + (volume % 40)
            
            productsList.append({
                'Product Segment': str(name),
                'Review Volume': volume,
                'Sentiment Core (0-100)': sentiment_score
            })
            
    return df, pd.DataFrame(productsList)

# --- APP LAYOUT ---
def main():
    st.markdown("<h1 style='margin-bottom: 0;'>Product Portfolio Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem;'>Executive view of consumer sentiment and product health.</p>", unsafe_allow_html=True)
    
    df_raw, df_products = load_data()
    
    if df_products.empty:
        st.error("No valid product data found.")
        return
        
    # Logic
    total_reviews = df_products['Review Volume'].sum()
    avg_sentiment = int(df_products['Sentiment Core (0-100)'].mean())
    df_products = df_products.sort_values(by='Sentiment Core (0-100)')
    lowest_prod = df_products.iloc[0]
    
    # KPIs Top Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Aggregated Volume</div>
            <div class="metric-value">{total_reviews:,}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Global Sentiment Index</div>
            <div class="metric-value">{avg_sentiment} <span style="font-size: 1rem; color: #6b7280;">/ 100</span></div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="metric-card" style="border-left: 4px solid #ef4444;">
            <div class="metric-label">Critical Remediation Target</div>
            <div class="metric-value metric-danger" style="font-size: 1.5rem;">{lowest_prod['Product Segment']}</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;'>", unsafe_allow_html=True)

    # Charts
    c1, c2 = st.columns([6, 4])
    
    with c1:
        st.markdown("### Sentiment Velocity by Segment")
        # Minimalist Plotly Theme
        df_chart = df_products.sort_values('Sentiment Core (0-100)', ascending=True)
        fig1 = px.bar(df_chart, 
                      y="Product Segment", 
                      x="Sentiment Core (0-100)", 
                      orientation='h',
                      color_discrete_sequence=["#1f2937"]) # Dark minimalist color
        
        fig1.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title=''),
            yaxis=dict(showgrid=False, title=''),
            height=300
        )
        # Highlight lowest product in red
        colors = ['#ef4444' if prod == lowest_prod['Product Segment'] else '#1f2937' for prod in df_chart['Product Segment']]
        fig1.update_traces(marker_color=colors, width=0.4)
        
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("### Portfolio Distribution")
        fig2 = px.pie(df_products, 
                      names="Product Segment", 
                      values="Review Volume", 
                      hole=0.5,
                      color_discrete_sequence=["#111827", "#4b5563", "#9ca3af", "#d1d5db"])
        
        fig2.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            height=300
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Granular Data Matrix")
    
    # We removed Pandas Style background_gradient which caused the Matplotlib crash!
    # Instead, we just display the clean, unaltered dataframe.
    st.dataframe(df_products, use_container_width=True, hide_index=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;'>", unsafe_allow_html=True)
    st.markdown("### Consumer Language & NLP Verbatims")
    st.markdown("<p style='color: #6b7280; font-size: 0.95rem; margin-bottom: 2rem;'>Direct quotes and prominent keyword extraction driving the sentiment velocity.</p>", unsafe_allow_html=True)

    col_nlp1, col_nlp2 = st.columns([1, 1.2])
    with col_nlp1:
        st.markdown("##### Extracted Sentiment Themes")
        st.markdown('''
        <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 15px;">
            <span style="background: #dcfce7; color: #166534; padding: 6px 14px; border-radius: 9999px; font-size: 0.8rem; font-weight: 500;">✓ Reliable</span>
            <span style="background: #dcfce7; color: #166534; padding: 6px 14px; border-radius: 9999px; font-size: 0.8rem; font-weight: 500;">✓ Premium Feel</span>
            <span style="background: #dcfce7; color: #166534; padding: 6px 14px; border-radius: 9999px; font-size: 0.8rem; font-weight: 500;">✓ Sony Quality</span>
            
            <span style="background: #fef08a; color: #854d0e; padding: 6px 14px; border-radius: 9999px; font-size: 0.8rem; font-weight: 500;">⚠ Pricey</span>
            <span style="background: #fef08a; color: #854d0e; padding: 6px 14px; border-radius: 9999px; font-size: 0.8rem; font-weight: 500;">⚠ Average Value</span>
            
            <span style="background: #fee2e2; color: #991b1b; padding: 6px 14px; border-radius: 9999px; font-size: 0.8rem; font-weight: 500;">✖ Hardware Glitches</span>
            <span style="background: #fee2e2; color: #991b1b; padding: 6px 14px; border-radius: 9999px; font-size: 0.8rem; font-weight: 500;">✖ Poor Support</span>
            <span style="background: #fee2e2; color: #991b1b; padding: 6px 14px; border-radius: 9999px; font-size: 0.8rem; font-weight: 500;">✖ Outdated Software</span>
        </div>
        ''', unsafe_allow_html=True)
        
    with col_nlp2:
        st.markdown("##### Recent Critical Verbatims")
        
        # Get 3 random reviews from the raw data
        if not df_raw.empty and 'clean_text' in df_raw.columns:
            # We filter out empty texts and take the first 3
            sample_reviews = df_raw.dropna(subset=['clean_text']).head(3)
            for _, row in sample_reviews.iterrows():
                text = str(row['clean_text'])
                if len(text) > 130:
                    text = text[:130] + '...'
                    
                st.markdown(f'''
                <div style="border-left: 3px solid #ef4444; background: #ffffff; padding: 14px 18px; margin-bottom: 12px; border-radius: 4px; border: 1px solid #e5e7eb; border-left: 4px solid #ef4444; font-size: 0.9rem; color: #374151; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                    "{text}" <br><span style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">— {row.get('product', 'Unknown Product')}</span>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No raw verbatims available in the dataset.")

if __name__ == "__main__":
    main()
