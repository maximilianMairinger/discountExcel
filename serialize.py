from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from typing import *


class FsHandler(FileSystemEventHandler):
  def __init__(self, filePath, updateCallback, moveCallback):
    self.filePath = filePath
    self.lastFileContent = ""
    self.updateCallback = updateCallback
    self.moveCallback = moveCallback

  def on_deleted(self, event):
    # print("del")
    if self.filePath == os.path.abspath(event.src_path):
      self.updateCallback("")

  def on_modified(self, event):
    print("mod",self.filePath, event.src_path )
    if self.filePath == os.path.abspath(event.src_path):
      content = open(self.filePath, "r").read()
      if self.lastFileContent != content:
        self.lastFileContent = content
        self.updateCallback(content)

  def on_moved(self, event):
    # print("mov")
    if self.filePath == os.path.abspath(event.src_path):
      print("event.dest_path")
      print(event.dest_path)
      print("event.dest_path")
      self.moveCallback(event.dest_path)



class Serialize:
  def __init__(self, filePath: str, ending: str = None, onChange = None): 
    self._ending = ""
    self._path = ""
    self._observer = None

    self.filePath(filePath, True)
    self.ending(ending, True)
    if onChange != None: 
      self.enableLiveFileObserver(onChange)
  
  def ending(self, ending = None, dontWrite = False): 
    if ending == None: 
      return self._ending
    else:
      if ending[-1:] != ".":
        ending = "." + ending
      self._ending = ending
      self._changeFilePath(self.filePath(), ending, dontWrite)


  def enableLiveFileObserver(self, onChange = None):
    if self._observer == None: 
      if onChange == None:
        if hasattr(self, "lastOnChange"):
          onChange = self.lastOnChange
        else:
          return
      self.lastOnChange = onChange
      def change(content):
        print("new")
        nonlocal onChange
        onChange(content)
      
      def onFileMoved(to):
        self.filePath(to)

      event_handler = FsHandler(self._path, change, onFileMoved)
      self._observer = observer = Observer()
      observer.schedule(event_handler, os.path.dirname(os.path.realpath(self._path)), True)
      observer.start()

  def disableLiveFileObserver(self):
    if self._observer != None: 
      self._observer.stop()
      self._observer = None

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
      observerActive = self._observer != None
      
      if observerActive: 
        self.disableLiveFileObserver()
      if (not dontWrite):
        read = self.read()

      self._path = os.path.abspath(to)

      if (not dontWrite):
        self.write(read)
      if observerActive: 
        self.enableLiveFileObserver()

  def read(self):
    return open(self._path, "r").read()


  def write(self, data):
    observerActive = self._observer != None
    if observerActive:
      self.disableLiveFileObserver()

    ret = open(self._path, "w").write(data)

    if observerActive:
      self.enableLiveFileObserver()

    return ret

