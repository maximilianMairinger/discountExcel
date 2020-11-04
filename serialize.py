from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from typing import *

class FsHandler(FileSystemEventHandler):
  """
  Handles FS events
  """
  def __init__(self, filePath, updateCallback, moveCallback):
    self.filePath = filePath
    self.lastFileContent = ""
    self.updateCallback = updateCallback
    self.moveCallback = moveCallback

  def on_deleted(self, event):
    """
    Gets called when file is deleted

    :param event: onDeleted event
    """
    # print("del")
    if self.filePath == os.path.abspath(event.src_path):
      # we consider this as deleting the content of the file
      content = ""
      # if content has not prev been equal trigger event
      if self.lastFileContent != content:
        self.lastFileContent = content
        self.updateCallback(content)

  def on_modified(self, event):
    """
    Gets called when file is modified

    :param event: onModified event
    """
    # print("mod", self.filePath, event.src_path )
    if self.filePath == os.path.abspath(event.src_path):
      content = open(self.filePath, "r").read()
      # if content has not prev been equal trigger event
      if self.lastFileContent != content:
        self.lastFileContent = content
        self.updateCallback(content)

  def on_moved(self, event):
    """
    Gets called when file is moved

    :param event: onMoved event
    """
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
    """
    Set the ending of the file or get it

    :param ending: The file 
    """

    if ending == None: 
      return self._ending
    else:
      if ending[-1:] != ".":
        ending = "." + ending
      self._ending = ending
      self._changeFilePath(self.filePath(), ending, dontWrite)

  def enableLiveFileObserver(self, onChange = None):
    """
    Enable the fileobserver

    :param ending: Ending will be appended if not already present in filePath
    :param dontWrite: True when you want to only switch path but not instantly write to new location
    """
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

  def disableLiveFileObserver(self):
    """
    Disable the fileobserver
    """
    if self._observer != None: 
      # clear up resources
      self._observer.stop()
      self._observer = None

  def filePath(self, filePath = None, dontWrite = False): 
    """
    Set the file path or get it

    :param filePath: The filepath, may have a ending
    :param dontWrite: True when you want to only switch path but not instantly write to new location
    """
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

  def _changeFilePath(self, filePath, ending, dontWrite): 
    """
    Combine filePath and ending logic

    :param filePath: The filepath, may have a ending
    :param ending: Ending will be appended if not already present in filePath
    :param dontWrite: True when you want to only switch path but not instantly write to new location
    """
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


  def read(self):
    """
    Read from file
    """
    open(self._path, "r").read()


  def write(self, data):
    """
    Write to file
    
    :param data: Data to write to file
    """
    # Disable observer - since we dont want to trigger own write
    observerActive = self._observer != None
    if observerActive:
      self.disableLiveFileObserver()

    open(self._path, "w").write(data)

    # Enable observer - if it was enabled prior
    if observerActive:
      self.enableLiveFileObserver()


