
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

x=  {
        "GET":int(0),
        "PUT":int(0),
        "DELETE":int(0),
        "POST":int(0),
    }
y= {
        "GET":int(0),
        "PUT":int(0),
        "DELETE":int(0),
        "POST":int(0),
    }
y["GET"]=23
x=addValues(x,y)
print(str(x)+"----"+str(y))

y["PUT"]=3
x=addValues(x,y)
print(str(x)+"----"+str(y))


while(1):
    
    for i in range(60):
        request_set1=getValues("R")
        duration_set1=getValues("D")

        time.sleep(1)

        request_set2=getValues("R")
        duration_set2=getValues("D")

        temp_r=diffValues(request_set2, request_set1)
        temp_d=diffValues(duration_set2, duration_set1)

        lmr=addValues(lmr, temp_r)
        lmd=addValues(lmd, temp_d)
        
        print(str(lmr)+"___"+str(request_last_hour))
        print(lmd)

        setValues(lmr, "LMR")
        setValues(lmd, "LMD")


    request_queue.put(lmr)
    duration_queue.put(lmd)

    print(lmr)
    print(lmd)

    request_last_hour=addValues(request_last_hour, lmr)
    duration_last_hour=addValues(duration_last_hour, lmd)

    if not request_queue.empty():
        request_last_hour=diffValues(request_last_hour, request_queue.get())
    if not duration_queue.empty():
        duration_last_hour=diffValues(duration_last_hour,duration_queue.get()) 

    print(request_last_hour)
    print(duration_last_hour)
    setValues(request_last_hour, "LHR")
    setValues(duration_last_hour, "LHD")

    lmr=empty_set()
    lmd=empty_set()




