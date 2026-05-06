#  Google Play Store Analytics Dashboard

An interactive analytics dashboard built using **Python, Streamlit, and Plotly** to explore and visualize Google Play Store data across **6 detailed analytical tasks**.

---

##  Live Application  
https://playstore-dashboard-utkz4edqog2apcpm8wxdek.streamlit.app  

---

## Demo Mode (For Reviewers)

Each chart in the dashboard is **time-restricted** based on task requirements (IST).

 To view **all charts at any time**, enable **“Demo Mode”** from the left sidebar inside the app.

---

##  Task Availability (IST)

| Task | Chart Type              | Time Window |
|------|------------------------|------------|
| Task 1 | Grouped Bar Chart     | 3:00 PM – 5:00 PM |
| Task 2 | Choropleth Map        | 6:00 PM – 8:00 PM |
| Task 3 | Dual-Axis Chart       | 1:00 PM – 2:00 PM |
| Task 4 | Time Series Line Chart| 6:00 PM – 9:00 PM |
| Task 5 | Bubble Chart          | 5:00 PM – 7:00 PM |
| Task 6 | Stacked Area Chart    | 4:00 PM – 6:00 PM |

---

##  Task Overview

###  Task 1 — Grouped Bar Chart  
**Compares:** Average Rating vs Total Reviews (Top 10 Categories by Installs)

**Filters Applied:**
- Average rating ≥ 4.0  
- App size ≥ 10 MB  
- Last updated in January  

---

###  Task 2 — Choropleth Map  
**Visualizes:** Global installs by category

**Filters Applied:**
- Top 5 categories by installs  
- Installs > 1,000,000  
- Excludes categories starting with A, C, G, S  

---

###  Task 3 — Dual-Axis Chart  
**Compares:**  
- Bars → Average Installs  
- Line → Average Revenue  

**Filters Applied:**
- Installs ≥ 10,000  
- Revenue ≥ $10,000  
- Android version > 4.0  
- App size > 15 MB  
- Content rating = Everyone  
- App name ≤ 30 characters  

---

###  Task 4 — Time Series Line Chart  
**Tracks:** Install growth over time (by category)

**Filters Applied:**
- Category starts with E, C, B  
- Reviews > 500  
- App name excludes x, y, z  
- App name must not contain "S"  

**Highlights:**
-  Growth periods (>20% MoM) marked with shaded bands  

**Translations:**

| Original | Translated | Language |
|----------|-----------|----------|
| Beauty | सौंदर्य | Hindi |
| Business | வணிகம் | Tamil |
| Dating | Partnersuche | German |

---

###  Task 5 — Bubble Chart  
**Analyzes:** App Size vs Rating (Bubble size = Installs)

**Filters Applied:**
- Rating > 3.5  
- Installs > 50,000  
- Reviews > 500  
- Sentiment subjectivity > 0.5  
- App name excludes "S"  

**Categories Included:**
Game, Beauty, Business, Comics, Communication, Dating, Entertainment, Social, Events  

**Highlights:**
-  Game category highlighted in **pink**

**Translations:**

| Original | Translated | Language |
|----------|-----------|----------|
| Beauty | सौंदर्य | Hindi |
| Business | வணிகம் | Tamil |
| Dating | Partnersuche | German |

---

###  Task 6 — Stacked Area Chart  
**Visualizes:** Cumulative installs over time

**Filters Applied:**
- Average rating ≥ 4.2  
- App name without numbers  
- Category starts with T or P  
- Reviews > 1,000  
- App size between 20–80 MB  

**Highlights:**
-  Growth >25% MoM marked in **gold shading**

**Legend Translations:**

| Original | Translated | Language |
|----------|-----------|----------|
| Travel & Local | Voyage & Local | French |
| Productivity | Productividad | Spanish |
| Photography | 写真 (Shashin) | Japanese |

---

##  Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python | Core programming |
| Pandas | Data processing |
| Plotly | Interactive charts |
| Streamlit | Web app framework |
| Pytz | Timezone handling |

---

##  Project Structure

```
Playstore-dashboard/
│
├── app.py                  
├── cleaned_dataset.csv     
├── requirements.txt        
└── README.md               
```

---

##  How to Run Locally

### 1️ Clone Repository
```bash
git clone https://github.com/vish970/Playstore-dashboard.git
cd Playstore-dashboard
```

### 2️ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️ Run Application
```bash
streamlit run app.py
```

### 4️ Open in Browser
```
http://localhost:8501
```

---

##  Requirements

- streamlit  
- pandas  
- plotly  
- pytz  

---

##  Author  
**Vishal S**  
_Data Science & Analytics Enthusiast_

---

##  Submitted To  
**Elevnce Skills Technology**  
Internship Project — *Google Play Store Analytics Dashboard*
