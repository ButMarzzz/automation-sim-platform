import pandas as pd
from pathlib import Path   
import streamlit as st
import plotly.express as px

# Helper functions
def format_avg_stat(series, unit):
    return f"{series.mean().round(2)} {unit}"

def format_max_stat(series, unit):
    return f"{series.max().round(2)} {unit}"

def section_title(title):
    st.markdown(
        f"""
        <h2 style="color:#4A90E2; margin-top:30px;">
            {title}
        </h2>
        """,
        unsafe_allow_html=True
    )

def plot_line_sensor(df, sensor, title):
    # create plot
    # display plot
    st.plotly_chart(px.line(df, x="time", y = sensor, title = title))

# =========================
# Load Data
# =========================

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

# =========================
# Overview
# =========================

section_title("Overview")

st.write(df.describe())
col1, col2 = st.columns(2)

col1.metric("Average RPM", round(mean_rpm,2))
col2.metric("Amount of Passes", len(df))

st.plotly_chart(px.bar(avg_rpm, x=avg_rpm.index, y=["avg_rpm", "max_rpm", "min_rpm"],
                        barmode="group", title="Average RPM by State" ))

section_title("Engine State Analysis")

st.write(state_counts)

df["prev_state"]= df['state'].shift(1)
df["changed_state"]= df["state"] != df["prev_state"]
df["groups"] = df["changed_state"].cumsum()

state_duration_chart = df.groupby("groups").agg(
    state=("state","first"),
    start=("time", min),
    end=("time", max),
    duration=("time", lambda x: x.max() - x.min())
)

#How many times did the engine enter each state?

number_of_state = state_duration_chart["state"].value_counts()

st.write(number_of_state)

#How much total time was spent in each state?

group_analysis = state_duration_chart.groupby("state").agg(
    total_duration_sec= ("duration", sum),
    mean_duration_sec= ("duration", "mean")
)
st.write(group_analysis)

longest = (state_duration_chart.loc[state_duration_chart["duration"].idxmax()])

col1, col2 = st.columns(2)

col1.metric("Longest State", longest["state"])
col2.metric("Longest Total Duration", f"{longest["duration"]} seconds")

#Total number of state events
st.metric("Count State Changes",(df["changed_state"] == True).sum())

#Total engine operating time
operating = df[(df["state"]!="OFF") & (df["state"]!="cranking")] 
st.metric("Total Operating Time (seconds)", (operating["time"].max() - operating["time"].min()).round(2))

#timeline-like visualization from state_duration_chart

st.write(state_duration_chart)
st.plotly_chart(px.bar(state_duration_chart, x="duration", y = "state", base="start", 
                       orientation="h", color='state',  title = "State Timeline", ))


# =========================
# Fault overview
# =========================

section_title("Fault Analysis")
# How many telemetry records have issues?
# How many are normal?
# What types of issues occurred?

total_issues= len(df[df["issues"]!="No faults detected"])
st.dataframe(issue_counts)

col1, col2 = st.columns(2)
issue_percentage = total_issues/len(df)
col1.metric("Total Issues", total_issues)
col2.metric("Issue Rate",issue_percentage, format="percent")

faults= issue_counts[issue_counts.index!="No faults detected"]
max_fault= faults.idxmax()
st.metric("Most Common Fault (Number of Occurrences)", f"{max_fault} - {faults[max_fault]}")

st.plotly_chart(px.bar(faults, x= faults.index, y= faults.values, title= "Fault Frequency", 
                       labels={"x":"Fault Type","y": "Occurrences"} ))

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

st.metric("Total Duration of Faults", f"{fault_chart["duration"].sum()} seconds" )
st.metric("Average Fault Duration", format_avg_stat(fault_chart["duration"], "seconds"))

longest_fault = fault_chart.loc[fault_chart["duration"].idxmax()]

col1, col2 = st.columns(2)

col1.metric("Longest Fault", longest_fault["fault"])
col2.metric("Duration (seconds)", longest_fault["duration"].round(2))

st.plotly_chart(px.bar(fault_chart,x="duration",y="fault",base="start",color= "fault", 
                       orientation="h",title="Fault Timeline"))

cooling = just_issues[just_issues["issues"] == "Cooling system issue"]
head_gasket = just_issues[just_issues["issues"] == "Possible head gasket failure"]
alternator = just_issues[just_issues["issues"] == "Alternator not charging"]

no_faults = df[df["issues"] == "No faults detected"]

with st.expander("Detailed Fault Comparisons"):
    # metrics go here
    st.subheader("Fault vs Normal")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)


    col1.metric("Average Temperature during Cooling Issue", format_avg_stat(cooling["temp"],"°C"))
    col2.metric("Average Temperature during Normal Operation", format_avg_stat(no_faults["temp"], "°C"))

    col3.metric("Average RPM during Cooling Issue", format_avg_stat(cooling["rpm"],"RPM"))
    col4.metric("Average RPM during Normal Operation", format_avg_stat(no_faults["rpm"], "RPM"))

    col5.metric("Max Temperature during Cooling Issue", format_max_stat(cooling["temp"] ,"°C"))
    col6.metric("Max Temperature during Normal Operation", format_max_stat(no_faults["temp"] ,"°C"))


    st.metric("Average Oil Pressure during Head Gasket Symptoms", format_avg_stat(head_gasket["pressure"] ,"psi"))

    st.metric("Average Temperature during Head Gasket Symptoms", format_avg_stat(head_gasket["temp"], "°C"))

    col5.metric("Average Voltage during Alternator Issue", format_avg_stat(alternator["voltage"], "V"))
    col6.metric("Average Voltage during Normal Operation", format_avg_stat(no_faults["voltage"], "V"))

# =========================
# Interactive Analysis
# =========================
section_title("Interactive Analysis")

selected_sensor = st.selectbox(
    label="Choose Sensor for graph vs Time:",
    options= options,
    placeholder="Select a Sensor"
)

chart_names= {
    "rpm": "RPM",
    "voltage": "System Voltage",
    "temp": "Engine Temperature",
    "pressure": "Engine Pressure"
}

if selected_sensor:
    st.success(f"You selected: {selected_sensor}")
    plot_line_sensor(df, selected_sensor , title= chart_names[selected_sensor] + " vs Time")

selected_fault = st.selectbox(
    label="Choose Fault for Statistics:",
    options= faults.index,
    placeholder="Select a Fault"
)

fault_names= {
    "Cooling system issue": cooling,
    "Possible head gasket failure": head_gasket, 
    "Alternator not charging": alternator 
}

# Average temperature
# Max temperature
# Average RPM
# Average pressure
# Average voltage
# Fault duration

selected_data = fault_names[selected_fault]

if selected_fault:
    st.success(f"You selected: {selected_fault}")
    st.write(just_issues[just_issues["issues"] == selected_fault ])

    st.metric(f"Average Temperature during {selected_fault}", format_avg_stat(selected_data["temp"], "°C"))
    st.metric(f"Max Temperature during {selected_fault}", format_max_stat(selected_data["temp"],"°C"))

    st.metric(f"Average RPM during {selected_fault}", format_avg_stat(selected_data["rpm"],"RPM"))
    st.metric(f"Max RPM during {selected_fault}", format_max_stat(selected_data["rpm"],"RPM"))

    st.metric(f"Average Pressure during {selected_fault}", format_avg_stat(selected_data["pressure"],"psi"))

    st.metric(f"Average Voltage during {selected_fault}", format_avg_stat(selected_data["voltage"], "V"))
    st.metric(f"Duration of fault: {selected_fault}", fault_chart[fault_chart["fault"]==selected_fault]["duration"].sum().round(2))

    st.plotly_chart(px.bar(fault_chart[fault_chart["fault"] == selected_fault], x= "duration",y= "fault",orientation = "h",base="start", title=f" Full Timeline for Fault: {selected_fault}"))

selected_state = st.selectbox(
    label= "Choose State:",
    options= state_counts.index,
    placeholder= "Select a State"
)

selected_data = df[df["state"]==selected_state]
if selected_state:
    st.success(f"You selected: {selected_state}")

    st.metric(f"Avg RPM during {selected_state}", format_avg_stat(selected_data["rpm"],"RPM"))
    st.metric(f"Max RPM during {selected_state}", format_max_stat(selected_data["rpm"],"RPM"))

    st.metric(f"Avg Temperature during {selected_state}", format_avg_stat(selected_data["temp"],"°C"))
    st.metric(f"Max Temperature during {selected_state}", format_max_stat(selected_data["temp"], "°C"))

    st.metric(f"Avg Pressure during {selected_state}", format_avg_stat(selected_data["pressure"], "psi"))

    st.metric(f"Avg Voltage during {selected_state}", format_avg_stat(selected_data["voltage"], "V"))
    st.metric(f"Duration of state: {selected_state}", state_duration_chart[state_duration_chart["state"] == selected_state]["duration"].sum().round(2))

    st.plotly_chart(px.bar(state_duration_chart[state_duration_chart["state"] == selected_state], x= "duration",y= "state",orientation = "h",base="start", title=f"Timeline for {selected_state} State"))

time_range = st.slider(
    label="Choose a time:",
    min_value=df["time"].min(),
    max_value=df["time"].max(),
    value=(df["time"].min(), df["time"].max())
)


if time_range:
    
    min_value, max_value = time_range
    filtered_df = df[(df["time"] >= min_value) & (df["time"] <= max_value) & (df["state"] == selected_state)]
    if filtered_df.empty:
        st.write("There is no data")
    else:
        plot_line_sensor(filtered_df, selected_sensor, title= chart_names[selected_sensor]  + "__" + selected_state + "__" + str(round(min_value,0)) + " - " + str(round(max_value,0)) + " seconds")



# df2 = pd.DataFrame({
#     'date': ['2022-02-01', '2022-03-01', '2022-04-01'] * 3,
#     'type': ['TYPE1', 'TYPE1', 'TYPE1', 'TYPE2', 'TYPE2', 'TYPE2', 'TYPE3', 'TYPE3', 'TYPE3'],
#     'value': [15,10,15,20,19,20,33,29,24]
# })

# # Pivot to get multi-index
# df_pivot = df2.pivot_table(index=['type', 'date'], values='value', aggfunc='mean')

# fig = px.line(df_pivot.reset_index(), x='type', y='value', color='date')
# fig.show()
