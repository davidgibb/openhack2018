import time
from mcstatus import MinecraftServer
from os import listdir
from os.path import isfile, join

host = "localhost"
print("Monitoring script starting")
while True:
 
   try:
      server = MinecraftServer.lookup(host)
      status = server.status()
      online = status.players.online
      capacity = status.players.max
      folder = '/data/world/playerdata'
      population = (len([f for f in listdir(folder) if isfile(join(folder, f))]))


      msg = "mcnumplayers=%d," % online \
          + "mccapacity=%d," % capacity \
          + "mcpopulation=%d" % population
   except Exception:
       msg = "Error: could not connect to minecraft server on localhost"

   print(msg)
   with open('logfile.txt','a') as f:
       f.write(msg + '\n')
   time.sleep(5)
