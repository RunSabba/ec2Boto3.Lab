#ec2 scripting hands on to create and manage ec2 instances using Boto3

import boto3

#create ec2 resource and name your instance. I kept getting an ImageID "AMI-..." doesnt exist. Found info saying that adding the region name resolves this.
ec2 = boto3.resource('ec2', region_name= 'us-east-2')
instance_name = 'AAN-ec2'

#store the instance id
instance_id = None


#create a list of all our instances.
instances = ec2.instances.all()
instance_exists = False

#nested4loop to check for instance name within or instance's list by the Tags.Using this to make sure we dont create another ec2 with once that already exists.
for instance in instances:
    for tag in instance.tags:
        if tag ['Key'] == 'Name' and tag ['Value'] == instance_name:
            instance_exists = True
            instance_id = instance.id
            print(f"An instance name {instance_name}'with ID'{instance_id}'already exists")
            break
        if instance_exists:
            break
        

if not instance_exists:
#launch a new ec2 instance if it hasn't been created yet.
    new_instance = ec2.create_instances(
            ImageId='ami-0ccabb5f82d4c9af5', 
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName="",
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name', 
                            'Value': instance_name
                        },    
                    ]    
                },
            ]
        )
    instance_id = new_instance[0].id
    print(f"An instance name {instance_name}'with ID'{instance_id}'created")
    
#stop an instance
ec2.Instance(instance_id).stop()
print(f"An instance name {instance_name}-{instance_id}'Has been Stopped")

#start an instance
#c2.Instance(instance_id).start()
#rint(f"An instance name {instance_name}-{instance_id}'Has been started")

#Terminate an instance
#c2.Instance(instance_id).terminate()
#rint(f"An instance name {instance_name}-{instance_id}'Has been Terminated")
