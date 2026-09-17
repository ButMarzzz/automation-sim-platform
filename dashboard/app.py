import pandas as pd
from pathlib import Path   
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def plot_sensor(df, sensor, title):
    # create plot
    # display plot
    st.plotly_chart(px.line(df, x="time", y = sensor, title = title))

BASE_DIR = Path(__file__).resolve().parent.parent
log_path = BASE_DIR / "logs" / "engine_data.csv"

df = pd.read_csv(log_path)

options = ["rpm", "voltage", "temp", "pressure"]

avg_rpm = df.groupby("state").agg(
    avg_rpm=pd.NamedAgg(column="rpm", aggfunc="mean"),
    max_rpm=pd.NamedAgg(column="rpm", aggfunc="max"),
    min_rpm=pd.NamedAgg(column="rpm", aggfunc="min")
)

mean_rpm = df["rpm"].mean()
issue_counts = df["issues"].value_counts()
state_counts = df["state"].value_counts()

st.title("Automotive Telemetry Dashboard")

st.write("Engine monitoring dashboard")

st.write(df.describe())
st.dataframe(df[df["state"]=="OFF"])
st.metric("Avg RPM", mean_rpm)
st.metric("Amount of Passes", len(df))

st.plotly_chart(px.bar(avg_rpm, x=avg_rpm.index, y=["avg_rpm", "max_rpm", "min_rpm"],
                        barmode="group", title="Average RPM by State"))

selected_sensor = st.selectbox(
    label="Choose Sensor for graph vs Time:",
    options= options,
    placeholder="Select a sensor"
)

chart_names= {
    "rpm": "RPM",
    "voltage": "System Voltage", 
    "temp": "Engine Temperature", 
    "pressure": "Engine Pressure"
}

if selected_sensor:
    st.success(f"You selected: {selected_sensor}")
    plot_sensor(df, selected_sensor , title= chart_names[selected_sensor] + " vs Time")

st.write(state_counts)

df["prev_state"]= df['state'].shift(1)
df["changed_state"]= df["state"] != df["prev_state"]
df["groups"] = df["changed_state"].cumsum()

grouped_chart = df.groupby("groups").agg(
    state=("state","first"),
    start=("time", min),
    end=("time", max),
    duration=("time", lambda x: x.max() - x.min())
)

#How many times did the engine enter each state?

number_of_state = grouped_chart["state"].value_counts()

st.write(number_of_state)

#How much total time was spent in each state?

group_analysis = grouped_chart.groupby("state").agg(
    total_duration_sec= ("duration", sum),
    mean_duration_sec= ("duration", "mean")
)
st.write(group_analysis)

longest = (grouped_chart.loc[grouped_chart["duration"].idxmax()])
st.metric("Longest duration (seconds)", f"{longest['state']} — {longest['duration']} seconds")

col1, col2 = st.columns(2)

col1.metric("Longest State", longest["state"])
col2.metric("Longest Duration", longest["duration"])

st.write(number_of_state.sum())

#Total number of state events
st.metric("Count State Changes",(df["changed_state"] == True).sum())
st.write(len(grouped_chart))

st.write(df[df["changed_state"]==True])
#Total engine operating time
operating = df[(df["state"]!="OFF") & (df["state"]!="cranking")] 
st.metric("Total Operating Time", operating["time"].sum())

#timeline-like visualization from grouped_chart

st.write(grouped_chart)
st.plotly_chart(px.bar(grouped_chart, x="duration", y = "state", base="start", orientation="h", color='state',  title = "State Timeline"))

st.write(grouped_chart.dtypes)

# Fault overview

# How many telemetry records have issues?
# How many are normal?
# What types of issues occurred?

total_issues= len(df[df["issues"]!="No faults detected"])
st.dataframe(issue_counts)

st.metric("Total Issues", total_issues)
st.metric("Issue Percentage",total_issues/len(df))
st.metric("Number of Fault Type", ((df["issues"]!="No faults detected")).count())

faults= issue_counts[issue_counts.index!="No faults detected"]
max_fault= faults.idxmax()
st.metric("Most Common Fault(Number of Occurrences)", f"{max_fault} - {faults[max_fault]}")

st.plotly_chart(px.bar(faults, x= faults.index, y= faults.values, title= "Fault Frequency", labels={"x":"Fault Type","y": "Occurrences"}  ))

just_issues = df[df["issues"] != "No faults detected"].copy()
just_issues["prev_fault"]= just_issues["issues"].shift(1)
just_issues["changed_fault"]= just_issues["prev_fault"] != just_issues["issues"]
just_issues["group_fault"]= just_issues["changed_fault"].cumsum()

fault_chart = just_issues.groupby("group_fault").agg(
    fault=("issues","first"),
    start=("time", min),
    end=("time", max),
    duration=("time", lambda x: x.max() - x.min())
)

st.write(fault_chart)
st.write(just_issues)
st.metric("Total Duration of Faults", fault_chart["duration"].sum())
st.metric("Average Fault Duration", fault_chart["duration"].mean().round(2))

longest_fault = fault_chart.loc[fault_chart["duration"].idxmax()]
col1,col2 = st.columns(2)

col1.metric("Longest Fault", longest_fault["fault"])
col2.metric("Duration(seconds)", longest_fault["duration"].round(2))

st.plotly_chart(px.bar(fault_chart,x="duration",y="fault",base="start",color= "fault", orientation="h",title="Fault Timeline"))

cooling = just_issues[just_issues["issues"] == "Cooling system issue"]
head_gasket = just_issues[just_issues["issues"] == "Possible head gasket failure"]
alternator = just_issues[just_issues["issues"] == "Alternator not charging"]
st.metric("Average Temperature during Cooling Issue", cooling["temp"].mean().round(2))
st.metric("Average RPM during Cooling Issue", cooling["rpm"].mean.round(2))
st.metric("Max Temperature during Cooling Issue", cooling["temp"].max.round(2))

st.metric("Average Oil Pressure during Head Gasket Symptoms", head_gasket["pressure"].mean.round(2))
st.metric("Average Temperature during Head Gasket Symptoms", head_gasket["temp"].mean.round(2))

st.metric("Average Voltage during Alternator Issue", alternator["voltage"].mean.round(2))

# df2 = pd.DataFrame({
#     'date': ['2022-02-01', '2022-03-01', '2022-04-01'] * 3,
#     'type': ['TYPE1', 'TYPE1', 'TYPE1', 'TYPE2', 'TYPE2', 'TYPE2', 'TYPE3', 'TYPE3', 'TYPE3'],
#     'value': [15,10,15,20,19,20,33,29,24]
# })

# # Pivot to get multi-index
# df_pivot = df2.pivot_table(index=['type', 'date'], values='value', aggfunc='mean')

# fig = px.line(df_pivot.reset_index(), x='type', y='value', color='date')
# fig.show()
