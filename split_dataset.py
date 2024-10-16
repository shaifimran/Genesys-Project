import pandas as pd

# Load the Excel file
df = pd.read_excel('./medicalDataset/combined_dataset.xlsx')

# Determine the number of rows per split
rows_per_split = 100

# Calculate the number of splits needed
num_splits = len(df) // rows_per_split + (1 if len(df) % rows_per_split else 0)

# Split the dataframe and save each chunk as a separate file
for i in range(num_splits):
    start_row = i * rows_per_split
    end_row = (i + 1) * rows_per_split
    chunk = df.iloc[start_row:end_row]
    chunk.to_excel(f'output_split_{i+1}.xlsx', index=False)
