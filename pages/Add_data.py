import streamlit as st 
import pandas as pd
from sqlalchemy.sql import text
from datetime import date

st.set_page_config(
    page_title="Add Data",
    page_icon="🧬",
    layout="wide")

# Initialize connection.
conn = st.connection('mysql', type='sql')
conn.reset()

st.sidebar.success("What you would like to do?")

st.markdown("#### First, we'll need the Study info:")
st.write(":red[*Required]")

title = st.text_input("Title:red[*]", 
                      placeholder="E4BP4 Coordinates Circadian Control of Cognition in Delirium")
diseaseFocus = st.text_input("Disease Focus:red[*]", placeholder="Delirium")
doi = st.text_input("DOI", placeholder="10.1002/advs.202200559")
url = st.text_input("URL:red[*]", help="Preferably to the full text", 
                    placeholder="https://onlinelibrary.wiley.com/doi/10.1002/advs.202200559")
journal = st.text_input("Journal:red[*]", placeholder="Wiley")
datePub = st.date_input("Date Published:red[*]", value=None, 
                        min_value=date(2000,1,1), max_value=date.today())
if datePub == None:
    datePub = ""
else:
    datePub = str(datePub)
contactName = st.text_input("Contact Full Name", placeholder="John Smith",
                            help="The main contact for this study. Please provide if data is not publicly available.")
contactEmail = st.text_input("Contact Email", placeholder="example@gmail.com")
study_cols = (title,diseaseFocus,doi,url,journal,datePub,contactName,contactEmail)
req_study_cols = (title,diseaseFocus,url,journal,datePub)

def submit_data(table, columns):
    if table == "Study":
        sql_str = f"INSERT INTO {table} VALUES (NULL,'{columns[0]}'"
        ######################################################################
    for i in columns[1:]:
        if i != "":
            sql_str += f",'{i}'"
        else:
            sql_str += ",NULL"
    sql_str += ");"
    print(sql_str)
    with conn.session as session:
        session.execute(text(sql_str))
        session.commit()

def check_req(table, req_cols, all_columns):
    if all(len(i) != 0 for i in req_cols):
        submit_data(table, all_columns)
        return True
    else:
        return False


st.write("\n")

pressed = st.button("Submit")


if pressed == False:
    st.write("\n")
elif check_req("Study", req_study_cols, study_cols):
    st.write("Success!")
else:
    st.write(":red[Please fill out all required fields]")



st.divider()

st.markdown("#### Next, some info about the sequencing:")
st.write(":red[*Required]")


dataAvail = st.selectbox("Is the Data publicly available?:red[*]", ("Yes", "No"), index=None)
if dataAvail == None:
    dataAvail = ""
else:
    if dataAvail == "Yes":
        dataAvail = 1
    else:
        dataAvail = 0
method = st.text_input("Method:red[*]", placeholder="scRNA-seq")
exp_groups = st.text_input("Experimental Groups:red[*]", 
                           placeholder="Four E4bp4−/− mice and four control mice")
prep = st.text_input("Library Prep Protocol:red[*]", 
                     placeholder="Bioanalyzer 2100 RNA 6000 Nano Kit, 10x Genomics (Chromium Single Cell Controller)")
platform = st.text_input("Platform:red[*]", placeholder="Illumina NovaSeq 6000")
align_soft = st.text_input("Alignment Software", 
                           placeholder="HISAT2 v2.0.4 (GRCm38/mm10 genome) with default parameters")
data_process_soft = st.text_input("Data Processing Software:red[*]", 
                                  placeholder="Ballgown software, Cuffdiff v2.0.1 with default parameters")
seq_cols = (dataAvail,method,exp_groups,prep,platform,align_soft,data_process_soft)
req_seq_cols = (dataAvail,method,exp_groups,prep,platform,data_process_soft)

st.write("\n")
st.write("Submit button coming soon :)")