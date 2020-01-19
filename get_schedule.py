import httphelper
import json
import datetime

def getCalendars(auth:str, start:datetime, end:datetime, userId:str):
    
    url = "https://api-prod.hypercare.com/graphql/private"
    hypercareScope=httphelper.encodeBase64('eyJvcmdhbml6YXRpb25JZCI6NzEsInN0YXR1cyI6ImFkbWluIn0K')

    start = str(start).split(" ")
    start = start[0]+"T"+start[1]+".000Z"

    end = str(end).split(" ")
    end = end[0]+"T"+end[1]+".001Z"

    print(start, end)

    #payload = "{\"query\":\"query FetchDepartment($departmentId: Int!, $startDate: String!, $endDate: String!) {\\n    locating {\\n        department(id: $departmentId) {\\n            ...DepartmentFragment\\n        }\\n    }\\n}\\n\\nfragment GeneralUserFragment on GeneralUser {\\n    id\\n    firstname\\n    lastname\\n    username\\n}\\n\\nfragment DepartmentFragment on Department {\\n    id\\n    name\\n    roles {\\n        ...RoleFragment\\n    }\\n}\\n\\nfragment RoleFragment on Role {\\n    id\\n    name\\n    startTime\\n    duration\\n    pagerNumber\\n    site {\\n        id\\n        name\\n    }\\n    currentShift {\\n        ...ShiftFragment\\n    }\\n    nextShift {\\n        ...ShiftFragment\\n    }\\n    shifts(startDate: $startDate, endDate: $endDate) {\\n        ...ShiftFragment\\n    }\\n    createdAt\\n    updatedAt\\n}\\n\\nfragment ShiftFragment on Shift {\\n    id\\n    startDate\\n    endDate\\n    user {\\n        ...GeneralUserFragment\\n    }\\n}\\n\",\"variables\":{\"departmentId\":105,\"endDate\":\""+end+"\",\"startDate\":\""+start+"\"}}"
    payload = "{\"query\":\"query FetchShiftsInRange($departmentId: Int!, $startDate: String!, $endDate: String!) {\\n    locating {\\n        department(id: $departmentId) {\\n            roles {\\n                id\\n                shifts(startDate: $startDate, endDate: $endDate) {\\n                    ...ShiftFragment\\n                }\\n            }\\n        }\\n    }\\n}\\n\\nfragment ShiftFragment on Shift {\\n    id\\n    user {\\n        ...GeneralUserFragment\\n    }\\n    startDate\\n    endDate\\n}\\n\\nfragment GeneralUserFragment on GeneralUser {\\n    id\\n    firstname\\n    lastname\\n    username\\n}\",\"variables\":{\"departmentId\":105,\"endDate\":\""+end+"\",\"startDate\":\""+start+"\"}}"

    print('HI')
    print(payload)

    headers = {
    'hypercare-scope': hypercareScope,
    'Content-Type': 'application/json',
    'Authorization':'Bearer '+auth
    }

    response = httphelper.post(url, headers, payload)

    #print(response.status_code)
    #print(response.text.encode('utf8'))

    file = json.loads(response.text)
    print(str(file))
    prog = file["data"]["locating"]["department"]["roles"][2]["shifts"]
    print(str(prog))
    for shift in prog:
        if shift["user"]["id"] == userId:
            return False
    return True
    
    #print(response.status_code)
    #print(response.text.encode('utf8'))

def setUnavail(auth:str, userId:str, start:datetime):

    url = "https://api-prod.hypercare.com/graphql/private"
    # hypercareScope=httphelper.encodeBase64('eyJvcmdhbml6YXRpb25JZCI6NzEsInN0YXR1cyI6ImFkbWluIn0K')
    hypercareScope='eyJvcmdhbml6YXRpb25JZCI6NzEsInN0YXR1cyI6ImFkbWluIn0K'

    end = start + datetime.timedelta(hours=1)

    start = str(start).split(" ")
    start = start[0]+"T"+start[1]+".000Z"

    end = str(end).split(" ")
    end = end[0]+"T"+end[1]+".000Z"
    print(start,end)

    #payload = "{\"query\":\"mutation CreateShift($departmentId: Int!, $scheduleId: Int!, $roleId: Int!, $shiftDetails: CreateShiftDetails!) {\\n    admin {\\n        locating {\\n            department(id: $departmentId) {\\n                schedule(id: $scheduleId) {\\n                    createShift(roleId: $roleId, details: $shiftDetails) {\\n                        ...ShiftFragment\\n                    }\\n                }\\n            }\\n        }\\n    }\\n}\\n\\nfragment ShiftFragment on Shift {\\n    id\\n    user {\\n        ...GeneralUserFragment\\n    }\\n    startDate\\n    endDate\\n    createdAt\\n    updatedAt\\n}\\n\\nfragment GeneralUserFragment on GeneralUser {\\n    id\\n    firstname\\n    lastname\\n    username\\n}\",\"variables\":{\"departmentId\":105,\"scheduleId\":125,\"roleId\":300,\"shiftDetails\":{\"userId\":\""+userId+"\",\"startTime\":\""+start+"\",\"endTime\":\""+end+"\"}}}"
    payload = "{\"query\":\"mutation CreateShift($departmentId: Int!, $scheduleId: Int!, $roleId: Int!, $shiftDetails: CreateShiftDetails!) {\\n    admin {\\n        locating {\\n            department(id: $departmentId) {\\n                schedule(id: $scheduleId) {\\n                    createShift(roleId: $roleId, details: $shiftDetails) {\\n                        ...ShiftFragment\\n                    }\\n                }\\n            }\\n        }\\n    }\\n}\\n\\nfragment ShiftFragment on Shift {\\n    id\\n    user {\\n        ...GeneralUserFragment\\n    }\\n    startDate\\n    endDate\\n    createdAt\\n    updatedAt\\n}\\n\\nfragment GeneralUserFragment on GeneralUser {\\n    id\\n    firstname\\n    lastname\\n    username\\n}\",\"variables\":{\"departmentId\":105,\"scheduleId\":125,\"roleId\":300,\"shiftDetails\":{\"userId\":\""+userId+"\",\"startTime\":\""+start+"\",\"endTime\":\""+end+"\"}}}"

    print(payload)
    
    headers = {
    'hypercare-scope': hypercareScope,
    'Content-Type': 'application/json',
    'Authorization':'Bearer '+auth
    }

    response = httphelper.post(url, headers, payload)

    print(response.text.encode('utf8'))

def availability(userId:str):
    avail = []
    date = datetime.datetime.now()
    date += datetime.timedelta(days=1)
    date = date.replace(hour = 13, minute = 0, second = 0, microsecond = 0)
    end_date = date + datetime.timedelta(hours=1)
    while len(avail) < 5:
        if date.hour <= 22:
            if getCalendars("36d69d6507f3e05fc98169fcc698305e1793dc60",date, end_date, userId):
                avail.append(date)
            date += datetime.timedelta(hours=1)
            end_date += datetime.timedelta(hours=1)
        else:
            print("noo")
            date += datetime.timedelta(days=1)
            date = date.replace(hour = 13)
            end_date += datetime.timedelta(days=1)
            end_date = end_date.replace(hour = 14)
    return avail




if __name__ == '__main__':
    start = datetime.datetime(2020,1,19,13)
    end = datetime.datetime(2020,1,19,14)
    #getCalendars("36d69d6507f3e05fc98169fcc698305e1793dc60",start,end,"57bdf0d7-88bd-47c1-9b20-5a71a959c6bf")

    #print(availability('57bdf0d7-88bd-47c1-9b20-5a71a959c6bf'))
    setUnavail("18ecd0386e499c51eb77db042d13d0f8377a8edb","57bdf0d7-88bd-47c1-9b20-5a71a959c6bf",start)


