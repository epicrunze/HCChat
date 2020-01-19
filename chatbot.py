import base64
import helperlists
import authentication
import fetchUtils
import datetime
import message
import firebasehelper
import get_schedule


def initialize(chatId, username, password, clientId, clientSecret, userId):
    accessToken = authentication.getAuthKey(username, password, clientId, clientSecret)[0]
    orgId = 71
    identity = authentication.getId(accessToken, orgId)
    data = {str(chatId): {"type": "None",
                            "mode": "None",
                            "process": "None",
                            "hypercareScope": "eyJvcmdhbml6YXRpb25JZCI6NzEsInN0YXR1cyI6ImFkbWluIn0K",
                            "accessToken": accessToken,
                            "id": identity,
                            "userId": str(userId),
                            "chatId": str(chatId),
                            "defaultDoc": "None",
                            "docAvail": "None",
                            "orgId": orgId
                            }
                        }
    return firebasehelper.writeData(data)


def patOrDoc(chatId, string, data):
    parsedString = string.strip().lower()
    if parsedString == "patient":
        data["type"] = "patient"
        return True
    elif parsedString == "doctor":
        data["type"] = "doctor"
        return True
    return False

def menuParse(chatId, string, data):
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
        if data['type'] == "doctor" and word in helperlists.mode3:
            m3 += 1
    
    if m1 > m2 and m1 > m3:
        data['mode'] = 1
    elif m2 > m1 and m2 > m3:
        data['mode'] = 2
    elif m3 > m2 and m3 > m1:
        data['mode'] = 3
    else:
        return False
    return True

def parseString(chatId, string):
    data = firebasehelper.getDict(chatId)
    if string == "reset":
        data["type"] = "None"
        data["mode"] = "None"
        data["process"] = "None"

    if data["process"] == "None":
        data["process"] = "checktype"
        firebasehelper.writeDict(data, chatId)
        return "Are you a patient or a doctor?"

    if data["process"] == "checktype":
        if patOrDoc(chatId, string, data):
            data["process"] = "checkmode"
            firebasehelper.writeDict(data, chatId)
            return "Thanks for your response {}".format(data["type"].capitalize())
        else:
            firebasehelper.writeDict(data, chatId)
            return "Please try again"

    if data["process"] == "checkmode":
        if menuParse(chatId, string, data):
            if data["mode"] == 1:
                data["process"] = "1-symptoms"
                firebasehelper.writeDict(data, chatId)
                return "Please list your symptoms"
            elif data["mode"] == 2:
                nameTup = fetchUtils.fetchName(string)
                if nameTup[0] == "user":
                    data["process"] = "2-docappt"
                    data["defaultDoc"] = list(nameTup)
                    doctorName = nameTup[2]
                    firebasehelper.writeDict(data, chatId)
                    return "Would you like to book an appointment with {}?".format(doctorName)
                else:
                    firebasehelper.writeDict(data, chatId)
                    return "Try another doctor"
            elif data["mode"] == 3:
                data["process"] = "checkmode"
                if findPerson(chatId, string):
                    data["process"] = "checkmode"
                    firebasehelper.writeDict(data, chatId)
                    return None
                else:
                    data["process"] = "checkmode"
                    firebasehelper.writeDict(data, chatId)
                    return "Department finding will be implemented"
    if data["process"] == "1-symptoms":
        data["process"] = "checkmode"
        firebasehelper.writeDict(data, chatId)
        return "placeholder diagnosis"#DIAGNOSIS FUNCTION

    if data["process"] == "2-docappt":
        yes = 0
        no = 0
        for word in string.lower().split():
            if word in helperlists.yes:
                yes += 1
            elif word in helperlists.no:
                no += 1
        if yes > 0 or no > 0:
            if yes > no:
                data["process"] = "2-rectime"
                availList = get_schedule.availability(data["accessToken"],data["defaultDoc"][1])
                data["docAvail"] = str(availList)
                print(data)
                print(firebasehelper.writeDict(data, chatId))
                outputString = ""
                for num, time in enumerate(availList):
                    time -= datetime.timedelta(hours=5)
                    outputString += str(num+1) + ") " + time.strftime("%c") + " "
                string = "Here are some available appointment times: {}".format(outputString)
                return string
            else:
                data["process"] = "checkmode"
                firebasehelper.writeDict(data, chatId)
                return "Ok, anything else you would like?"
        else:
            firebasehelper.writeDict(data, chatId)
            return "Please say yes or no"
    
    if data["process"] == "2-rectime":
        choice = ''
        for i in range(5):
            if str(i+1) in string:
                choice = i+1
                break
        if choice:
            get_schedule.setUnavail(data["accessToken"], eval(data["defaultDoc"])[1], eval(data["docAvail"])[int(choice)-1])
            data["process"] = "checkmode"
            firebasehelper.writeDict(data, chatId)
            return "Your appointment is booked!"
        else:
            data["process"] = "checkmode"
            firebasehelper.writeDict(data, chatId)
            return "Try again"
    
def findPerson(chatId, string):
    data = firebasehelper.getDict(chatId)
    identity = fetchUtils.fetchName(string)
    if identity[0] == "user":
        idList = [data["userId"], identity[1]]
        writeString = "We have brought you two together to chat"
        fetchUtils.newChat(idList, writeString, data["accessToken"], data["hypercareScope"], int(data["orgId"]))
        firebasehelper.writeDict(data, chatId)
        return True
    firebasehelper.writeDict(data, chatId)
    return False

if __name__ == "__main__":
    chatId = "1"
    initialize("1", "chatbot", "chat@bot", "uofthacksteam2", "Lu7qXWP3b3d3", "23a58200-58c0-49a4-b359-e40f0a47d4f7")
    print(parseString(chatId, "Hello"))
    print(parseString(chatId, "patient"))
    print(parseString(chatId, "book appointment with ryan"))
    print(parseString(chatId, "yes"))
    #print(parseString(chatId, "1"))
