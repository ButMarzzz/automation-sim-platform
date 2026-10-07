import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
log_path = BASE_DIR / "logs" / "engine_data.csv"

df = pd.read_csv(log_path)

print(df.head())      # first 5 rows
print(df.tail())      # last 5 rows

# print(df.columns)

print(df.info())

print(df.describe())

# rev = df[df["state"] == "REV"]

# print("rpm.mean: ",rev["rpm"].mean())

# cooling = df[df["issues"] == "Cooling system issue"]
# print(cooling)

# high_rpm = df[df["rpm"] > 3000]

# print(df["rpm"].max())
# rev = df[df["state"] == "REV"]

# hot_running = df[
#     (df["temp"] > 100) &
#     (df["state"] == "RUNNING")
# ]

# print("Temp max: ", df["temp"].max())
# print("AVG temp: ", df["temp"].mode())

# print("count of enginestate: ", df[df["state"] == "REV"].value_counts())
# print(df[df["issues"] == "Cooling system issue"].value_counts())
# print(df["state"].value_counts())
# print(df["state"].nlargest(5))
# print(df["state"].sort_values("time"))
# print(df[df["issues"] != "No faults detected"].value_counts())
# print(df["voltage"].sort_values(ascending=False).head(5))

# print(df[df["state"] == "RUNNING"]["rpm"].mean())
# print(df["voltage"].min())

# print(df[df["issues"]=="Cooling system issue"].iloc[0]["time"])
# print(df.groupby("state")["rpm"].mean().max())

#Learing grouping groupby() and agg()
'''
For each state, show
average RPM
maximum RPM
minimum RPM
'''
print(df.groupby("state").agg(
    avg_rpm=("rpm", 'mean'),
    max_rpm=("rpm", "max"),
    min_rpm=("rpm", "min")
))
# Which state has the largest average pressure?
print(df.groupby("state").agg(
    avg_pres=("pressure","mean")
))

#Level 4 - Create New Columns
df["overheating"] = df["temp"]>110
df["warm"] = (df["temp"] > 90) & (df["temp"]<110)
print(df[df["overheating"] == True].value_counts())
# faults = df[df["issues"] != "No faults detected"]

# Time Series Thinking
# How long did the engine spend above 100°C?
hot = df[df["temp"]>100]
print(hot["time"].sum())

# At what time did the engine first exceed 5000 RPM?
high_rpm = df[df["rpm"] > 5000]
print(high_rpm["time"].iloc[0]) # or use .min() to get the first time

#.How long after starting did the cooling issue first appear?
start_time = df[df["state"] == "IDLE"]["time"].iloc[0]
cooling_issue_time = df[df["issues"] == "Cooling system issue"]["time"].iloc[0]
time_after_start = cooling_issue_time - start_time
print(f"Time after start: {time_after_start}")

df["previous_state"] = df["state"].shift(1)
df["change_state"] = df["state"] != df["previous_state"]

df["group"] = df["change_state"].cumsum()
print(df.groupby)
duration = df[df["state"]=="REV"].groupby("group").agg(
    start_time=("time", "min"),
    end_time=("time", "max"),
    duration=("time", lambda x: x.max() - x.min())
)

print(duration["duration"].max())
#print(df[df["change_state"] == True])
# print(faults)


# plt.plot(df["time"], df["rpm"])
# plt.xlabel("Time")
# plt.ylabel("RPM")
# plt.title("RPM vs Time")
# plt.show()

# plt.plot(df["time"], df["temp"])
# plt.xlabel("Time")
# plt.ylabel("Temperature")
# plt.show()

# plt.plot(df["time"], df["voltage"])
# plt.xlabel("Time")
# plt.ylabel("Voltage")
# plt.show()

# plt.plot(df["time"], df["pressure"])
# plt.xlabel('Time')
# plt.ylabel("Pressure")
# plt.show()

# print(df.nlargest(10, "temp"))
# print(df.nsmallest(10, "voltage"))
# print(df.nlargest(10, "pressure"))

# print(
#     df.groupby("state")[["rpm", "temp", "voltage", "pressure"]]
#       .mean()
# )