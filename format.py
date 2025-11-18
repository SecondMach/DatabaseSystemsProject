import pandas as pd

# Not in 3NF
bios_df = pd.read_csv("clean-data/bios_locs.csv")

# Not in 1NF
results_df = pd.read_csv("clean-data/results.csv")
print(bios_df.head())