import boto3
import json


def lambda_handler(event, context):
    # Your code goes here!
    client = boto3.resource('dynamodb', region_name='us-west-1').Table('pizzashop')
    myevent = {}
    try:
        myevent["pizzamenuid"] = event["menu_id"]
		myevent["store_name"] = event["store_name"]
		myevent["selection"] = event["selection"]
		myevent["size"] = event["size"]
		myevent["price"] = event["price"]
		myevent["store_hours"] = event["store_hours"]
		client.put_item(Item=myevent)
     
       
    except Exception, e:
        return 400, e
    return 200, "OK"