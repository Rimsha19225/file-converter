import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# Fix: Use `type` instead of `types`
files = st.file_uploader("Upload CSV and Excel files", type=[
                         "csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Removes Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed")
            st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df = df.fillna(df.select_dtypes(
                include={"number"}).mean(), inplace=True)
            st.success("Missing Values filled with mean")
            st.dataframe(df.head())

        selected_columns = st.multiselect(
            f"Select Cloumns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", [
                                 "csv", "Excel"], key=file.name)

        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mine = "text/csv"
                new_namme = file.name.replace(ext, "csv")

            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mine = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_namme = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("Download file", file_name=new_namme, data=output, mime=mine)

            st.success("Processing Complete!")
