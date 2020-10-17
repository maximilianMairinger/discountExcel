class Serialize:
  def __init__(self, filePath: str, ending: str = None): 
    self._ending = ""
    self._path = ""
    self.filePath(filePath, True)
    self.ending(ending, True)
  
  def ending(self, ending = None, dontWrite = False): 
    if ending == None: 
      return self._ending
    else:
      if ending[-1:] != ".":
        ending = "." + ending
      self._ending = ending
      self._changeFilePath(self.filePath(), ending, dontWrite)



  def filePath(self, filePath = None, dontWrite = False): 
    if filePath == None: 
      return self._filePath
    else:  
      if filePath[-1:] == ".": 
        filePath = filePath[:-1]
      if filePath[-1:] == "/": 
        filePath += "data"
      self._filePath = filePath
      self._changeFilePath(filePath, self.ending(), dontWrite)

  def _changeFilePath(self, filePath, ending, dontWrite): 
    if not filePath.endswith(ending): 
      to = filePath + ending
    else:
      to = filePath
    
    if (self._path != to):
      if (not dontWrite):
         read = self.read()
      self._path = to
      if (not dontWrite):
         self.write(read)

  def read(self):
    return open(self._path, "r").read()


  def write(self, data):
    return open(self._path, "w").write(data)

