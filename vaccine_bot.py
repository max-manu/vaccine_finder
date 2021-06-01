import os
import requests,json,time,os
#from twilio.rest import Client

def get_district_id(state="himachal pradesh",district='hamirpur'):
  with open('districts.json') as file:
    dic=json.load(file)
  state=state.lower()
  district=district.lower()
  return dic[state][district]

def data(date,district_id=363):
      parameters={
      'district_id':district_id,
      'date':date
      }

      r=requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict',params=parameters)
    #text=json.dumps(r.json(),indent=4)
      dic=r.json()
    #print(text)
      return dic
#strftime(gmtime())

def get_message(date,district_id,block_name=None,min_age_limit=18):
    
    def data(date,district_id=363):
      parameters={
      'district_id':district_id,
      'date':date
      }

      r=requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict',params=parameters)
    #text=json.dumps(r.json(),indent=4)
      dic=r.json()
    #print(text)
      return dic
#strftime(gmtime())
    
    def tell(item,vaccine):
        text=' Hospital: {0}\n Address: {1}\n Block: {3}\n Vaccine: {2} '.format(item['name'],item['address'],vaccine,item['block_name'])
        #dic=dict({"Hospital":item['name'],"Address":item['address'],'Block':item['block_name']})
        return text#,dic
    def vaccine_text(i):
          text=i['vaccine']+'('+str(i['available_capacity_dose1'])+")"+" Date: {}".format(i['date'])
          
          return text
    available=False
    vaccine=set()
    vaccine_dic={}
    message=''
    total_vaccine=0
    dic=data(date,district_id)
    for item in dic['centers']:
        for i in item['sessions']:
            #print(item)
            if i['min_age_limit']==min_age_limit:
                  if block_name==None:
                        if i['available_capacity_dose1']>0:
                          available=True
                          text=vaccine_text(i)
                          vaccine.add(text)
                          total_vaccine+=1
                          #dic={i['vaccine']:i['available_capacity_dose1'],'Date':i['date']}
                  else:
                        block_name=map(lambda item:item.lower(),block_name)
                        if i['available_capacity_dose1']>0 and  item['block_name'].lower() in block_name:
                          available=True
                          text=vaccine_text(i)
                          vaccine.add(text)
                          total_vaccine+=1
                          #dic={i['vaccine']:i['available_capacity_dose1'],'Date':i['date']}
                      #tell()
                      
                      #print(i,item)
        if available:
            text=tell(item,', '.join(vaccine))
            message+=text+'\n\n'
            available=False
            vaccine=set()
    return message,total_vaccine


def send_telegram(message):
    pass
    chat_id=os.environ('CHAT_ID')
    parameter={'chat_id': chat_id,'text':message}
   
    token=os.environ['TELEGRAM_TOKEN']
    
    requests.get('https://api.telegram.org/bot{}/sendMessage'.format(token),params=parameter)

def send_call(message='hello',heart_beat=1):
    pass
    if len(message)==0:
        return 'not send'
    account_sid =os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    
    client = Client(account_sid, auth_token)
    numbers=list(os.environ['numbers'].split())
    if heart_beat==1:
        
        for number in numbers:
            call = client.calls.create(
                                url='http://demo.twilio.com/docs/voice.xml',
                                to = '+91'+number,
                                from_='+12017194978'
                            )
            # message = client.messages.create(
            #                         body=message,
            #                         from_='whatsapp:+14155238886',
            #                         to='whatsapp:+91'+number
            #                     )
            
    else:
        pass
        # message = client.messages.create(
        #                             body="Bot working well",
        #                             from_='whatsapp:+14155238886',
        #                             to='whatsapp:+91'+numbers[0]
        #                         )


def decide(message,total_vaccine):
    H=time.strftime('%H')
    M=time.strftime('%M')
    HM=H+":"+M
    Sec=time.strftime('%S')
    send_telegram(message)

    if HM in('07:00','19:00') and int(Sec) in range(5)  :
          print('BOT beat @ {}:{}:{}'.format(H,M,Sec))
          
          #send_telegram("BOT beat @ {}:{}:{}".format(H,M,Sec),0)
    else:
        if H in range(6,21) and total_vaccine>=2:
              send_call(message)

def run(id):
    os.environ['TZ'] = 'india-05:30'
    time.tzset()
    
    #send_telegram('app started')
    
    print('search started')

    while True:
        date=time.strftime('%d-%m-%Y')
        
        message,total_vaccine=get_message(date=date,district_id=id) #optional parameter-->block_name={'haveli','any block near you'})
        
        #send_telegram(message)
        
        print(message)
        
        #decide(message,total_vaccine)
        
        time.sleep(50)
def finder(state="himachal pradesh",district='hamirpur'):
  id=get_district_id(state,district)
  print(data(time.strftime('%d-%m-%Y'),district_id=id)
  print('Data transfer started')
  run(id)

if __name__ == "__main__":     
  state=input('Enter Your State here: ')
  district=input('Enter Your District here: ')
  
  id=get_district_id(state,district) 
  print(data(time.strftime('%d-%m-%Y'),district_id=id)
  print('Data transfer started')
  run(id)
