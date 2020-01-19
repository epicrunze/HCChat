import base64
import helperlists
import httphelper
import authentication
import fetchUtils
import datetime

class Chatbot():
    def __init__(self, username, password, chatId, orgId):
        clientId = "uofthacksteam2"
        clientSecret = "Lu7qXWP3b3d3"
        self.hypercareScope = httphelper.encodeBase64("organizationId:" + str(orgId))
        self.accessToken = authentication.getAuthKey(username, password, clientId, clientSecret)[0]
        self.chatId = chatId
        self.type = None
        self.mode = None
        self.process = None
    
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
            if word in helperlists.mode1:
                m1 += 1
            if word in helperlists.mode2:
                m2 += 1
            if self.type == "doctor" and word in helperlists.mode3:
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
    
    def parseString(self, string):
        if string == "reset":
            self.type = None
            self.mode = None
            self.process = None

        if self.process is None:
            self.process = "checktype"
            return "Are you a patient or a doctor?"

        if self.process == "checktype":
            if self.patOrDoc(string):
                self.process = "checkmode"
                return "Thanks for your response {}".format(self.type)
            else:
                return "Please try again"

        if self.process == "checkmode":
            if self.menuParse(string):
                if self.mode == 1:
                    self.process = "1-symptoms"
                    return "Please list your symptoms"
                elif self.mode == 2:
                    #extract doctor's name
                    self.process = "2-docappt"
                    doctorName = None
                    return "Would you like to book an appointment with {}?".format(doctorName)
                elif self.mode == 3:
                    self.process = "checkmode"
                    return "placeholder menu parse"#FIND DOCTOR FUNCTION

        if self.process == "1-symptoms":
            self.process = "checkmode"
            return "placeholder diagnosis"#DIAGNOSIS FUNCTION
        
        if self.process == "2-docappt":
            yes = 0
            no = 0
            for word in string.lower().split():
                if word in helperlists.yes:
                    yes += 1
                elif word in helperlists.no:
                    no += 1
            if yes > 0 or no > 0:
                if yes > no:
                    self.process = "2-rectime"
                    return "placeholder cal"#calendar function
                else:
                    self.process = "checkmode"
                    return "Ok, anything else you would like?"
            else:
                return "Please say yes or no"
        
        if self.process == "2-rectime":
            #string.lower().split()[0]
            self.process = "checkmode"
            return "Your appointment is booked!"
        
    def findPerson(self, string):
        return

