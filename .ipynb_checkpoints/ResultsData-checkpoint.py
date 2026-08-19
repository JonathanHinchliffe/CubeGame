import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import requests
import seaborn as sns

df = pd.read_csv("game-results.csv", index_col=0, parse_dates=True, header=None, names=["Date", "Time Survived", "Score"])

time_bins = [0, 10, 30, 60, 90, float("inf")]
time_labels = ["< 10 seconds", "10–29 seconds", "30–59 seconds", "60-89 seconds", "90+ seconds"]

df["Survival Group"] = pd.cut(df["Time Survived"], bins=time_bins, labels=time_labels)

score_bins = [0, 100, 500, 1000, 5000, 10000, 50000, float("inf")]
score_labels = ["< 100 points", "100-499 points", "500-999 points", "1000-4999 points", "5000-9999 points", "10000-49999 points", ">50000 points"]

df["Points Group"] = pd.cut(df["Score"], bins=score_bins, labels=score_labels)
print(df.head())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

sns.countplot(data=df, x="Survival Group", ax=axes[0])
axes[0].set_xlabel("Survival Group")
axes[0].set_ylabel("Number of Results")
axes[0].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[0].set_title("Results by Survival Group")
axes[0].tick_params(axis="x", rotation=45)

sns.countplot(data=df, x="Points Group", ax=axes[1])
axes[1].set_xlabel("Points Group")
axes[1].set_ylabel("Number of Results")
axes[1].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[1].set_title("Results by Points Group")
axes[1].tick_params(axis="x", rotation=45)

plt.tight_layout()


fig.savefig("result-groups.png")
plt.show()