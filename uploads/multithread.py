# Image Distortion Script Daniel Piet 2012
import threading
import Queue
import Image
import sys
import shutil
from time import time

# moves pixels to the left 
# if they pass color test (red)
def shift(imageName,red,offset):
  source=Image.open(imageName)
  x,y=source.size
  data = source.getdata()
  array=list(data)
  for x in range(len(array)):
    if array[x][1]>red:
      array[x]=array[x-offset]
  return make(array,source.size,imageName)

#saves array into image with name
def make(array,size,name):
  new = Image.new('RGB',size)
  new.putdata(array)
  new.save(name)
  return name+'.png'

# sorts pixels in between indices set by color test
# adds array to queue
def sort(imageName,array,start,fin,tol,red,grn,blu,num,queue):
  source=Image.open(imageName)
  width,height=source.size
  for i in range(start,fin):
    var=array[i*width:i*width+width]
    beg=0
    num=0
    for q in range(len(var)):
      r,g,b=var[len(var)-1-q]
      if r>=red and g>=grn and b>=blu:
        if r<red+tol or g<grn+tol or b<blu+tol:
          num=len(var)-1-q
          break
      else:
        num=0
    for q in range(len(var)):
      r,g,b=var[q]
      if r>=red and g>=grn and b>=blu:
        if r<red+tol or g<grn+tol or b<blu+tol:
          beg=q
          break
      else:
        beg=0
    if beg>=num: continue
    first=array[start*width:i*width+beg]
    last=array[i*width+num:fin*width]
    row=array[i*width+beg:i*width+num]
    row.sort()
    array=first+row+last
  queue.put(array)
  queue.task_done()
  
# finds average color in array
# returns 3-tuple
def aveCol(array):
  sumr=0
  sumg=0
  sumb=0
  for i in range (0,len(array),20):
    r,g,b = array[i]
    sumr+=r
    sumg+=g
    sumb+=b
  aver=sumr/(len(array)/20)
  aveg=sumg/(len(array)/20)
  aveb=sumb/(len(array)/20)
  return (aver,aveg,aveb)

# splits image array and sorts
# parts in seperate threads
def multiSort(imageName):
  thrds=20

  source=Image.open(imageName)
  data=source.getdata()
  arrayQ=list(data)
  r,g,b=aveCol(arrayQ)
  x,y=source.size

  thrice=[]
  for i in range(1,thrds+1):
      q=(x*y)/thrds
      low=q*(i-1)
      hi=q*i
      thrice.append(arrayQ[low:hi])
      
  jobs = []
  queue=Queue.Queue()
  
  stuff=[]
  t1=time()
  for i in range(1,thrds+1):
      q=(x*y)/thrds
      low=q*(i-1)
      hi=q*i
      p = threading.Thread(target=sort, args=(imageName,thrice[i-1],0,len(thrice[i-1]),2,r,g,b,i,queue,))
      p.daemon = True
      jobs.append(p)
      p.start()
      stuff.append(list(queue.get()))
      
  array=[]    
  for i in range(len(stuff)):
    array+=stuff[i]

  make(array,source.size,imageName)
    
# who cares about alpha layers anyway
def clean(imageName):
  source=Image.open(imageName)
  data=source.getdata()
  array=list(data)
  if len(array[0]) == 4:
    for i in range(len(array)):
      r,g,b,a=array[i]
      array[i]=(r,g,b)
  make(array,source.size,imageName)
    
# do the stuff
def main():
  name='/glitchit/uploads/' + sys.argv[1]
  clean(name)
  multiSort(name)
  shift(name,100,15000)
  
main()
