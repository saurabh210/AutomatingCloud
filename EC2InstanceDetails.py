##This Script Provides list of all EC2 instance with its details for each Region
##Please contact Saurabh Shah for any Enhancements/Modifications

try:
    import boto3,pandas as pd
except ModuleNotFoundError:
    import os
    os.system('pip install boto3 pandas')
    import boto3,pandas as pd
print("")
print("This Script Provides list of all EC2 instance with its details for each Region")
print("")

def listec2(profilename):
    print("Using Profile: {}".format(profilename))
    session = boto3.Session(profile_name=profilename)
    ec2 = session.client('ec2')
    response = ec2.describe_regions()
    coloumndict = {'InstanceId': [],'InstanceType': [],'PrivateIpAddress': [],'VpcId': [],'PublicIpAddress': []}
    maindict = {'EC2 Name': [],'State': [],'AvailabilityZone': []}
    print("")
    print("Getting the list of EC2 instances with details...")
    for region in response['Regions']:
        ec2 = session.client('ec2',region_name=region['RegionName'])
        eachresponse = ec2.describe_instances()
        for reservation in eachresponse['Reservations']:
            try:
                Tags = reservation['Instances'][0]['Tags']
                NameTag = None
                for Tag in Tags:
                    if Tag['Key'] == 'Name':
                        NameTag = (Tag['Value'])
                maindict['EC2 Name'].append(NameTag)
            except KeyError:
                maindict['EC2 Name'].append(None)
            maindict['State'].append(reservation['Instances'][0]['State']['Name'])
            maindict['AvailabilityZone'].append(reservation['Instances'][0]['Placement']['AvailabilityZone'])
            for each in list(coloumndict.keys()):
                try:
                    output = reservation['Instances'][0][each]
                except KeyError:
                    output = None
                coloumndict[each].append(output)
    maindict.update(coloumndict)
    df = pd.DataFrame(maindict)
    print(df)
    df.to_excel("AWSEC2Details.xlsx")
    print("")
    print("Data is Saved in excel with name AWSEC2Details.csv under same path from where script runs..")
    print("")

def main():
    profilename = input("Please enter aws credentials profile name: ")
    listec2(profilename)

if __name__ == '__main__':
    main()