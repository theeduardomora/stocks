import psycopg2
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import logging
import os
import plotly.offline as pyo
import io



# def upload_file():
#   """Create a folder and prints the folder ID
#   Returns : Folder Id"""

#   scope = ['https://www.googleapis.com/auth/drive']
#   service_account_json_key = 'google_service_acc_key.json'
#   credentials = service_account.Credentials.from_service_account_file(
#                               filename=service_account_json_key, 
#                               scopes=scope)
#   try:
#     service = build('drive', 'v3', credentials=credentials)
#     media = MediaFileUpload(
#         "stocks_graph.html", mimetype="application/zip", resumable=True
#     )
#     # pylint: disable=maybe-no-member
#     file = (
#         service.files()
#         .update(fileId="1klK1dIYvscKzT9Wlz9K_1p14Dzz46J8X", media_body=media)
#         .execute()
#     )
#     print(f'File ID: "{file.get("id")}".')
#     return file.get("id")

#   except HttpError as error:
#     print(f"An error occurred: {error}")
#     return None


# Initialize figure with subplots
fig = make_subplots(
    rows=2, cols=3
)

index = 0
print("Connecting to the database...")
conn = psycopg2.connect(
    database="practice_stocks",
    user="theeduardomora",
    host="stocks-database.cykiacyw8qvr.us-east-1.rds.amazonaws.com",
    port='5432', 
    password="passwordpassword145"
)
print("Connected!")
cur = conn.cursor()

tables_arr = ["min_day_stocks", "min_month_stocks", "min_year_stocks", "max_day_stocks", 
"max_month_stocks", "max_year_stocks"]
go_objs_arr = []
tickers_arr = []

for table in tables_arr:
    sql_query = f"SELECT * FROM {table}"
    cur.execute(sql_query)
    df = pd.DataFrame(cur.fetchall(), columns=['stocks_ticker', 'stocks_price', 'stocks_date', 'stocks_time'])

    go_objs_arr.append(go.Scatter(
        x=df['stocks_time'],
        y=df['stocks_price'],
        mode='lines+markers',
        hoverinfo='x+y',  # Display both date and value on hover
        line=dict(color='rgba(0, 230, 24, 0.58)', width=2),
        marker=dict(color='rgba(41, 154, 47, 1)', size=8),
        name=f"{df['stocks_ticker'][0]}", 
        showlegend=False
    ))
    tickers_arr.append(df['stocks_ticker'][0])
print("Query executed successfully!")
cur.close()
conn.close()

fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=[f"{table}: {ticker}" for table, ticker in zip(tables_arr, tickers_arr)]
)

for i in range(len(tickers_arr)):
    fig.add_trace(go_objs_arr[i], row=((i // 3) + 1), col=((i % 3) + 1))
    # fig.update_xaxes()

fig.update_layout(title_text="S&P 500 Biggest Growers and Biggest Losers", title_x=0.5, title_y=0.95)
fig.show()

pyo.plot(fig, filename='stocks_graph.html', auto_open=False)

# upload_file()
