##This Script Provides Inbound Rules for a given Secuirty Group
##Please contact Saurabh Shah for any Enhancements/Modifications

try:
    import boto3,pandas as pd
except ModuleNotFoundError:
    import os
    os.system('pip install boto3 pandas')
    import boto3,pandas as pd
print("")
#print("This Script Provides Inbound Rules for a given Secuirty Group")
print("")

def SecurityGroupInboundRules(profilename,SecurityGroupID):
    session = boto3.Session(profile_name=profilename)
    ec2 = session.resource('ec2')
    security_group = ec2.SecurityGroup(SecurityGroupID)
    Maindict = {'Protocol':[],'FromPort':[],'ToPort':[],'Source':[],'Description':[]}
    for each1 in security_group.ip_permissions:
        if each1['IpProtocol'] == '-1':
            Porto = 'All Traffic'
            Port_From = 'All'
            Port_To = 'All'
        else:
            Porto = each1['IpProtocol']
            Port_From = each1['FromPort']
            Port_To = each1['ToPort']       
        
        for each2 in each1['IpRanges']:
            Maindict['Source'].append(each2['CidrIp'])
            try:
                Maindict['Description'].append(each2['Description'])
            except KeyError:
                Maindict['Description'].append(None)
            Maindict['Protocol'].append(Porto)
            Maindict['FromPort'].append(Port_From)
            Maindict['ToPort'].append(Port_To)
        
        for each3 in each1['UserIdGroupPairs']:
            Maindict['Source'].append(each3['GroupId'])
            try:
                Maindict['Description'].append(each3['Description'])
            except KeyError:
                Maindict['Description'].append(None)
            Maindict['Protocol'].append(Porto)
            Maindict['FromPort'].append(Port_From)
            Maindict['ToPort'].append(Port_To)
             
    df = pd.DataFrame(Maindict)
    df.to_excel("SecurityGroupInbound.xlsx")
    print(df)
    print("")
    print("Data is Saved in excel with name SecurityGroupInbound under same path from where script runs..")
    print("")

def main():
    profilename = input("Please enter aws credentials profile name: ")
    print("")
    SecurityGroupID = input("Please enter SecurityGroupID to get list of Inbound Rules: ")
    SecurityGroupInboundRules(profilename,SecurityGroupID)

if __name__ == '__main__':
    main()