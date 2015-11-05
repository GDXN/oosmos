#
#  oosmos.py - A set of common python functions.
#
import sys
import shutil
import subprocess
import os
import glob

def WalkDir(Dir, pFunc, UserArg):
  for RootDir, DirList, FileList in os.walk(Dir):
    for File in FileList:
      FullFilePath = os.path.join(RootDir, File)
      pFunc(os.path.normpath(FullFilePath), UserArg)

    for Dir in DirList:
      WalkDir(Dir, pFunc, UserArg)


def Clean(Dir, Extensions):
  Extensions = Extensions.split()

  for SubDir, Dirs, Files in os.walk(Dir):
    if 'dist' in Dirs:
      shutil.rmtree(SubDir+'/dist')

    if 'build' in Dirs:
      shutil.rmtree(SubDir+'/build')

    if SubDir == 'dist' or SubDir == 'build':
      print('remove '+SubDir)
      continue

    for File in Files:
      for Extension in Extensions:
        if File.endswith('.'+Extension):
          os.remove(SubDir+'/'+File)

class cWindows:
  @staticmethod
  def Clean():
    WildRemove('*.exe')
    WildRemove('*.pdb')
    WildRemove('*.obj')
    WildRemove('*.ilk')
    WildRemove('*.suo')
    WildRemove('*.tds')

  @staticmethod
  def Compile(FileName, Options = ''):
    print 'Compiling '+FileName+'...'

    p = subprocess.Popen('cl /nologo /Zi /W4 /wd4065 /wd4100 /wd4127 /D_CRT_SECURE_NO_WARNINGS '+FileName+' oosmos.c '+Options+' -Doosmos_DEBUG',
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd = os.getcwd())
  
    for Line in p.stdout:
      Line = Line.rstrip()
  
      if Line.startswith(('reg', 'Generating Code...', 'Compiling...')):
        continue
  
      if Line.endswith(('.c', '.cpp')):
        continue
  
      print Line

class cLinux:
  @staticmethod
  def Compile(Target, Files):
    print('Compiling %s...' % (Files))
    os.system("gcc -Wall -o %s -Doosmos_DEBUG -Doosmos_ORTHO %s oosmos.c " % (Target, Files))

def WildRemove(FilenamePattern):
  FileList = glob.glob(FilenamePattern)

  for FileName in FileList:
    os.remove(FileName)

def MakeReadWrite(Filename):
  os.chmod(Filename, 0o777)

def MakeReadOnly(Filename):
  os.chmod(Filename, 0o444)

def CopyFileReadOnly(FromFile, ToFile):
  if os.path.exists(ToFile):
    MakeReadWrite(ToFile)

  shutil.copyfile(FromFile, ToFile)
  MakeReadOnly(ToFile)

'''
def Compile(Filename):
  p = subprocess.Popen('cl /nologo '+Filename, stdout=subprocess.PIPE, cwd = os.getcwd())

  for Line in p.stdout:
    Line = Line.rstrip()

    if Line == Filename:
      continue

    print(Line)
'''

'''
def ZZZ_Copy(From, FromExtensions, To, ToExtensions, Files, bCopyOosmos):
  FromExtensions = FromExtensions.split()
  ToExtensions   = ToExtensions.split()

  if bCopyOosmos:
    for Index, FromExtension in enumerate(FromExtensions):
      ToExtension = ToExtensions[Index]

      FromFile = './oosmos/Source/oosmos.%(FromExtension)s' % locals()
      ToFile   = './oosmos/%(To)s/oosmos.%(ToExtension)s'   % locals()
      CopyFileReadOnly(FromFile, ToFile)

  if Files == '':
    return

  Files = Files.split()

  for File in Files:
    for Index, FromExtension in enumerate(FromExtensions):
      ToExtension = ToExtensions[Index]

      FromFile = './oosmos/%(From)s/%(File)s.%(FromExtension)s' % locals()
      ToFile   = './oosmos/%(To)s/%(File)s.%(ToExtension)s'     % locals()
      CopyFileReadOnly(FromFile, ToFile)
'''

if __name__ == '__main__':
  print("'oosmos.py' is a module of reusable scripting elements and is not a standalone script.")
