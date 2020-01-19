import httphelper
import datetime

def sendMessage(auth:str,orgId:str,startDate:datetime, endDate:datetime):
    
    url = "https://api-prod.hypercare.com/graphql/private"
    #hypercareScope = httphelper.encodeBase64('{"Id":'+str(orgId)+'}')

    payload = "{\"query\":\"mutation CreateSchedule($departmentId: Int!, $scheduleDetails: CreateScheduleDetails!) {\\n    admin {\\n        locating {\\n            department(id: $departmentId) {\\n                createSchedule(details: $scheduleDetails) {\\n                    ...ScheduleFragment\\n                }\\n            }\\n        }\\n    }\\n}\\n\\nfragment ScheduleFragment on Schedule {\\n    id\\n    name\\n    startDate\\n    endDate\\n    state\\n    createdAt\\n    updatedAt\\n}\",\"variables\":{\"scheduleDetails\":{\"name\":\"Long Schedule\",\"startDate\":\"2019-10-30T00:00:00.000Z\",\"endDate\":\"2019-10-31T23:59:59.999Z\"},\"departmentId\":105}}"

    headers = {
    'hypercare-scope': orgId,
    'Content-Type': 'application/json',
    'Authorization':'Bearer '+auth
    }

    response = httphelper.post(url, headers, payload)
    
    print(response.status_code)
    print(response.text.encode('utf8'))

if __name__ == '__main__':
    sendMessage("36d69d6507f3e05fc98169fcc698305e1793dc60","eyJvcmdhbml6YXRpb25JZCI6NzEsInN0YXR1cyI6ImFkbWluIn0K",datetime.datetime(2020,1,1),datetime.datetime(2020,1,2))


