
import json, time, random, datetime, sys
# adding locations to other modulesin different folder
from bottle import Bottle, get, post, delete, put, route, run, request
import redis

#initial redis client
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# baseapp = Bottle()
# app = Bottle()
# baseapp.mount("/test/", app)



#===========================================PROCESS_CONTROLLER===================================================
def process_req(request, rpath="",):
    
    #parsing request body
    body = request.body.read().decode("utf-8")

    #declare dictionary for 
    retVal={
        "time": str(datetime.datetime.now()),
        "method": request.method,
        "headers": {},
        "path": rpath,
        "query": {},
        "body": body,
        "duration": "0"
    }

    #fill header dictionary
    for header in request.headers:
        retVal["headers"][str(header)]=str(request.headers[header])

    #fill query dictionary
    for key in request.query:
        retVal["query"][str(key)]=str(request.query[key])

    #getting random duration between 10-15 seconds
    duration=random.randint(10,15)
    retVal["duration_"]=str(duration)

    time.sleep(duration)

    return json.dumps(retVal, indent=2), duration


def process_controller(request, rpath=""):
    r.incrby("active_"+request.method, 1)
    response, duration = process_req(request, rpath)
    r.incrby("active_"+request.method, -1)
    r.incrby("R_"+request.method, 1)
    r.incrby("D_"+request.method, duration)
    return response

@get('/process/<rpath:re:.*>')
def handle_get(rpath=""):
    return process_controller(request, rpath)

@post('/process/<rpath:re:.*>')
def handle_post(rpath=""):
    return process_controller(request, rpath)

    
@put('/process/<rpath:re:.*>')
def handle_put(rpath=""):
    return process_controller(request, rpath)

@delete('/process/<rpath:re:.*>')
def handle_delete(rpath=""):
    return process_controller(request, rpath)


#==================================================STATS_CONTROLLER================================================

def getValues(arg='R'):
    dataset={
        "GET":int(r.get(arg+"_GET")),
        "PUT":int(r.get(arg+"_PUT")),
        "DELETE":int(r.get(arg+"_DELETE")),
        "POST":int(r.get(arg+"_POST")),
    }
    return dataset



def stats_controller(request, rpath="",):
    
    #declare dictionary for 
    retVal={
        "LMR": getValues("LMR"),
        "LHR": getValues("LHR"),
        "R": getValues("R"),
        "D": getValues("D"),
    }

    return json.dumps(retVal, indent=2)

@get('/stats<rpath:re:[.]*|>')
def handle_get(rpath=""):
    return stats_controller(request, rpath)



#============================================for stand-alone purpose===============================================
run(server='waitress', host="localhost", port=2525, debug=True)

