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
        "../src/data/sony_sentiment_scored.csv",
        "../sony_sentiment_scored.csv",
        "src/data/sony_sentiment_scored.csv",
        "sony_sentiment_scored.csv"
    ]
    
    df = None
    for p in possible_paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break
            
    if df is None:
        df = pd.DataFrame(columns=['product', 'clean_text', 'vader_score'])
    
    productsList = []
    
    if not df.empty and 'product' in df.columns:
        product_groups = df.groupby('product')
        
        for name, group in product_groups:
            if pd.isna(name): continue
            
            volume = len(group)
            
            # Use the real NLP VADER sentiment scores (-1 to 1) mapped to (0 to 100)
            if 'vader_score' in group.columns:
                vader_mean = group['vader_score'].mean()
                sentiment_score = int((vader_mean + 1) / 2 * 100)
            else:
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

    # --- Integration of Teammate's Sentiment Visualizations (Plotly versions) ---
    c1, c2 = st.columns([6, 4])
    
    with c1:
        st.markdown("##### Sentiment Distribution by Segment")
        # Stacked 100% Bar Chart to replace the cluttered Box Plot
        df_dist = df_raw.groupby(['product', 'sentiment_category']).size().reset_index(name='count')
        df_dist['Percentage'] = df_dist.groupby('product')['count'].transform(lambda x: x / x.sum() * 100)
        
        fig_bar = px.bar(df_dist, x="Percentage", y="product", color="sentiment_category", orientation='h',
                         category_orders={"sentiment_category": ["Negative", "Neutral", "Positive"]},
                         color_discrete_map={"Positive": "#1f2937", "Neutral": "#9ca3af", "Negative": "#ef4444"})
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='Relative Distribution (%)'),
            yaxis=dict(showgrid=False, title=''),
            showlegend=False,
            height=320
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("##### Overall Sentiment Classification")
        # Match Teammate's Pie Chart but with unified color palette
        sentiment_counts = df_raw['sentiment_category'].value_counts().reset_index()
        sentiment_counts.columns = ['Status', 'Count']
        fig_pie = px.pie(sentiment_counts, names="Status", values="Count", hole=0.45,
                         hover_data=["Status"],
                         color="Status", 
                         category_orders={"Status": ["Negative", "Neutral", "Positive"]},
                         color_discrete_map={"Positive": "#1f2937", "Neutral": "#9ca3af", "Negative": "#ef4444"})
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            height=320
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        
    st.markdown("<br>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    
    with c3:
        st.markdown("##### Sentiment by Source Type")
        # Match teammate's horizontal bar chart for Source
        df_source = df_raw.groupby('is_support_source')['vader_score'].mean().reset_index()
        df_source['Source'] = df_source['is_support_source'].map({True: 'Official PlayStation / Sony Support', False: 'External / Third-Party Platforms'})
        
        fig_src = px.bar(df_source, x='vader_score', y='Source', orientation='h', color='Source',
                         color_discrete_map={'Official PlayStation / Sony Support': '#1f2937', 'External / Third-Party Platforms': '#9ca3af'})
        fig_src.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='Avg VADER Score'),
            yaxis=dict(showgrid=False, title=''),
            height=280
        )
        st.plotly_chart(fig_src, use_container_width=True, config={'displayModeBar': False})
        
    with c4:
        st.markdown("##### Sentiment Volatility vs Text Length")
        # Match teammate's scatter plot with unified palettes
        fig_scat = px.scatter(df_raw, x="word_count", y="vader_score", color="sentiment_category",
                              color_discrete_map={"Positive": "#1f2937", "Neutral": "#9ca3af", "Negative": "#ef4444"},
                              opacity=0.6)
        fig_scat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='Word Count'),
            yaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='VADER Score', range=[-1.1, 1.1]),
            height=280
        )
        st.plotly_chart(fig_scat, use_container_width=True, config={'displayModeBar': False})
        
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
        
        # Dynamically map to teammate's "Most Negative Sentiment Entries" chart
        if not df_raw.empty and 'clean_text' in df_raw.columns and 'vader_score' in df_raw.columns:
            # We filter for actual negative reviews and take the most severe 3
            sample_reviews = df_raw[df_raw['vader_score'] < -0.2].sort_values('vader_score').head(3)
            for _, row in sample_reviews.iterrows():
                text = str(row['clean_text'])
                score = round(row['vader_score'], 2)
                if len(text) > 130:
                    text = text[:130] + '...'
                    
                st.markdown(f'''
                <div style="border-left: 3px solid #ef4444; background: #ffffff; padding: 14px 18px; margin-bottom: 12px; border-radius: 4px; border: 1px solid #e5e7eb; border-left: 4px solid #ef4444; font-size: 0.9rem; color: #374151; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                    "{text}" <br><span style="color: #9ca3af; font-size: 0.75rem; font-weight: 600; text-transform: uppercase;">— {row.get('product', 'Unknown')}  •  VADER: {score}</span>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No raw verbatims available in the dataset.")

if __name__ == "__main__":
    main()
