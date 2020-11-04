from serialize import *
from ob import *

line = "\n"
splitter = "|"

class UPOI:
  def __init__(self, filePath, predefinedHeader = None, onChange = None): 
    changeCB = None
    self._predefinedHeader = predefinedHeader
    if onChange != None:
      def c(content):
        nonlocal changeCB
        self._parse(content)
        onChange()

      changeCB = c
        

    self.file = Serialize(filePath, "upoi", changeCB)
    raw = self.file.read()
    self._parse(raw)
    
  # Parse the string
  def _parse(self, raw: str):
    while raw[-1:] == "\n" or raw[-1:] == " " or raw[-1:] == "\t":
      raw = raw[:-1]

    split = raw.split(line)
    if self._predefinedHeader == None:
      self.types = split[0].split(splitter)
      split.pop(0)
    else: 
      unknownCount = 0
      self.types = self._predefinedHeader
      wantedLength = len(split[0].split(splitter))
      while len(self._predefinedHeader) < wantedLength:
        unknownCount = unknownCount + 1
        self.types.append("Unknown " + str(unknownCount))
      

    self.data = []
    for d in split:
      o = Object()
      self.data.append(o)

      q = d.split(splitter)
      for i in range(len(q)):
        setattr(o, self.types[i], q[i])


  # Save the file
  def save(self): 
    if self._predefinedHeader == None:
      s = splitter.join(self.types) + line
    else:
      s = ""
      
    for ob in self.data:
      for name in self.types:
        if not hasattr(ob, name): 
          setattr(ob, name, "")
        s += getattr(ob, name) + splitter
      
      s = s[:-1]
      s += line
      

    self.file.write(s)

    
  
        


