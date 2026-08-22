import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import requests
import seaborn as sns
from sklearn.linear_model import LinearRegression

def read_results(file_name="Data/game-results.csv", split_on_game_version = False, time_group=[0, 5, 10, 30, 60, 90, float("inf")], score_group=[0, 100, 500, 1000, 5000, 10000, 50000, float("inf")]):
    gr_df = pd.read_csv(file_name, parse_dates=[0,1], header=None, names=["Game Version", "Date", "Time Survived", "Score"], dtype={"Time Survived":"float64","Score":"Int64"})

    gr_df = gr_df.replace(r"^\s*$", pd.NA, regex=True)
    gr_df["Date"] = gr_df["Date"].str.strip()
    gr_df["Date"] = pd.to_datetime(gr_df["Date"])

    gr_df.set_index("Date", inplace=True)

    gr_df = gr_df[gr_df.index.notna()]

    gr_df.dropna(subset=["Time Survived", "Score"], inplace=True)

    missing = gr_df["Game Version"].isna()

    for idx in gr_df.index[missing]:
        pos = gr_df.index.get_loc(idx)

        # First or Last
        if pos == 0 or pos == len(gr_df) -1:
            df.drop(idx, inplace=True)
            continue

        above = gr_df.iloc[pos -1]["Game Version"]
        below = gr_df.iloc[pos + 1]["Game Version"]

        if pd.notna(above) and pd.notna(below) and above == below:
            gr_df.at[idx, "Game Version"] = above
        else:
            gr_df.drop(idx, inplace=True)

    time_group_labels = []
    i = 1
    while i <= len(time_group)-2:
        time_group_labels.append(f"{time_group[i-1]} < {time_group[i]}")
        i += 1
    time_group_labels.append(f"> {time_group[i-1]}")

    score_group_labels = []
    i = 1
    while i <= len(score_group)-2:
        score_group_labels.append(f"{score_group[i-1]} < {score_group[i]-1}")
        i += 1
    score_group_labels.append(f"> {score_group[i-1]}")

    gr_df["Survival Group"] = pd.cut(gr_df["Time Survived"], bins=time_group, labels=time_group_labels, right=False)

    gr_df["Score Group"] = pd.cut(gr_df["Score"], bins=score_group, labels=score_group_labels, right=False)

    if split_on_game_version:
        return split_game_version(gr_df)

    else:
        return gr_df

def read_powerup_data(file_name="Data/powerup-data.csv"):
    powerup_df = pd.read_csv("Data/powerup-data.csv", 
                         parse_dates=["Date"], 
                         header=None, 
                         names=["Date","Powerup","Time Spawned","Time Activated","Time Effect Ended"], 
                         dtype={"Powerup":"string", "Time Spawned":"float64", "Time Activated":"float64","Time Effect Ended":"float64"})

    powerup_df = powerup_df.replace(r"^\s*$", pd.NA, regex=True)

    powerup_df.set_index("Date", inplace=True)

    powerup_df = powerup_df[powerup_df.notna()]

    powerup_df.dropna(subset=["Powerup","Time Spawned"], inplace=True)

    powerup_df = powerup_df[~(powerup_df["Time Effect Ended"].notna() & powerup_df["Time Activated"].isna())]

    return powerup_df

def score_over_time(game_version=1, remove_edges=True, data=[], file_name=""):
    if type(data) == list:
        gv_df = dfs[game_version]
    else:
        gv_df = data
    
    if remove_edges:
        gv_df = gv_df[(
        (gv_df["Score"] >= gv_df["Score"].quantile(0.025)) &
        (gv_df["Score"] <= gv_df["Score"].quantile(0.975)))]
    

    # Exponential regression requires positive y values
    plot_df = gv_df[gv_df["Score"] > 0]

    # Generate smooth curve
    x_fit = pd.DataFrame({
        "Time Survived": np.linspace(
            plot_df["Time Survived"].min(),
            plot_df["Time Survived"].max(),
            100
        )
    })

    # -----------------------
    # Exponential regression
    # Score = a * exp(bx)
    # -----------------------

    X_exp = plot_df[["Time Survived"]]
    y_exp = np.log(plot_df["Score"])

    exp_model = LinearRegression()
    exp_model.fit(X_exp, y_exp)

    y_exp_fit = np.exp(exp_model.predict(x_fit))


    # -----------------------
    # Power-law regression
    # Score = a * x^b
    # -----------------------

    X_power = np.log(plot_df[["Time Survived"]])
    y_power = np.log(plot_df["Score"])

    power_model = LinearRegression()
    power_model.fit(X_power, y_power)

    y_power_fit = np.exp(
        power_model.predict(np.log(x_fit))
    )

    # Plot
    sns.scatterplot(
        data=plot_df,
        x="Time Survived",
        y="Score",
        color="black"
    )
    sns.set_style("whitegrid")
    #sns.axes_style(style="white")
    sns.despine(offset=10)
    
    plt.plot(
        x_fit["Time Survived"],
        y_exp_fit,
        label="Exponential Regression",
        color="red"
    )

    plt.plot(
        x_fit["Time Survived"],
        y_power_fit,
        label="Power-law Regression",
        color="blue"
    )

    plt.xlabel("Time Survived (seconds)")
    plt.ylabel("Score")
    plt.title("Score vs Time Survived")
    plt.legend()

    if file_name != "":
        if file_name.endswith(".png") == False:
            file_name = file_name + ".png"
        plt.savefig(f"Data/{file_name}")    

    
    plt.show()

    # Exponential Regression
    a = np.exp(exp_model.intercept_)
    b = exp_model.coef_[0]

    print(f"Exponential:   Score = {a:.2f} * exp({b:.6f} * Time Survived)")

    r2 = exp_model.score(X_exp, y_exp)
    print(f"Exponential R²: {r2:.3f}")

    # Power-law Regression   
    a_power = np.exp(power_model.intercept_)
    b_power = power_model.coef_[0]

    print(f"Power-law:   Score = {a_power:.2f} × Time Survived^{b_power:.2f}")

    print(f"Power-law R²:   {power_model.score(X_power, y_power):.3f}")

def bar_charts(game_version=1, data=[], file_name=""):
    

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    if type(data) == list:
        data = dfs[game_version]
        fig.suptitle(f"Game Results for Game Version {game_version}", fontsize=16,fontweight="bold")
    else:
        fig.suptitle("Game Results", fontsize=16,fontweight="bold")
        
    # Survival Group
    sns.countplot(
        data=data,
        x="Survival Group",
        ax=axes[0]
    )
    axes[0].set_xlabel("Survival Group")
    axes[0].set_ylabel("Number of Results")
    axes[0].yaxis.set_major_locator(MaxNLocator(integer=True))
    axes[0].set_title("Results by Survival Group")
    axes[0].tick_params(axis="x", rotation=45)

    # Score Group
    sns.countplot(
        data=data,
        x="Score Group",
        ax=axes[1]
    )
    axes[1].set_xlabel("Score Group")
    axes[1].set_ylabel("Number of Results")
    axes[1].yaxis.set_major_locator(MaxNLocator(integer=True))
    axes[1].set_title("Results by Score Group")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    
    if file_name != "":
        if file_name.endswith(".png") == False:
            file_name = file_name + ".png"
        plt.savefig(f"Data/{file_name}")    

    plt.show()

def powerup_gr_merge(powerup_df, gr_df):
    com_df = powerup_df.merge(gr_df, left_index=True, right_index=True, how="inner")
    com_df["Time Survived After Activated"] = (com_df["Time Survived"]-com_df["Time Activated"])

    return com_df

def split_game_version(df, gv=0):
    version = pd.Series(df["Game Version"].unique()).sort_values().reset_index(drop=True)

    version_map = pd.Series( version.values, index = range(1, len(version)+1))

    #if gv hasn't changed return all the separate gvs and the version map
    if gv == 0:

        df["Game Version"] = df["Game Version"].map(lambda x: version_map[version_map == x].index[0])
        
        dfs = {}

        for version in df["Game Version"].unique():
            dfs[version] = df[df["Game Version"] == version].drop(columns="Game Version").copy()
        return dfs, version_map 

    #if gv is an int return the df for that game version
    elif type(gv) == int and gv != 0:
        new_df = df[df["Game Version"] == version_map[gv]].copy()
        
        return new_df

    #if gv is a datetime
    elif type(gv) == np.datetime64:
        new_df = df[df["Game Version"] == gv].copy()

        return new_df

    #if gv is a list of ints
    elif type(gv) == list and type(gv[0]) == int:
        new_df = df[df["Game Version"].isin(version_map[gv])].copy()

        return new_df

    #if gv is a list of datetime
    elif type(gv) == list and type(gv[0]) == np.datetime64:
        new_df = df[df["Game Version"].isin(gv)].copy()

        return new_df