"""
A program to:
- Load our CSVs containing our data into pandas DataFrames
- Convert them to 3NF, and save the results as parquet files
"""

__author__ = "Debra Ritter"

import pandas as pd

# Not in 3NF
bios_df: pd.DataFrame = pd.read_csv("clean-data/bios_locs.csv")

# Not in 1NF
results_df: pd.DataFrame = pd.read_csv("clean-data/results.csv")
print(bios_df.head())


# Note that our relational database needs to be reformatted to have everything
# fit in at least 3NF.
