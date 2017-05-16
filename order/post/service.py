import boto3
import json

def convertListToString(list):
    count = 1
    string = ""
    for item in list:
        string = string + str(count) + ":" + item + " "
        count = count + 1
    return string

def lambda_handler(event, context):

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
    