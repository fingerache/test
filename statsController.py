import json, time, random, datetime, sys
# adding locations to other modulesin different folder
from bottle import get, post, delete, put, route, run, request
import redis

#initial redis client
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def getValues(arg='R'):
    dataset={
        "GET":int(r.get(arg+"_GET")),
        "PUT":int(r.get(arg+"_PUT")),
        "DELETE":int(r.get(arg+"_DELETE")),
        "POST":int(r.get(arg+"_POST")),
    }
    return dataset

#Calculate and return average Response time
def getAvgResponseTimes(dataset_Request, dataset_Duration):
    dataset={
        "GET":0,
        "PUT":0,
        "DELETE":0,
        "POST":0,
    }
    methods=["GET", "PUT", "POST", "DELETE"]

    for method in methods:
        if dataset_Request[method] != 0:
            dataset[method]=float(float(dataset_Duration[method])/dataset_Request[method])
    
    return dataset

def stats_controller(request):
    
    #prepare the dictionary for the response
    retVal={
        "Last_Minute_Requests": getValues("LMR"),
        "Last_Minute_Avg_ResponseTime": getAvgResponseTimes(getValues("LMR"), getValues("LMD")),
        "Last_Hour_Requests": getValues("LHR"),
        "Last_Hour_Avg_ResponseTime": getAvgResponseTimes(getValues("LHR"), getValues("LHD")),
        "Total_Requests": getValues("R"),
        "Overall_Avg_ResponseTime": getAvgResponseTimes(getValues("R"), getValues("D")),
        "Total_Active_Requests": getValues("active")
    }

    return json.dumps(retVal, indent=2)

@get('/stats')
def handle_get():
    return stats_controller(request)

# @post('/process/<rpath:re:.*>')
# def handle_post(rpath=""):
#     return process_controller(request, rpath)

    
# @put('/process/<rpath:re:.*>')
# def handle_put(rpath=""):
#     return process_controller(request, rpath)

# @delete('/process/<rpath:re:.*>')
# def handle_delete(rpath=""):
#     return process_controller(request, rpath)

#for stand-alone purpose(no-concurrency)
run(server="waitress", host="localhost", port=2526, debug=True)