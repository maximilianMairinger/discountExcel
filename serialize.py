from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from typing import *

# Handles FS events
class FsHandler(FileSystemEventHandler):
  def __init__(self, filePath, updateCallback, moveCallback):
    self.filePath = filePath
    self.lastFileContent = ""
    self.updateCallback = updateCallback
    self.moveCallback = moveCallback

  # Gets called when file is deleted
  def on_deleted(self, event):
    # print("del")
    if self.filePath == os.path.abspath(event.src_path):
      # we consider this as deleting the content of the file
      content = ""
      # if content has not prev been equal trigger event
      if self.lastFileContent != content:
        self.lastFileContent = content
        self.updateCallback(content)

  # Gets called when file is deleted
  def on_modified(self, event):
    # print("mod", self.filePath, event.src_path )
    if self.filePath == os.path.abspath(event.src_path):
      content = open(self.filePath, "r").read()
      # if content has not prev been equal trigger event
      if self.lastFileContent != content:
        self.lastFileContent = content
        self.updateCallback(content)

  def on_moved(self, event):
    # print("mov")
    if self.filePath == os.path.abspath(event.src_path):
      # call move event
      # print("event.dest_path")
      # print(event.dest_path)
      # print("event.dest_path")
      self.moveCallback(event.dest_path)


# Serialize class, comfortably write and read from your file. 
# Change filepaths. Get notified on file changes.
class Serialize:
  def __init__(self, filePath: str, ending: str = None, onChange = None): 
    self._ending = ""
    self._path = ""
    self._observer = None

    self.filePath(filePath, True)
    self.ending(ending, True)
    if onChange != None: 
      self.enableLiveFileObserver(onChange)
  
  # Set the ending of the file or get it
  def ending(self, ending = None, dontWrite = False): 
    if ending == None: 
      return self._ending
    else:
      if ending[-1:] != ".":
        ending = "." + ending
      self._ending = ending
      self._changeFilePath(self.filePath(), ending, dontWrite)

  # Enable the fileobserver
  def enableLiveFileObserver(self, onChange = None):
    if self._observer == None: 
      if onChange == None:
        if hasattr(self, "lastOnChange"):
          onChange = self.lastOnChange
        else:
          return
      self.lastOnChange = onChange

      # gets called on file change
      def change(content):
        nonlocal onChange
        onChange(content)
      
      # gets called on file move
      def onFileMoved(to):
        self.filePath(to)

      # init observer
      event_handler = FsHandler(self._path, change, onFileMoved)
      self._observer = observer = Observer()
      observer.schedule(event_handler, os.path.dirname(os.path.realpath(self._path)), True)
      observer.start()

  # Disable the fileobserver
  def disableLiveFileObserver(self):
    if self._observer != None: 
      # clear up resources
      self._observer.stop()
      self._observer = None

  # Set the file path or get it
  def filePath(self, filePath = None, dontWrite = False): 
    if filePath == None: 
      return self._filePath
    else:  
      # try to fix invalid paths
      if filePath[-1:] == ".": 
        filePath = filePath[:-1]
      if filePath[-1:] == "/": 
        filePath += "data"
      self._filePath = filePath
      self._changeFilePath(filePath, self.ending(), dontWrite)

  # Combine filePath and ending logic
  def _changeFilePath(self, filePath, ending, dontWrite): 
    if not filePath.endswith(ending): 
      to = filePath + ending
    else:
      to = filePath
    
    # If new path is different than last, reinit fileobserver if needed and maybe save to new location - depending on option "dontWrite"
    if (self._path != to):
      observerActive = self._observer != None
      
      # reinit fileobserver if needed
      if observerActive: 
        self.disableLiveFileObserver()

      # read from last location, depending on option "dontWrite"
      if (not dontWrite):
        read = self.read()

      self._path = os.path.abspath(to)

      # save to new location, depending on option "dontWrite"
      if (not dontWrite):
        self.write(read)

      # reinit fileobserver if needed
      if observerActive: 
        self.enableLiveFileObserver()


  # Read from file
  def read(self):
    return open(self._path, "r").read()

  # write to file
  def write(self, data):
    # Disable observer - since we dont want to trigger own write
    observerActive = self._observer != None
    if observerActive:
      self.disableLiveFileObserver()

    ret = open(self._path, "w").write(data)

    # Enable observer - if it was enabled prior
    if observerActive:
      self.enableLiveFileObserver()

    return ret

