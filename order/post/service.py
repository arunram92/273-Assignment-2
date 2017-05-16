import boto3
import json
import datetime
#from pytz import timezone

def convertListToString(list):
    count = 1
    string = ""
    for item in list:
        string = string + str(count) + ":" + item + " "
        count = count + 1
    return string

def withInStoreHours(event):
    week = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}
    menuclient = boto3.resource('dynamodb', region_name='us-west-1').Table('pizzashop')
    storehours = menuclient.get_item(Key={'pizzamenuid': event['menu_id']}).get('Item').get('store_hours')
    currentDayStoreHours = storehours[week[datetime.datetime.today().weekday()]].split('-')
    startTime = int(filter(str.isdigit, str(currentDayStoreHours[0])))
    endTime = int(filter(str.isdigit, str(currentDayStoreHours[1]))) + 12
    currentTime = datetime.datetime.today().hour
    print datetime.datetime.today().weekday()
    print startTime
    print endTime
    print currentTime
    if currentTime>startTime and currentTime < endTime:
        return True
    else:
        return False

def lambda_handler(event, context):
    if withInStoreHours(event):
        client = boto3.resource('dynamodb', region_name='us-west-1').Table('order')
        myevent = {}
        try:
            myevent["pizzamenuid"] = event["menu_id"]
            myevent["order_id"] = event["order_id"]
            myevent["customer_name"] = event["customer_name"]
            myevent["customer_email"] = event["customer_email"]
            myevent["order_status"] = "processing"
            order = {}
            order["selection"] = "none"
            order["size"] = "none"
            order["costs"] = "none"
            order["order_time"] = "none"
            myevent["order"] = order
            client.put_item(Item=myevent)
            menuclient = boto3.resource('dynamodb', region_name='us-west-1').Table('pizzashop')
            selection = menuclient.get_item(Key={'pizzamenuid': event['menu_id']}).get('Item').get('selection')
            return "200 OK { Hi %s , please choose one of these selection: %s }" % (myevent["customer_name"], convertListToString(selection))

        except Exception, e:
            return 400, e
    else:
        return "200 OK. Store Closed. Please order during the store hours."