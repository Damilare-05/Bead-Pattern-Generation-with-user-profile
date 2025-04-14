import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.cluster import KMeans
from PIL import Image
import time
import os
import sqlite3

# ------------------------ CONFIG ------------------------
BEAD_COST_DEFAULT = 0.05

# ------------------------ CUSTOM STYLING ------------------------
st.markdown("""
    <style>
        .main {
            background-color: #F9F9F9;
        }
        h1, h2, h3 {
            color: #3F51B5;
        }
        .stButton>button {
            background-color: #FF7043;
            color: white;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------------ HELPERS ------------------------
def extract_color_palette(image, k=5):
    """
    Extracts a color palette from the provided image by clustering pixel colors using KMeans.
    
    Parameters:
        image (np.array): The image array.
        k (int): Number of clusters/colors.
    
    Returns:
        List[tuple]: Sorted list of color tuples.
    """
    pixels = image.reshape(-1, 3).astype(np.float32)
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pixels)
    palette = np.uint8(kmeans.cluster_centers_)
    _, counts = np.unique(kmeans.labels_, return_counts=True)
    sorted_idx = np.argsort(-counts)
    return [tuple(color) for color in palette[sorted_idx]]

# ------------------------ PATTERN GENERATORS ------------------------
def generate_vertical_symmetric_grid(palette, rows=8, cols=8):
    grid = [[None]*cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols // 2):
            color = palette[(i + j) % len(palette)]
            grid[i][j] = grid[i][cols - j - 1] = color
    return grid

def generate_horizontal_symmetric_grid(palette, rows=8, cols=8):
    grid = [[None]*cols for _ in range(rows)]
    for i in range(rows // 2):
        for j in range(cols):
            color = palette[(i + j) % len(palette)]
            grid[i][j] = grid[rows - i - 1][j] = color
    return grid

def generate_radial_symmetric_grid(palette, rows=8, cols=8):
    grid = [[None]*cols for _ in range(rows)]
    for i in range(rows // 2):
        for j in range(cols // 2):
            color = palette[(i + j) % len(palette)]
            grid[i][j] = grid[i][cols - j - 1] = grid[rows - i - 1][j] = grid[rows - i - 1][cols - j - 1] = color
    return grid

def generate_random_grid(palette, rows=8, cols=8, seed=42):
    rng = np.random.default_rng(seed)
    return [[palette[rng.integers(len(palette))] for _ in range(cols)] for _ in range(rows)]

def generate_linear_pattern(palette, pattern_length=12, mode="symmetric"):
    colors = [tuple(color) for color in palette]
    if mode == "symmetric":
        half = pattern_length // 2
        pattern = [colors[i % len(colors)] for i in range(half)]
        return pattern + pattern[::-1]
    elif mode == "alternating":
        pattern, forward, i = [], True, 0
        while len(pattern) < pattern_length:
            pattern.append(colors[i % len(colors)])
            i += 1 if forward else -1
            if i == len(colors) or i < 0:
                forward = not forward
                i = max(min(i, len(colors)-1), 0)
        return pattern
    elif mode == "gradient":
        return [colors[i % len(colors)] for i in range(pattern_length)]
    elif mode == "zigzag":
        pattern, reverse = [], False
        while len(pattern) < pattern_length:
            seq = colors[::-1] if reverse else colors
            for color in seq:
                if len(pattern) >= pattern_length:
                    break
                pattern.append(color)
            reverse = not reverse
        return pattern
    elif mode == "burst":
        half = pattern_length // 2
        half_pattern = [colors[i % len(colors)] for i in range(half)]
        pattern = half_pattern[::-1] + half_pattern
        if pattern_length % 2 != 0:
            pattern.insert(half, colors[half % len(colors)])
        return pattern
    return []

# ------------------------ VISUALIZATION ------------------------
def plot_grid(grid, title="Bead Pattern"):
    """
    Plots a 2D bead pattern using matplotlib.
    
    Parameters:
        grid (list[list[tuple]]): The 2D bead grid.
        title (str): Title of the plot.
    
    Returns:
        matplotlib.figure.Figure: The generated figure.
    """
    rows, cols = len(grid), len(grid[0])
    fig, ax = plt.subplots(figsize=(cols, rows))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if cell is None:
                continue
            color = np.array(cell) / 255
            circle = patches.Circle((j + 0.5, rows - i - 0.5), 0.45, color=color)
            ax.add_patch(circle)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title)
    return fig

def plot_linear_pattern(pattern, title="1D Pattern"):
    """
    Plots a 1D linear bead pattern using matplotlib.
    
    Parameters:
        pattern (list[tuple]): The 1D bead pattern.
        title (str): Title of the plot.
    
    Returns:
        matplotlib.figure.Figure: The generated figure.
    """
    fig, ax = plt.subplots(figsize=(len(pattern), 2))
    for i, color in enumerate(pattern):
        circle = patches.Circle((i + 0.5, 0.5), 0.45, color=np.array(color)/255)
        ax.add_patch(circle)
    ax.set_xlim(0, len(pattern))
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title)
    return fig

def load():
    """
    Displays a progress bar to simulate a work process.
    """
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(100):
        latest_iteration.text(f'Progress {i+1} %')
        bar.progress(i + 1)
        time.sleep(0.001)

def save_pattern(pattern, filename):
    """
    Saves the current pattern as an image file.
    
    Parameters:
        pattern (list[list[tuple]] or list[tuple]): The bead pattern.
        filename (str): Name of the file to save the image.
    """
    rows, cols = len(pattern), len(pattern[0])
    fig, ax = plt.subplots(figsize=(cols, rows))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    for i in range(rows):
        for j in range(cols):
            cell = pattern[i][j]
            if cell is None:
                continue
            color = np.array(cell) / 255
            circle = patches.Circle((j + 0.5, rows - i - 0.5), 0.45, color=color)
            ax.add_patch(circle)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

# ------------------------ COST ESTIMATION ------------------------
def estimate_total_cost(pattern, bead_cost=0.05):
    """
    Estimates total cost based on the number of beads/pattern elements.
    
    Parameters:
        pattern (list[list] or list): The bead pattern.
        bead_cost (float): Cost per bead.
    
    Returns:
        float: The estimated total cost.
    """
    if isinstance(pattern[0], list):
        total_beads = sum(len(row) for row in pattern)
    else:
        total_beads = len(pattern)
    return round(total_beads * bead_cost, 2)

# ------------------------ STATE MANAGEMENT ------------------------
def get_user_credentials():
    """
    Retrieves the current user credentials stored in session state.
    
    Returns:
        tuple: (email, password) or (None, None) if not set.
    """
    email = st.session_state.get("EMAIL")
    password = st.session_state.get("PASSWORD")
    return email, password

# ------------------------ DATABASE INTERACTION ------------------------
def fetch_user_profile(db_path="bead_project.db"):
    """
    Fetches the user profile from the database using credentials stored in session state.
    
    Returns:
        tuple: (id, firstname, email) if the profile is found, otherwise None.
    """
    email, password = get_user_credentials()
    if not email or not password:
        return None
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT id, firstname, email FROM profile WHERE email=? AND password=? LIMIT 1"
    cursor.execute(query, (email, password))
    profile = cursor.fetchone()
    conn.close()
    return profile

def init_saved_images_table(db_path="bead_project.db"):
    """
    Creates the saved_images table if it doesn't exist.
    
    The table links a saved image to a user profile via person_id.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS saved_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            saved_at TEXT
        );
    """
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

def insert_saved_image(person_id, image_path, db_path="bead_project.db"):
    """
    Inserts a new record into saved_images linking the image to the given person_id.
    
    Parameters:
        person_id (int): The user's ID.
        image_path (str): The file path where the image is saved.
    """
    saved_at = time.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    insert_query = "INSERT INTO saved_images (person_id, image_path, saved_at) VALUES (?, ?, ?)"
    try:
        cursor.execute(insert_query, (person_id, image_path, saved_at))
        conn.commit()
    except Exception as e:
        st.error(f"Error linking saved image: {e}")
    conn.close()

def get_saved_images(person_id, db_path="bead_project.db"):
    """
    Retrieves all saved images linked to the given person_id.
    
    Returns:
        list: List of tuples (id, image_path, saved_at).
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT id, image_path, saved_at FROM saved_images WHERE person_id=?"
    cursor.execute(query, (person_id,))
    images = cursor.fetchall()
    conn.close()
    return images

def delete_all_patterns(linked_images):
            for rec in linked_images:
                if os.path.exists(rec[1]):
                    os.remove(rec[1])
            conn = sqlite3.connect("bead_project.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM saved_images WHERE person_id=?", (person_id,))
            conn.commit()
            conn.close()
            st.rerun()
            st.success("All linked patterns deleted successfully!")
            

# Initialize the saved_images table on startup.
init_saved_images_table()

# ------------------------ STREAMLIT APP ------------------------
# Link to the home page (adjust label and link as needed)
st.page_link("main/pages/Home.py", label="🏠 HOME")
tab1, tab2 = st.tabs(["Bead Pattern Generation", "History"])

# Directory to save patterns
save_dir = "saved_patterns"
os.makedirs(save_dir, exist_ok=True)

# Display user profile details using session state credentials
profile = fetch_user_profile()
if profile:
    # profile now contains (id, firstname, email)
    st.sidebar.subheader("User Profile")
    st.sidebar.text(f"Name: {profile[1]}")
    st.sidebar.text(f"Email: {profile[2]}")
else:
    st.sidebar.warning("No user profile found. Please sign in.")

with tab1:
    st.title("🎨 Bead Pattern Generator")
    uploaded_file = st.file_uploader("Upload an image to generate a bead pattern:", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        image = np.array(image)
        palette = extract_color_palette(image, k=5)
        load()

        # Display the uploaded image and its extracted color palette
        st.image(image, caption="Uploaded Image", use_container_width=True)
        load()
        st.subheader("Extracted Color Palette")
        fig_palette = plt.figure(figsize=(5, 1))
        ax = fig_palette.add_subplot(111)
        for i, color in enumerate(palette):
            ax.fill_between([i, i+1], 0, 1, color=np.array(color)/255)
        ax.set_xlim(0, len(palette))
        ax.axis('off')
        st.pyplot(fig_palette)

        # Pattern Settings in the sidebar
        st.sidebar.subheader("Pattern Settings")
        pattern_type = st.sidebar.selectbox("Pattern Type", ["2D Pattern", "1D String Pattern"])
        symmetry_type = st.sidebar.selectbox("Symmetry Type", ["Vertical", "Horizontal", "Radial", "Random"])
        pattern_style = st.sidebar.selectbox("1D Pattern Style", ["symmetric", "alternating", "gradient", "zigzag", "burst"])
        rows = st.sidebar.slider("Rows (for 2D)", 4, 20, 8)
        cols = st.sidebar.slider("Columns (for 2D / Length for 1D)", 4, 20, 8)
        bead_cost = st.sidebar.slider('Bead Cost ($)', 0.001, 1.0, BEAD_COST_DEFAULT)

        # Generate the pattern based on user selections
        if pattern_type == "2D Pattern":
            if symmetry_type == "Vertical":
                grid = generate_vertical_symmetric_grid(palette, rows, cols)
            elif symmetry_type == "Horizontal":
                grid = generate_horizontal_symmetric_grid(palette, rows, cols)
            elif symmetry_type == "Radial":
                grid = generate_radial_symmetric_grid(palette, rows, cols)
            else:
                grid = generate_random_grid(palette, rows, cols)
            pattern = grid
            fig = plot_grid(grid, title=f"{symmetry_type} Symmetry Pattern")
        else:
            pattern = generate_linear_pattern(palette, pattern_length=cols, mode=pattern_style)
            fig = plot_linear_pattern(pattern, title=f"1D {pattern_style.capitalize()} Pattern")

        # Show the generated pattern and its estimated cost
        st.subheader("Generated Bead Pattern")
        st.pyplot(fig)
        total_cost = estimate_total_cost(pattern, bead_cost)
        st.subheader("Estimated Cost")
        st.markdown(f"💰 This pattern would cost approximately :blue-background[**${total_cost}**]")

        # Save pattern button
        if st.button("Save Current Pattern"):
            if pattern is not None:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                filename = os.path.join(save_dir, f"pattern_{timestamp}.png")
                save_pattern(pattern, filename)
                st.success(f"Pattern saved as {filename}")
                # Link the saved image to the user profile in the database
                if profile:
                    person_id = profile[0]  # Extract the user ID from profile
                    insert_saved_image(person_id, filename)
                    st.success("Pattern successfully linked to your profile!")
                else:
                    st.warning("No user profile found; the pattern was saved locally only.")
            else:
                st.warning("No pattern to save. Generate a pattern first.")
    else:
        st.warning("📸 Please upload an image to get started.")

with tab2:
    # List all saved pattern image files .
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        if st.button("Refresh Gallery"):
            st.rerun()
    # ------------------------ DISPLAY LINKED SAVED IMAGES AS A GRID ------------------------
    if profile:
            st.subheader("Saved Patterns Gallery")
            person_id = profile[0]
            linked_images = get_saved_images(person_id)

            if linked_images:
                # Set the number of columns for the grid.
                columns_per_row = 4
                # Create a list of column containers for a row.
                cols = st.columns(columns_per_row)
                for idx, rec in enumerate(linked_images):
                    # If necessary, rotate through new rows for every set of columns.
                    with cols[idx % columns_per_row]:
                        if os.path.exists(rec[1]):
                            st.image(rec[1], use_container_width=True)
                        else:
                            st.warning(f"File {rec[1]} not found.")
                    # When reaching the end of the row, create a new row for the remaining images.
                    if (idx + 1) % columns_per_row == 0 and (idx + 1) < len(linked_images):
                        cols = st.columns(columns_per_row)
                for idx, rec in enumerate(linked_images):
                    image_path = rec[1]
                    if os.path.exists(image_path):

                        with st.popover(f"total cost : ${total_cost}"):
                            left, center = st.columns(2)
                            with left:
                                if st.button("Delete", key=f"delete_{idx}"):
                                    os.remove(image_path)
                                    conn = sqlite3.connect("bead_project.db")
                                    cursor = conn.cursor()
                                    cursor.execute("DELETE FROM saved_images WHERE id=?", (rec[0],))
                                    conn.commit()
                                    conn.close()
                                    st.success(f"Deleted pattern ID: {rec[0]}")
                                    st.rerun()
                                st.image(image_path, use_container_width=True) 
                            with center:
                                st.write("Pattern Details")
                                st.write(f"Saved At: {rec[2]}")
                                st.write(f'total cost: ${total_cost}')
                                st.write(f"Bead Cost: ${BEAD_COST_DEFAULT}")
                                
                    else:
                        st.warning(f"File {image_path} not found.")
            else:
                st.info("No saved patterns found.")
    else:
        st.info("No user profile found. Please sign in.")
        
    with col3:
        if st.button("Delete All Patterns"):
            if profile:
                person_id = profile[0]
                linked_images = get_saved_images(person_id)
                if linked_images:
                    delete_all_patterns(linked_images)
                    
            else:
                st.info("No linked patterns to delete.")
           
