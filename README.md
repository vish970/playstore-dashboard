 Google Play Store Analytics Dashboard
An interactive analytics dashboard built with Python, Streamlit, and Plotly to visualize and explore Google Play Store data across 6 detailed tasks.

 Live Application
 https://playstore-dashboard-utkz4edqog2apcpm8wxdek.streamlit.app

 Demo Mode (For Reviewers)
Each chart is time-restricted as per task requirements and is only visible during a specific IST time window.

 To view all charts at any time, please enable  Demo Mode from the left sidebar of the dashboard.

TaskChart TypeTime Window (IST)Task 1Grouped Bar Chart3:00 PM – 5:00 PMTask 2Choropleth Map6:00 PM – 8:00 PMTask 3Dual-Axis Chart1:00 PM – 2:00 PMTask 4Time Series Line Chart6:00 PM – 9:00 PMTask 5Bubble Chart5:00 PM – 7:00 PMTask 6Stacked Area Chart4:00 PM – 6:00 PM

Task Overview
Task 1 — Grouped Bar Chart (3 PM – 5 PM IST)
Compares average rating and total review count for the top 10 app categories by installs.
Filters Applied:

Average rating ≥ 4.0
App size ≥ 10 MB
Last updated in January only


Task 2 — Choropleth Map (6 PM – 8 PM IST)
Visualizes global installs by category using an interactive Plotly choropleth map.
Filters Applied:

Top 5 app categories by total installs
Installs > 1,000,000
Categories must not start with: A, C, G, or S


Task 3 — Dual-Axis Chart (1 PM – 2 PM IST)
Compares average installs (bars) and average revenue (lines) for Free vs Paid apps across the top 3 categories.
Filters Applied:

Installs ≥ 10,000
Revenue ≥ $10,000
Android version > 4.0
App size > 15 MB
Content rating = Everyone
App name ≤ 30 characters (including spaces and special characters)


Task 4 — Time Series Line Chart (6 PM – 9 PM IST)
Tracks total installs over time segmented by category. Periods of significant growth are highlighted with shaded bands and percentage annotations.
Filters Applied:

Category starts with: E, C, or B
Reviews > 500
App name does not start with: x, y, or z
App name does not contain the letter S (case-insensitive)
Growth highlight: months where installs increase > 20% month-over-month

Translations:
OriginalTranslatedLanguageBeautyसौंदर्यHindiBusinessவணிகம்TamilDatingPartnersucheGerman

Task 5 — Bubble Chart (5 PM – 7 PM IST)
Analyzes the relationship between app size and average rating, with bubble size representing number of installs.
Filters Applied:

Rating > 3.5
Installs > 50,000
Reviews > 500
Sentiment subjectivity > 0.5
App name does not contain the letter S (case-insensitive)
Categories: Game, Beauty, Business, Comics, Communication, Dating, Entertainment, Social, Events

Highlights:

 Game category is highlighted in Pink

Translations:
OriginalTranslatedLanguageBeautyसौंदर्यHindiBusinessவணிகம்TamilDatingPartnersucheGerman

Task 6 — Stacked Area Chart (4 PM – 6 PM IST)
Visualizes cumulative installs over time for each category as a color-banded area chart.
Filters Applied:

Average rating ≥ 4.2
App name does not contain any numbers
Category starts with: T or P
Reviews > 1,000
App size between 20 MB and 80 MB
Growth highlight: months where total installs increase > 25% month-over-month (gold shading)

Legend Translations:
OriginalTranslatedLanguageTravel & LocalVoyage & LocalFrenchProductivityProductividadSpanishPhotography写真 (Shashin)Japanese

 Tech Stack
TechnologyPurposePythonCore programming languagePandasData manipulation and filteringPlotlyInteractive visualizationsStreamlitWeb application frameworkPytzIST timezone handling

 Project Structure
Playstore-dashboard/
├── app.py                  # Main Streamlit application
├── cleaned_dataset.csv     # Cleaned dataset used for analysis
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

 How to Run Locally
Step 1 — Clone the repository
bashgit clone https://github.com/vish970/Playstore-dashboard.git
cd Playstore-dashboard
Step 2 — Install dependencies
bashpip install -r requirements.txt
Step 3 — Run the app
bashstreamlit run app.py
Step 4 — Open in browser
The app will open automatically at:
http://localhost:8501

 Requirements
streamlit
pandas
plotly
pytz

 Author
Vishal S
Data Science & Analytics Enthusiast

Submitted To
Elevnce Skills Technology
Internship Project — Google Play Store Analytics Dashboard
