import streamlit as st  # Import the Streamlit library, which is used for building web applications with ease.

# ----------Page Setup----------
# The following sections define different pages for the multi-page Streamlit application.
# Each page is configured with a file path, title, icon, and a boolean value determining if it is the default page.

# Define the "home" page with its respective settings.
about_page = st.Page(
    page="main/pages/Home.py",
    title="home",
    icon="👤",
    default=True,  # This page is set as the default page when the application is launched.
)

# Define the first project page for bead pattern generation.
project_page = st.Page(
    page="main/pages/BeadPatternGeneraton.py",
    title="bead pattern generation",
    icon="📿",
    default=False,  # This page is not the default landing page.
)



# ----------Logo (Shared on all pages)----------
# Set a shared logo across all pages using an image located at the given path.
st.logo(
    "main/logo/ChatGPT Image Apr 11, 2025, 03_18_52 AM.png",
    size="large",  # The logo is rendered with a large size specification.
)

# Add a sidebar text element to provide a consistent message across the application.
st.sidebar.text("beadmaking is fun!")


# --------Navigation Menu----------
# The navigation menu aggregates the defined pages into an interactive menu.
# Note that only the first two pages (about_page and project_page) are included here.
pg = st.navigation(
    pages=[about_page, project_page],
    position='hidden'  # Set the navigation menu to be hidden; can be toggled or altered based on user interaction.
)

# Run the navigation menu to enable page switching as part of the application flow.
pg.run()
