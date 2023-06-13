import re       #import regular expression
import streamlit as st #import streamlit.....
import pandas as pd
import altair as alt

def parse_log_data(log_data): #parse_log_data function is used to process log data and extract information from it. 
    pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' #\d: This is a special character in regular expressions that matches any digit (0-9). (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) is used to match an IP address format
                                                      

    log_entries = [] # to store the extracted log entries.
    for log in log_data: #goes through each iteams in the log data list and for each item  it assigns the item's value to the variable log so that it can be used within the loop.
        ipaddress = re.search(pattern, log)  #is a function call that searches for the specified pattern within the given text(in log)
        if ipaddress:
            split_entry = log.split() #is used to split the content in the file (log)into a list of substrings. 
            if len(split_entry) >= 12: #checks if the split_entry list is greater than or equal to 12
                ip = ipaddress.group() # is used to extract the matched IP address from the ipaddress object returned by the re.search() function.
                response_code = split_entry[8] # extracts the matched pattern from the ipaddress object and assigns it to the variable ip.
                date = split_entry[3][1:] #
                user_agent = ' '.join(split_entry[11:])
                log_entries.append([ip, response_code, date, user_agent])

    df = pd.DataFrame(log_entries, columns=['IP Address', 'Response Code', 'Date', 'User Agent'])
    return df

def plot_graph(df):
    status_ip_counts = df.groupby(['IP Address', 'Response Code']).size().reset_index(name='Count')

    chart = alt.Chart(status_ip_counts).mark_bar().encode(
        x='Count:Q',
        y=alt.Y('IP Address:O', sort='-x'),
        color='Response Code:N',
        tooltip=['IP Address', 'Response Code', 'Count']
    )

    st.subheader("IP Address and Response Code Distribution")#subheader which displays on streamlit web application
    st.altair_chart(chart, use_container_width=True) #used to display altair chart on streamlit

def main():
    st.title("Log Data Analyzer") #is used to display a title or heading on the Streamlit web application.
    accesslog = open("access.log", "r") # is used to open a file named "access.log" in read mode
    log_data = accesslog.readlines() #is used to read all the line from accesslog and helps to store them in a list of strings in log_data
    accesslog.close()

    log_df = parse_log_data(log_data) #used to process the data stored in log_data variable using the parse_log_data() function and assign the resulting DataFrame to the variable log_df.
   
    if log_df.empty: #checking if the DataFrame log_df is empty, meaning it does not contain any data.
        st.write("No log data found.")# used to display the message "No log data found." on the Streamlit web application.
    else:
        st.subheader("Access Log Data")#used to display on the streamlit web application
        st.dataframe(log_df)#used to display the DataFrame log_df in a tabular format on the Streamlit web application.

        plot_graph(log_df)#used to generate and display a graph based on the log data stored in the DataFrame log_df on the Streamlit web application.

if __name__ == "__main__": #used to check the python script is exected as the main prgm.
    main()
