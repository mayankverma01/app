
import re
import time
import pandas as pd
import numpy as np
from textblob import TextBlob
import streamlit as st
import numbers

import pybase64
from io import BytesIO
#_____________________________AP number_______________________________
def AP1(x):
    x=x.split()
    a='AP'
    b= 'PLAN'
    for i in x:
        if a ==i :
            return ' '.join(x[x.index(i)+1:])
            
        elif b ==i :
            return ' '.join(x[x.index(i)+1:])
        else:
            pass 
            
    return '-'

def AP2(x):
    x=x.split()
    if len(x)>0:
        if x[0]=='AP':
            y= x[1]
        else:
            y= x[0]
    else:
        y='-'
        
    if y.isdigit()==True:
        y=y
    else:
        y=''
    return y


#_____________________________MDDR number_______________________________
def len_6(x):
    y=x
    if len(y)==0:
        y=np.nan
    else:
        
        for i in y:
            if len(str(i))==6:
                y=int(i)
            else:
                y=np.nan
    return y

#_________________________________________________________________________
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output)#, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = pybase64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download excel file</a>' # decode b'abc' => abc
#_________________________________________________________________________

def main():
    
    html_temp = """
    <div style="background-color:lightgray;padding:10px">
    <h1 style="color:black;text-align:center;">MDDR Finding App </h2>
    </div>
    
    """
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
    st.markdown(html_temp,unsafe_allow_html=True)
#______________________________________________________________________________    
    st.subheader("SELECT Excel FILE that contain 'defect_description' and 'MDDR' col. ")
    uploaded_file = st.file_uploader("Choose a excel file", type=['csv','xlsx'])
    
    if uploaded_file:
        df1 = pd.read_csv(uploaded_file ,encoding='cp1252')
        
        
#_____________________________AP number_______________________________        
        
        df1['ACTION_PLAN_NO']=df1.DEFECT_DESCRIPTION.apply(lambda x: re.sub('[^a-z_A-Z_0-9]',' ',str(x)))
        df1['ACTION_PLAN_NO']=df1.ACTION_PLAN_NO.str.replace('  ',' ')
        df1['ACTION_PLAN_NO']=df1.ACTION_PLAN_NO.apply(AP1)
        df1['ACTION_PLAN_NO']=df1.ACTION_PLAN_NO.apply(AP2)

#_____________________________MDDR number_______________________________

        df=df1[['DEFECT_DESCRIPTION','MDDR']]
        df['MDDR']=np.round(df.MDDR,0)
        df.MDDR=df.MDDR.astype(pd.Int64Dtype())
        MDDR=list(df.MDDR.unique())
        MDDR=MDDR[1:len(MDDR)+1]

        df['defect_description_1']=df.DEFECT_DESCRIPTION.str.replace("[^0-9]", "")
        df['defect_description_1']=df.defect_description_1.str.split()
        df['defect_description_1']=df['defect_description_1'].apply(lambda x:len_6(x))
        df['defect_description_1']=np.round(df.defect_description_1,0)
        df.defect_description_1=df.defect_description_1.astype(pd.Int64Dtype())


        df2=df[['DEFECT_DESCRIPTION','MDDR']]
        df2=df2.drop_duplicates()
        df2=df2[df2.MDDR!='<NA>']

        df3=pd.merge(df,df2,how='left',left_on='defect_description_1',right_on='MDDR',suffixes=('_x', '_present'))
        df3=df3[['DEFECT_DESCRIPTION_present','MDDR_present']]
        df1=pd.concat((df1,df3),axis=1)
        st.markdown(get_table_download_link(df1), unsafe_allow_html=True)
    
   #___________________________________________________________________________________________     
if __name__=='__main__':
    main()
    