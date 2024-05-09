import streamlit as st
from streamlit_folium import st_folium

from utils.prepare import prepare_df
from utils.constant import WEIGHT_CHOICE
from utils.cluster import generate_map


# Cache the prepare_df function
@st.cache_data()
def cached_prepare_df():
    return prepare_df()

def distribution_center():
    
    @st.cache_data()
    def cached_prepare_df():
        return prepare_df()
    
    st.set_page_config(layout = 'wide')
    #st.title("Folium Map with Clustering")
    c1, c2, _, c3, c4  = st.columns((0.5, 2, 0.5, 4, 0.5))

    # c1.title('Column 1')
    # c2.title('Column 2')
    
    
    
    df_stateonly = cached_prepare_df()
    COUNTRY_CHOICE = df_stateonly["country_region_name"].unique()
    # Widget to select countries
    with c2:
        selected_countries = st.multiselect("Select Countries", COUNTRY_CHOICE, default=COUNTRY_CHOICE)
        
        if not selected_countries:
            st.warning("Please select at least one country.")
            return

        # Widget to select weighted attribute
        weight_attr = st.selectbox("Select Weighted Attribute", WEIGHT_CHOICE, index=4)

        # Widget to select number of clusters
        n_clusters = st.slider("Select Number of Clusters", min_value=2, max_value=10, value=3)

    df_stateonly = df_stateonly[df_stateonly["country_region_name"].isin(selected_countries)] 

    map = generate_map(df_stateonly, weight_attr, n_clusters=n_clusters)

    # Display the Folium map using Streamlit
    with c3:
        st_folium(map, width=1500, height=900)

if __name__ == "__main__":
    distribution_center()