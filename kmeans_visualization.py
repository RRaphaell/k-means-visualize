import streamlit as st
import matplotlib.pyplot as plt
from k_means import kmeans
from generate_data import generate_sample_data, generate_sample_data_centroids
from config import sidebar, main_page, figure

# config file vnaxo
st.set_page_config(
    page_title="K-Means clustering",
)


def create_plot_window():
    if 'fig' not in st.session_state:
        st.session_state.fig, st.session_state.ax = plt.subplots(figsize=figure["figsize"])
        st.session_state.ax.axes.xaxis.set_visible(False)
        st.session_state.ax.axes.yaxis.set_visible(False)
        st.session_state.data_plot = st.pyplot(st.session_state.fig)
    else:
        st.session_state.ax.clear()


# ---------------- Sidebar ---------------------
with st.sidebar.form(key="User input form"):
    st.write(sidebar["title"], unsafe_allow_html=True)
    st.write(sidebar["data_title"])
    data_size = st.slider("Data size",
                          min_value=sidebar["data"]["size"][0],
                          max_value=sidebar["data"]["size"][1])

    data_cluster_size = st.slider('Number of Clusters',
                                  min_value=sidebar["data"]["cluster_size"][0],
                                  max_value=sidebar["data"]["cluster_size"][1])

    data_variance = st.slider("Variance",
                              min_value=sidebar["data"]["variance"][0],
                              max_value=sidebar["data"]["variance"][1])
    generate_button = st.form_submit_button(label="Generate")

with st.sidebar.form(key="Training form"):
    st.write(sidebar["train_title"])
    centroid_size = st.slider("Number of Centroids",
                              min_value=sidebar["train"]["centroid_size"][0],
                              max_value=sidebar["train"]["centroid_size"][1])
    train_button = st.form_submit_button(label="Train")


# --------------- Main page ---------------------
st.write(main_page["title"], unsafe_allow_html=True)
st.write(main_page["description"])

create_plot_window()

# generate centers for all cluster and plot data around it
if generate_button:
    sample_data_centroids = generate_sample_data_centroids(data_cluster_size,
                                                           figure["xlim"][1], figure["ylim"][1],
                                                           offset=figure["offset"])

    st.session_state.sample_data = generate_sample_data(sample_data_centroids,
                                                        [[data_variance, 0], [0, data_variance]],
                                                        data_size)

    st.session_state.ax.plot(st.session_state.sample_data[:, 0], st.session_state.sample_data[:, 1], '.', alpha=0.5)
    st.session_state.ax.set(xlim=figure["xlim"], ylim=figure["ylim"])
    st.session_state.data_plot.pyplot(st.session_state.fig)

# train the K-Means and color the data
if train_button:
    kmeans(st.session_state.sample_data, centroid_size, st.session_state.data_plot,
           st.session_state.fig, st.session_state.ax)
