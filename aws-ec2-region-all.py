##This Script provides Provides number of EC2 instances for each Region
##Please contact Saurabh Shah for any Enhancements/Modifications
import os,pip
try:
    import boto3
except ModuleNotFoundError:
    os.system('pip install boto3')
    import boto3
print("")
print("This Script provides Provides number of EC2 instances for each Region")
print("")
def activeregion(access_key,secret_key,session_key):
    ec2 = boto3.client('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_key)
    response = ec2.describe_regions()
    ec2count = {}
    for region in response['Regions']:
        vm = boto3.client('ec2', aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_key,region_name=region['RegionName'])
        eachresponse = vm.describe_instances()
        count = 0
        for reservation in eachresponse['Reservations']:
            for instance in reservation["Instances"]:
                count += 1
        ec2count.update({region['RegionName']:count})
    print("")
    print("Below is Mapping of Region : number of EC2 instances")
    print("")
    for key , value in ec2count.items():
        print (key + " : " + str(value))
        if max(ec2count.values()) == value:
            max_region = key
    print("")
    print ("Region with maximum EC2 instance is {}".format(max_region))
    print("")

def main():
    access_key = input("please enter access key id:")
    secret_key = input("please enter secret key id:")
    session_key = input("please enter session key id:")
    activeregion(access_key,secret_key,session_key)

if __name__ == '__main__':
    main()