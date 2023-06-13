import json
import uuid
import boto3

db_client = boto3.client('dynamodb')

new_game_data = {
    'game_id': None,
    'user_id': None,
    'score': {
        'category': { 1:None,2:None,3:None,4:None,5:None,6:None},
        'category_bonus': 0,
        'three_of_a_kind': 0,
        'four_of_a_kind': 0,
        'full_house': 0,
        'small_straight': 0,
        'large_straight': 0,
        'chance': 0,
        'yatesee': 0,
        'yatesee_count': 0,
        'total': 0
    },
    'dice': [6,6,6,6,6],
    'roll': 0
}

def save_game(game_data) :

    data = db_client.put_item(
        TableName='YateseeGames',
        Item={
            'user_id': {
              'S': game_data['user_id']
            },
            'game_id': {
              'S': game_data['game_id']
            },
            'data': {
              'S': json.dumps(game_data)
            }
        }
    )


def lambda_handler(event, context):

    new_game_data['user_id'] = event['requestContext']['authorizer']['claims']['sub']
    #new_game_data['user_id'] = "NoAuth12345678"
    new_game_data['game_id'] = str(uuid.uuid1())

    save_game(new_game_data)

    return {
        'statusCode': 200,
        'body': json.dumps(new_game_data)
    }
