import streamlit as st

st.markdown("# Frequency Matrix")

import os
import pandas as pd

data_dir = "Data_csv"
dataframes = []

for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path)
        dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

# Print
sorted_df = combined_df.sort_values('Video ID')
filtered_df = combined_df[combined_df['Time (s)'] < 1]
center_counts = filtered_df.groupby(['Center X', 'Center Y']).size().reset_index(name='Count')
highest_frequency = center_counts.sort_values('Count', ascending=False).iloc[0]
highest_frequency_center_x = highest_frequency['Center X']
highest_frequency_center_y = highest_frequency['Center Y']

import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Define the dimensions of the chart
width = 1280
height = 800

# Define the number of squares in each dimension
num_squares = 10

# Calculate the size of each square
square_width = width // num_squares
square_height = height // num_squares

# Create a grid of coordinates
x = np.arange(0, width, square_width)
y = np.arange(0, height, square_height)
X, Y = np.meshgrid(x, y)

# Initialize an empty frequency matrix
frequency_matrix = np.zeros((num_squares, num_squares))

# Iterate over the rows of the combined_df dataframe
for _, row in combined_df.iterrows():
    # Get the coordinates of the current row
    center_x = row['Center X']
    center_y = row['Center Y']
    
    # Find the square where the coordinates fall
    square_x = int(center_x // square_width)
    square_y = int(center_y // square_height)
    
    # Increment the frequency count for the corresponding square
    frequency_matrix[square_y, square_x] += 1

# Create a color map for the heatmap
cmap = plt.cm.get_cmap('cool')

# Plot the heatmap
plt.figure(figsize=(10, 6))
plt.imshow(frequency_matrix, cmap=cmap, origin='lower')
plt.colorbar(label='Frequency')
plt.title('Frequency Heatmap')
plt.xlabel('Square X')
plt.ylabel('Square Y')
st.pyplot(plt.gcf())

# Get the top 10 square regions with the highest frequency
top_regions = np.unravel_index(np.argsort(frequency_matrix, axis=None)[-10:], frequency_matrix.shape)

# Print the top 10 square regions
st.write("Top 10 Square Regions:")
for region in top_regions:
    st.write(f"Square X: {region[1]}, Square Y: {region[0]}")
