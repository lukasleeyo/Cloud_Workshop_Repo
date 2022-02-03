from Backend.initGCP import InitGCP
# Initialize to GCP
GCP_DB = InitGCP.initDB()


class UsersDB:
    # Check if user is registered using their gmail account
    def checkAccount(userID):
        try:
            # Create a reference to the Users collection
            users_ref = GCP_DB.collection(u'Users')

            # Create a query against the collection
            query_ref = users_ref.where(u'userID', u'==', userID).get()
            for doc in query_ref:
                return userID == doc.to_dict()['userID']
        except:
            print("check_account_error")
            return "check_account_error"

    # check if name already exist in db
    def checkName(account, name):
        try:
            users_ref = GCP_DB.collection(u'Users')
            query_ref = users_ref.where(u'userID', u'!=', account).where(
                u'name', u'==', name).get()
            return not bool(query_ref)
        except:
            print("check_name_error")
            return "check_name_error"

    # get name by userID
    def getName(userID):
        try:
            users_ref = GCP_DB.collection(u'Users')
            query_ref = users_ref.where(u'userID', u'==', userID).get()
            if bool(query_ref):
                for doc in query_ref:
                    return doc.to_dict()['name']
            else:
                return ""
        except:
            print("get_name_error")
            return "get_name_error"

    # update name by userID and new name
    def setName(userID, name):
        try:
            users_ref = GCP_DB.collection(u'Users').document(userID)
            users_ref.update({u'name': name})
        except:
            print("set_name_error")
            return "set_name_error"
