import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.prepare import prepare_df_dim_fact

#     st.plotly_chart(bar_fig)

def overall():
    print("runinig")
    import os
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from utils.prepare import prepare_df_dim_fact, prepare_df

    #Load data
    df_date = pd.read_csv("DateDim.csv")
    df_stat = pd.read_csv("StateProvinceFact.csv")

    # df_date, df_stat = prepare_df_dim_fact()

    # Merge datasets
    merged_df = pd.merge(df_stat, df_date, on="DateID", how="left")
    st.set_page_config(page_title="Sales Dashboard", layout="wide")
    # Set page title and layout
    #st.set_page_config(page_title="Sales Dashboard", layout="wide")

    # Section 1: Map visualization
    st.title("Map Visualization")
    st.sidebar.subheader("Map Settings")

    # Sidebar for filtering map
    selected_countries_map = st.sidebar.multiselect(
        "Select Country(s):",
        options=df_stat["CountryRegionName"].unique(),
        default=df_stat["CountryRegionName"].unique()
    )

    filtered_provinces = df_stat[df_stat["CountryRegionName"].isin(selected_countries_map)]["StateProvinceName"].unique()

    # Sidebar for filtering by province
    selected_provinces = st.sidebar.multiselect(
        "Select State(s):",
        options=filtered_provinces,
        default=filtered_provinces
    )

    attributes = ["ProductCount", "OrderCount", "TotalDiscount", "CustomerCount", "TotalSale"]
    selected_attribute = st.sidebar.selectbox(
        "Select an Attribute:",
        options=attributes,
        index=0  # Set the default selection to the first attribute
    )

    selected_year = st.sidebar.selectbox(
        "Select Year:",
        options=merged_df["Year"].unique(),
        format_func=lambda x: int(x) if not pd.isnull(x) else None,
        index=0
    )

    # Filter data for map
    filtered_df_map = merged_df[(merged_df["CountryRegionName"].isin(selected_countries_map)) 
                                & (merged_df["Year"] == selected_year)
                                & (merged_df["StateProvinceName"].isin(selected_provinces))]
    agg_functions = {
        'ProvinceLat': 'mean',
        'ProvinceLong': 'mean',
        'ProductCount': 'sum',
        'OrderCount': 'sum',
        'TotalDiscount': 'sum',
        'CustomerCount': 'sum',
        'TotalSale': 'sum',
        'CountryRegionName': 'first'
    }

    filtered_df = filtered_df_map.groupby('StateProvinceName').agg(agg_functions)
    # print(filtered_df)
    country_colors = px.colors.qualitative.Set1[:len(selected_countries_map)]

    # Customize map based on user selection
    fig_map = px.scatter_geo(
        filtered_df,
        lat="ProvinceLat",
        lon="ProvinceLong",
        hover_name="CountryRegionName",
        size=selected_attribute,
        projection="natural earth",
        title=f"{selected_attribute} by Country for Year {selected_year}",
        color="CountryRegionName",  # Assign different colors based on country
    )
    st.plotly_chart(fig_map)

    # Section 2: Pie chart
    st.title("Pie Chart")
    st.sidebar.subheader("Pie Chart Settings")

    # Sidebar for filtering pie chart with unique key
    selected_countries_pie = st.sidebar.multiselect(
        "Select Country(s) for Pie Chart:",
        options=df_stat["CountryRegionName"].unique(),
        default=df_stat["CountryRegionName"].unique(),
        key="pie_country_multiselect"  # Unique key for this multiselect widget
    )

    # Sidebar for selecting attributes and year
    attributes_pie = ["ProductCount", "OrderCount", "TotalDiscount", "CustomerCount", "TotalSale"]
    selected_attribute_pie = st.sidebar.selectbox(
        "Select an Attribute:", 
        options=attributes_pie,
        key="pie_attribute_multiselect"
    )
    selected_year_pie = st.sidebar.selectbox(
        "Select Year:", 
        options=merged_df["Year"].unique(),
        key="pie_year_select"
    )

    # Filter data for pie chart
    filtered_df_pie = merged_df[(merged_df["CountryRegionName"].isin(selected_countries_pie)) & (merged_df["Year"] == selected_year_pie)]
    agg_functions = {
        'ProvinceLat': 'mean',
        'ProvinceLong': 'mean',
        'ProductCount': 'sum',
        'OrderCount': 'sum',
        'TotalDiscount': 'sum',
        'CustomerCount': 'sum',
        'TotalSale': 'sum',
        'CountryRegionName': 'first'
    }

    filtered_pie = filtered_df_pie.groupby('StateProvinceName').agg(agg_functions)

    # Create pie chart
    fig_pie = px.pie(
        filtered_pie,
        names="CountryRegionName",
        values=selected_attribute_pie,
        title=f"{selected_attribute_pie} by State for Year {selected_year}"
    )
    st.plotly_chart(fig_pie)

    for country in selected_countries_pie:
        data = filtered_df_pie[filtered_df_pie["CountryRegionName"] == country]
        total = data[selected_attribute_pie].sum()    
        if total == 0:
            continue   
        fig_pie = px.pie(
            data,
            names="StateProvinceName",
            values=selected_attribute_pie,
            title=f"{selected_attribute_pie} by State for Year {selected_year} in {country}"
        )
        st.plotly_chart(fig_pie)

    # Section 3: Line chart
    st.title("Line Chart")
    st.sidebar.subheader("Line Chart Settings")

    # Sidebar for filtering line chart
    selected_countries_line = st.sidebar.multiselect(
        "Select Country(s):",
        options=df_stat["CountryRegionName"].unique(),
        default=df_stat["CountryRegionName"].unique(),
        key="line_country_multiselect"
    )

    filtered_provinces = df_stat[df_stat["CountryRegionName"].isin(selected_countries_line)]["StateProvinceName"].unique()

    selected_provinces_line = []
    for country in selected_countries_line:
        provinces = df_stat[df_stat["CountryRegionName"] == country]["StateProvinceName"].unique()[:3]  # Get the first three provinces
        selected_provinces_line.extend(provinces)

    selected_provinces_line = st.sidebar.multiselect(
        "Select State(s):",
        options=filtered_provinces,
        default=selected_provinces_line,
        key="province_line_select"
    )

    # Filter data for line chart
    filtered_df_line = merged_df[merged_df["CountryRegionName"].isin(selected_countries_line)]

    # Sidebar for selecting attributes and year
    attributes_line = ["ProductCount", "OrderCount", "TotalDiscount", "CustomerCount", "TotalSale"]
    selected_attribute_line = st.sidebar.selectbox(
        "Select an Attribute:", 
        options=attributes_line,
        key="line_attribute_select"
    )
    selected_year_line = st.sidebar.selectbox(
        "Select Year:", 
        options=merged_df["Year"].unique(),
        key="line_year_select"
    )

    # Filter data based on user selection
    filtered_df_line = merged_df[(merged_df["CountryRegionName"].isin(selected_countries_line)) 
                                & (merged_df["Year"] == selected_year_line)
                                & (merged_df["StateProvinceName"].isin(selected_provinces_line))]
    # agg_functions = {
    #     'ProvinceLat': 'mean',
    #     'ProvinceLong': 'mean',
    #     'ProductCount': 'sum',
    #     'OrderCount': 'sum',
    #     'TotalDiscount': 'sum',
    #     'CustomerCount': 'sum',
    #     'TotalSale': 'sum',
    #     'CountryRegionName': 'first',
    #     'FullDate': 'first',
    # }

    for country in selected_countries_line:
        data = filtered_df_line[filtered_df_line["CountryRegionName"] == country]
        line_fig = px.line(
            data,
            x="FullDate",
            y=selected_attribute_line,
            color="StateProvinceName",
            title=f"{selected_attribute_line} by Date for Year {selected_year_line} in {country}",
            labels={"FullDate": "Date", selected_attribute_line: selected_attribute_line},
            height=600,  # Adjust height as needed
        )

        # Update layout
        line_fig.update_layout(
            xaxis_title="Date",
            yaxis_title=selected_attribute_line,
            showlegend=True,  # Hide legend to prevent clutter
        )

        st.plotly_chart(line_fig)

    # for country in selected_countries_line:
    #     data = filtered_df_line[filtered_df_line["CountryRegionName"] == country]
    #     bar_fig = px.bar(
    #         data,
    #         x="FullDate",
    #         y=selected_attribute_line,
    #         color="StateProvinceName",
    #         title=f"{selected_attribute_line} by Date for Year {selected_year_line} in {country}",
    #         labels={"FullDate": "Date", selected_attribute_line: selected_attribute_line},
    #         barmode="group",  # Grouped bars
    #         height=600,  # Adjust height as needed
    #     )

    #     # Update layout
    #     bar_fig.update_layout(
    #         xaxis_title="Date",
    #         yaxis_title=selected_attribute_line,
    #         showlegend=True,  # Show legend to differentiate provinces
    #         bargap=0,
    #     )

    # #     st.plotly_chart(bar_fig)
    # if __name__ == "__main__":
    #     overall()
    

import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.prepare import prepare_df_dim_fact, prepare_df

#Load data
df_date = pd.read_csv("DateDim.csv")
df_stat = pd.read_csv("StateProvinceFact.csv")

# df_date, df_stat = prepare_df_dim_fact()

# Merge datasets
merged_df = pd.merge(df_stat, df_date, on="DateID", how="left")
st.set_page_config(page_title="Sales Dashboard", layout="wide")
# Set page title and layout
#st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Section 1: Map visualization
st.title("Map Visualization")
st.sidebar.subheader("Map Settings")

# Sidebar for filtering map
selected_countries_map = st.sidebar.multiselect(
    "Select Country(s):",
    options=df_stat["CountryRegionName"].unique(),
    default=df_stat["CountryRegionName"].unique()
)

filtered_provinces = df_stat[df_stat["CountryRegionName"].isin(selected_countries_map)]["StateProvinceName"].unique()

# Sidebar for filtering by province
selected_provinces = st.sidebar.multiselect(
    "Select State(s):",
    options=filtered_provinces,
    default=filtered_provinces
)

attributes = ["ProductCount", "OrderCount", "TotalDiscount", "CustomerCount", "TotalSale"]
selected_attribute = st.sidebar.selectbox(
    "Select an Attribute:",
    options=attributes,
    index=0  # Set the default selection to the first attribute
)

selected_year = st.sidebar.selectbox(
    "Select Year:",
    options=merged_df["Year"].unique(),
    format_func=lambda x: int(x) if not pd.isnull(x) else None,
    index=0
)

# Filter data for map
filtered_df_map = merged_df[(merged_df["CountryRegionName"].isin(selected_countries_map)) 
                            & (merged_df["Year"] == selected_year)
                            & (merged_df["StateProvinceName"].isin(selected_provinces))]
agg_functions = {
    'ProvinceLat': 'mean',
    'ProvinceLong': 'mean',
    'ProductCount': 'sum',
    'OrderCount': 'sum',
    'TotalDiscount': 'sum',
    'CustomerCount': 'sum',
    'TotalSale': 'sum',
    'CountryRegionName': 'first'
}

filtered_df = filtered_df_map.groupby('StateProvinceName').agg(agg_functions)
# print(filtered_df)
country_colors = px.colors.qualitative.Set1[:len(selected_countries_map)]

# Customize map based on user selection
fig_map = px.scatter_geo(
    filtered_df,
    lat="ProvinceLat",
    lon="ProvinceLong",
    hover_name="CountryRegionName",
    size=selected_attribute,
    projection="natural earth",
    title=f"{selected_attribute} by Country for Year {selected_year}",
    color="CountryRegionName",  # Assign different colors based on country
)
st.plotly_chart(fig_map)

# Section 2: Pie chart
st.title("Pie Chart")
st.sidebar.subheader("Pie Chart Settings")

# Sidebar for filtering pie chart with unique key
selected_countries_pie = st.sidebar.multiselect(
    "Select Country(s) for Pie Chart:",
    options=df_stat["CountryRegionName"].unique(),
    default=df_stat["CountryRegionName"].unique(),
    key="pie_country_multiselect"  # Unique key for this multiselect widget
)

# Sidebar for selecting attributes and year
attributes_pie = ["ProductCount", "OrderCount", "TotalDiscount", "CustomerCount", "TotalSale"]
selected_attribute_pie = st.sidebar.selectbox(
    "Select an Attribute:", 
    options=attributes_pie,
    key="pie_attribute_multiselect"
)
selected_year_pie = st.sidebar.selectbox(
    "Select Year:", 
    options=merged_df["Year"].unique(),
    key="pie_year_select"
)

# Filter data for pie chart
filtered_df_pie = merged_df[(merged_df["CountryRegionName"].isin(selected_countries_pie)) & (merged_df["Year"] == selected_year_pie)]
agg_functions = {
    'ProvinceLat': 'mean',
    'ProvinceLong': 'mean',
    'ProductCount': 'sum',
    'OrderCount': 'sum',
    'TotalDiscount': 'sum',
    'CustomerCount': 'sum',
    'TotalSale': 'sum',
    'CountryRegionName': 'first'
}

filtered_pie = filtered_df_pie.groupby('StateProvinceName').agg(agg_functions)

# Create pie chart
fig_pie = px.pie(
    filtered_pie,
    names="CountryRegionName",
    values=selected_attribute_pie,
    title=f"{selected_attribute_pie} by State for Year {selected_year}"
)
st.plotly_chart(fig_pie)

for country in selected_countries_pie:
    data = filtered_df_pie[filtered_df_pie["CountryRegionName"] == country]
    total = data[selected_attribute_pie].sum()    
    if total == 0:
        continue   
    fig_pie = px.pie(
        data,
        names="StateProvinceName",
        values=selected_attribute_pie,
        title=f"{selected_attribute_pie} by State for Year {selected_year} in {country}"
    )
    st.plotly_chart(fig_pie)

# Section 3: Line chart
st.title("Line Chart")
st.sidebar.subheader("Line Chart Settings")

# Sidebar for filtering line chart
selected_countries_line = st.sidebar.multiselect(
    "Select Country(s):",
    options=df_stat["CountryRegionName"].unique(),
    default=df_stat["CountryRegionName"].unique(),
    key="line_country_multiselect"
)

filtered_provinces = df_stat[df_stat["CountryRegionName"].isin(selected_countries_line)]["StateProvinceName"].unique()

selected_provinces_line = []
for country in selected_countries_line:
    provinces = df_stat[df_stat["CountryRegionName"] == country]["StateProvinceName"].unique()[:3]  # Get the first three provinces
    selected_provinces_line.extend(provinces)

selected_provinces_line = st.sidebar.multiselect(
    "Select State(s):",
    options=filtered_provinces,
    default=selected_provinces_line,
    key="province_line_select"
)

# Filter data for line chart
filtered_df_line = merged_df[merged_df["CountryRegionName"].isin(selected_countries_line)]

# Sidebar for selecting attributes and year
attributes_line = ["ProductCount", "OrderCount", "TotalDiscount", "CustomerCount", "TotalSale"]
selected_attribute_line = st.sidebar.selectbox(
    "Select an Attribute:", 
    options=attributes_line,
    key="line_attribute_select"
)
selected_year_line = st.sidebar.selectbox(
    "Select Year:", 
    options=merged_df["Year"].unique(),
    key="line_year_select"
)

# Filter data based on user selection
filtered_df_line = merged_df[(merged_df["CountryRegionName"].isin(selected_countries_line)) 
                            & (merged_df["Year"] == selected_year_line)
                            & (merged_df["StateProvinceName"].isin(selected_provinces_line))]
# agg_functions = {
#     'ProvinceLat': 'mean',
#     'ProvinceLong': 'mean',
#     'ProductCount': 'sum',
#     'OrderCount': 'sum',
#     'TotalDiscount': 'sum',
#     'CustomerCount': 'sum',
#     'TotalSale': 'sum',
#     'CountryRegionName': 'first',
#     'FullDate': 'first',
# }

for country in selected_countries_line:
    data = filtered_df_line[filtered_df_line["CountryRegionName"] == country]
    line_fig = px.line(
        data,
        x="FullDate",
        y=selected_attribute_line,
        color="StateProvinceName",
        title=f"{selected_attribute_line} by Date for Year {selected_year_line} in {country}",
        labels={"FullDate": "Date", selected_attribute_line: selected_attribute_line},
        height=600,  # Adjust height as needed
    )

    # Update layout
    line_fig.update_layout(
        xaxis_title="Date",
        yaxis_title=selected_attribute_line,
        showlegend=True,  # Hide legend to prevent clutter
    )

    st.plotly_chart(line_fig)