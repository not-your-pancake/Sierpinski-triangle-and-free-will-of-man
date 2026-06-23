import random
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Sierpinski Chaos Game", layout="centered")

st.title("🔺 The Chaos Game: Sierpinski Triangle")
st.write(
    "Watch order emerge from pure randomness. Select the number of iterations "
    "below to see how the fractal forms."
)

# --- Sidebar Controls ---
st.sidebar.header("Simulation Settings")

# User input for iterations
num_iterations = st.sidebar.slider(
    label="Number of Iterations",
    min_value=100,
    max_value=50000,
    value=10000,
    step=100,
)

# Visual customization options
dot_color = st.sidebar.selectbox(
    "Color Palette", ["inferno", "viridis", "copper", "cool", "magma"]
)
bg_style = st.sidebar.radio("Background Style", ["Dark Mode", "Light Mode"])

# --- Core Chaos Game Logic ---
# Define vertices of the equilateral triangle
vertices = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2]])

# Seed the random number generator for stability inside Streamlit's rerun loop
random.seed(42)

# Initialize a random starting point
current_point = np.array([random.uniform(0, 1), random.uniform(0, 1)])

x_points = [current_point[0]]
y_points = [current_point[1]]

# Generate points based on user configuration
for _ in range(num_iterations):
    chosen_vertex = vertices[random.randint(0, 2)]
    current_point = (current_point + chosen_vertex) / 2
    x_points.append(current_point[0])
    y_points.append(current_point[1])

# --- Plotting ---
fig, ax = plt.subplots(figsize=(8, 7))

# Apply dark or light mode styling dynamically
if bg_style == "Dark Mode":
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")
    title_color = "white"
else:
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    title_color = "black"

# Render the generated points
# Size 's' scales down automatically as iterations grow to preserve resolution
dot_size = 0.5 if num_iterations < 5000 else 0.05

scatter = ax.scatter(
    x_points,
    y_points,
    s=dot_size,
    c=y_points,
    cmap=dot_color,
    marker=".",
)

# Highlight original vertices
ax.scatter(
    vertices[:, 0], vertices[:, 1], color="#FF4B4B", s=50, marker="^"
)

# Formatting adjustments
ax.axis("off")
ax.set_title(
    f"Sierpinski Gasket ({num_iterations:,} dots)",
    color=title_color,
    fontsize=14,
    pad=10,
)

# Output the plot inside the Streamlit app layout
st.pyplot(fig)

# --- Dynamic Analytics ---
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Dots Rendered", value=f"{num_iterations:,}")
with col2:
    st.metric(
        label="Fractal Dimension", value="~1.585", help="ln(3) / ln(2)"
    )