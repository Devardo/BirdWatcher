# BirdWatcher
## Bird Spotting With Raspberry Pi and Amazon Rekognition

## Description
This project uses a Raspberry pi complete with a camera and motion sensor to identify birds. The device can be placed near where you would expect to see birds (backyard, bird feeder, etc.). This project utilizes several cloud resources such as: API Gateway, AWS Lambda, Amazon Rekognition, Amazon SNS, Dynamo DB, and Amazon S3:

![BirdWatcher_Diagram](https://github.com/Devardo/BirdWatcher/assets/44452354/68fa67e1-86c3-4c55-b0da-a9536dd16125)


## What You Will Need
- Raspberry Pi (any model)
- Raspberry Pi camera (Arducam is a cheaper alternative that works just as well)
- PIR motion sensor
- USB Wifi dongle (if not built in to your Pi model)
- Power supply for Raspberry Pi
- LED diode (optional)
- 5 male female jumper wires
- 1 100ohm resistor 

Wire the connections as shown in the diagram below:

![Raspberry Pi Connections (3)](https://github.com/Devardo/BirdWatcher/assets/44452354/ea60104c-32ff-433e-a8da-59e8158f1ca4)

## Future Development
- Add frontend
- Incorporate Google Cloud Vision to improve results
- Implement AI to give information for birds
