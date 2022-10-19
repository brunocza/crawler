

import os
import ast
import pathlib
import yaml
import os
import time
os.putenv('TZ', 'America/Sao_Paulo')
time.tzset()

# Path
BASE_PATH = pathlib.Path(__file__).parent.resolve()


try:
    DATABASES =ast.literal_eval( os.environ['DATABASE'])
    aws_credencials = ast.literal_eval(os.environ['aws_credencials'])
    twilio_credentials = os.environ['twilio_credentials']
    oxylabs_credentials = os.environ['oxylabs_credentials']

except:
    with open(BASE_PATH.joinpath("secrets.yml"), "r") as file:
        data = yaml.load(file)
    DATABASES =ast.literal_eval( data['DATABASE'])
    aws_credencials = ast.literal_eval(data['aws_credencials'])
    twilio_credentials =  ast.literal_eval( data['twilio_credentials'])  
    oxylabs_credentials =  ast.literal_eval( data['oxylabs_credentials'])  
    
