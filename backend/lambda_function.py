import json
import boto3
from decimal import Decimal

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('visitor-counter')

def lambda_handler(event, context):
    try:
        # Retrieve the current visitor count
        response = table.get_item(Key={'id': 'visits'})
        
        # Get the current count or default to 0 if no record exists
        visit_count = response.get('Item', {}).get('count', 0)

        # Ensure count is an integer (fix Decimal issue)
        if isinstance(visit_count, Decimal):
            visit_count = int(visit_count)
        
        # Increment the visitor count
        visit_count += 1
        
        # Update the count in DynamoDB
        table.put_item(Item={'id': 'visits', 'count': visit_count})
        
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
