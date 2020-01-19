import httphelper
import datetime
import json

def getSched(auth:str,startDate:datetime, endDate:datetime):
    
    url = "https://api-prod.hypercare.com/graphql/private"
    hypercareScope = httphelper.encodeBase64('eyJvcmdhbml6YXRpbklkIjo3MSwic3RhdHVzIjoiYWRtaW4ifQo=')

    start = startDate.isoformat() + ".000-05:00"
    # start = str(startDate).split(" ")
    # start = start[0]+"T"+start[1]+".000Z"

    print(start)

    end = endDate.isoformat() + ".000-05:00"
    # end = str(endDate).split(" ")
    # end = end[0]+"T"+end[1]+".000Z"

    print(end)

    # payload = "{\"query\":\"query FetchSchedules($startDate: String!, $endDate: String!) {\\n    me {\\n        organizations {\\n            sites {\\n                departments {\\n                    id\\n                    name\\n                    schedules(startDate: $startDate, endDate: $endDate) {\\n                        ...ScheduleFragment\\n                    }\\n                    # roles {\\n                    #     ...RoleFragment\\n                    # }\\n                }\\n            }\\n        }\\n    }\\n}\\n\\nfragment ScheduleFragment on Schedule {\\n    id\\n    name\\n    startDate\\n    endDate\\n    state\\n    createdAt\\n    updatedAt\\n    shifts(startDate: $startDate, endDate: $endDate) {\\n        ...ShiftFragment\\n    }\\n}\\n\\n# fragment RoleFragment on Role {\\n#     id\\n#     name\\n#     startTime\\n#     endTime\\n#     shifts(startDate: $startDate, endDate: $endDate) {\\n#         ...ShiftFragment\\n#     }\\n# }\\n\\nfragment ShiftFragment on Shift {\\n    id\\n    user {\\n        ...PublicUserFragment\\n    }\\n    startDate\\n    endDate\\n}\\n\\nfragment PublicUserFragment on GeneralUser {\\n    id\\n    firstname\\n    lastname\\n    username\\n}\",\"variables\":{\"startDate\":\""+start+"\",\"endDate\":\""+end+"\"}}"
    payload = {
        "query": '''
        query FetchSchedules($startDate: String!, $endDate: String!) {
    me {
        organizations {
            sites {
                departments {
                    id
                    name
                    schedules(startDate: $startDate, endDate: $endDate) {
                        ...ScheduleFragment
                    }
                    # roles {
                    #     ...RoleFragment
                    # }
                }
            }
        }
    }
}

fragment ScheduleFragment on Schedule {
    id
    name
    startDate
    endDate
    state
    createdAt
    updatedAt
    shifts(startDate: $startDate, endDate: $endDate) {
        ...ShiftFragment
    }
}

# fragment RoleFragment on Role {
#     id
#     name
#     startTime
#     endTime
#     shifts(startDate: $startDate, endDate: $endDate) {
#         ...ShiftFragment
#     }
# }

fragment ShiftFragment on Shift {
    id
    user {
        ...PublicUserFragment
    }
    startDate
    endDate
}

fragment PublicUserFragment on GeneralUser {
    id
    firstname
    lastname
    username
}''',
    "variables": {
        "startDate": start,
        "endDate": end
    }
    }

    headers = {
    'hypercare-scope': hypercareScope,
    'Content-Type': 'application/json',
    'Authorization':'Bearer '+auth
    }

    print(json.dumps(payload))

    response = httphelper.post(url, headers, json.dumps(payload))
    
    print(response.status_code)
    print(response.text.encode('utf8'))

if __name__ == '__main__':
    start = datetime.datetime(2020,1,1)
    end = datetime.datetime(2020,2,1)
    getSched("36d69d6507f3e05fc98169fcc698305e1793dc60",start,end)


