import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns #if it is yellow, you need to manually install in the terminal
import streamlit as st
import pandas as pd
import numpy as np

from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.set_page_config(
    page_title="California - Real Estate Agency 🏡",
    layout="centered",
    page_icon="🏡"
)

st.image("house2.jpg")

st.write("  ")
st.write("  ")
st.write("  ")
df = pd.read_csv("housing.csv")


## Step 01-Introduction
st.sidebar.title("California - Real Estate Agency 🏡")
page = st.sidebar.selectbox("Select Page", ["Introduction 📘", "Data Visualization 📊", "Automated Report 📑"])

## Step 02-Load Dataset
if page == "Introduction 📘":
    st.subheader("01 Introduction 📘")

    st.markdown("#### Data Preview")
    rows = st.slider("Select a number of rows to display", 5,20,5) 
#users can selection the number from 5 to 20 every 5 rows Displayed ???
    st.dataframe(df.head(rows))

    st.markdown("#### Missing values")
    missing = df.isnull().sum() #可以在Collab里跑一下，.insnull()是给一个表格-表格里面是False True 代表这个数据是否缺失
    st.write(missing)

    if missing.sum() == 0:
        st.success("✅ No missing values found")
    else:
        st.warning("⚠️ You have missing values")


    st.markdown("#### 📈 Summary Statistics")
    if st.button("Show Describe Table"):
        st.dataframe(df.describe())

elif page == "Data Visualization 📊":
    ## Step 03-Data viz
    st.subheader("02 Data Visualization 📊")

    col_x = st.selectbox("Select X-axis variable", df.columns, index=0)
    col_y = st.selectbox("Select Y-axis variable", df.columns, index=1)

    tab1, tab2, tab3 = st.tabs(["Bar Chart 📊", "Line Chart 📈", "Correlation Hearmap 🔥"])

    with tab1:
        st.subheader("Bar Chart")
        st.bar_chart(df[[col_x, col_y]].sort_values(by=col_x), use_container_width=True)

    with tab2:
        st.subheader("Line Chart")
        st.bar_chart(df[[col_x, col_y]].sort_values(by=col_x), use_container_width=True)

    with tab3:
        st.subheader("Correlation Matrix")
        df_numeric = df.select_dtypes(include=np.number) #select only numberic variables
        
        ## start with creating the empty frame that receives the plot
        fig_corr, ax_corr = plt.subplots(figsize=(18,14))
        ## create the plot, in this case with seaborn 
        sns.heatmap(df_numeric.corr(),annot=True,fmt=".2f",cmap='coolwarm')
        ## render the plot in streamlit 
        st.pyplot(fig_corr)

elif page == "Automated Report 📑":
    st.subheader("03 Automated Report 📑")
    if st.button("Generating report..."):
        with st.spinner("Generating report..."):
            profile = ProfileReport(df,title="california Housing Report",explorative=True,minimal=True)
            st_profile_report(profile)
        
        export = profile.to_html()
        st.download_button(label="📥 Download full Report",data=export,file_name="california_housing_report.html",mime='text/html')
        