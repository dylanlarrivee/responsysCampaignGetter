from worker import test_worker
from worker import auth
import json



listName1 = 'CONTACTS_LIST'

def run():
    test_worker.getAuthToken(auth.user_name, auth.password, auth.authUrl)
    test_worker.getCList(test_worker.getAuthToken.token, auth.pod)

    test_worker.getPet(test_worker.getAuthToken.token, test_worker.getCList.jsonCListPythonDict, auth.pod)

    #test_worker.cListUpdtTblHt(test_worker.getCList.jsonCListPythonDict, test_worker.getPet.jsonPetPythonDict)
    
    test_worker.finalPayloadFormatter(test_worker.getCList.jsonCListPythonDict, test_worker.getPet.jsonPetPythonDict)

    test_worker.awsS3Dump(auth.aws_key, auth.aws_sec_key, test_worker.finalPayloadFormatter.jsonPythonArray)
    

if __name__ == '__main__':
    run()