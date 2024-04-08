import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from tqdm import tqdm
import plotly.graph_objs as go

# path stuff
data_path = "./data/"
sample_path = data_path + "your_sample/"
pre_path = "./data/pre_run/"

def load_sand():
    sand_init = np.load(pre_path + "sand_castle_init.npy")
    sand_final = np.load(pre_path + "sand_castle_final.npy")
    return sand_init, sand_final

# title and layout
st.set_page_config(layout="wide")
st.header("The sandpiles algorithm")   
st.divider()

s = 20
# load some data
sand_init, sand_final = load_sand()

def plot_2d(sand):
    fig, ax = plt.subplots()
    sand[np.logical_and(sand > -100, sand < -5)] = -80  
    plt.imshow(sand, cmap='Greys_r')
    plt.axis('off')
    # plt.colorbar()
    # set ticks on cbar white
    cbar = plt.colorbar()
    cbar.ax.yaxis.set_tick_params(color='blue', labelcolor='blue')
    # remove background
    fig.patch.set_visible(False)
    return fig, ax

cols_ = st.columns([4, 1])

with cols_[0]:
    '''To create a smooth energy landscape and integrate spatial information into our predictions,
    we apply the "sandpiles" algorithm for an example of cross section. Imagine iteratively pouring 
    sand on each pixel and letting it share between neighbours, with finite sinks to build a steady state.
    Click on the RUN button to start the algorithm and explore the final energy landscape.'''

with cols_[1]:
    st.write('#')
    run = st.toggle(f'RUN', key=531)

cols = st.columns([1, 1])

with cols[0]:
    st.write('  ***Sinks initialisation***')
    fig_i, ax = plot_2d(sand_init)
    st.pyplot(fig_i, use_container_width=True)

with cols[1]:
    if run == True:
        st.write('  ***Final sandpiles***')
        fig_f, ax = plot_2d(sand_final)
        st.pyplot(fig_f, use_container_width=True)

def matrix_trim(matrix, trim_value):
    """Trim a matrix, removing rows and columns that are all equal to a given value."""
    # full rows and columns
    full_cols = np.where(np.any(matrix != trim_value, axis=0))[0]
    full_rows = np.where(np.any(matrix != trim_value, axis=1))[0]

    # trim the matrix
    matrix = matrix[full_rows[0]:full_rows[-1]+1, full_cols[0]:full_cols[-1]+1]
    return matrix


if run == True:
    st.write('  ***- 3D view of the final sandpiles -***')

    sand_2 = np.load(pre_path + 'sand_castle_final.npy')
    
    sand_2 = matrix_trim(sand_2, -100)

    # sand_2 = sand_2[::2, ::2]

    sand_2[sand_2 < -40] = 100

    sand_2[sand_2 < -1] = -.1
    sand_2[sand_2 > 10] = -.5

    x = np.arange(sand_2.shape[1])
    y = np.arange(sand_2.shape[0])
    X, Y = np.meshgrid(x, y)

    heatmap = go.Surface(x=X, y=Y, z=sand_2, colorscale='Greys_r')

    layout = go.Layout(
        width=1000,
        height=800,
        # plot_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Z'),
            aspectratio=dict(x=1, y=1, z=0.7),
            camera=dict(eye=dict(x=1.2, y=1.2, z=0.6)),

            # z tick labels -0.5 = sink level, 
        
            # zlabel
            zaxis_title='Energy (amount of sand)',

        )
    )

    # add cbar label
    heatmap.update(colorbar=dict(title='Energy (amount of sand)'))

    fig = go.Figure(data=[heatmap], layout=layout)

    st.plotly_chart(fig)
