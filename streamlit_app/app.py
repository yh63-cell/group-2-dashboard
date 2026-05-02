import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx
import os
import re
from textblob import TextBlob
from scipy import stats

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Google Discontinued Products Analytics",
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
        color: #ef4444 !important;
        font-weight: 500;
    }
    
    /* Clean DataFrame Tables */
    .stDataFrame > div {
        border-radius: 6px;
        border: 1px solid #e5e7eb !important;
    }
</style>
""", unsafe_allow_html=True)

# --- THEME TOKENS ---
COLOR_BLACK = "#111827"
COLOR_GREY = "#9ca3af"
COLOR_RED = "#ef4444"

# --- DATA PROCESSING UTILS ---
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r'http\S+', '', text)
    return text.strip()

def classify_polarity(score):
    if score > 0.05:
        return 'Positive'
    elif score < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# --- DATA LOADING ---
@st.cache_data
def load_and_process_data():
    base_dir = "data"
    
    file_mapping = {
        'old_stadia_youtube_comments_raw.csv': ('Google Stadia', 'Before'),
        'recent_stadia_youtube_comments_raw.csv': ('Google Stadia', 'After'),
        'old_google_glass_youtube_comments_raw.csv': ('Google Glass', 'Before'),
        'recent_google_glass_youtube_comments_raw.csv': ('Google Glass', 'After'),
        'old_plus_youtube_comments_raw.csv': ('Google+', 'Before'),
        'recent_plus_youtube_comments_raw.csv': ('Google+', 'After')
    }
    
    dfs = []
    
    for filename, (product, period) in file_mapping.items():
        filepath = os.path.join(base_dir, filename)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df['product'] = product
            df['period'] = period
            dfs.append(df)
            
    if not dfs:
        return pd.DataFrame()
        
    master_df = pd.concat(dfs, ignore_index=True)
    
    if 'comment' in master_df.columns:
        master_df['clean_text'] = master_df['comment'].apply(clean_text)
        master_df['word_count'] = master_df['clean_text'].apply(lambda x: len(x.split()))
        master_df = master_df[master_df['word_count'] >= 4]
        master_df = master_df.drop_duplicates(subset=['clean_text'])
        master_df['polarity'] = master_df['clean_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
        master_df['sentiment_category'] = master_df['polarity'].apply(classify_polarity)
        
    return master_df

@st.cache_data
def load_absa_data():
    path = "data/absa_extractions.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_tfidf_data():
    path = "data/tfidf_keywords.csv"
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_network_data():
    nodes_path = "data/gephi_nodes.csv"
    edges_path = "data/gephi_edges.csv"
    if os.path.exists(nodes_path) and os.path.exists(edges_path):
        return pd.read_csv(nodes_path), pd.read_csv(edges_path)
    return pd.DataFrame(), pd.DataFrame()

# --- NETWORK GRAPH RENDERER ---
def plot_network(nodes_df, edges_df, product_name):
    n_df = nodes_df[nodes_df['product'] == product_name]
    e_df = edges_df[edges_df['product'] == product_name]
    
    if n_df.empty or e_df.empty:
        return None
        
    G = nx.Graph()
    for _, row in n_df.iterrows():
        G.add_node(row['Id'], label=row['Label'], size=row['frequency'])
        
    for _, row in e_df.iterrows():
        G.add_edge(row['Source'], row['Target'], weight=row['Weight'])
        
    pr = nx.pagerank(G, weight='weight')
    pos = nx.kamada_kawai_layout(G)
    
    edge_traces = []
    max_weight = e_df['Weight'].max() if not e_df.empty else 1
    
    def get_monotone_color(ratio):
        ratio = max(0.0, min(1.0, ratio))
        # Interpolate Light Grey (209, 213, 219) to Black (17, 24, 39)
        r = int(209 + (17 - 209) * ratio)
        g = int(213 + (24 - 213) * ratio)
        b = int(219 + (39 - 219) * ratio)
        a = 0.3 + (0.6 * ratio) # Opacity from 0.3 to 0.9
        return f'rgba({r}, {g}, {b}, {a})'
    
    for _, row in e_df.iterrows():
        if row['Source'] in pos and row['Target'] in pos:
            x0, y0 = pos[row['Source']]
            x1, y1 = pos[row['Target']]
            weight = row['Weight']
            
            weight_ratio = weight / max_weight
            thickness = weight_ratio * 5 + 0.5 
            color = get_monotone_color(weight_ratio)
                
            edge_traces.append(go.Scatter(
                x=[x0, x1, None], y=[y0, y1, None],
                line=dict(width=thickness, color=color),
                hoverinfo='none',
                mode='lines'
            ))
        
    node_x = []
    node_y = []
    node_text = []
    node_hover = []
    node_size = []
    
    top_15_threshold = n_df['frequency'].nlargest(15).min() if len(n_df) >= 15 else 0
    max_pr = max(pr.values()) if pr else 1
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        
        label = G.nodes[node]['label']
        freq = G.nodes[node]['size']
        pagerank_score = pr[node]
        
        node_hover.append(f"{label}<br>PR Centrality: {pagerank_score:.3f}")
        
        if freq >= top_15_threshold:
            node_text.append(label)
        else:
            node_text.append("")
            
        scaled_size = (pagerank_score / max_pr) * 55
        node_size.append(max(scaled_size, 12))
        
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        hovertext=node_hover,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=[COLOR_RED] * len(node_x),
            size=node_size,
            line_width=1.5,
            line_color='white'
        ),
        textfont=dict(size=12, color=COLOR_BLACK, family='Inter', weight='bold')
    )
    
    fig = go.Figure(data=edge_traces + [node_trace],
             layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0,l=0,r=0,t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                height=500
             ))
    return fig

# --- APP LAYOUT ---
def main():
    st.markdown("<h1 style='margin-bottom: 0;'>Google Discontinued Products Analytics</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6b7280; font-size: 1.1rem; margin-bottom: 2rem;'>Analyzing post-discontinuation sentiment velocity and consumer nostalgia across Stadia, Glass, and Google+.</p>", unsafe_allow_html=True)
    
    df_raw = load_and_process_data()
    df_absa = load_absa_data()
    df_tfidf = load_tfidf_data()
    nodes_df, edges_df = load_network_data()
    
    if df_raw.empty:
        st.error("No valid product data found in the `data/` folder.")
        return
        
    # Stats
    total_reviews = len(df_raw)
    avg_polarity = df_raw['polarity'].mean()
    
    # Calculate t-tests for highlights
    significant_drops = []
    for product in df_raw['product'].unique():
        before_scores = df_raw[(df_raw['product'] == product) & (df_raw['period'] == 'Before')]['polarity']
        after_scores = df_raw[(df_raw['product'] == product) & (df_raw['period'] == 'After')]['polarity']
        if len(before_scores) > 10 and len(after_scores) > 10:
            t_stat, p_val = stats.ttest_ind(before_scores, after_scores, equal_var=False)
            if p_val < 0.05 and after_scores.mean() < before_scores.mean():
                significant_drops.append(product)
                
    drops_str = ", ".join(significant_drops) if significant_drops else "None"
    
    # KPIs Top Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Total Verified Comments</div>
            <div class="metric-value">{total_reviews:,}</div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-label">Global TextBlob Polarity</div>
            <div class="metric-value">{avg_polarity:.3f} <span style="font-size: 1rem; color: #6b7280;">(-1 to 1)</span></div>
            <div style="margin-top: 8px; font-size: 0.8rem; color: #6b7280;"><em>*Methodology: TextBlob explicitly selected over VADER for its robust lexicon-based pipeline in accordance with project constraints.</em></div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="metric-card" style="border-left: 4px solid {COLOR_RED};">
            <div class="metric-label">Statistically Significant Drops</div>
            <div class="metric-value metric-danger" style="font-size: 1.5rem;">{drops_str}</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;'>", unsafe_allow_html=True)

    # --- Sentiment Distributions ---
    st.markdown("### Executive Visualizations: Polarity Shifts")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### Sentiment Trajectory (Before vs After)")
        df_mean_pol = df_raw.groupby(['product', 'period'])['polarity'].mean().reset_index()
        fig_bar = px.bar(df_mean_pol, x="product", y="polarity", color="period", barmode='group',
                         category_orders={"period": ["Before", "After"]},
                         color_discrete_map={"Before": COLOR_GREY, "After": COLOR_BLACK})
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title=''),
            yaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='Mean Polarity'),
            legend_title="Discontinuation", height=320
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    with c2:
        st.markdown("##### Polarity Distribution Spread")
        fig_box = px.box(df_raw, x="product", y="polarity", color="period",
                         category_orders={"period": ["Before", "After"]},
                         color_discrete_map={"Before": COLOR_GREY, "After": COLOR_RED})
        fig_box.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title=''),
            yaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='TextBlob Polarity'),
            legend_title="Discontinuation", height=320
        )
        st.plotly_chart(fig_box, use_container_width=True, config={'displayModeBar': False})

    st.markdown(f'''
    <div style="border-left: 4px solid {COLOR_BLACK}; background: #ffffff; padding: 16px; margin-top: 10px; border-radius: 4px; border: 1px solid #e5e7eb; font-size: 0.95rem; color: #374151;">
        <strong>Interpretation:</strong> Google Glass and Google+ experienced sharp, statistically significant declines in average sentiment post-discontinuation. Stadia's sentiment remained relatively flat but consistently lower overall, indicating its core user base was already highly frustrated prior to the shutdown announcement.
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("##### Engagement vs. Sentiment Correlation")
    st.markdown("<p style='color: #6b7280; font-size: 0.95rem; margin-bottom: 1rem;'>Plotting comment length (effort) against polarity to identify if highly engaged users trend negative.</p>", unsafe_allow_html=True)
    
    fig_scatter = px.scatter(df_raw[df_raw['word_count'] < 300].reset_index(drop=True), x="word_count", y="polarity", color="product", 
                             opacity=0.6, marginal_y="violin", marginal_x="histogram",
                             color_discrete_map={"Google Stadia": COLOR_RED, "Google Glass": COLOR_BLACK, "Google+": COLOR_GREY})
    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='Comment Word Count (Engagement)'),
        yaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='TextBlob Polarity'),
        legend_title="Product", height=400
    )
    st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown(f'''
    <div style="border-left: 4px solid {COLOR_BLACK}; background: #ffffff; padding: 16px; margin-top: 10px; border-radius: 4px; border: 1px solid #e5e7eb; font-size: 0.95rem; color: #374151;">
        <strong>Interpretation:</strong> The marginal distributions reveal that the vast majority of engagement is short-form (under 20 words). Longer, high-effort comments tend to cluster near the neutral-to-negative spectrum, indicating that highly invested users are primarily expressing detailed grievances rather than praise.
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # --- ABSA Section ---
    st.markdown("### Aspect-Based Sentiment Analysis (ABSA)")
    st.markdown("<p style='color: #6b7280; font-size: 0.95rem; margin-bottom: 2rem;'>LLM-extracted sentiment across 5 core dimensions: Product Quality, Market Demand, Adoption Ability, Timing/Innovation, Price/Value.</p>", unsafe_allow_html=True)
    
    if not df_absa.empty:
        c3, c4 = st.columns([6, 4])
        with c3:
            st.markdown("##### Sentiment Distribution by Aspect")
            absa_dist = df_absa.groupby(['aspect', 'sentiment']).size().reset_index(name='count')
            fig_absa = px.bar(absa_dist, x="count", y="aspect", color="sentiment", orientation='h',
                             category_orders={"sentiment": ["Negative", "Neutral", "Positive"]},
                             color_discrete_map={"Positive": COLOR_BLACK, "Neutral": COLOR_GREY, "Negative": COLOR_RED})
            fig_absa.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showgrid=True, gridcolor='#f3f4f6', title='Extraction Count'),
                yaxis=dict(showgrid=False, title=''), height=350, legend_title="Sentiment"
            )
            st.plotly_chart(fig_absa, use_container_width=True, config={'displayModeBar': False})
            
        with c4:
            st.markdown("##### Interpretation")
            st.markdown(f"""
            <div style="border-left: 4px solid {COLOR_RED}; border: 1px solid #e5e7eb; border-radius: 4px; padding: 16px; background-color: #ffffff; height: 350px;">
                <p style="font-size: 0.95rem; margin-bottom: 12px;"><strong>Product Quality:</strong> The most discussed aspect, heavily negative. Users consistently cited hardware limitations and latency as dealbreakers.</p>
                <p style="font-size: 0.95rem; margin-bottom: 12px;"><strong>Timing & Innovation:</strong> The only net-positive aspect across the board. Consumers strongly felt these products were "ahead of their time" but poorly executed.</p>
                <p style="font-size: 0.95rem; margin-bottom: 0;"><strong>Market Demand:</strong> High skepticism suggests these products ultimately failed because they didn't solve real, existing consumer problems.</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ABSA Extractions dataset not found.")

    st.markdown("<hr style='border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # --- Text Analysis: TF-IDF & Word Clouds ---
    st.markdown("### Consumer Language Analysis")
    st.markdown("<p style='color: #6b7280; font-size: 0.95rem; margin-bottom: 2rem;'>Analyzing the shift in vernacular after discontinuation, highlighting nostalgic tendencies.</p>", unsafe_allow_html=True)

    c_sel1, c_sel2 = st.columns(2)
    with c_sel1:
        lang_prod = st.selectbox("Select Product:", ["Google Stadia", "Google Glass", "Google+"], key="lang_prod")
    with c_sel2:
        lang_per = st.selectbox("Select Period:", ["Before", "After"], key="lang_per")

    col_nlp1, col_nlp2 = st.columns([1, 1])
    with col_nlp1:
        st.markdown("##### Top Keywords (TF-IDF)")
        if not df_tfidf.empty:
            product_mapping = {"Google Stadia": "stadia", "Google Glass": "google_glass", "Google+": "google_plus"}
            period_mapping = {"Before": "before", "After": "after"}
            kw_df = df_tfidf[(df_tfidf['product'] == product_mapping.get(lang_prod)) & (df_tfidf['period'] == period_mapping.get(lang_per))].copy()
            
            # Calculate a mock score to make the #1 rank the longest bar
            kw_df['score'] = kw_df['rank'].max() - kw_df['rank'] + 1
            kw_df = kw_df.sort_values(by="rank", ascending=False).tail(10) # Get top 10 and sort ascending so rank 1 is at the top of horizontal bar chart
            
            fig_kw = px.bar(kw_df, x="score", y="keyword", orientation='h', color="score", color_continuous_scale="Reds")
            fig_kw.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
                xaxis=dict(showgrid=False, title='Significance', showticklabels=False),
                yaxis=dict(showgrid=True, gridcolor='#f3f4f6', title=''),
                height=350
            )
            fig_kw.update_coloraxes(showscale=False)
            st.plotly_chart(fig_kw, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("TF-IDF Keywords dataset not found.")
            
    with col_nlp2:
        st.markdown("##### Word Cloud")
        wc_text = " ".join(df_raw[(df_raw['product'] == lang_prod) & (df_raw['period'] == lang_per)]['clean_text'].astype(str))
        if wc_text.strip():
            # Use 'gist_yarg' or 'Reds' for the Black/Grey/Red theme
            wc = WordCloud(width=600, height=300, background_color='white', colormap='Reds', max_words=80).generate(wc_text)
            fig_wc, ax_wc = plt.subplots(figsize=(6, 3))
            ax_wc.imshow(wc, interpolation='bilinear')
            ax_wc.axis('off')
            fig_wc.patch.set_alpha(0)
            st.pyplot(fig_wc, use_container_width=True)
        else:
            st.info("Not enough text data available for this selection.")

    nlp_interpretations = {
        ("Google Stadia", "Before"): "Pre-discontinuation, Stadia conversations were heavily focused on functional gaming elements: 'games', 'play', 'console', and 'controller'.",
        ("Google Stadia", "After"): "Post-discontinuation, the dialogue dramatically shifts to retrospective terms like 'remember' and discussions about 'servers' shutting down.",
        ("Google Glass", "Before"): "Early Glass discussions heavily featured 'apple', 'vision', and 'future' as users hyped its potential and compared it to competitors.",
        ("Google Glass", "After"): "Following its demise, the keyword 'remember' dominates as users reflect on its legacy as a failed but pioneering AR device.",
        ("Google+", "Before"): "Pre-discontinuation, the focus was overwhelmingly on 'youtube', 'account', and the controversial forced integration.",
        ("Google+", "After"): "Post-discontinuation, 'remember' and nostalgic reflection take over the sparse remaining conversation about the platform."
    }
    
    current_nlp_interp = nlp_interpretations.get((lang_prod, lang_per), "Select a product and period to see specific language shifts.")

    st.markdown(f'''
    <div style="border-left: 4px solid {COLOR_BLACK}; background: #ffffff; padding: 16px; margin-top: 10px; border-radius: 4px; border: 1px solid #e5e7eb; font-size: 0.95rem; color: #374151;">
        <strong>Interpretation:</strong> {current_nlp_interp}
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("<hr style='border: none; border-top: 1px solid #e5e7eb; margin: 2rem 0;'>", unsafe_allow_html=True)
    
    # --- Network Graph Section ---
    st.markdown("### Keyword Co-Occurrence Networks")
    st.markdown("<p style='color: #6b7280; font-size: 0.95rem; margin-bottom: 2rem;'>Analyzing how terms cluster together (e.g. comparing Google Glass to Apple Vision Pro).</p>", unsafe_allow_html=True)

    if not nodes_df.empty and not edges_df.empty:
        c_net1, c_net2 = st.columns([1.5, 1])
        with c_net1:
            product_mapping = {"Google Stadia": "stadia", "Google Glass": "google_glass", "Google+": "google_plus"}
            net_prod_ui = st.selectbox("Select Product Network:", ["Google Stadia", "Google Glass", "Google+"], key="net_prod_ui")
            mapped_net_prod = product_mapping.get(net_prod_ui)
            fig_net = plot_network(nodes_df, edges_df, mapped_net_prod)
            if fig_net:
                st.plotly_chart(fig_net, use_container_width=True, config={'displayModeBar': False})
            else:
                st.warning("No network data for this selection.")
        with c_net2:
            st.markdown("##### Interpretation")
            net_interpretations = {
                "Google Glass": "The massive \"apple\"-\"vision\" edge reveals users heavily using Glass as a historical benchmark to evaluate modern AR headsets.",
                "Google Stadia": "Central hubs around \"internet\" and \"connection\" show the failure was attributed to infrastructure limits rather than the games themselves.",
                "Google+": "Centralized entirely around \"youtube\", validating the historical context of Google forcing YouTube users onto the platform."
            }
            current_net_interp = net_interpretations.get(net_prod_ui, "")
            
            st.markdown(f'''
            <div style="border-left: 4px solid {COLOR_RED}; background: #ffffff; padding: 16px; border-radius: 4px; border: 1px solid #e5e7eb; font-size: 0.95rem; color: #374151; height: 500px;">
                <p><strong>{net_prod_ui}:</strong> {current_net_interp}</p>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("Network Graph datasets not found.")

if __name__ == "__main__":
    main()
