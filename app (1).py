import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("owid-covid-data.csv")
    columns_needed = [
        "location", "date", "total_cases", "new_cases",
        "total_deaths", "population", "people_vaccinated"
    ]
    df = df[columns_needed]
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna(subset=["location", "date"])
    df = df[df["location"] != "World"]
    return df

df = load_data()

st.title("🌎 COVID-19 Data Dashboard")

# --- Global Cases Over Time ---
st.subheader("Global Total COVID-19 Cases Over Time")
global_cases = df.groupby("date")["total_cases"].sum()
fig, ax = plt.subplots()
ax.plot(global_cases)
ax.set_xlabel("Date")
ax.set_ylabel("Total Cases")
st.pyplot(fig)

# --- Top 10 Countries by Total Cases ---
st.subheader("Top 10 Countries by Total COVID-19 Cases")
top_cases = df.groupby("location")["total_cases"].max().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
top_cases.plot(kind="bar", ax=ax)
ax.set_ylabel("Total Cases")
st.pyplot(fig)

# --- Top 10 Countries by Total Deaths ---
st.subheader("Top 10 Countries by Total COVID-19 Deaths")
top_deaths = df.groupby("location")["total_deaths"].max().sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
top_deaths.plot(kind="bar", ax=ax)
ax.set_ylabel("Total Deaths")
st.pyplot(fig)

# --- Daily New Cases ---
st.subheader("Daily New COVID-19 Cases (Global)")
daily_cases = df.groupby("date")["new_cases"].sum()
fig, ax = plt.subplots()
ax.plot(daily_cases)
ax.set_xlabel("Date")
ax.set_ylabel("New Cases")
st.pyplot(fig)

# --- Population vs Total Cases ---
st.subheader("Population vs Total COVID-19 Cases")
country_data = df.groupby("location").max()
fig, ax = plt.subplots()
ax.scatter(country_data["population"], country_data["total_cases"])
ax.set_xlabel("Population")
ax.set_ylabel("Total Cases")
st.pyplot(fig)

# --- Cases per Million ---
st.subheader("Top 10 Countries by Cases per Million")
country_data["cases_per_million"] = (country_data["total_cases"] / country_data["population"]) * 1_000_000
top_cases_pm = country_data["cases_per_million"].sort_values(ascending=False).head(10)
fig, ax = plt.subplots()
top_cases_pm.plot(kind="barh", ax=ax)
ax.set_xlabel("Cases per Million")
st.pyplot(fig)

# --- Lowest Death Rate ---
st.subheader("Countries with Lowest COVID-19 Death Rate")
country_data["death_rate"] = (country_data["total_deaths"] / country_data["total_cases"])
death_rate = country_data["death_rate"].sort_values().head(10)
fig, ax = plt.subplots()
death_rate.plot(kind="barh", ax=ax)
ax.set_xlabel("Death Rate")
st.pyplot(fig)

# --- Global Vaccination Trend ---
st.subheader("Global Vaccination Trend Over Time")
vaccination_trend = df.groupby("date")["people_vaccinated"].sum()
fig, ax = plt.subplots()
ax.plot(vaccination_trend)
ax.set_xlabel("Date")
ax.set_ylabel("People Vaccinated")
st.pyplot(fig)

# --- Country Comparison ---
st.subheader("COVID-19 Cases Comparison by Country")
selected_countries = st.multiselect(
    "Select Countries:", options=df["location"].unique(), default=["India", "United States", "Germany"]
)
fig, ax = plt.subplots()
for country in selected_countries:
    country_df = df[df["location"] == country]
    ax.plot(country_df["date"], country_df["total_cases"], label=country)
ax.set_xlabel("Date")
ax.set_ylabel("Total Cases")
ax.legend()
st.pyplot(fig)

# --- Monthly Cases ---
st.subheader("Monthly COVID-19 New Cases")
df["month"] = df["date"].dt.to_period("M")
monthly_cases = df.groupby("month")["new_cases"].sum()
fig, ax = plt.subplots()
monthly_cases.plot(ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("New Cases")
st.pyplot(fig)
