import streamlit as st
from streamlit_lottie import st_lottie
import seaborn as sns
import pandas as pd
import requests
import altair as alt
import plotly.express as px

# Header
st.title("Palmer Penguins :penguin:")

# Subtitle/Description
st.write(
    """
    This is a simple example of a Streamlit app using the Palmer Penguins dataset. 
    The Palmer Penguins dataset is a popular dataset for data exploration and visualization. 
    The dataset contains various measurements of penguins, including bill length, bill depth, flipper length, body mass, and species. 
    In this example, we explore the Palmer Penguins dataset through various visualizations.
    For further details, please refer to the [Palmer Penguins dataset](https://allisonhorst.github.io/palmerpenguins/articles/intro.html).
    """
)

# Animated penguin
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_penguin = load_lottieurl(
    "https://lottie.host/ba70f2c0-0396-4957-9413-60c184cf2bee/tzy7xktBVd.json"
)
st_lottie(lottie_penguin, height=300, key="penguin_animation")

# Sidebar for data loading
st.sidebar.title("Load Data")
penguins = None

# Button to load penguins dataset from seaborn
if st.sidebar.button("Load from seaborn"):
    penguins = sns.load_dataset("penguins")

# Upload file
uploaded_file = st.sidebar.file_uploader("Or upload a file", type=["csv", "txt"])
if uploaded_file is not None:
    # Read the file
    penguins = pd.read_csv(uploaded_file)

# Show YouTube video based on sidebar button
if st.sidebar.button("Show Video"):
    st.video("https://youtu.be/q3uXXh1sHcI")

# Proceed only if penguins data is loaded
if penguins is not None:
    # Display the dataset
    st.header("Penguin Data Table")
    st.write("This table displays the raw data of penguin measurements.")
    st.dataframe(penguins)

    # Bar chart with pandas
    st.header("Species Distribution")
    st.write("A bar chart showing the count of each penguin species in the dataset.")
    st.bar_chart(penguins["species"].value_counts())

    # Scatter Plot with Seaborn
    st.header("Pairwise Relationships")
    st.write("Scatter plots showing pairwise relationships between different measurements, colored by species.")
    st.pyplot(sns.pairplot(penguins, hue="species"))

    # Scatter Plot with Altair
    st.header("Flipper Length vs. Bill Depth")
    st.write("An interactive scatter plot of flipper length against bill depth, colored by species.")
    chart = alt.Chart(penguins).mark_point().encode(
        x=alt.X('flipper_length_mm', scale=alt.Scale(domain=(160, 240))),
        y=alt.Y('bill_depth_mm', scale=alt.Scale(domain=(12, 22))),
        color='species'
    )
    st.altair_chart(chart, use_container_width=True)

    # Scatter Plot with Plotly
    st.header("Flipper Length vs. Bill Depth with Plotly")
    st.write("A scatter plot created with Plotly, showing flipper length against bill depth, colored by species.")
    fig = px.scatter(penguins, x="flipper_length_mm", y="bill_depth_mm", color="species")
    st.plotly_chart(fig)

    # Violin Plot with Plotly
    st.header("Bill Length Distribution by Species")
    st.write("A violin plot illustrating the distribution of bill lengths across different penguin species.")
    fig = px.violin(penguins, y="bill_length_mm", x="species", box=True, points="all")
    st.plotly_chart(fig)
