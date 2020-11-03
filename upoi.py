from serialize import *
from ob import *

line = "\n"
splitter = "|"

class UPOI:
  def __init__(self, filePath): 
    self.file = Serialize(filePath, "upoi")
    raw: str = self.file.read()
    while raw[-1:] == "\n" or raw[-1:] == " " or raw[-1:] == "\t":
      raw = raw[:-1]

    split = raw.split(line)
    self.types = split[0].split(splitter)
    split.pop(0)

    self.data = []
    for d in split:
      o = Object()
      self.data.append(o)

      q = d.split(splitter)
      for i in range(len(q)):
        setattr(o, self.types[i], q[i])



  def save(self): 
    s = splitter.join(self.types) + line
    for ob in self.data:
      for name in self.types:
        if not hasattr(ob, name): 
          setattr(ob, name, "")
        s += getattr(ob, name) + splitter
      
      s = s[:-1]
      s += line
      

    self.file.write(s)

    
  
        


