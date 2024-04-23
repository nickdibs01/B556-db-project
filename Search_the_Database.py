import streamlit as st 
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Database Search",
    page_icon="🧬",
    layout="wide")

st.sidebar.success("What you would like to do?")

st.title("Delirium and Sepsis in Transgenic Mice Database")

# Initialize connection.
conn = st.connection('mysql', type='sql')
conn.reset()

col1, col2 = st.columns([1,1])
with col1:
    disease_filter = st.multiselect("Disease Focus", 
                                    options = conn.query("SELECT DISTINCT DiseaseFocus FROM Study;", ttl=1), 
                                    default=None)
with col2:
    start_date, end_date = st.slider("Date Published", min_value=2000, max_value=date.today().year, 
                            value=(2015,2023))

select1 = ("SELECT * FROM Study WHERE ")

if disease_filter != []:
    for i in range(len(disease_filter)):
        if i == 0:
            select1 += f"(DiseaseFocus='{disease_filter[i]}'"
        else:
            select1 += f" OR DiseaseFocus='{disease_filter[i]}'"
    select1 += f") AND DatePub BETWEEN '{start_date}-01-01' AND '{end_date}-12-31';"
else:
    select1 += f"DatePub BETWEEN '{start_date}-01-01' AND '{end_date}-12-31';"

study_df = conn.query(select1, ttl=1)
if study_df.empty == True:
    st.write("There were no studies that match your search :slightly_frowning_face:")
else:
    st.write("Studies that match your search:")
    st.dataframe(study_df, hide_index=True, 
                 column_config={"URL": st.column_config.LinkColumn("URL")})

st.divider()


table_name = st.selectbox('Additional Study information', options=["Intervention", "Mice", "Sequencing"], index=2)

IDs = study_df[study_df.columns[0]]


filter = st.toggle("Use above filters")

pkeys = {"Intervention":"TreatmentID",
         "Mice":"MouseID"}

if filter == False:
    if table_name == "Sequencing":
        seq_df = conn.query("SELECT * FROM Sequencing;", ttl=1)
        seq_df["DataAvailable"] = seq_df["DataAvailable"].map({0: False, 1: True})
        st.dataframe(seq_df, hide_index=True)
    else:
        st.dataframe(conn.query(f"Select * FROM {table_name};", ttl=1).drop(pkeys[table_name], axis=1), 
                     hide_index=True)
elif len(IDs) == 0:
    st.write("Your search returned no results :slightly_frowning_face:")
else:
    select2 = f"SELECT * FROM {table_name} WHERE"
    first = True
    for i in IDs:
        if first == True:
            select2 += f" StudyID={i}"
            first = False
        else:
            select2 += f" OR StudyID={i}"
    select2 += ";"
    if table_name == "Sequencing":
        seq_df = conn.query(select2, ttl=1)
        seq_df["DataAvailable"] = seq_df["DataAvailable"].map({0: False, 1: True})
        st.dataframe(seq_df, hide_index=True)
    else:
        st.dataframe(conn.query(select2, ttl=1).drop(pkeys[table_name], axis=1), hide_index=True)


if table_name == "Sequencing" and len(IDs) != 0 and filter == True:
    st.write("Sequence Data")
    select3 = ("SELECT s.SequenceID,DataDescription,DatabaseName,AccessionNumber,URL FROM "
               "DataRepository AS dr JOIN Sequencing AS s ON dr.SequenceID=s.SequenceID WHERE ")
    first = True
    for i in IDs:
        if first == True:
            select3 += f" StudyID={i}"
            first = False
        else:
            select3 += f" OR StudyID={i}"
    select3 += ";"
    data_rep_df = conn.query(select3, ttl=1)
    if data_rep_df.empty:
        st.write("There are no available datasets for any of these sequences :slightly_frowning_face:")
    else:
        st.dataframe(data_rep_df, hide_index=True, column_config={"URL": st.column_config.LinkColumn("URL")})
elif table_name == "Sequencing" and filter == False:
    st.write("Sequence Data")
    st.dataframe(conn.query("SELECT SequenceID,DataDescription,DatabaseName,AccessionNumber,URL FROM DataRepository",
                            ttl=1), 
                 hide_index=True, column_config={"URL": st.column_config.LinkColumn("URL")})


