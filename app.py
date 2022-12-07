import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

from streamlit_pandas_profiling import st_profile_report
import streamlit.components.v1 as components

from pandas_profiling import ProfileReport
import sweetviz as sv
import codecs

# -------------- General body --------------
st. set_page_config(layout="wide")

# Title and subtitle
st.title("Palmer's Penguins")
st.markdown("Use this Streamlit app to make your own scatterplot about penguins!")

# Caching for file
penguin_file = st.file_uploader("Select Your Local Penguins CSV")
@st.cache()
def load_file(penguin_file):
    if penguin_file is not None:
        penguins_df = pd.read_csv(penguin_file)
    else:
        st.stop()
    return(penguins_df)
penguins_df = load_file(penguin_file)

# Set multiple tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Scatter Plot", "Bar Plot", "Pair Plot", "Correlation Graph", "Data Exploration"])

#-----------------------------------

with tab1:
    # User input for graph title
    graph_titleTab1 = st.text_input(label='Graph Title', key = 'tab1')

    # User selection for X and Y Axis labels
    selected_x_var = st.selectbox("Select X variable:", penguins_df.columns, key= "tab1.1",)
    selected_y_var = st.selectbox("Select Y variable:", penguins_df.columns, key= "tab1.2",)
    if st.checkbox("Enable Hue as option:", key= "tab1.3"):
        selected_hue = st.selectbox("Select Hue:", penguins_df.columns, key= "tab1.4",)

    if st.button(label = "Visualize now", key = "tab1.5"):
        # Chart options
        fig, ax = plt.subplots()
        ax = sns.scatterplot(x = penguins_df[selected_x_var], y = penguins_df[selected_y_var], hue = penguins_df[selected_hue])
        plt.xlabel(selected_x_var)
        plt.ylabel(selected_y_var)
        plt.title(graph_titleTab1)
        st.pyplot(fig)

        # Download chart
        fn = 'scatter.png'
        img = io.BytesIO()
        plt.savefig(img, format='png')
            
        btn = st.download_button(
        label="Download chart",
        data=img,
        file_name=fn,
        mime="image/png"
        )

with tab2:
    # User input for graph title
    graph_titleTab2 = st.text_input(label='Graph Title', key = 'tab2')

    # User selection for X and Y Axis labels
    selected_x_var = st.selectbox("Select X variable:", penguins_df.columns, key= "tab2.1",)
    selected_y_var = st.selectbox("Select Y variable:", penguins_df.columns, key= "tab2.2",)
    if st.checkbox("Enable Hue as option:", key= "tab2.3"):
        selected_hue = st.selectbox("Select Hue:", penguins_df.columns, key= "tab2.4",)

    if st.button(label = "Visualize now", key = "tab2.5"):
        # Chart options
        fig, ax = plt.subplots()
        ax = sns.barplot(x = penguins_df[selected_x_var], y = penguins_df[selected_y_var], hue = penguins_df[selected_hue])
        plt.xlabel(selected_x_var)
        plt.ylabel(selected_y_var)
        plt.title(graph_titleTab2)
        st.pyplot(fig)

        # Download chart
        fn = 'Bar.png'
        img = io.BytesIO()
        plt.savefig(img, format='png')
            
        btn = st.download_button(
        label="Download chart",
        data=img,
        file_name=fn,
        mime="image/png"
        )

with tab3:
    # User input for graph title
    if st.checkbox("Enable Hue as option:", key= "tab3.1"):
        selected_hue = st.selectbox("Select Hue:", penguins_df.columns, key= "tab3.2",)

    if st.button(label = "Visualize now", key = "tab3.3"):
        # Chart options
        fig = sns.pairplot(penguins_df)
        st.pyplot(fig)

        # Download chart
        fn = 'Pairplot.png'
        img = io.BytesIO()
        plt.savefig(img, format='png')
            
        btn = st.download_button(
        label="Download chart",
        data=img,
        file_name=fn,
        mime="image/png"
        )

with tab4:
    if st.button(label = "Visualize now", key = "tab4.1"):
    # Chart options
        fig, ax = plt.subplots()
        sns.heatmap(penguins_df.corr(), ax=ax)
        st.write(fig)

def st_display_sweetviz(report_html,width=1000,height=500):
	report_file = codecs.open(report_html,'r')
	page = report_file.read()
	components.html(page,width=width,height=height,scrolling=True)

with tab5:
    # Show dataset
    if st.checkbox("Show Dataset"):
        number = int(st.number_input("Number of rows to view", None, None, 5))
        st.dataframe(penguins_df.head(number))

    # show columns
    if st.checkbox("View Column Names"):
        st.write(penguins_df.columns)

    # show shapes
    if st.checkbox("Show Shape of the dataset"):
        st.write(penguins_df.shape)
        dataDim = st.radio("Show Dimension by ", ("Rows", "Columns"))
        if dataDim == 'Rows':
            st.text("Number of Rows")
            st.write(penguins_df.shape[0])
        elif dataDim == 'Columns':
            st.text("Number of Rows")
            st.write(penguins_df.shape[1])
        else:
            st.write(penguins_df.shape)

    # show datatypes
    if st.checkbox("Data Types"):
        st.write(penguins_df.dtypes)

   # show summary
    if st.checkbox("Summary"):
        st.write(penguins_df.describe().T)

    if st.checkbox("Generate report with Pandas Profiling"):
        if penguin_file is not None:
            # df = pd.read_csv(penguin_file)
            # st.dataframe(penguins_df.head())
            profile = ProfileReport(penguins_df)
            st_profile_report(profile)
            export=profile.to_html()
            st.download_button(label="Download Full Report", data=export, file_name='Pandas_report.html')

    if st.checkbox("Generate report with Sweetviz"):
        if penguin_file is not None:
            # df = pd.read_csv(penguin_file)
            # st.dataframe(penguins_df.head())
            report = sv.analyze(penguins_df)
            report.show_html()
            # st_display_sweetviz("SWEETVIZ_REPORT.html")

