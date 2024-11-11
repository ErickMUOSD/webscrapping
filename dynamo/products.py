import os
from typing import Dict

import boto3
from loguru import logger as log
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from pynamodb.models import Model



class Products(Model):
    """
    A DynamoDB User
    """
    class Meta:
        table_name = os.environ.get("TABLE_NAME")
        region = os.environ.get("AWS_REGION")
    id = UnicodeAttribute(hash_key=True)
    availability_status = UnicodeAttribute(default=None)
    current_price = NumberAttribute(default=0.00)
    old_price = NumberAttribute(default=0.00)
    source = UnicodeAttribute(default=None)
    name = UnicodeAttribute(default=None)

def send_sns_topic(message):
    sns = boto3.client('sns')
    # Publish a message to the topic
    response = sns.publish(
        TopicArn=os.environ.get("SNS_ARN_TOPIC"),
        Message='This is a test message'
    )

    # Print the message ID
    print(response['MessageId'])

def save_product_data(product: Dict):
#     get product from id
    try :
        product_instance = Products.get(product['id'])
        if product_instance.current_price != product['current_price']:
            product_instance.old_price = product_instance.current_price
            product_instance.current_price = product['current_price']
            product_instance.save()
            message = f"Price of product {product['id']} has changed from {product_instance.old_price} to {product_instance.current_price} at {product_instance.source} "
            send_sns_topic(message)
    except Products.DoesNotExist:
        log.info(f"Saving product {product['id']}")

        product = Products(
            id=product['id'],
            availability_status=product['availability_status'],
            current_price=product['current_price'],
            name=product['name'],
            source=product['type']
        )
        product.save()
    except Exception as e:
        log.error(f"Error: {e}")
        raise e
