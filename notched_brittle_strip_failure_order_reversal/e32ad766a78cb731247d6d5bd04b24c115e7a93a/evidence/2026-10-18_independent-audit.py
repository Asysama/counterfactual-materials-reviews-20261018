"""External decoded and mechanics audit. Does not call the generator's graders."""
import sys,json,subprocess,hashlib,itertools,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
B=Path(sys.argv[1]);version=sys.argv[2];H=json.loads((B/('heads-'+version+'.json')).read_text());V={n:version for n in H};O=B/('independent-'+version);O.mkdir(exist_ok=False);(O/'README.md').write_text('# Independent audit\n\nDecoded formal-video and mechanics verification external to generator self-checks.\n')
def decoder(f,w):
 p=subprocess.Popen(['ffmpeg','-v','error','-threads','1','-i',str(f),'-f','rawvideo','-pix_fmt','rgb24','-threads','1','-'],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 try:
  count=w*w*3
  while True:
   buf=bytearray()
   while len(buf)<count:
    chunk=p.stdout.read(count-len(buf))
    if not chunk:break
    buf.extend(chunk)
   if not buf:break
   assert len(buf)==count
   yield np.frombuffer(buf,np.uint8).reshape(w,w,3)
 finally:
  p.stdout.close();assert p.wait()==0

from mechanics import mechanics
records={}
for n,h in H.items():
 if not n.startswith('notched'):
  old=json.loads((B/'independent-v6/audit.json').read_text());assert old['status']=='PASS';record=old['generators'][n];assert record['head_sha']==h
  for case in record['cases']:
   for rel,a in case['files'].items():
    f=B/('formal-'+version)/n/case['case_id']/rel;assert f.stat().st_size==a['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256']
   for label in ['decoded-contact-sheet','true-all120','counterfactual-all120']:
    import shutil
    shutil.copy2(B/'independent-v6'/(case['case_id']+'-'+label+'.jpg'),O/(case['case_id']+'-'+label+'.jpg'))
  record['retained_from']='independent-v6/audit.json; unchanged exact head and formal file hashes verified';records[n]=record;continue
 cases=[];reference=None
 for mf in sorted((B/('formal-'+V[n])/n).glob('*/metadata.json')):
  case=mf.parent;m=json.loads(mf.read_text());assert m['generation']['git']==h;assert m['render']['res']==[2048,2048] and m['render']['native'];p=m['phenomenon_data']['scene_params'];assert m['timebase']['physical_seconds_per_video_second']==1 and m['timebase']['outer_steps_per_recorded_frame']==1
  files=[case/m['paths']['true']['video']]+[case/m['paths']['counterfactual'][k] for k in ['video','mask','mask_overlay']]
  for f in files:
   probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(f)],text=True))['streams'][0]
   assert probe['codec_name']=='h264' and (probe['width'],probe['height'])==(2048,2048) and probe['r_frame_rate']=='24/1' and int(probe['nb_frames'])==120 and abs(float(probe['duration'])-5)<1e-8
  first=None;maskfirst=None;areas=[];e=m['evidence_frame'];frames=sorted(set([0,m['intervention_frame'],e,min(e+12,119),90,119]));sheet=Image.new('RGB',(4*480,len(frames)*510),'white');dd=ImageDraw.Draw(sheet);sample=None
  films=[Image.new('RGB',(1280,1776),'white') for _ in range(2)]
  for i,parts in enumerate(itertools.zip_longest(*(decoder(f,2048) for f in files))):
   assert all(x is not None for x in parts);a,b,mask,overlay=parts
   for j,im in enumerate([a,b]):
    xx=(i%10)*128;yy=(i//10)*148;films[j].paste(Image.fromarray(im).resize((128,128)),(xx,yy+20));ImageDraw.Draw(films[j]).text((xx+4,yy+3),str(i),fill='black')
   assert np.all((mask==0)|(mask==255)) and np.array_equal(mask[:,:,0],mask[:,:,1]) and np.array_equal(mask[:,:,0],mask[:,:,2]);fg=mask[:,:,0]>0;areas.append(int(fg.sum()))
   if first is None and not np.array_equal(a,b):first=i
   if maskfirst is None and fg.any():maskfirst=i
   if i<m['intervention_frame']:assert np.array_equal(a,b) and not fg.any()
   if i<m['mask_start_frame']:assert not fg.any()
   else:assert fg.sum()>8
   assert np.array_equal(overlay[~fg],b[~fg]) and np.all(overlay[fg]==[255,0,0])
   if i==e:assert np.count_nonzero(np.any(a!=b,axis=2))>150
   if i in frames:
    row=frames.index(i)
    for j,(label,img) in enumerate(zip(['True','Counterfactual','Binary mask','Red overlay'],parts)):
     dd.text((j*480+10,row*510+8),f'{label} frame {i}',fill='black');sheet.paste(Image.fromarray(img).resize((480,480)),(j*480,row*510+30))
   if i==90:sample=a[::4,::4].copy()
  assert i+1==120 and first==m['first_changed_frame'] and maskfirst==m['mask_start_frame'] and first<=e<96
  sheet.save(O/(case.name+'-decoded-contact-sheet.jpg'),quality=91)
  for j,label in enumerate(['true','counterfactual']):films[j].save(O/(case.name+'-'+label+'-all120.jpg'),quality=92)
  t=dict(np.load(case/m['paths']['true']['trajectory']));c=dict(np.load(case/m['paths']['counterfactual']['trajectory']));physics=mechanics(n,p,t,c)
  variation=None
  if reference is not None:
   variation=dict(mean_abs_difference=float(np.mean(np.abs(sample.astype(float)-reference))),changed_fraction=float(np.mean(np.any(sample!=reference,axis=2))))
   assert variation['mean_abs_difference']>1 and variation['changed_fraction']>.04
  reference=sample
  cases.append(dict(case_id=case.name,head_sha=h,status='PASS',frames=120,native_resolution=[2048,2048],first_changed_frame=first,mask_start_frame=maskfirst,evidence_frame=e,mask_area_min_active=min(areas[maskfirst:]),mask_area_max=max(areas),mechanics=physics,formal_case_diversity=variation,files={str(f.relative_to(case)):dict(bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in files}))
  print('INDEPENDENT_PASS',case.name,flush=True)
 assert len(cases)==2;records[n]=dict(head_sha=h,cases=cases)
(O/'audit.json').write_text(json.dumps(dict(status='PASS',scope='Two full formal cases per generator; external decoded and mechanics audit; human visual review separate',generators=records),indent=2))
