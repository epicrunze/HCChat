import base64
import modetokens
class Chatbot():
    def __init__(self, accessToken, userId, orgId):
        self.hypercareScope = base64.b64encode('organizationId:{}'.format(orgId))
        self.accessToken = accessToken
        self.userId = userId
        self.type = None
        self.mode = None
    
    def patOrDoc(self, string):
        parsedString = string.strip().lower()
        if parsedString == "patient":
            self.type = "patient"
            return True
        elif parsedString == "doctor":
            self.type = "doctor"
            return True
        return False

    def menuParse(self, string):
        '''
        Menu options:
        1 -> Diagnosis
        2 -> Make appointment
        3 -> Find person
        '''

        m1, m2, m3 = 0, 0, 0
        for word in string.lower().split():
            if word in modetokens.mode1:
                m1 += 1
            if word in modetokens.mode2:
                m2 += 1
            if word in modetokens.mode3:
                m3 += 1
        
        if m1 > m2 and m1 > m3:
            self.mode = 1
        elif m2 > m1 and m2 > m3:
            self.mode = 2
        elif m3 > m2 and m3 > m1:
            self.mode = 3
        else:
            return False
        return True

    


        