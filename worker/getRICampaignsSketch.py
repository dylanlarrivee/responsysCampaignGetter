import requests
import json
import boto3
import xlsxwriter
import requests
import json
import boto3
import xlsxwriter
import auth

#AWS
aws_key = auth.aws_key
aws_sec_key = auth.aws_sec_key

#Prosper
user_name = auth.user_name
password = auth.password
authUrl = auth.authUrl
authToken = auth.authToken

validCampaigns = auth.validCampaigns



def getAuthToken(user_name, password, authUrl):
    data = {
        "user_name": user_name,
        "password": password,
        "auth_type": "password"
    }


    headers = {'content-type': 'application/x-www-form-urlencoded'}
    context = json.loads(requests.post(authUrl, data=data, headers=headers).text)

    if 'authToken' in context:
        print(context['authToken'])
        getAuthToken.token = context['authToken']
    elif 'errorCode' in context:
        print(context['errorCode'])



def getCampaigns(authToken,validCampaigns):
    params = '/rest/api/v1.3/campaigns?limit=200&offset=0&type=email'
    cnt = 0
    i = 1
    pythonCampaignArray = []

    #validCampaigns = ['Campaign', '2016_03_2ndLoan_1', '2016_03_2ndLoan_2_update', '2016_03_2ndLoan_3', '2016_03_PreviouslyDeclined', '2018_08_DX1', '2018_08_DX10', '2018_08_DX10_RM', '2018_08_DX11', '2018_08_DX11_RM', '2018_08_DX12', '2018_08_DX2', '2018_08_DX2_RM', '2018_08_DX3', '2018_08_DX3_RM', '2018_08_DX4', '2018_08_DX4_RM', '2018_08_DX5', '2018_08_DX5_RM', '2018_08_DX6', '2018_08_DX6_RM', '2018_08_DX7', '2018_08_DX7_RM', '2018_08_DX8', '2018_08_DX8_RM', '2018_08_DX9', '2018_08_DX9_RM', '2018_12_Abandonment_03', '2018_12_Abandonment_05', '2018_12_Abandonment_06', '2018_12_Abandonment_06_RM', '2018_12_Abandonment_08', '2018_AmOneReferral_Touch1', '2018_AmOneReferral_Touch2', '2018_Onboarding_T1', '2018_Onboarding_T3', '2018_Onboarding_T4', '2018_Onboarding_T5', '2018_Onboarding_T6', '2019_01_HELOC_NAR_Legal', '2019_03_HL_CXCall_Followup', 'API_Prod_Password_Change', 'Abandonment_01_RM_v2', 'Abandonment_01_v2', 'Abandonment_02_RM_v2', 'Abandonment_02_v2', 'Abandonment_03_RM_v2', 'Abandonment_04_RM_v2', 'Abandonment_04_v2', 'Abandonment_05_RM_v2', 'Abandonment_07_RM_v2', 'Abandonment_07_v2', 'Abandonment_08_RM_v2', 'Abandonment_09_RM_v3', 'Abandonment_09_v3', 'Abandonment_10_v3', 'EP-Automation-EM1', 'EP-Automation-EM2', 'EP-Automation-EM7', 'EP-Automation-EM8', 'EP-Automation-EM9', 'NTB_Automation_T1', 'PreListing - 2015 - App by Phone_Prod', 'PreListing - 2015 - App by Phone_Prospect_PROD']
    #validCampaigns = ['2019_BCT_Automation_Trimail', '2019_BCT_Automation_Primary', '2019_BCT_Automation_Remail']

    while i == 1:

        endpoint = 'https://api2-023.responsys.net' + params
        #endpoint = 'https://api5-021.responsys.net' + params
        headers = {'Authorization': authToken, 'Content-Type': 'application/json'}
        campaignsResponse = json.loads(requests.get(url=endpoint, headers=headers).text)

        #print(json.dumps(campaignsResponse, sort_keys=True, indent=4))

        #print(campaignsResponse['links'])
        #print(campaignsResponse['campaigns'][0]['name'])
        #print(campaignsResponse['campaigns'])
        print(campaignsResponse)

        for ii in campaignsResponse['campaigns']:
            if ii['name'] in validCampaigns:
                #print(ii)
                pythonCampaignArray.append(ii)
        params = campaignsResponse['links'][1]['href']
        print(params)

        moreCampaignsTest = False
        x = 1
        for ii in campaignsResponse['links']:
            print(ii)
            if ii['rel'] == 'next':
                moreCampaignsTest = True
            x += 1
        print('new page')
        if moreCampaignsTest == False:
            print('end of campaigns')
            break

    jsonCampaignPythonDict = {}
    jsonCampaignPythonDict['campaigns'] = pythonCampaignArray
    #print(jsonCampaignPythonDict['campaigns'])
    getCampaigns.jsonCampaignPythonDict = jsonCampaignPythonDict
    #print(json.dumps(jsonCampaignPythonDict, sort_keys=True, indent=4))
    print('jsonCampaignPythonDict')
    print(jsonCampaignPythonDict)

def campaignPetGetter(jsonCampaignPythonDict):
    profileListArray = []
    dataSourceTableArray = []
    for i in jsonCampaignPythonDict['campaigns']:
        print('Campaign Data Source Tables:')
        for ii in i['supplementaryCampaignDataSourcePaths']:
            dataSourceTableArray.append(ii.split('/')[1])
            folder = ii.split('/')[0]
            tableName = ii.split('/')[1]
            print('Folder: ' + folder)
            print('Table Name: ' + tableName)
        print(dataSourceTableArray)
        print('Campaign Contacts List:')
        print(profileListArray)
        profileListArray.append(i['listName'])
        campaignPetGetter.listName = profileListArray[0]
        campaignPetGetter.dataSourceTableArray = dataSourceTableArray

def getPets(authToken,listName,validPets):

    params = '/rest/api/v1.3/lists/' + listName + '/listExtensions'
    cnt = 0
    pythonPetsArray = []


    endpoint = 'https://api2-023.responsys.net' + params
    # endpoint = 'https://api5-021.responsys.net' + params
    headers = {'Authorization': authToken, 'Content-Type': 'application/json'}
    petsResponse = json.loads(requests.get(url=endpoint, headers=headers).text)

    # print(json.dumps(campaignsResponse, sort_keys=True, indent=4))

    print(petsResponse)

    for i in petsResponse:
        if i['profileExtension']['objectName'] in validPets:
            # print(ii)
            pythonPetsArray.append(i)
    print('pythonPetsArray')
    print(json.dumps(pythonPetsArray, sort_keys=True, indent=4))

    jsonPetsPythonDict = {}
    jsonPetsPythonDict['PETs'] = pythonPetsArray
    # print(jsonPetsPythonDict['PETs'])
    getPets.jsonPetsPythonDict = jsonPetsPythonDict
    # print(json.dumps(jsonPetsPythonDict, sort_keys=True, indent=4))
    print('jsonPetsPythonDict')
    print(jsonPetsPythonDict)


def finalPayloadFormatter(jsonCampaignPythonDict, jsonPetsPythonDict):
    jsonPythonArray = []
    jsonPythonArray.insert(0, jsonCampaignPythonDict)
    jsonPythonArray.insert(1, jsonPetsPythonDict)
    jsonPythonArray = json.dumps(jsonPythonArray, indent=2, sort_keys=True)
    with open('test1.json', 'w') as json_file:
        json_file.write(jsonPythonArray)
    finalPayloadFormatter.jsonPythonArray = jsonPythonArray
    print('jsonPythonArray')
    print(json.dumps(jsonPythonArray, sort_keys=True, indent=4))

def awsS3Dump(aws_key,aws_sec_key,jsonPythonArray):
    s3 = boto3.resource('s3', aws_access_key_id=aws_key, aws_secret_access_key=aws_sec_key)
    content = jsonPythonArray
    s3.Object('ssdataflobe', 'dev/sketch/BCT_Automation_Program.json').put(Body=content,ContentType='application/jsonl', ACL='public-read')

# Need to pull in all campaigns by looping through the limits and offsets. Then need to go through all
# of the campaigns and only include the ones from the list. Then need to put those campaigns into a json payload


getCampaigns(authToken, validCampaigns)
campaignPetGetter(getCampaigns.jsonCampaignPythonDict)
getPets(authToken, campaignPetGetter.listName, campaignPetGetter.dataSourceTableArray)
finalPayloadFormatter(getCampaigns.jsonCampaignPythonDict, getPets.jsonPetsPythonDict)
awsS3Dump(aws_key,aws_sec_key,finalPayloadFormatter.jsonPythonArray)