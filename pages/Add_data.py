import streamlit as st 
import pandas as pd

st.set_page_config(
    page_title="Add Data",
    page_icon="🧬",
    layout="wide")

st.sidebar.success("What you would like to do?")

st.markdown("#### Please input the Study info")
st.write(":red[*Required]")

title = st.text_input("Title:red[*]")
diseaseFocus = st.text_input("Disease Focus:red[*]", placeholder="ex. Delirium")
doi = st.text_input("DOI", placeholder="ex. 10.1002/advs.202200559")
url = st.text_input("URL:red[*]", help="Preferably to the full text")
journal = st.text_input("Journal:red[*]", placeholder="ex. Wiley")
datePub = st.text_input("Date Published:red[*]", placeholder="ex. 2024-03-27")
contactName = st.text_input("Contact Full Name", placeholder="ex. Zhigang Wang")
contactEmail = st.text_input("Contact Email", placeholder="ex. drwangzg@hotmail.com")
study_cols = (title,diseaseFocus,doi,url,journal,datePub,contactName,contactEmail)


def submit_data(table, columns):
    sql_str = f"INSERT INTO {table} VALUES ({columns[0]}"
    for i in study_cols[1:]:
        if i != "":
            sql_str += f",{i}"
        else:
            sql_str += ",NULL"
    sql_str += ");"
    return(st.write(sql_str))


st.button("Submit", on_click=submit_data, args=("Study", study_cols))