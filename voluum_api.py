import json
import requests
import httplib
from requests.exceptions import ConnectionError, Timeout
import sys
import logging
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('C:\Temp\Log_File.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

#Process Date Argument
if len(sys.argv)>1:
    process_date = sys.argv[1]
else:
    logger.error("no input date!")
    sys.exit(1)

#process_date='2016-11-22'
logger.info("starting to load data")
start_date = datetime.datetime.strptime(process_date, '%Y-%m-%d').date()
print start_date
end_date = start_date + datetime.timedelta(days=1)
print end_date

DSP='Blabla'
data='C:\Temp\data_%s.txt' % process_date

# Authorization
url = "https://security.voluum.com/login"
from requests.auth import HTTPBasicAuth
r=requests.get(url, auth=HTTPBasicAuth('email', 'pass'))
json_response = r.json()
token =json_response["token"]

with open(data, 'w') as output_file:
   output_file.write('campaignCountry,campaignName,campaignNamePostfix,conversions,cost,cpv,ecpa,trafficSourceName,visits\n')

list=[]
try:
    url="https://portal.voluum.com/report?from=%sT00:00:00Z&to=%sT00:00:00Z&tz=Europe%%2FAmsterdam&filter=Blabla&sort=conversions&direction=desc&columns=campaignName&columns=status&columns=bid&columns=bids&columns=winRate&columns=visits&columns=conversions&columns=cost&columns=cpv&columns=ap&columns=errors&columns=rpm&columns=ecpc&columns=trafficSourceName&columns=cpa&groupBy=campaign&offset=0&limit=1000&include=all" % (start_date, end_date)
    headers={'cwauth-token':'%s' % token}
    r=requests.get(url, headers=headers)
    for item in r.json()["rows"]:
        with open(zeropark_data, 'a') as output_file:
            output_file.write('%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %( item['campaignCountry'], item['campaignName'], item['campaignNamePostfix'], item['conversions'], \
                                                                   item['cost'], item['cpv'], item['ecpa'], item['trafficSourceName'], item['visits']))
except Exception as e:
    logger.error("Api error %s" % e)

