import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo


#Repo.clone_from("https://github.com/PhonePe/pulse.git","/data")

# SETTING PAGE CONFIGURATIONS
icon = Image.open(r"images\ICN.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization and Exploration",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                   )

#creating connection with mysql
mysql_connection = sql.connect(host="localhost",
                user="jai",
                password="jai123",
                database= "phonepe_db",
                auth_plugin='mysql_native_password',
                charset='utf8mb4'
                )
mysql_cursor = mysql_connection.cursor()

with st.sidebar:
    selected = option_menu(None, ["Home","Data Visualization","Geo Visualization","Explore Data"], 
                icons=["house","pie-chart-fill","globe-americas","bar-chart-line"],
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
# MENU 1 - HOME
if selected == "Home":
   
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Domain :] Fintech")
        st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        image = Image.open(r"images\phone.png")
        st.image(image, caption='Phonepe pulse THE BEAT OF PROGRESS', use_column_width=True)
#Data visualization
if selected == "Data Visualization":
    st.markdown("## :violet[Data Visualization]")
    column1,column2,column3= st.columns(3)
    with column1:
        st.header("Type")
        Type=st.selectbox(
            "Select the Type",
            ("Transaction","Users"),
        )
    with column2:
        st.header("Year")
        Year=st.selectbox(
          "Select the year",
            ("2018","2019","2020","2021","2022","2023"), 
        )
    with column3:
        st.header("Quarter")
        Quarter=st.selectbox(
          "Select the quarter",
            ("1","2","3","4"), 
        )
#Data visualization - TRANSACTIONS     
    if  Type == "Transaction":
        tab1,tab2,tab3=st.tabs(["State Analysis","District Analysis","Pincode Analysis"])
        #col1,col2,col3 = st.columns([1,1,1],gap="small")
            
        with tab1:
                st.markdown("### :violet[State wise data]")
                mysql_cursor.execute(f"select state,year, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state,year order by Total desc limit 10")
                df = pd.DataFrame(mysql_cursor.fetchall(), columns=['State', 'Year','Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                                names='State',
                                title='Top 10 State',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)        

        with tab2:
            st.markdown("### :violet[District wise data]")
            mysql_cursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame( mysql_cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10 District',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with tab3:
            st.markdown("### :violet[Pincode wise data]")
            mysql_cursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame( mysql_cursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                                names='Pincode',
                                title='Top 10 Pincode',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
#Data visualization- USERS          
    if Type == "Users":
        tab1,tab2,tab3,tab4=st.tabs(["Brand Analysis","District Analysis","Pincode Analysis","State Analysis"])
        #col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with tab1:
            st.markdown("### :violet[Brands]")
            if Year == 2023 and Quarter in [3,4]:
                st.markdown("### :Sorry No Data to Display for 2023 Qtr 3,4")
            else:
                mysql_cursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame( mysql_cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10 Brands',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with tab2:
            st.markdown("### :violet[District wise data]")
            mysql_cursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame( mysql_cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10 District',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
              
        with tab3:
            st.markdown("### :violet[Pincode wise data]")
            mysql_cursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame( mysql_cursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10 Pincode',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with tab4:
            st.markdown("### :violet[State wise data]")
            mysql_cursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame( mysql_cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10 State',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

# Geo Visualization

if selected== "Geo Visualization":
    #st.markdown("## :violet[Geo Visualization]")
    column1,column2,column3= st.columns(3)
    with column1:
        st.header("Type")
        Type=st.selectbox(
            "Select the Type",
            ("Transaction","Users"),
        )
    with column2:
        st.header("Year")
        Year=st.selectbox(
          "Select the year",
            ("2018","2019","2020","2021","2022","2023"), 
        )
    with column3:
        st.header("Quarter")
        Quarter=st.selectbox(
          "Select the quarter",
            ("1","2","3","4"), 
        )

   
#Maps
    if Type == "Transaction":
        col1,col2=st.columns(2)
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mysql_cursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mysql_cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r'C:\Users\GVJai\OneDrive\Desktop\Project\PhonePe\Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mysql_cursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mysql_cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r'C:\Users\GVJai\OneDrive\Desktop\Project\PhonePe\Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)

    if Type == "Users":   
            # Overall State Data - TOTAL APPOPENS - INDIA MAP
            st.markdown("## :violet[Overall State Data - User App opening frequency]")
            mysql_cursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mysql_cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            df2 = pd.read_csv(r'C:\Users\GVJai\OneDrive\Desktop\Project\PhonePe\Statenames.csv')
            df1.Total_Appopens = df1.Total_Appopens.astype(float)
            df1.State = df2
            
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Appopens',
                    color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
#Explore data
if selected== "Explore Data":
    st.markdown("## :violet[Explore Data]")
    column1,column2,column3= st.columns(3)
    with column1:
        st.header("Type")
        Type=st.selectbox(
            "Select the Type",
            ("Transaction","Users"),
        )
    with column2:
        st.header("Year")
        Year=st.selectbox(
          "Select the year",
            ("2018","2019","2020","2021","2022","2023"), 
        )
    with column3:
        st.header("Quarter")
        Quarter=st.selectbox(
          "Select the quarter",
            ("1","2","3","4"), 
        )
#EXPLORE DATA - TRANSACTIONS
    if Type == "Transaction":

    # BAR CHART - TOP PAYMENT TYPE
            st.markdown("## :violet[Top Payment Type]")
            mysql_cursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

            fig = px.bar(df,
                        title='Transaction Types vs Total_Transactions',
                        x="Transaction_type",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=False)
            
    # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("## :violet[Select any State to explore more]")
            selected_state = st.selectbox("",
                                ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
            
            mysql_cursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
            
            df1 = pd.DataFrame(mysql_cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                            'Total_Transactions','Total_amount'])
            fig = px.bar(df1,
                        title=selected_state,
                        x="District",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
    # EXPLORE DATA - USERS      
    if Type == "Users":
            # BAR CHART TOTAL USERS - DISTRICT WISE DATA 
            st.markdown("## :violet[Select any State to explore more]")
            selected_state = st.selectbox("",
                                ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
            
            mysql_cursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
            
            df = pd.DataFrame(mysql_cursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(int)
            
            fig = px.bar(df,
                        title=selected_state,
                        x="District",
                        y="Total_Users",
                        orientation='v',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

        
    
