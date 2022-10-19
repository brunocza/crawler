
import os
import time

os.putenv('TZ', 'America/Sao_Paulo')
time.tzset()
import io
import boto3
import settings
import json
import ast        
import pandas as pd
from tempfile import mkdtemp
from unidecode import unidecode
from datetime import datetime, timedelta
import pandas as pd
from tempfile import mkdtemp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup

def depara_():
    """
    It reads the csv file, creates two dataframes, concatenates them, drops duplicates, resets the
    index, creates a new column, and then fills it with the location names
    :return: A dataframe with the cities and states of the origin and destination of the flights.
    """
    depara = pd.read_csv('concorrencia.csv', sep=';')
    df1= pd.DataFrame(depara[['origin_name', 'origin_state']]).rename(columns={'origin_name':'name', 'origin_state':'state'})
    df2= pd.DataFrame(depara[['destination_name', 'destination_state']]).rename(columns={'destination_name':'name', 'destination_state':'state'})
    depara = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
    depara['loc'] = str
    for i in range(len(depara)):
        depara['loc'][i] = str(unidecode(depara['name'][i].lower().replace(' ','-')) + '-'+ unidecode(depara['state'][i].lower()))
    return depara   

def chrome_proxy(user, password, endpoint):
    """
    It takes a username, password, and endpoint, and returns a dictionary that can be used to configure
    a ChromeDriver instance to use the proxy
    
    :param user: The username for the proxy
    :param password: The password you use to log into the proxy
    :param endpoint: The endpoint of the proxy server
    :return: A dictionary with the key "proxy" and the value of a dictionary with the keys "http" and
    "https"
    """
    wire_options = {
        "proxy": {
            "http": "http://{0}:{1}@{2}".format(user, password, endpoint),
            "https": "http://{0}:{1}@{2}".format(user, password, endpoint),
        }
    }
    return wire_options

def options():
    """
    It creates a new instance of the ChromeOptions class, sets the binary location, adds some arguments,
    and then creates a new instance of the Chrome webdriver class, passing in the options and the proxy
    :return: The driver is being returned.
    """
    # Creating an instance of the Options class.
    # try:
    proxies = chrome_proxy(settings.oxylabs_credentials['USERNAME'], settings.oxylabs_credentials['PASSWORD'], settings.oxylabs_credentials['ENDPOINT'])
    
    chrome_options = Options()
    chrome_options.binary_location = '/opt/chrome/chrome'
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1739x3600")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--window-size=1366x768")
    # mobile_emulation = {
    #     "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
    #     "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    # }

    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    
    
    driver = webdriver.Chrome("/opt/chromedriver",options=chrome_options,  seleniumwire_options=proxies)
    time.sleep(4)

    '''   
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument('--profile-directory=Profile 2')
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--window-size=1739x5600")
    mobile_emulation = {
        "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    }

    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            
    driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=proxies)
    
    
    
    '''
    return driver

# driver.save_screenshot('foto.png')
# driver.close()

def cbla(event):
    """
    It takes a JSON object as input, and returns a JSON object as output
    
    :param event: A dict that contains the payload of the event
    :return: A JSON object with the following keys:
    """

    try:
        depara = depara_()
        try:
            origin0 = event['origin_name']
            destination0 = event['destination_name']
            departure_date0 =  event['departure_date']

            input_data = {'origin':origin0,
                        'destination':destination0,
                        'departure_date':departure_date0}

            depara_df =pd.DataFrame([input_data['origin'],input_data['destination']], columns=['de']).merge(depara, left_on='de', right_on='loc')
            
            origin = [depara_df['name'][0] ,  depara_df['state'][0]]    
            destination = [depara_df['name'][1] ,  depara_df['state'][1]]      
        except:
            return {'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body':'Rota nao existente no portal blablacar',
                    'info': {'avaliable_locations' : str(list(depara['loc']))}}
        
        
        driver = options()
        url = "https://www.blablacar.com.br/search?fn={0}%2C {1}%2C Brasil&tn={2}%2C {3}%2C Brasil&db={4}".format(origin[0],origin[1],destination[0],destination[1],str(departure_date0))
        # driver.set_window_size(1739, 3600)

        time.sleep(5)
        driver.get(url)
        
        WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".kirk-tab-content > .sc-fWQKxP")))
        driver.find_element(By.CSS_SELECTOR, ".kirk-tab-content > .sc-fWQKxP").click()
        driver.set_window_size(1739, 3000)
        driver.implicitly_wait(5) # seconds
        time.sleep(7)

        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        bloco_0 = []
        for ele in soup.select('li[class="kirk-cardItem"]'):
            bloco_0.append(ele)

        data, duracao, chegada, origem, destino, operadora, price, cheio = [],[],[],[],[],[],[],[]



        for element in bloco_0:
            dt = departure_date0 + ' ' + element.select('div[class="sc-pyfCe jNmsWG kirk-timeDuration notranslate"]')[0].contents[0].contents[0]
            data.append(datetime.strptime(dt, "%Y-%m-%d %H:%M"))
            try:
                duracao.append(element.select('div[class="sc-pyfCe jNmsWG kirk-timeDuration notranslate"]')[0].contents[1].contents[0])
                cheio.append(False)
            except:
                duracao.append(None)
                cheio.append(True)
            try:
                hora = element.select('div[class="sc-pyfCe jNmsWG kirk-timeDuration notranslate"]')[0].contents[1].contents[0].split('h')[0]
                minuto = element.select('div[class="sc-pyfCe jNmsWG kirk-timeDuration notranslate"]')[0].contents[1].contents[0].split('h')[1]
                dtc = datetime.strptime(departure_date0, "%Y-%m-%d") + timedelta(hours=int(hora), minutes= int(minuto))
                chegada.append(dtc)
            except:
                chegada.append(None)       
            try:
                origem.append(element.select('span[class="sc-gswNZR sc-eDvSVe sc-jSUZER sc-idXgbr kQcYu bUlgNG chLGiP eOMoJF"]')[0].contents[0])
            except:
                origem.append(None)  
            try:
                destino.append(element.select('span[class="sc-gswNZR sc-eDvSVe sc-jSUZER sc-idXgbr kQcYu bUlgNG chLGiP eOMoJF"]')[1].contents[0])
            except:
                destino.append(None)
            try:
                operadora.append(element.select('span[class="kirk-text kirk-text-title sc-UpCWa bFfXPI"]')[0].contents[0])
            except:
                operadora.append(None)
            try:
                price.append(float(element.select('span[class="sc-gswNZR sc-eDvSVe sc-jSUZER sc-grxQYx kQcYu bUlgNG chLGiP hqKJhi"]')[0].contents[0].replace(u'R$\xa0', u'').replace(u',', u'.')))
            except:
                price.append(None)

        df = pd.DataFrame(
            {'data': data,
            'duracao': duracao,
            'chegada': chegada,
            'origem': origem,
            'destino': destino,
            'operadora': operadora,
            'price': price,
            'cheio':cheio
            })
        df['tipo']='carona'
        df.drop_duplicates(inplace=True)
        print('carona: ',str(len(df)))

        driver.find_element(By.CSS_SELECTOR, ".kirk-tab-content > .jdLpHs").click()
        time.sleep(7)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        bloco_0 = []
        for ele in soup.select('li[class="kirk-cardItem"]'):
            bloco_0.append(ele)

        data, duracao, chegada, origem, destino, operadora, price, cheio = [],[],[],[],[],[],[],[]

        for element in bloco_0:
            dt = departure_date0 + ' ' + element.select('div[class="sc-pyfCe jNmsWG kirk-timeDuration notranslate"]')[0].contents[0].contents[0]
            data.append(datetime.strptime(dt, "%Y-%m-%d %H:%M"))

            try:
                duracao.append(element.select('div[class="sc-pyfCe jNmsWG kirk-timeDuration notranslate"]')[0].contents[1].contents[0])
                cheio.append(False)
            except:
                duracao.append(None)
                cheio.append(True)
            try:
                hora = element.select('div[class="sc-pyfCe jNmsWG kirk-timeDuration notranslate"]')[0].contents[1].contents[0].split('h')[0]
                minuto = element.select('div[class="sc-pyfCe jNmsWG kirk-timeDuration notranslate"]')[0].contents[1].contents[0].split('h')[1]
                dtc = datetime.strptime(departure_date0, "%Y-%m-%d") + timedelta(hours=int(hora), minutes= int(minuto))
                chegada.append(dtc)
            except:
                chegada.append(None)
            try:
                origem.append(element.select('span[class="sc-gswNZR sc-eDvSVe sc-jSUZER sc-idXgbr kQcYu bUlgNG chLGiP eOMoJF"]')[0].contents[0])
            except:
                origem.append(None)
            try:
                destino.append(element.select('span[class="sc-gswNZR sc-eDvSVe sc-jSUZER sc-idXgbr kQcYu bUlgNG chLGiP eOMoJF"]')[1].contents[0])
            except:
                destino.append(None)
            try:
                operadora.append(element.select('span[class="kirk-text kirk-text-title sc-UpCWa bFfXPI"]')[0].contents[0])
            except:
                operadora.append(None)
            try:
                price.append(float(element.select('span[class="sc-gswNZR sc-eDvSVe sc-jSUZER sc-grxQYx kQcYu bUlgNG chLGiP hqKJhi"]')[0].contents[0].replace(u'R$\xa0', u'').replace(u',', u'.')))
            except:
                price.append(None)
                
        df_2 = pd.DataFrame(
            {'data': data,
            'duracao': duracao,
            'chegada': chegada,
            'origem': origem,
            'destino': destino,
            'operadora': operadora,
            'price': price,
            'cheio':cheio
            })
        df_2['tipo']='onibus'
        df_2.drop_duplicates(inplace=True)
        print('onibus: ',str(len(df_2)))

        driver.close()
            
        df_out = pd.concat([df,df_2])
        df_out['cheio'] = df_out['cheio'].apply(lambda x:bool(x))
        if len(df_out) == 0 :
            return {'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body':'Não foi possivel oberter informação no site do concorrente.'}
        else:
            return {'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body':json.dumps(df_out.to_json(orient="records", force_ascii=False), ensure_ascii=False, indent=2).encode("utf-8")}


    except:
        s3 = boto3.client('s3', aws_access_key_id=settings.aws_credencials['default']['aws_access_key_id'],
                        aws_secret_access_key=settings.aws_credencials['default']['aws_secret_access_key'])
        with io.BytesIO(driver.get_screenshot_as_png()) as f:
            s3.upload_fileobj(f, 'arca-redshift', 'vendas/print_selenium.png')
        driver.close()
        return {'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body':'https://arca-redshift.s3.us-east-2.amazonaws.com/vendas/print_selenium_blabla.png'}


def blablacar(event, context):
    """
    > The function takes the event as a string, converts it to a dictionary, and passes it to the `cbla`
    function
    
    :param event: The event parameter contains the payload data that is sent to the Lambda function by
    the event source
    :param context: This is the context object that is passed to the Lambda function. It contains
    runtime information about the Lambda function that is executing
    """
    event = ast.literal_eval(str(event))
    response = cbla( event = event )  
    return response
  