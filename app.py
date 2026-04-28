import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout="wide")
st.title("📊 Google Play Store Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("C:/Users/Vishal.S/Downloads/intership of google play store/cleaned_dataset.csv")

df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')
df['Category'] = df['Category'].str.strip()
df['App Name'] = df['App Name'].astype(str)

# =============================
# TASK 1
# =============================
st.header("Task 1")

df1 = df[
    (df['Rating'] >= 4.0) &
    (df['Size'] >= 10) &
    (df['Month'] == 1)
]

if not df1.empty:
    top10 = df1.groupby('Category')['Installs'].sum().nlargest(10).index
    df1 = df1[df1['Category'].isin(top10)]

    agg = df1.groupby('Category').agg({
        'Rating': 'mean',
        'Rating Count': 'sum'
    }).reset_index()

    fig1 = px.bar(agg, x='Category', y=['Rating','Rating Count'], barmode='group')
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No data for Task 1")

# =============================
# TASK 2
# =============================
st.header("Task 2")

df2 = df[
    (~df['Category'].str.startswith(('A','C','G','S'), na=False)) &
    (df['Installs'] > 1_000_000)
]

df2 = df2.dropna(subset=['Country'])

if not df2.empty:
    top5 = df2['Category'].value_counts().nlargest(5).index
    df2 = df2[df2['Category'].isin(top5)]

    df2_map = df2.groupby('Country')['Installs'].sum().reset_index()

    fig2 = px.choropleth(df2_map,
                         locations="Country",
                         locationmode="country names",
                         color="Installs")

    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No data for Task 2")

# =============================
# TASK 3
# =============================
st.header("Task 3")

df3 = df[
    (df['Installs'] >= 10000) &
    (df['Revenue'] >= 10000) &
    (df['Minimum Android'] > 4.0) &
    (df['Size'] > 15) &
    (df['Content Rating'] == 'Everyone') &
    (df['App Name'].str.len() <= 30)
]

if not df3.empty:
    df3 = df3.copy()
    df3['Type'] = df3['Free'].apply(lambda x: 'Free' if x else 'Paid')

    top3 = df3['Category'].value_counts().nlargest(3).index
    df3 = df3[df3['Category'].isin(top3)]

    agg = df3.groupby('Type').agg({
        'Installs': 'mean',
        'Revenue': 'mean'
    }).reset_index()

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=agg['Type'], y=agg['Installs'], name='Installs'))
    fig3.add_trace(go.Scatter(x=agg['Type'], y=agg['Revenue'], yaxis='y2'))

    fig3.update_layout(yaxis2=dict(overlaying='y', side='right'))

    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No data for Task 3")

# =============================
# TASK 4
# =============================
st.header("Task 4")

df4 = df[
    (df['Category'].str.startswith(('E','C','B'), na=False)) &
    (df['Rating Count'] > 500) &
    (~df['App Name'].str.startswith(('x','y','z'), na=False)) &
    (~df['App Name'].str.contains('S', na=False))
]

if not df4.empty:
    df4 = df4.copy()

    df4['Category'] = df4['Category'].replace({
        'Beauty': 'सौंदर्य',
        'Business': 'வணிகம்',
        'Dating': 'Dating-DE'
    })

    df4_trend = df4.groupby(['Last Updated','Category'])['Installs'].sum().reset_index()
    df4_trend = df4_trend.sort_values('Last Updated')

    fig4 = px.line(df4_trend, x='Last Updated', y='Installs', color='Category')

    st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("No data for Task 4")

# =============================
# TASK 5
# =============================
st.header("Task 5")

categories = ['Game','Beauty','Business','Comics','Communication',
              'Dating','Entertainment','Social','Events']

df5 = df[
    (df['Rating'] > 3.5) &
    (df['Installs'] > 50000) &
    (df['Rating Count'] > 500) &
    (df['Sentiment_Subjectivity'] > 0.5) &
    (~df['App Name'].str.contains('S', na=False)) &
    (df['Category'].isin(categories))
]

if not df5.empty:
    df5 = df5.copy()

    df5['Category'] = df5['Category'].replace({
        'Beauty': 'सौंदर्य',
        'Business': 'வணிகம்',
        'Dating': 'Dating-DE'
    })

    fig5 = px.scatter(df5,
                      x='Size',
                      y='Rating',
                      size='Installs',
                      color='Category',
                      color_discrete_map={'Game': 'pink'})

    st.plotly_chart(fig5, use_container_width=True)
else:
    st.warning("No data for Task 5")

# =============================
# TASK 6
# =============================
st.header("Task 6")

df6 = df[
    (df['Rating'] >= 4.2) &
    (~df['App Name'].str.contains(r'\d', regex=True)) &
    (df['Category'].str.startswith(('T','P'), na=False)) &
    (df['Rating Count'] > 1000) &
    (df['Size'].between(20,80))
]

if not df6.empty:
    df6 = df6.copy()

    df6['Category'] = df6['Category'].replace({
        'Travel & Local': 'Voyage',
        'Productivity': 'Productividad',
        'Photography': '写真'
    })

    df6_trend = df6.groupby(['Last Updated','Category'])['Installs'].sum().reset_index()
    df6_trend = df6_trend.sort_values('Last Updated')

    fig6 = px.area(df6_trend,
                   x='Last Updated',
                   y='Installs',
                   color='Category')

    st.plotly_chart(fig6, use_container_width=True)
else:
    st.warning("No data for Task 6")
