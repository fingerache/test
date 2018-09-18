import time, redis, queue

#initialize redis client
r = redis.StrictRedis(host='localhost', port=6379, db=0)
print("Connection established with redis-server @localhost:6379")


def empty_set():
    return {
        "GET":int(0),
        "PUT":int(0),
        "DELETE":int(0),
        "POST":int(0),
    }

#get Values from Redis
def getValues(arg='R'):
    dataset={
        "GET":int(r.get(arg+"_GET")),
        "PUT":int(r.get(arg+"_PUT")),
        "DELETE":int(r.get(arg+"_DELETE")),
        "POST":int(r.get(arg+"_POST")),
    }
    return dataset

#get Values to Redis
def setValues(dataset, arg='LM'):
    r.set(arg+"_GET",dataset["GET"])
    r.set(arg+"_PUT",dataset["PUT"])
    r.set(arg+"_POST",dataset["POST"])
    r.set(arg+"_DELETE",dataset["DELETE"])


def diffValues(dataset1, dataset2):
    diffDataSet= {
        "GET":int(dataset1["GET"])-int(dataset2["GET"]),
        "POST":int(dataset1["POST"])-int(dataset2["POST"]),
        "PUT":int(dataset1["PUT"])-int(dataset2["PUT"]),
        "DELETE":int(dataset1["DELETE"])-int(dataset2["DELETE"]),
    }
    return diffDataSet

def addValues(dataset1, dataset2):
    sumdataSet= {
        "GET":int(dataset1["GET"])+int(dataset2["GET"]),
        "POST":int(dataset1["POST"])+int(dataset2["POST"]),
        "PUT":int(dataset1["PUT"])+int(dataset2["PUT"]),
        "DELETE":int(dataset1["DELETE"])+int(dataset2["DELETE"]),
    }
    return sumdataSet


#creating queues to keep track of the last 60 mins of statistics
request_queue=queue.Queue()
duration_queue=queue.Queue()

print("All initial values fetched from the redis-server")
print("Monitoring and Updating Values in progress..")

lmr=empty_set()
lmd=empty_set()
request_last_hour=empty_set()
duration_last_hour=empty_set()

while(1):
    
    for i in range(60):

        # sampling after 1 second interval
        request_set1=getValues("R")
        duration_set1=getValues("D")

        time.sleep(1)

        request_set2=getValues("R")
        duration_set2=getValues("D")

        #getting all the samples fetched during the sampling period
        temp_r=diffValues(request_set2, request_set1)
        temp_d=diffValues(duration_set2, duration_set1)

        #updating last minute requests and duration
        lmr=addValues(lmr, temp_r)
        lmd=addValues(lmd, temp_d)

        #setting last min values in Redis
        setValues(lmr, "LMR")
        setValues(lmd, "LMD")

    #updating the values for the last 60 mins
    request_last_hour=addValues(request_last_hour, lmr)
    duration_last_hour=addValues(duration_last_hour, lmd)

    #values from the queue is not popped until the queue has data of the last 60mins
    if not request_queue.empty() and request_queue.qsize() >= 60 :
        request_last_hour=diffValues(request_last_hour, request_queue.get())
    if not duration_queue.empty() and duration_queue.qsize() >= 60 :
        duration_last_hour=diffValues(duration_last_hour,duration_queue.get()) 

    #updating the queue with last minute
    request_queue.put(lmr)
    duration_queue.put(lmd)

    #setting values for the last 60 mins in Redis
    setValues(request_last_hour, "LHR")
    setValues(duration_last_hour, "LHD")

    lmr=empty_set()
    lmd=empty_set()





    
    