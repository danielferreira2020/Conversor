import streamlit as st
import numpy as np
from st_aggrid import AgGrid
import pandas as pd

data = {
    'country': ['norway', 'russia', 'china', 'japan'],
    'capital': ['oslo', 'moscow', 'beijing', 'tokyo']
}

df = pd.DataFrame(data)

with st.container():
    st.write("This is inside the container")
    AgGrid(df, height=200)    
    st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container.")