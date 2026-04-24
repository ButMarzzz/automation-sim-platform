import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("engine_data.csv")

# Peek at data (don’t skip this — prevents dumb mistakes)
print(df.head())

# Example: plot one column vs another
plt.plot(df["time"], df["temperature"])

plt.xlabel("Time")
plt.ylabel("Temperature")
plt.title("Temperature Over Time")

plt.show()