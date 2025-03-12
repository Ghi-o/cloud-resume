import json
import boto3
from decimal import Decimal

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('visitor-counter')
ip_table = dynamodb.Table('visitor-ips')

def lambda_handler(event, context):
    try:
        # get visitor ip
        visitor_ip = event['requestContext']['identity']['sourceIp']
        
        # Retrieve the current visitor count
        response = table.get_item(Key={'id': 'visits'})
        
        # Get the current count or default to 0 if no record exists
        visit_count = response.get('Item', {}).get('count', 0)
        
        # Ensure count is an integer (fix Decimal issue)
        if isinstance(visit_count, Decimal):
            visit_count = int(visit_count)
        
        # check if ip is already used
        ip_check = ip_table.get_item(Key={'ip': visitor_ip})

        if 'Item' in ip_check:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    "Content-Type": "application/json"
                },
                'body': json.dumps({'message':'Duplicate visit', 'visitorCount': visit_count})
            }
    
        # Increment the visitor count
        visit_count += 1
        
        # Update the count in DynamoDB
        table.put_item(Item={'id': 'visits', 'count': visit_count})

        # adds visitor ip
        ip_table.put_item(Item={'ip': visitor_ip})
        
        # Return the updated count
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            },
            'body': json.dumps({'visitorCount': visit_count})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }