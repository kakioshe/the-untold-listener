import boto3

def uploadFile(bucket, emotion, file):
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print(bucket.name)

    data = open(file, 'rb')
    s3.Bucket(bucket).put_object(Key='{}/{}'.format(emotion,file), Body=data)


file = 'test.wav'
bucket = 'the-untold'
emotion = 'sad'
uploadFile(bucket, emotion, file)
