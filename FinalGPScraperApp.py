import time
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import os
from selenium import webdriver
import csv
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import dash_bootstrap_components as dbc


#PAGE_SIZE = 6
app = dash.Dash(__name__, meta_tags=[
    {'name': ' Grailed Price Scraper ',
     'content': 'NONE'},
    {'charset': 'utf-8'},
    {'name': 'viewport',
     'content': 'width=device-width, initial-scale=0.95'},
], title='Grailed Scraper', prevent_initial_callbacks=True)

app.layout = html.Div([
    dcc.Store(id='memory-output'),
    html.Div(
        html.Header(
            html.H1("G{P}SCRAPR")
        )
    ),
    html.Div(
        className='back-container',
        children=[
            html.Div(
                className='left-container',
                children=[
                    html.H2('Overview', className= 'header-2'),
                    html.Ul(
                            children=[
                                #html.Li('Purpose'),
                                html.Details([
                                    html.Summary('Purpose', className='summarytitle'),
                                    html.Div(children=[
                                        html.P('The purpose of this application is to collect real time sales data from Grailed.com .'
                                               'This application in conjunction with Microsoft Excel, Python or any other data analysis program'
                                               ' will allow any user to harness the sales data of specific items for pricing, trending'
                                               ' or visualizing historical market conditions.', className='p-container')
                                    ])
                                ], className='summarybody'),
                                html.Details([
                                    html.Summary('How to use', className='summarytitle'),
                                    html.Div(children=[
                                        html.P(['In order for this application to work you must have a Grailed.com account, use https://www.grailed.com/sold (generic sold page), or have a known sold URL.'
                                               ' To find the sold page for a specific query, you must first find an active listing of the desired item. Then click on the price comparison button below the description.'
                                               ' And finally, copy the Url of the sold page into this application and click "Submit".', " ", html.B('Please allow up to 5 minutes for the file + Dataframe to appear ')], className='p-container')
                                    ])
                                ], className='summarybody'),
                                html.Details([
                                    html.Summary('About', className='summarytitle'),
                                    html.Div(children=[
                                        html.P(['This Application was built and is currently maintained by',
                                                html.A('www.Caretag.us', className="no-underline", href='https://www.caretag.us/',style={'margin': '0.25rem', 'color': '#2a30c9' })
                                                ], className='p-container')
                                    ])
                                ], className='summarybody'),
                                html.Li('This is left intentionally transparent IF you read this HELLU LOL', className='transparenttxt')
                            ]),
                ]),
            html.Div(
                className='right-container',
                children=[
                    html.P('Grailed sold address',
                           className='p-input'),
                    dcc.Input(
                        className='input-rounded',
                        id='input-url',
                        placeholder='Input Grailed Sold Address',
                        type="text",
                        style={"width": "73%", }
                    ),
                    html.Div(id='output-url'),
                    # ____________________________#
                    html.P('How many pages to scrape?',
                           className='p-input'),
                    dcc.Input(
                        className='input-rounded',
                        id='input-pages',
                        placeholder='1 page = 40 listings',
                        type="text",
                        min="1",
                        style={"width": "73%", }
                    ),
                    html.Div(id='output-pages'),
                    # ----------Where CSV Name Export would go--------------#
                    html.Div(id='output-csv'),
                    # ------------------------------#
                    html.Button('submit',
                                id='input-submit',
                                className='button-1'),
                    html.Div(id='output-submit'),
                             #children='Your CSV will be available to download soon'),
                ]),
        ]),
    html.Div(className='back-container-2',
             children=[
                html.Div(id='output-data-upload', className='datatable-p'),
                 html.Nav([
                     html.A('Contact', href='mailto: Caretagus@gmail.com'),
                     html.A('Caretag', href='https://www.caretag.us/'),
                     html.A('Instagram', href='https://www.instagram.com/caretag.us/'),
                     html.Div(className='animation start-home')
                 ]),

    ])
])



@app.callback(
    Output(component_id='output-data-upload', component_property='children'),
    Input(component_id='input-submit', component_property='n_clicks'),
    [State(component_id='input-url', component_property='value'),
     State(component_id='input-pages', component_property='value')])
     #State(component_id='input-csv', component_property='value')

def run_script(n_clicks, url, pages):
    if n_clicks:
        url1=str(url)
        pages= str(pages)
        pages2 = int(pages)
        CSV= 'Generic.csv'
        email = # Your Grailed Email
        password = # Your Grailed Password
        url = 'https://www.grailed.com/'
        option = webdriver.ChromeOptions()
        # For older ChromeDriver under version 79.0.3945.16
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option('useAutomationExtension', False)
        # For ChromeDriver version 79.0.3945.16 or over
        option.add_argument('--disable-blink-features=AutomationControlled')
        # Save log-in information
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="global-header-login-btn"]'))).click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div/div[2]/div/div/button[4]'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]'))).send_keys(email)
        time.sleep(10)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(
            password)
        time.sleep(10)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div/div[2]/div/div/form/button'))).click()
        time.sleep(10)
        driver.get(url1)
        time.sleep(10)
        scroll_count = round((pages2 * 40) / 40) + 1
        for i in range(scroll_count):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)

        time.sleep(3)

        titles = driver.find_elements_by_css_selector("p.listing-title")
        prices = driver.find_elements_by_css_selector("p.sub-title.sold-price")
        sizes = driver.find_elements_by_css_selector("p.listing-size.sub-title")
        sold = driver.find_elements_by_css_selector("span.date-ago")
        #filename = CSV
        #path = f"/Users/kylemartin/Desktop/webspider/{filename}"
        data = [titles, prices, sizes, sold]

        data = [list(map(lambda element: element.text, arr)) for arr in data]
        with open(CSV, 'w') as file:
            writer = csv.writer(file)
            j = 0
            while j < len(titles):
                row = []
                for i in range(len(data)):
                    row.append(data[i][j])
                writer.writerow(row)
                j += 1
        df = pd.read_csv(CSV, names=['Title', 'Sold Price', 'Size', 'Sold Date'])
        #df = df.to_csv
        driver.quit()
        return html.Div([
			dash_table.DataTable(
				id='table',
				columns=[{"name": i, "id": i} for i in df.columns],
				data=df.to_dict('records'),
                export_format="csv",
                style_table={
                    'height': 200,
                    'overflowY': 'scroll',
                    'display': 'inline-block',
                    'border-radius': '18px',
                    'border-width': '1px'
                    #'width': 100,
                })
			])

    else:
        raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)

    #app.run_server(host=os.getenv('IP', '0.0.0.0'),
                   #port=int(os.getenv('PORT', 1113)))

"""
                    html.P('CSV Filename', className='p-input'),
                    dcc.Input(
                        className='input-rounded',
                        id='input-csv',
                        placeholder='Input filename',
                        type="text",
                        style={"width": "73%", }
                    ),
                    """
