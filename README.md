# test
read README before install/execution

#=====================Prerequisites===================================
1.Redis must be installed
2.Python version >= 3.6.2

#=====================Abbreviations in Code===========================
LMR=> Last Minute Requests
LMD=> Last Minute Duration on all requests

LHR=>Last Hour Requests
LHD=> Last Hour Duration on all requests

#====================Installation and Execution=======================
1.execute ./startInstall.sh withll required permission, if any
  for initial services set ups and configuration including running redis-server  

2.execute ./startServices.sh for starting listening at the given endpoints
(these would: (a) /process/* (b)/stats )

