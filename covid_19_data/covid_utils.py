import os

import matplotlib.pyplot as plt
import pandas as pd


class Utils:
    def __init__(self):
        super().__init__()
        self.counties_csv = r"us-counties.csv"
        self.diff_1_suffix = " - Daily Increase"
        self.diff_2_suffix = " - Change in Daily Increase"

    def read_counties_csv(self):
        df = pd.read_csv(self.counties_csv, parse_dates=["date"])
        df["cfr"] = df["deaths"] / df["cases"]
        df["county_state"] = df["county"] + ", " + df["state"]

        self.state_names = df["state"].unique()
        return df

    def get_top(self, df, column, num_to_show=5):
        if column == "cfr":
            df = df.dropna()
        df = df[df["cfr"] <= 1]
        df = df.sort_values(by=column)
        lo = df.head(num_to_show)
        hi = df.tail(num_to_show).sort_values(by=column, ascending=False)
        return lo, hi

    def compute_diffs(self, df, window_size=5, center=True):

        counties = df.pivot(index="date", columns="county_state", values="cases")
        for county in counties.columns:
            counties[county + self.diff_1_suffix] = (
                counties[county].diff().rolling(window_size, center=center).mean()
            )
            counties[county + self.diff_2_suffix] = counties[
                county + self.diff_1_suffix
            ].diff()
        return counties

    def generate_plots(self, counties, state_names):
        for state in state_names:
            county_names = [c for c in counties.columns if c.endswith(state)]

            os.makedirs(f"plots/{state}", exist_ok=True)

            for county in county_names:
                df = counties[
                    [county, county + self.diff_1_suffix, county + self.diff_2_suffix]
                ].dropna()
                df["date"] = df.index.date
                if not df.empty:
                    df.plot.bar(x="date", subplots=True)
                    plt.savefig(f"plots/{state}/{county}.png", bbox_inches="tight")
                    plt.close()

    def plot_cases_by_weekday(self, counties, county):
        daily_increase = counties[[county + self.diff_1_suffix]]
        weekday = daily_increase.groupby([daily_increase.index.weekday]).sum()
        weekday.plot.bar()


if __name__ == "__main__":
    utils = Utils()
    counties = utils.read_counties_csv()
    counties = utils.compute_diffs(counties)

    # Generate all plots
    plt.rcParams["figure.figsize"] = [15, 10]
    utils.generate_plots(counties, utils.state_names)
