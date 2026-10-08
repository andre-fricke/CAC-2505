import ctypes as c, plistlib, sys as py_sys, time, signal, subprocess, base64
from pathlib import Path
if py_sys.argv[1:]:raise SystemExit('Read-only capture; no arguments')
P=c.c_void_p; U=c.c_uint32; Q=c.c_uint64
io=c.CDLL('/System/Library/Frameworks/IOKit.framework/IOKit')
cf=c.CDLL('/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation')
fb=c.CDLL('/System/Library/PrivateFrameworks/IOMobileFramebuffer.framework/IOMobileFramebuffer')
sys=c.CDLL(None)
def fn(lib,name,args,result):
 f=getattr(lib,name);f.argtypes=args;f.restype=result;return f
match=fn(io,'IOServiceMatching',[c.c_char_p],P)
services=fn(io,'IOServiceGetMatchingServices',[U,P,c.POINTER(U)],U)
nextsvc=fn(io,'IOIteratorNext',[U],U)
release=fn(io,'IOObjectRelease',[U],U)
prop=fn(io,'IORegistryEntryCreateCFProperty',[U,P,P,U],P)
regid=fn(io,'IORegistryEntryGetRegistryEntryID',[U,c.POINTER(Q)],U)
string=fn(cf,'CFStringCreateWithCString',[P,c.c_char_p,U],P)
data=fn(cf,'CFPropertyListCreateData',[P,P,c.c_long,U,c.POINTER(P)],P)
length=fn(cf,'CFDataGetLength',[P],c.c_long)
bytesptr=fn(cf,'CFDataGetBytePtr',[P],P)
cfrel=fn(cf,'CFRelease',[P],None)
openfb=fn(fb,'IOMobileFramebufferOpen',[U,U,U,c.POINTER(P)],U)
fbtype=fn(fb,'IOMobileFramebufferGetTypeID',[],c.c_ulong)
gettype=fn(cf,'CFGetTypeID',[P],c.c_ulong)
getmode=fn(fb,'IOMobileFramebufferGetDigitalOutMode',[P,c.POINTER(U),c.POINTER(U)],U)
def readprop(svc,name):
 k=string(None,name.encode(),0x08000100)
 try:v=prop(svc,k,None,0)
 finally:cfrel(k)
 if not v:return None
 try:
  error=P();blob=data(None,v,100,0,c.byref(error))
  if not blob:
   if error.value:cfrel(error)
   return None
  try:return plistlib.loads(c.string_at(bytesptr(blob),length(blob)))
  finally:cfrel(blob)
 finally:cfrel(v)
def connected_edid():
 iterator=U();r=services(0,match(b'IOPortTransportStateDisplayPort'),c.byref(iterator))
 if r:return None
 found=[]
 try:
  while True:
   device=nextsvc(iterator.value)
   if not device:break
   try:
    if readprop(device,'BranchDeviceID')=='SYNAq' and readprop(device,'Active') is True:
     found.append(readprop(device,'EDID'))
   finally:release(device)
 finally:
  if iterator.value:release(iterator.value)
 return found[0] if len(found)==1 else None
import json
it=U();status=services(0,match(b'IOMobileFramebuffer'),c.byref(it));found=[]
if status:raise SystemExit('Enumeration failed')
try:
 while True:
  svc=nextsvc(it.value)
  if not svc:break
  try:
   attrs=readprop(svc,'DisplayAttributes') or {}
   if attrs.get('ProductAttributes',{}).get('ProductName')!='LG TV SSCR2':continue
   conn=P();rc=openfb(svc,U.in_dll(sys,'mach_task_self_').value,0,c.byref(conn))
   record={'open_status':rc,'timestamp':time.time()}
   if rc==0 and conn.value and gettype(conn)==fbtype():
    try:
     color=U();timing=U();rc=getmode(conn,c.byref(color),c.byref(timing))
     record.update({'get_status':rc,'color_id':color.value,'timing_id':timing.value})
     if rc==0:
      timings=readprop(svc,'TimingElements') or []
      for t in timings:
       if t.get('ID')==timing.value:
        record['active_timing']={k:v for k,v in t.items() if k!='ColorModes'}
        record['active_color']=next((cm for cm in t.get('ColorModes',[]) if cm.get('ID')==color.value),None)
    finally:cfrel(conn)
   found.append(record)
  finally:release(svc)
finally:
 if it.value:release(it.value)
print(json.dumps(found,indent=2,default=str),flush=True)
if len(found)!=1 or found[0].get('get_status')!=0:raise SystemExit('Active source timing not uniquely verified')
