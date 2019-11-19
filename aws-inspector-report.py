##This Script provides you AWS Inspector Findings Report of Current Month from Ative Region having Maximum EC2 Instances
##Please contact Saurabh Shah for any Enhancements/Modifications
import os,pip
try:
    import boto3
except ModuleNotFoundError:
    os.system('pip install boto3')
    import boto3
print("")
print("This Script provides you AWS Inspector Findings Report of Current Month from Ative Region having Maximum EC2 Instances..")
print("")
def activeregion(access_key,secret_key,session_key):
    ec2 = boto3.client('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_key)
    response = ec2.describe_regions()
    ec2count = {}
    for region in response['Regions']:
        vm = boto3.client('ec2',aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_key,region_name=region['RegionName'])
        eachresponse = vm.describe_instances()
        count = 0
        for reservation in eachresponse['Reservations']:
            for instance in reservation["Instances"]:
                count += 1
        ec2count.update({region['RegionName']:count})
    for key , value in ec2count.items():
        if max(ec2count.values()) == value:
            print("")
            print ("Getting AWS-Inspector Findings Report from {} Region..".format(key))
            return key

def awsinspector(region,access_key,secret_key,session_key):
    
    from urllib import request
    from datetime import datetime
    import time
    today = datetime.today()
    inspector = boto3.client('inspector',aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_key,region_name=region)
    responselist = inspector.list_assessment_runs(filter={'states':['COMPLETED'],'startTimeRange': {'beginDate': datetime(today.year, today.month, 1)}})
    if responselist['assessmentRunArns'] != []:
        uniqunumber = 1
        for eacharn in responselist['assessmentRunArns']:
            responsereport = inspector.get_assessment_report(
            assessmentRunArn=eacharn,
            reportFileFormat='PDF',
            reportType='FINDING')
            time.sleep(5)
            url = responsereport['url']
            path = os.environ['USERPROFILE']
            request.urlretrieve(url, path+"/Documents/aws-inspector-findings-report-{}.pdf".format(uniqunumber))
            uniqunumber+=1
        print("")
        print("AWS inspector reports downloaded to %userprofile%\Documents Folder.Please validate")
        print("")
    else:
        print("")
        print("cannot find any assesment reports available to download for this month. Please login to console and validate")
        print("")
def main():
    access_key = input("please enter access key id:")
    secret_key = input("please enter secret key id:")
    session_key = input("please enter session key id:")
    region = activeregion(access_key,secret_key,session_key)
    awsinspector(region,access_key,secret_key,session_key)

if __name__ == '__main__':
    main()