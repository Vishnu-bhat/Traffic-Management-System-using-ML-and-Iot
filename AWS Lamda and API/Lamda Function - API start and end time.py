import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

#JSON encoder for Decimal values
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('vehicle-data')

    try:
        start_time = int(event['queryStringParameters']['start_time'])
        end_time = int(event['queryStringParameters']['end_time'])
    except (KeyError, ValueError) as e:
        return {
            'statusCode': 400,  # Bad Request
            'body': json.dumps({'error': 'Invalid query parameters. Ensure start_time and end_time are provided and are integers.'})
        }

    try:
        # Perform a scan with a filter expression
        response = table.scan(
            FilterExpression=Key('detection_time').between(start_time, end_time)
        )

        # Extract and format data
        data = []
        for item in response.get('Items', []):
            try:
                payload = item.get('payload', {})  # Directly use the 'payload' dictionary
                data.append({
                    'detection_time': int(payload.get('detection_time', 0)),
                    'bus': int(payload.get('bus', 0)),
                    'car': int(payload.get('car', 0)),
                    'motor_cycle': int(payload.get('motor_cycle', 0)),
                    'auto_rikshaw': int(payload.get('auto_rikshaw', 0))
                })
            except (KeyError, ValueError, TypeError) as e:
                # Skip invalid items and log for debugging
                print(f"Error parsing item: {item}, error: {e}")

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(data, cls=DecimalEncoder)
        }

    except Exception as e:
        # Log the exception and return a 500 status code
        print(f"Error during DynamoDB scan: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


