import sys,os
import zipfile,shutil
import re


''' This program allows you to delete a set of files from a directory or from a zip file according to a given pattern
	
	The syntax is 
	
	python rmPattern [zip|dir] [path] [pattern]
	
	The pattern must be a regular expression

'''


ZIPFILE='.\Dev_04082011.zip'

TEMP='tmp' #temporary dir



############# Zip METHODS #############

def extractZipFile(zf=ZIPFILE,tmp=TEMP):

  f=zipfile.ZipFile(zf,'r')
  try: os.mkdir(tmp)    #create a temporary dir ./tmp
  except: pass
  f.extractall(tmp)
  f.close()

def replaceZipFile(list,zf=ZIPFILE,tmp=TEMP):

  f=zipfile.ZipFile(zf,'w',zipfile.ZIP_DEFLATED)

  for i in list:
    f.write(i,i[i.find(tmp)+len(tmp)+1:]); 
  f.close()

  shutil.rmtree(tmp)    #remove temporary dir


def selectFiles(d,pattern,listIN=[],listOUT=[]):     #Select files according to a pattern
  l=os.listdir(d)

  p=re.compile(pattern) #compile the pattern METTI CONTROLLO
  
  for i in l:
    l_item=os.path.join(d,i)

    if os.path.isfile(l_item):
      if p.search(i)!=None: listIN.append(l_item)
      else: listOUT.append(l_item)

    elif os.path.isdir(l_item):
      selectFiles(l_item,pattern,listIN,listOUT)
  return listIN,listOUT


def deleteFiles(list,msg=''):
  for i in list:
    try:
      os.remove(i)
      if msg: print i,msg
    except OSError:
      os.chmod(i,0777); os.remove(i)
      if msg: print i,msg

      

def main(opt,arg,patt):
  if opt=='z':
    extractZipFile(arg)
    l_in,l_out=selectFiles(TEMP,patt)
    replaceZipFile(l_out,arg)

  if opt=='d':
    l_in,l_out=selectFiles(arg,patt)
    deleteFiles(l_in,'\tDELETED')



if __name__=="__main__":
  args=sys.argv
  try:

    if args[3]: patt=args[3]
    else: patt='^\._'

    
    if args[1]=='zip':
      if os.path.isfile(args[2]):
        main('z',args[2],patt)
    elif args[1]=='dir':
      if os.path.isdir(args[2]):
        main('d',args[2],patt)
    else:
      print 'Syntax not valid: [zip|dir] [path] [pattern]'
      for i in args:
        print i

  except: print sys.exc_info()








