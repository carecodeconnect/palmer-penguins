# load libraries
import streamlit as st
from streamlit_lottie import st_lottie
import seaborn as sns
import pandas as pd
import requests
import altair as alt

# header
st.title("Palmer Penguins :penguin:")

# subtitle
st.write(
    """
    This is a simple example of a Streamlit app using the Palmer Penguins dataset. 
    The Palmer Penguins dataset is a popular dataset for data exploration and visualization. 
    The dataset contains various measurements of penguins, including bill length, bill depth, flipper length, body mass, and species. 
    In this example, we will use the Palmer Penguins dataset to create a simple Streamlit app that includes a bar chart, scatter plot, violin plots, and a YouTube video.
    """
)

# animated penguin
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_penguin = load_lottieurl(
    "https://lottie.host/61d21d73-ab4b-43de-a5c0-5e67b0cdbd11/E87nM5RrTf.json"
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

# Proceed only if penguins data is loaded
if penguins is not None:
    # Sidebar options
    st.sidebar.title("Options")
    option = st.sidebar.selectbox("Choose an option", ["Dataframe", "Visualisation"])

    if option == "Dataframe":
        # Display the dataset
        st.write(penguins)

        # Download dataset as CSV
        csv = penguins.to_csv(index=False)
        st.download_button(label="Download csv", data=csv, file_name="penguins.csv", mime="text/csv")

    elif option == "Visualisation":
        # title for pandas
        st.title("Bar chart with pandas")

        # visualise the dataset
        st.bar_chart(penguins["species"].value_counts())

        # title for seaborn
        st.title("Scatter plot with seaborn")
        # plot a scatter plot
        st.pyplot(sns.pairplot(penguins, hue="species"))

        # title for altair
        st.title("Scatter plot with altair")
        # plot with altair with x-axis from 160 to 240 and y-axis from 12 to 22

        chart = alt.Chart(penguins).mark_point().encode(
            x=alt.X('flipper_length_mm', scale=alt.Scale(domain=(160, 240))),
            y=alt.Y('bill_depth_mm', scale=alt.Scale(domain=(12, 22))),
            color='species'
        )
        st.altair_chart(chart, use_container_width=True)

        # title for plotly
        st.title("Scatter plot with plotly")
        # plot with plotly
        import plotly.express as px
        fig = px.scatter(penguins, x="flipper_length_mm", y="bill_depth_mm", color="species")
        st.plotly_chart(fig)

        # violion plot with plotly
        st.title("Violin plot with plotly")
        # plot a violin plot with plotly
        fig = px.violin(penguins, y="bill_length_mm", x="species", box=True, points="all")
        st.plotly_chart(fig)

# title for youtube
st.title("Youtube video")
# youtube video
st.write("Youtube video")
# embed a youtube video
st.video("https://youtu.be/q3uXXh1sHcI")
