#!/usr/bin/env python3

'''An example of how to build a web counter API using Chalice.

Note that this does not stand alone, and references a DynamoDB table
with name "chalice-counter".

'''

import json

import boto3
from chalice import Chalice

app = Chalice(app_name='chalice-counter')

def _update_counter():
    '''Update the counter in dynamodb, and return the int value.'''
    client = boto3.client('dynamodb')

    kargs = {
        'TableName': 'chalice-counter',
        'Key': {
            'counter': {
                'S': 'codestock'
            }
        },
        'UpdateExpression': 'SET countvalue = countvalue + :one',
        'ExpressionAttributeValues': {
            ":one": {
                "N": "1"
            }
        },
        'ReturnValues': 'ALL_NEW'
    }
    retval = client.update_item(**kargs)

    try:
        assert 'Attributes' in retval
    except:
        print('No Attributes returned')
        print('retval was:')
        print(json.dumps(retval, indent=2))
        raise

    return int(retval['Attributes']['countvalue']['N'])

def _get_counter():
    '''Return the counter's value as int, without incrementing.'''
    client = boto3.client('dynamodb')

    kargs = {
        'TableName': 'chalice-counter',
        'Key': {
            'counter': {
                'S': 'codestock'
            }
        }
    }
    retval = client.get_item(**kargs)

    try:
        assert 'Item' in retval
    except:
        print('No Item returned.')
        print('retval was:')
        print(json.dumps(retval, indent=2))
        raise

    return int(retval['Item']['countvalue']['N'])


@app.route('/get', cors=True)
def get():
    '''Return the counter value, without incrementing.'''
    return {'count': _get_counter()}

@app.route('/increment', cors=True)
def increment():
    '''Increment the counter, and return the incremented value.'''
    return {'count': _update_counter()}


if __name__ == '__main__':
    print(json.dumps(_get_counter(), indent=2))
    print(json.dumps(_update_counter(), indent=2))
