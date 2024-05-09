# app1.py
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st

# main.py
import streamlit as st

def home():
    
    st.title('Combined App')
        
    if st.button("Visualization Dashboard"):
        st.switch_page("pages/dashboard.py")
    if st.button("Dsitribution Center"):
        st.switch_page("pages/distribution_center.py")

if __name__ == '__main__':
    home()
