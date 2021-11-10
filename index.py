import pandas as pd

# from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import dash
import dash_html_components as html

import dash_bootstrap_components as dbc


# # get weblinks for scraper
# def scrape_weblinks():
#     from datetime import date

#     start_date = '04/28/2013'

#     def allsundays(start):
#         return pd.date_range(start=start, end=date.today(),
#                              freq='W-SUN').strftime('%Y/%m/%d').tolist()

#     date_list = allsundays(start_date)

#     for i in date_list:
#         print('https://coinmarketcap.com/historical/' + i.replace('/', '') + '/')


# # scrape_weblinks()

external_stylesheets = [dbc.themes.CERULEAN]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# df = pd.read_csv('coin_rankings.csv')
df = pd.read_csv('coin_rankings_fulldata.csv', parse_dates=['Date'])
name_dict = pd.read_csv('ticker_name.csv')

df = pd.merge(df, name_dict, how="left", on='label')

# print(df); quit()



stablecoins = ['USDTTether', 'USDCUSD Coin', 'BUSDBinance USD']

df_rank = df.groupby(['Rank', 'Name']).size().reset_index().rename(columns={0: '# of Weeks'}).drop_duplicates(
    subset=['Name'], keep='first').sort_values(by=['Rank', '# of Weeks'], ascending=[True, False])


last_date = str(max(df.Date))[:10]

# print(df_rank); quit()

updated = html.Div(
    [
        html.P("Last updated: " + last_date,
                style={'text-align': 'right', 'color': 'light grey'})
    ], className='card-title'
)



table = dbc.Table.from_dataframe(df_rank[['Rank', 'Name', '# of Weeks']], striped=True, bordered=True, hover=True)

attribution = dbc.Row(
    [dbc.Row([
        dbc.CardLink("Created by: @tc_madt", href="https://www.twitter.com/tc_madt")],
    ),
        dbc.Row([dbc.CardLink("Data Source: CoinMarketCap", href="https://coinmarketcap.com/")]),
    ]
)

title = html.Div(
    [
        html.H1("Highest Rank Achieved By Market Cap",
                style={'text-align': 'center'}),
        # html.H5("How significant is the 'lindy effect' in crypto?",
        #         style={'text-align': 'center', 'color': 'grey'})
    ], className='card-title'
)

app.layout = html.Div([
    updated,
                       title,
                       table,
                       attribution
]
                      ,
                      style={'margin-top': 10, 'margin-bottom': 10,
                             'margin-right': '25px', 'margin-left': '25px',
                             }
                      )

if __name__ == '__main__':
    app.run_server(debug=True)

# add last updated
# add logo/ticker
# add color for gold, silver, bronze
# only show the coin with the longest record in each position
# add current rank
# get coinlindy.com domain name
