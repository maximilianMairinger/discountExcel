from serialize import *
from ob import *

line = "\n"
splitter = "|"

# UPOI (CSV) File, bound to location. 
# Parsing on file change.
# Custom header (not reflected in file) can be given
class UPOI:
  def __init__(self, filePath, predefinedHeader = None, onChange = None): 
    changeCB = None
    self._predefinedHeader = predefinedHeader
    if onChange != None:
      def c(content):
        nonlocal changeCB
        self.parse(content)
        onChange()

      changeCB = c
        

    self.file = Serialize(filePath, "upoi", changeCB)
    self.parse()
    
  # Parse the string
  def parse(self):
    raw = self.file.read()

    # Padding
    while raw[-1:] == "\n" or raw[-1:] == " " or raw[-1:] == "\t":
      raw = raw[:-1]

    # Parse header
    # May take into account the given header
    split = raw.split(line)
    if self._predefinedHeader == None:
      self.types = split[0].split(splitter)
      split.pop(0)
    else: 
      unknownCount = 0
      self.types = self._predefinedHeader
      wantedLength = len(split[0].split(splitter))
      # Lables unknowns with incrementing Unknown headers (Unknown 1, Unknown 2, etc.)
      while len(self._predefinedHeader) < wantedLength:
        unknownCount = unknownCount + 1
        self.types.append("Unknown " + str(unknownCount))
      
    # Parses main content and sets it to running poi object
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
      
    # Stringify the current parsed input
    for ob in self.data:
      for name in self.types:
        if not hasattr(ob, name): 
          setattr(ob, name, "")
        s += getattr(ob, name) + splitter
      
      s = s[:-1]
      s += line
      
    # Write to fs
    self.file.write(s)

    
  
        


