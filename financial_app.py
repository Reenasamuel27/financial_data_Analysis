import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# --- Database Connection and Data Retrieval ---
conn = sqlite3.connect("financial.db")  # Assuming financial.db is in the same directory

def get_data(query):
    df = pd.read_sql(query, conn)
    return df


# --- Page Configuration ---
st.set_page_config(
    page_title="Financial Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

# --- Sidebar ---
st.sidebar.header("Filters")


# --- Main Content ---
st.title("Financial Dashboard")


# --- Yearly Profit by Segment ---
st.header("Yearly Profit by Segment")
df_yearly_profit = get_data("SELECT Segment,Year,_Profit_,SUM(CAST(REPLACE(REPLACE(_Profit_,'$',''),',','') AS REAL)) AS yearly_profit FROM financial GROUP BY Segment,Year ORDER BY Year DESC")
df_yearly_profit['yearly_profit'] = df_yearly_profit['yearly_profit'].apply(lambda x: '${:.2f}'.format(x))

# Plotting Logic (same as before, but using st.pyplot)
years = ["2013", "2014"]  
segments = df_yearly_profit['Segment'].unique()

year_1 = []
year_2 = []
# ... (rest of the plotting logic remains the same)

fig, ax = plt.subplots(figsize=(10, 6))
# ... (rest of the plotting logic)
st.pyplot(fig)


# --- Other Charts ---
# Functions for chart generation
def create_bar_chart(df, x_col, y_col, title):
    fig, ax = plt.subplots()
    ax.bar(df[x_col], df[y_col])
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title)
    for i, value in enumerate(df[y_col]):
        plt.text(i, value, str(value), ha='center', va='bottom')
    st.pyplot(fig)

# ... (rest of the SQL queries)
df_highest_profit = get_data("SELECT Segment,_Profit_,SUM(CAST(REPLACE(REPLACE(_Profit_,'$',''),',','') AS REAL)) AS highest_profit FROM financial GROUP BY Segment ORDER BY _Profit_ DESC LIMIT 3")
df_highest_profit['highest_profit'] = df_highest_profit['highest_profit'].apply(lambda x: '${:.2f}'.format(x))

df_lowest_sales = get_data("SELECT Segment,__Sales_,SUM(CAST(REPLACE(REPLACE(__Sales_,'$',''),',','') AS REAL)) AS lowest_sales FROM financial GROUP BY Segment ORDER BY __Sales_  DESC LIMIT 2")
df_lowest_sales['lowest_sales'] = df_lowest_sales['lowest_sales'].apply(lambda x: '${:.2f}'.format(x))


df_highest_product = get_data("SELECT _Product_,_Profit_,SUM(CAST(REPLACE(REPLACE(_Profit_,'$',''),',','') AS REAL)) AS highest_product FROM financial GROUP BY _Product_ ORDER BY _Profit_ DESC LIMIT 2")
df_highest_product['highest_product'] = df_highest_product['highest_product'].apply(lambda x: '${:.2f}'.format(x))


# Displaying charts in Streamlit
create_bar_chart(df_highest_profit, 'Segment', 'highest_profit', 'Top 3 Segments by Profit')
create_bar_chart(df_lowest_sales, 'Segment', 'lowest_sales', 'Bottom 2 Segments by Sales')
create_bar_chart(df_highest_product, '_Product_', 'highest_product', 'Top 2 Products by Profit')

conn.close()

