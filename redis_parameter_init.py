import redis
#initial redis client
r = redis.StrictRedis(host='localhost', port=6379, db=0)


#params for all active connection
r.set("active_GET",0)
r.set("active_DELETE",0)
r.set("active_PUT",0)
r.set("active_POST",0)

#params for cumulative requests/method
r.set("R_GET",0)
r.set("R_DELETE",0)
r.set("R_PUT",0)
r.set("R_POST",0)

#params for cumulative time/method
r.set("D_GET",1)
r.set("D_DELETE",1)
r.set("D_PUT",1)
r.set("D_POST",1)

#last min params request
r.set("LMR_GET",0)
r.set("LMR_PUT",0)
r.set("LMR_POST",0)
r.set("LMR_DELETE",0)

#last min params time
r.set("LMD_GET",1)
r.set("LMD_PUT",1)
r.set("LMD_POST",1)
r.set("LMD_DELETE",1)

#last hour params request
r.set("LHR_GET",0)
r.set("LHR_PUT",0)
r.set("LHR_POST",0)
r.set("LHR_DELETE",0)

#last hour params time
r.set("LHD_GET",1)
r.set("LHD_PUT",1)
r.set("LHD_POST",1)
r.set("LHD_DELETE",1)