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


def getStudy():
    title = st.text_input("What is the title of this Study?:red[*]", 
                        placeholder="E4BP4 Coordinates Circadian Control of Cognition in Delirium")
    diseaseFocus = st.text_input("What disease is it focused on?:red[*]", placeholder="Delirium")
    diseaseFocus = diseaseFocus.title()
    doi = st.text_input("What is the DOI of this study?", placeholder="10.1002/advs.202200559")
    url = st.text_input("Please provide this link to this study:red[*]", help="Preferably to the full text", 
                        placeholder="https://onlinelibrary.wiley.com/doi/10.1002/advs.202200559")
    journal = st.text_input("What journal was it published in?:red[*]", placeholder="Wiley")
    datePub = st.date_input("When was it published?:red[*]", value=None, 
                            min_value=date(2000,1,1), max_value=date.today())
    if datePub == None:
        datePub = ""
    else:
        datePub = str(datePub)
    contactName = st.text_input("Who is the primary contact for this study?", 
                                placeholder="John Smith",
                                help="Please provide if data is not publicly available.")
    contactEmail = st.text_input("Please provide this person's email", 
                                 placeholder="example@gmail.com")
    study_cols = (title,diseaseFocus,doi,url,journal,datePub,contactName,contactEmail)
    req_study_cols = (title,diseaseFocus,url,journal,datePub)
    return study_cols, req_study_cols

def getMice(key):
    age = st.text_input("What age (or age range) are the mice?:red[*]", placeholder="6-8 weeks old", 
                        key=f"age{key}")
    strain = st.text_input("What strain of mice are they?:red[*]", placeholder="Wild type C57BL/6J",
                           key=f"strain{key}")
    sex = st.selectbox("What is their sex?:red[*]", ("Male", "Female", "Both", "Unknown"), None, 
                       key=f"sex{key}")
    if sex == None:
        sex = ""
    origin = st.text_input("Where were the mice obtained from?:red[*]",
                           placeholder="HFK Biotechnology (Beijing, China)", key=f"origin{key}")
    conditions = st.text_input("What conditions were they under?",
                               placeholder="Specific pathogen-free facility under a 12 h light/dark "
                               "cycle with free access to water and food", key=f"conditions{key}")
    mice_cols = (age, strain, sex, origin, conditions)
    req_mice_cols = (age, strain, sex, origin)
    return mice_cols, req_mice_cols

def getSeq(key):
    st.write("\n")
    seq_method = st.checkbox("Was scRNA-seq the method used for sequencing?:red[*]", value = True, 
                               key=f"seq_method{key}")
    if seq_method == True:
        seq_method = "scRNA-seq"
    else:
        seq_method = ""
        st.write("Sorry, all experiments added into this database should be scRNA experiments")
    st.write("\n")
    dataAvail = st.selectbox("Is the Data publicly available?:red[*]", ("Yes", "No"), index=None, 
                             key=f"dataAvail{key}")
    if dataAvail == None:
        dataAvail = ""
    else:
        if dataAvail == "Yes":
            dataAvail = '1'
        else:
            dataAvail = '0'
    exp_groups = st.text_input("Breifly describe the experimental groups:red[*]", 
                            placeholder="Four E4bp4−/− mice and four control mice", key=f"exp_groups{key}")
    prep = st.text_input("Which library preparation protocol was used?:red[*]", 
                        placeholder="Bioanalyzer 2100 RNA 6000 Nano Kit, 10x Genomics "
                        "(Chromium Single Cell Controller)", key=f"prep{key}")
    platform = st.text_input("What platform did the sequencing?:red[*]", placeholder="Illumina NovaSeq 6000", 
                             key=f"platform{key}")
    align_soft = st.text_input("Which alignment software was used?", 
                            placeholder="HISAT2 v2.0.4 (GRCm38/mm10 genome) with default parameters", 
                            key=f"align_soft{key}")
    data_process_soft = st.text_input("What data processing software was used?:red[*]", 
                                    placeholder="Ballgown software, Cuffdiff v2.0.1 with default parameters", 
                                    key=f"data_process_soft{key}")
    seq_cols = (dataAvail,seq_method,exp_groups,prep,platform,align_soft,data_process_soft)
    req_seq_cols = (dataAvail,seq_method,exp_groups,prep,platform,data_process_soft)
    return seq_cols, req_seq_cols

def getData(key):
    description = st.text_input("How was this data used in the study?:red[*]",
                                placeholder="Additional public data used to enrich murine dendritic "
                                "cells subset using Seurat",
                                key=f"description{key}")
    dbname = st.text_input("In what database can this data be found?:red[*]",
                           placeholder="GEO", key=f"dbname{key}")
    accNum = st.text_input("What is the accession number?", placeholder="GSE151658", key=f"accNum{key}")
    url = st.text_input("Please provide the URL to the data:red[*]",
                        placeholder="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE151658",
                        key=f"url{key}")
    data_cols = (description, dbname, accNum, url)
    req_data_cols = (description, dbname, url)
    return data_cols, req_data_cols

def getIntervention(key):
    treatment = st.text_input("What treatment were the mice given?:red[*]", 
                              placeholder="Induced polymicrobial sepsis", key=f"treatment{key}")
    method = st.text_input("What method was used to give this treatment?:red[*]", 
                           placeholder="Cecal ligation and puncture (CLP)", key=f"method{key}")
    intervention_cols = (treatment, method)
    req_intervention_cols = (treatment, method)
    return intervention_cols, req_intervention_cols


st.markdown("#### First, we'll need the Study info:")
st.write(":red[*Required]")
study_cols, req_study_cols = getStudy()

st.divider()

st.markdown("#### Next, some info about each group of Mice used:")
st.write(":red[*Required]")
mice = st.number_input("How many groups of Mice were obtained for this study?:red[*]", min_value=1, 
                       value=None, placeholder="Type a number...")
st.write("\n")
mice_groups = []
if mice != None:
    for i in range(1,mice+1):
        st.markdown(f"##### Group {i}:")
        mice_cols, req_mice_cols = getMice(i)
        mice_groups.append((mice_cols,req_mice_cols))
        st.write("\n")

st.divider()

st.markdown("#### Now, we'll need to know about each instance of Sequencing done and/or used:")
st.write(":red[*Required]")
seq = st.number_input("How many unique sequencing sets were used for this study?:red[*]", min_value=1,
                      value=None, placeholder="Type a number...")
st.write("\n")
seq_groups = []
data_groups = {}
if seq != None:
    for i in range(1,seq+1):
        st.markdown(f"##### Sequence set {i}:")
        seq_cols, req_seq_cols = getSeq(i)
        seq_groups.append((seq_cols, req_seq_cols))
        if seq_cols[0] == '1':
            st.markdown("##### About this Data you said was public...")
            data = st.number_input("How many datasets came from this sequencing?:red[*]", min_value=1,
                                value=None, placeholder="Type a number...", key=f"data{i}")
            if data != None:
                for j in range(1,data+1):
                    st.markdown(f"##### Dataset {j}:")
                    data_cols, req_data_cols = getData(str(i)+str(j))
                    if j == 1:
                        data_groups[i] = [(data_cols, req_data_cols)]
                    else:
                        data_groups[i] += [(data_cols, req_data_cols)]
            else:
                data_groups[i] = [(("",""),("",""))]
        st.write("\n")

all_answers = {"Study" : [(study_cols, req_study_cols)], "Mice" : mice_groups, "Sequencing": seq_groups}


if(any(i[0][0] == '1' for i in seq_groups)):
    all_answers["DataRepository"] = data_groups

st.divider()

st.markdown("#### Lastly, we'll need to know about any treatment the mice received")
st.write(":red[*Required]")
treated = st.selectbox("Were these Mice given any treatment?:red[*]", ("No", "Yes"), index=None)
treatment_groups = []
if treated == 'Yes':
    treatments = st.number_input("How many treatments were implemented in this study?", min_value=1,
                                 value=None, placeholder="Type a number...")
    st.write("\n")
    if treatments != None:
        for i in range(1,treatments+1):
            st.markdown(f"##### Treatment {i}:")
            intervention_cols, req_intervention_cols = getIntervention(i)
            treatment_groups.append((intervention_cols, req_intervention_cols))
            st.write("\n")
    all_answers["Intervention"] = treatment_groups
elif treated == None:
    all_answers["Intervention"] = treatment_groups




def check_req(group):
    if group != [] and group != {}:
        all_entries = []
        if isinstance(group, dict):
            for i in group.values():
                for j in i:
                    all_entries.append(all(len(k) != 0 for k in j[1]))
        else:
            for i in group:
                all_entries.append(all(len(j) != 0 for j in i[1]))
        valid = all(all_entries)
    else:
        valid = False
    return valid


all_valid = []
for i in all_answers.values():
    all_valid.append(check_req(i))


def submit_data(ans):

    study_str = "INSERT INTO Study VALUES (NULL"
    for i in ans['Study'][0][0]:
        if i == '':
            study_str += ",NULL"
        else:
            study_str += f",'{i}'"
    study_str += ");"
    sql_code.write(study_str)
    with conn.session as session:
        session.execute(text("ALTER TABLE Study AUTO_INCREMENT = 0;"))
        session.execute(text("ALTER TABLE Mice AUTO_INCREMENT = 0;"))
        session.execute(text("ALTER TABLE Sequencing AUTO_INCREMENT = 0;"))
        session.execute(text("ALTER TABLE DataRepository AUTO_INCREMENT = 0;"))
        session.execute(text("ALTER TABLE Intervention AUTO_INCREMENT = 0;"))
        session.commit()
        session.execute(text(study_str))
        session.commit()

    study_id = conn.query("SELECT LAST_INSERT_ID();", ttl=0)
    #print(study_id)
    study_id = study_id[study_id.columns[0]][0]
    
    for i in ans['Mice']:
        mice_str = f"INSERT INTO Mice VALUES (NULL,{study_id}"
        for j in i[0]:
            if j == '':
                mice_str += ",NULL"
            else:
                mice_str += f",'{j}'"
        mice_str += ");"
        sql_code.write(mice_str)
        with conn.session as session:
            session.execute(text(mice_str))
            session.commit()
    
    count = 1
    for i in ans['Sequencing']:
        seq_str = f"INSERT INTO Sequencing VALUES (NULL,{study_id}"
        for j in i[0]:
            if j == '':
                seq_str += ",NULL"
            else:
                seq_str += f",'{j}'"
        seq_str += ");"
        sql_code.write(seq_str)
        with conn.session as session:
            session.execute(text(seq_str))
            session.commit()
        seq_id = conn.query("SELECT LAST_INSERT_ID();", ttl=0)
        #print(seq_id)
        seq_id = seq_id[seq_id.columns[0]][0]

        if i[0][0] == '1':
            for j in ans['DataRepository'][count]:
                data_str = f"INSERT INTO DataRepository VALUES (NULL,{seq_id}"
                for k in j[0]:
                    if k == '':
                        data_str += ",NULL"
                    else:
                        data_str += f",'{k}'"
                data_str += ");"
                sql_code.write(data_str)
                with conn.session as session:
                    session.execute(text(data_str))
                    session.commit()
        count += 1
    
    if ans["Intervention"] != None:
        for i in ans['Intervention']:
            inter_str = f"INSERT INTO Intervention VALUES (NULL,{study_id}"
            for j in i[0]:
                if j == '':
                    inter_str += ",NULL"
                else:
                    inter_str += f",'{j}'"
            inter_str += ");"
            sql_code.write(inter_str)
            with conn.session as session:
                session.execute(text(inter_str))
                session.commit()



submit_placeholder = st.empty()
pressed = submit_placeholder.button("Submit")

#print("\n")
#print(all_answers)

if pressed == False:
    st.info("Please press the submit button after filling out all required fields")
elif all(all_valid):
    submit_placeholder.empty()
    st.success("Success!")
    sql_code = st.expander(":green[Show SQL code]")
    if 'DataRepository' not in all_answers:
        all_answers['DataRepository'] = None
    if 'Intervention' not in all_answers:
        all_answers['Intervention'] = None
    submit_data(all_answers)
else:
    st.error('Please fill out all required fields')

