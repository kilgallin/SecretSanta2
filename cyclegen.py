import cherrypy
import os
import urllib
import random
import json

def getFile(filename):
  f = file(filename)
  contents = f.read()
  f.close()
  return contents

passphrase = ""
  
class Journal(object):

  def __init__(self):
    global passphrase
    passphrase = getFile('passphrase.txt')
    return

  def gen(self):
    names = ["mihir", "kartik", "keith", "ron", "jdk", "kyle"]
    previous = {"kartik" : "keith","keith" : "jdk","jdk" : "kyle","kyle" : "ron","ron" : "jeff","jeff" : "mihir","mihir" : "kartik"}
    unacceptable = True
    while unacceptable:
      random.shuffle(names)
      map = {names[i] : names[i+1] for i in range(0,5)}
      map[names[5]] = names[0]
      map["jeff"] = map["kyle"]
      map["kyle"] = "jeff"
      #map["ron"] = map["kartik"]
      #map["kartik"] = "ron"
      unacceptable = False
      for i in map.keys():
        if map[i] == previous[i]: unacceptable = True
        if previous[map[i]] == i: unacceptable = True
    for i in map.keys():
      if map[i] == "ron": map[i] = "ron. Special note: he hasn't confirmed participation yet. In the event that he's out, you have " + map["ron"]
    #map["kartik"] = "ron, who has " + map["ron"]
    print map
    query = urllib.urlencode([("username","jdk"),("password","Dragon16"),
    ("filename","targets"),("passphrase",passphrase),("text",json.dumps(map))])
    page = urllib.urlopen("https://localhost:8766/write",query)
    return "done"
  gen.exposed = True

if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.server.socket_port = 8455
    cherrypy.quickstart(Journal(), config='config.txt')