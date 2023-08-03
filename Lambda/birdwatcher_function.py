import json
from email.message import Message
from email.mime import base
import os
import base64
import boto3
import time

Birds = ['Parakeet','Dove','Cardinal','Finch','Woodpecker','Robin','Titmouse','Sparrow','Warbler','Northern Cardinal', 'Carolina Wren', 'Mourning Dove',
    'Tufted Titmouse', 'Blue Jay', 'Carolina Chickadee', 'Red-bellied Woodpecker', 'Northern Mockingbird', 'Eastern Phoebe', 
    'Eastern Towhee', 'American Crow', 'Eastern Bluebird', 'Downy Woodpecker', 'American Robin', 'American Goldfinch', 'Chipping Sparrow', 
    'Pine Warbler', 'House Finch', 'White-breasted Nuthatch', 'Song Sparrow', 'Red-winged Blackbird', 'Northern Flicker', 
    'Pileated Woodpecker', 'Common Grackle', 'European Starling', 'Ruby-throated Hummingbird', 'Indigo Bunting', 'Gray Catbird'
    'Yellow-rumped Warbler', 'Ruby-crowned Kinglet', 'White-throated Sparrow', 'Yellow-bellied Sapsucker'
    ]

# Get AWS resources
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')

# Define resources
topic_arn = "YOUR SNS TOPIC ARN"
s3_bucket = 'YOUR S3 BUCKET'
bird_table = 'YOUR DYNAMODB TABLE'

# Go into temp directory
os.chdir('/tmp')

def lambda_handler(event, context):
    # Define Variables
    image_data = event['body']
    bird_type = ""
    bird_confidence = 0
    image_name = event['queryStringParameters']["ImageName"]
    capture_time = event['queryStringParameters']["CaptureTime"]
    table = dynamodb.Table("TestTable2")

    image_file = bytes(image_data, "ascii")
    image_bytes = base64.decodebytes(image_file)
    
    # Send data to rekognition
    rekognition_response = rekognition.detect_labels(Image ={'Bytes' : image_bytes}, MaxLabels = 10)
    #print(rekognition_response)

    # Parse the labels to determine if a bird type is recognized
    for label in rekognition_response["Labels"]:
        if label['Name'] in Birds:
            if label['Confidence'] > bird_confidence:
                bird_type = label['Name']
                bird_confidence = label['Confidence']  
            else:
                pass
        else:
            pass
        
    
    # Check labels again for bird that may not have been recognized or not in the bird list    
    for label in rekognition_response["Labels"]:
        if label['Name'] == "Bird" and bird_confidence == 0:
            bird_type = "Bird"
        else:
            pass

    # Send a message if their is confidence a bird is present in the bird feeder
    if bird_confidence > 0:
        #Decode image and write to file. This will be saved in the tmp directory
        temp_image = open("birdimage.jpg", "wb")
        temp_image.write(base64.b64decode(image_file))
        temp_image.close()
        
        #Upload image to s3
        s3_response = s3.upload_file('./birdimage.jpg', s3_bucket, image_name)
        object_url = '{}/{}/{}'.format(s3.meta.endpoint_url, s3_bucket, image_name)
        ID = int(image_name.replace(".jpg",""))
        
        #upload to dynamodb
        ddb_response = table.put_item(
            Item={
                
                'ID': ID,
                'Image_Name' : image_name,
                'Capture_Time' : capture_time,
                'Bird_Type' : bird_type,
                'Image_URL' : object_url

            }
            )
        sns_message = "There is a " + bird_type + " in the bird feeder. Download Link: " + object_url
        sns_subject = bird_type + " Detected!"
        sns_message = sns.publish(TopicArn=topic_arn, Subject=sns_subject, Message=sns_message)
        
    elif bird_type == "Bird":
        tmpimg = open("birdimage.jpg", 'wb')
        tmpimg.write(base64.b64decode(imgfile))
        tmpimg.close()
        s3response = s3.upload_file('./birdimage.jpg', s3Bucket, img_name)
        ddbresponse = table.put_item(
            Item={
                
                'ID': int(image_name.replace(".jpg","")),
                'Image_Name' : img_name,
                'Capture_Time' : capture_time,
                'Bird_Type' : 'Undetermined',
                'Image_URL' : object_url
                
            }
            )
        snsMessage = "There is a bird in the bird feeder. Download link: " + object_url 
        snsSubject = "Bird Detected!"
        snsMessage = sns.publish(TopicArn = topic_arn, Subject = sns_subject, Message = sns_message)
    else:
        bird_type = "None"
        
        
    

    bird_data = {'ImageName': image_name, 'CaptureTime' : capture_time, 'BirdType': bird_type}

    return {
        'statusCode': 200,
        'body': json.dumps(bird_data)
    }