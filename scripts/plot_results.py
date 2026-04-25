import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
log_path = BASE_DIR / "logs" / "engine_data.csv"
# Load CSV
df = pd.read_csv(log_path)

# Peek at data (don’t skip this — prevents dumb mistakes)
print(df.head())

# Example: plot one column vs another
plt.plot(df["time"], df["temp"], label="Temp(F)")

plt.xlabel("Time(seconds)")
plt.ylabel("value")
plt.title("Temperature Over Time")

output_path = BASE_DIR / "outputs" / "graphs" / "graph.png"
output_path.parent.mkdir(exist_ok=True)

plt.legend()
plt.savefig(output_path)
plt.show()
