import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
import pytz

st.set_page_config(
    page_title="Google Play Store Dashboard",
    layout="wide"
)

st.title("Google Play Store Analytics Dashboard")

ist = pytz.timezone("Asia/Kolkata")
now_ist = datetime.now(ist)
current_hour = now_ist.hour
st.caption(f"🕐 Current IST Time: {now_ist.strftime('%I:%M %p')}")


st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg", width=180)
st.sidebar.title("Dashboard Settings")

demo_mode = st.sidebar.checkbox(
    " Demo Mode (Override Time Restrictions)",
    value=False,
    help="Enable this to view all charts regardless of IST time window. For reviewer/demo purposes only."
)

if demo_mode:
    st.sidebar.success(" Demo Mode is ON — All charts are visible.")
else:
    st.sidebar.info(" Demo Mode is OFF — Charts appear only during their scheduled IST time windows.")

st.sidebar.markdown("---")
st.sidebar.markdown(" Chart Time Windows")
st.sidebar.markdown("""
| Task | Window (IST) |
|------|-------------|
| Task 1 | 3 PM – 5 PM |
| Task 2 | 6 PM – 8 PM |
| Task 3 | 1 PM – 2 PM |
| Task 4 | 6 PM – 9 PM |
| Task 5 | 5 PM – 7 PM |
| Task 6 | 4 PM – 6 PM |
""")

def in_window(start_hour, end_hour):
    """Returns True if current IST hour is in [start_hour, end_hour), OR demo mode is ON."""
    if demo_mode:
        return True
    return start_hour <= current_hour < end_hour

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_dataset.csv")
    df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
    df['Category'] = df['Category'].str.strip()
    df['App Name'] = df['App Name'].astype(str)
    df['Month'] = df['Last Updated'].dt.month   # needed for Task 1
    return df

df = load_data()

# ─────────────────────────────────────────────────────────────────────────────
# TASK 1: Grouped Bar Chart — Avg Rating & Total Review Count (3 PM – 5 PM IST)
# ─────────────────────────────────────────────────────────────────────────────
st.header("Task 1: Category Performance — Avg Rating & Review Count")
st.caption("⏰ Available: 3:00 PM – 5:00 PM IST")

if in_window(15, 17):
    df1 = df[
        (df['Rating'] >= 4.0) &
        (df['Size'] >= 10) &
        (df['Month'] == 1)
    ].copy()

    if not df1.empty:
        top10_cats = df1.groupby('Category')['Installs'].sum().nlargest(10).index
        df1 = df1[df1['Category'].isin(top10_cats)]

        agg1 = df1.groupby('Category').agg(
            Avg_Rating=('Rating', 'mean'),
            Total_Review_Count=('Rating Count', 'sum')
        ).reset_index()

        fig1 = px.bar(
            agg1,
            x='Category',
            y=['Avg_Rating', 'Total_Review_Count'],
            barmode='group',
            title='Top 10 App Categories: Avg Rating vs Total Review Count (January, Size >= 10 MB, Rating >= 4.0)',
            labels={'value': 'Value', 'variable': 'Metric'},
            color_discrete_map={
                'Avg_Rating': '#00C9FF',
                'Total_Review_Count': '#FF6B6B'
            }
        )
        fig1.update_layout(
            xaxis_tickangle=-30,
            legend_title='Metric',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.warning("No data available for Task 1 after applying filters.")
else:
    st.warning("Task 1 chart is only available between 3:00 PM - 5:00 PM IST. Enable Demo Mode in the sidebar to preview.")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TASK 2: Choropleth Map — Global Installs by Category (6 PM – 8 PM IST)
# ─────────────────────────────────────────────────────────────────────────────
st.header("Task 2: Global Installs by Category — Choropleth Map")
st.caption(" Available: 6:00 PM – 8:00 PM IST")

if in_window(18, 20):
    df2 = df[
        ~df['Category'].str.startswith(('A', 'C', 'G', 'S'), na=False)
    ].copy()

    top5_cats = df2.groupby('Category')['Installs'].sum().nlargest(5).index
    df2 = df2[df2['Category'].isin(top5_cats)]
    df2 = df2[df2['Installs'] > 1_000_000]

    if 'Country' in df2.columns:
        df2 = df2.dropna(subset=['Country'])
        if not df2.empty:
            df2_country = df2.groupby('Country')['Installs'].sum().reset_index()
            fig2 = px.choropleth(
                df2_country,
                locations="Country",
                locationmode="country names",
                color="Installs",
                hover_name="Country",
                color_continuous_scale="Viridis",
                title="Global App Installs by Country (Top 5 Categories, Installs > 1M, Excl. A/C/G/S)"
            )
            fig2.update_layout(
                geo=dict(showframe=False, showcoastlines=True),
                coloraxis_colorbar=dict(title="Total Installs")
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.subheader("Top 5 Categories Breakdown")
            cat_summary = df2.groupby('Category')['Installs'].sum().reset_index().sort_values('Installs', ascending=False)
            st.dataframe(cat_summary, use_container_width=True)
        else:
            st.warning("No data available for Task 2 after applying filters.")
    else:
        st.info("The dataset does not have a 'Country' column. Showing category-level install distribution instead.")
        if not df2.empty:
            cat_installs = df2.groupby('Category')['Installs'].sum().reset_index()
            fig2 = px.bar(
                cat_installs,
                x='Category',
                y='Installs',
                color='Category',
                title='Top 5 Category Installs (> 1M) — Categories not starting with A, C, G, S',
                text_auto=True
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No data available for Task 2 after applying filters.")
else:
    st.warning("Task 2 chart is only available between 6:00 PM - 8:00 PM IST. Enable Demo Mode in the sidebar to preview.")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TASK 3: Dual-Axis Chart — Free vs Paid Apps in Top 3 Categories (1 PM – 2 PM IST)
# ─────────────────────────────────────────────────────────────────────────────
st.header("Task 3: Free vs Paid Apps — Avg Installs & Revenue in Top 3 Categories")
st.caption(" Available: 1:00 PM – 2:00 PM IST")

if in_window(13, 14):
    df3 = df[
        (df['Installs'] >= 10000) &
        (df['Revenue'] >= 10000) &
        (df['Minimum Android'] > 4.0) &
        (df['Size'] > 15) &
        (df['Content Rating'] == 'Everyone') &
        (df['App Name'].str.len() <= 30)
    ].copy()

    if not df3.empty:
        if 'Free' in df3.columns:
            df3['Type'] = df3['Free'].apply(lambda x: 'Free' if x else 'Paid')
        elif 'Type' not in df3.columns:
            df3['Type'] = df3['Price'].apply(
                lambda x: 'Free' if float(str(x).replace('$', '').replace(',', '') or 0) == 0 else 'Paid'
            )

        top3_cats = df3.groupby('Category')['Installs'].sum().nlargest(3).index
        df3 = df3[df3['Category'].isin(top3_cats)]

        agg3 = df3.groupby(['Category', 'Type']).agg(
            Avg_Installs=('Installs', 'mean'),
            Avg_Revenue=('Revenue', 'mean')
        ).reset_index()

        fig3 = go.Figure()
        colors = {'Free': '#00C9FF', 'Paid': '#FF6B6B'}

        for app_type in ['Free', 'Paid']:
            subset = agg3[agg3['Type'] == app_type]
            color = colors[app_type]
            fig3.add_trace(go.Bar(
                x=subset['Category'],
                y=subset['Avg_Installs'],
                name=f'{app_type} - Avg Installs',
                marker_color=color,
                yaxis='y1',
                offsetgroup=app_type
            ))
            fig3.add_trace(go.Scatter(
                x=subset['Category'],
                y=subset['Avg_Revenue'],
                name=f'{app_type} - Avg Revenue',
                mode='lines+markers',
                line=dict(color=color, dash='dash', width=2),
                marker=dict(size=8),
                yaxis='y2'
            ))

        fig3.update_layout(
            title='Free vs Paid: Avg Installs (Bars) & Avg Revenue (Lines) — Top 3 Categories',
            xaxis=dict(title='Category'),
            yaxis=dict(title='Avg Installs', side='left'),
            yaxis2=dict(title='Avg Revenue ($)', side='right', overlaying='y'),
            barmode='group',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("No data available for Task 3 after applying filters.")
else:
    st.warning("Task 3 chart is only available between 1:00 PM - 2:00 PM IST. Enable Demo Mode in the sidebar to preview.")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TASK 4: Time Series Line Chart with >20% MoM Growth Shading (6 PM – 9 PM IST)
# ─────────────────────────────────────────────────────────────────────────────
st.header("Task 4: Install Trends Over Time by Category (>20% MoM Growth Highlighted)")
st.caption(" Available: 6:00 PM – 9:00 PM IST")

if in_window(18, 21):
    df4 = df[
        (df['Category'].str.startswith(('E', 'C', 'B'), na=False)) &
        (df['Rating Count'] > 500) &
        (~df['App Name'].str.lower().str.startswith(('x', 'y', 'z'), na=False)) &
        (~df['App Name'].str.contains('s', case=False, na=False))
    ].copy()

    if not df4.empty:
        df4['Category'] = df4['Category'].replace({
            'Beauty':   'सौंदर्य (Beauty)',
            'Business': 'வணிகம் (Business)',
            'Dating':   'Partnersuche (Dating)'
        })

        df4['YearMonth'] = df4['Last Updated'].dt.to_period('M').astype(str)
        df4_trend = df4.groupby(['YearMonth', 'Category'])['Installs'].sum().reset_index()
        df4_trend['Date'] = pd.to_datetime(df4_trend['YearMonth'])
        df4_trend = df4_trend.sort_values('Date')

        df4_trend['Prev_Installs'] = df4_trend.groupby('Category')['Installs'].shift(1)
        df4_trend['MoM_Growth'] = (
            (df4_trend['Installs'] - df4_trend['Prev_Installs']) / df4_trend['Prev_Installs']
        )
        df4_trend['High_Growth'] = df4_trend['MoM_Growth'] > 0.20

        fig4 = go.Figure()
        palette4 = px.colors.qualitative.Set2

        for i, cat in enumerate(df4_trend['Category'].unique()):
            cat_data = df4_trend[df4_trend['Category'] == cat].sort_values('Date')
            color = palette4[i % len(palette4)]

            fig4.add_trace(go.Scatter(
                x=cat_data['Date'],
                y=cat_data['Installs'],
                mode='lines+markers',
                name=cat,
                line=dict(color=color, width=2)
            ))

            for _, row in cat_data[cat_data['High_Growth']].iterrows():
                fig4.add_vrect(
                    x0=row['Date'],
                    x1=row['Date'] + pd.DateOffset(months=1),
                    fillcolor=color,
                    opacity=0.15,
                    layer='below',
                    line_width=0
                )
                fig4.add_annotation(
                    x=row['Date'],
                    y=row['Installs'],
                    text=f"+{row['MoM_Growth']:.0%}",
                    showarrow=True,
                    arrowhead=2,
                    font=dict(size=9, color=color),
                    bgcolor='white',
                    bordercolor=color,
                    borderwidth=1,
                    opacity=0.9
                )

        fig4.update_layout(
            title='Install Trends by Category — Shaded Regions = >20% Month-over-Month Growth',
            xaxis_title='Date',
            yaxis_title='Total Installs',
            legend_title='Category',
            plot_bgcolor='rgba(245,245,250,1)',
            hovermode='x unified'
        )
        st.plotly_chart(fig4, use_container_width=True)
        st.caption("Shaded vertical bands mark months with >20% MoM install growth per category.")
    else:
        st.warning("No data available for Task 4 after applying filters.")
else:
    st.warning("Task 4 chart is only available between 6:00 PM - 9:00 PM IST. Enable Demo Mode in the sidebar to preview.")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TASK 5: Bubble Chart — App Size vs Avg Rating (5 PM – 7 PM IST)
# ─────────────────────────────────────────────────────────────────────────────
st.header("Task 5: App Size vs Rating Bubble Chart (Bubble Size = Installs)")
st.caption(" Available: 5:00 PM – 7:00 PM IST")

if in_window(17, 19):
    allowed_cats5 = [
        'Game', 'Beauty', 'Business', 'Comics', 'Communication',
        'Dating', 'Entertainment', 'Social', 'Events'
    ]

    df5 = df[
        (df['Rating'] > 3.5) &
        (df['Installs'] > 50000) &
        (df['Rating Count'] > 500) &
        (df['Sentiment_Subjectivity'] > 0.5) &
        (~df['App Name'].str.contains('s', case=False, na=False)) &
        (df['Category'].isin(allowed_cats5))
    ].copy()

    if not df5.empty:
        df5['Category_Display'] = df5['Category'].replace({
            'Beauty':   'सौंदर्य (Beauty)',
            'Business': 'வணிகம் (Business)',
            'Dating':   'Partnersuche (Dating)'
        })

        unique_cats = df5['Category_Display'].unique().tolist()
        auto_colors = px.colors.qualitative.Plotly
        color_map5 = {}
        auto_idx = 0
        for cat in unique_cats:
            if 'Game' in cat or cat == 'Game':
                color_map5[cat] = 'pink'
            else:
                color_map5[cat] = auto_colors[auto_idx % len(auto_colors)]
                auto_idx += 1

        fig5 = px.scatter(
            df5,
            x='Size',
            y='Rating',
            size='Installs',
            color='Category_Display',
            color_discrete_map=color_map5,
            hover_name='App Name',
            hover_data={'Installs': True, 'Rating': True, 'Size': True},
            title='App Size vs Average Rating — Bubble Size = Installs (Game highlighted Pink)',
            labels={
                'Size': 'App Size (MB)',
                'Rating': 'Average Rating',
                'Category_Display': 'Category'
            }
        )
        fig5.update_layout(
            plot_bgcolor='rgba(245,245,250,1)',
            legend_title='Category'
        )
        st.plotly_chart(fig5, use_container_width=True)
        st.caption("Game = Pink | Beauty = Hindi | Business = Tamil | Dating = German")
    else:
        st.warning("No data available for Task 5 after applying filters.")
else:
    st.warning("Task 5 chart is only available between 5:00 PM - 7:00 PM IST. Enable Demo Mode in the sidebar to preview.")

st.divider()

# ─────────────────────────────────────────────────────────────────────────────
# TASK 6: Stacked Area Chart — Cumulative Installs Over Time (4 PM – 6 PM IST)
# ─────────────────────────────────────────────────────────────────────────────
st.header("Task 6: Cumulative Installs Over Time — Stacked Area Chart")
st.caption(" Available: 4:00 PM – 6:00 PM IST")

if in_window(16, 18):
    df6 = df[
        (df['Rating'] >= 4.2) &
        (~df['App Name'].str.contains(r'\d', regex=True, na=False)) &
        (df['Category'].str.startswith(('T', 'P'), na=False)) &
        (df['Rating Count'] > 1000) &
        (df['Size'].between(20, 80))
    ].copy()

    if not df6.empty:
        df6['Category_Display'] = df6['Category'].replace({
            'Travel & Local': 'Voyage & Local (Travel & Local)',
            'Productivity':   'Productividad (Productivity)',
            'Photography':    'Shashin - 写真 (Photography)'
        })

        df6['YearMonth'] = df6['Last Updated'].dt.to_period('M').astype(str)
        df6_trend = df6.groupby(['YearMonth', 'Category_Display'])['Installs'].sum().reset_index()
        df6_trend['Date'] = pd.to_datetime(df6_trend['YearMonth'])
        df6_trend = df6_trend.sort_values('Date')

        df6_trend['Prev_Installs'] = df6_trend.groupby('Category_Display')['Installs'].shift(1)
        df6_trend['MoM_Growth'] = (
            (df6_trend['Installs'] - df6_trend['Prev_Installs']) / df6_trend['Prev_Installs']
        )
        df6_trend['High_Growth'] = df6_trend['MoM_Growth'] > 0.25
        high_growth_months = df6_trend[df6_trend['High_Growth']]['Date'].unique()

        fig6 = px.area(
            df6_trend,
            x='Date',
            y='Installs',
            color='Category_Display',
            title='Cumulative Installs Over Time — T & P Categories (Gold = >25% MoM Growth)',
            labels={
                'Date': 'Date',
                'Installs': 'Total Installs',
                'Category_Display': 'Category'
            },
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        for hg_date in high_growth_months:
            fig6.add_vrect(
                x0=hg_date,
                x1=hg_date + pd.DateOffset(months=1),
                fillcolor='gold',
                opacity=0.25,
                layer='below',
                line_width=0,
                annotation_text=">25%",
                annotation_position="top left",
                annotation_font_size=9
            )

        fig6.update_layout(
            plot_bgcolor='rgba(245,245,250,1)',
            legend_title='Category',
            hovermode='x unified'
        )
        st.plotly_chart(fig6, use_container_width=True)
        st.caption("Gold-shaded months = any category grew >25% month-over-month in installs.")
    else:
        st.warning("No data available for Task 6 after applying filters.")
else:
    st.warning("Task 6 chart is only available between 4:00 PM - 6:00 PM IST. Enable Demo Mode in the sidebar to preview.")
