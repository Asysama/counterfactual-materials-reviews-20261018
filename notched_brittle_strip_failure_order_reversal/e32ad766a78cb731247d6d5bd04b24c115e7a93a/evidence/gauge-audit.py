"""Independent gauge evidence from final trajectories and decoded native pixels."""
from pathlib import Path
import json,subprocess,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;B=R/'backups';N='notched_brittle_strip_failure_order_reversal';O=B/'gauge-audit-v7';O.mkdir(exist_ok=True);(O/'README.md').write_text('# Force gauge audit\n\nIndependent decoded needle and force checks for revised notched generator; derived review images only.\n')
H=json.loads((R/'2026-10-18_heads-v7.json').read_text());records=[]
for mf in sorted((B/'formal-v7'/N).glob('*/metadata.json')):
 m=json.loads(mf.read_text());assert m['generation']['git']==H[N];p=m['phenomenon_data']['scene_params'];case=mf.parent
 branch_records=[]
 for branch in ['true','counterfactual']:
  q=dict(np.load(case/m['paths'][branch]['trajectory']));F=q['measured_force'];G=q['indicated_force'];first=int(np.flatnonzero(q['broken'].any(axis=1))[0])
  assert np.array_equal(F[:first,0],F[:first,1]) and np.array_equal(G[:first,0],G[:first,1])
  # Reconstruct instrument output independently as a superposition of step responses.
  tt=np.arange(120)/24;tau=.15;step=1-(1+tt/tau)*np.exp(-tt/tau)
  independent=np.column_stack([np.convolve(np.diff(F[:,j],prepend=0),step[1:],mode='full')[:120] for j in range(2)])
  assert np.allclose(G,independent,rtol=1e-11,atol=1e-7)
  max_step=float(np.abs(np.diff(G,axis=0)).max()/300000*180);assert max_step<8
  for j in range(2):
   broken=np.flatnonzero(q['broken'][:,j])
   if len(broken):assert np.all(F[broken,j]==0) and G[int(broken[0]),j]>0 and G[-1,j]<300
  cam0=np.array(m['camera']['pos']);target=np.array(m['camera']['lookat']);observed=[];errors=[]
  def project(world,frame):
   cam=cam0+np.array([.025*frame/119,0,0]);fwd=target-cam;fwd/=np.linalg.norm(fwd);right=np.cross(fwd,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,fwd);d=np.asarray(world)-cam
   z=np.dot(d,fwd);return np.array([1024+2730.6666666666665*np.dot(d,right)/z,1024-2730.6666666666665*np.dot(d,up)/z])
  f=case/m['paths'][branch]['video'];proc=subprocess.Popen(['ffmpeg','-v','error','-threads','1','-i',str(f),'-f','rawvideo','-pix_fmt','rgb24','-threads','1','-'],stdout=subprocess.PIPE)
  film=Image.new('RGB',(1600,1680),'white');selected=sorted(set([first-3,first-2,first-1,first,first+1,first+2,first+3,first+5,first+8,first+12,90,119]));sheet=Image.new('RGB',(1100,len(selected)*160),'white')
  for i in range(120):
   size=2048*2048*3;buf=bytearray()
   while len(buf)<size:
    d=proc.stdout.read(size-len(buf));assert d;buf.extend(d)
   im=np.frombuffer(buf,np.uint8).reshape(2048,2048,3);row=[];crops=[]
   for j,x in enumerate([-.95,.95]):
    hub=project([x,-.347,.43],i);xx,yy=np.round(hub).astype(int);patch=im[yy-105:yy+80,xx-105:xx+105];assert patch.shape==(185,210,3)
    red=(patch[:,:,0].astype(float)>patch[:,:,1].astype(float)*1.6)&(patch[:,:,0]>70)&(patch[:,:,1]<160)
    ry,rx=np.where(red);assert len(rx)>15,(case.name,branch,i,j,'missing red needle')
    points=np.column_stack([rx+xx-105,ry+yy-105]);direction=points.mean(axis=0)-hub
    angle=math.pi*G[i,j]/300000;end=project([x-.151*math.cos(angle),-.347,.43+.151*math.sin(angle)],i);expected=end-hub
    cosine=np.dot(direction,expected)/(np.linalg.norm(direction)*np.linalg.norm(expected));err=math.degrees(math.acos(np.clip(cosine,-1,1)));errors.append(err);assert err<8,(case.name,branch,i,j,err)
    row.append(float(math.atan2(-direction[1],-direction[0])));crops.append(Image.fromarray(patch))
   observed.append(row)
   pair=Image.new('RGB',(420,185),'white');pair.paste(crops[0],(0,0));pair.paste(crops[1],(210,0))
   x0=(i%8)*200;y0=(i//8)*112;film.paste(pair.resize((200,88)),(x0,y0+22));ImageDraw.Draw(film).text((x0+3,y0+3),str(i),fill='black')
   if i in selected:
    k=selected.index(i);sheet.paste(pair.resize((336,148)),(0,k*160+12));sheet.paste(Image.fromarray(im).resize((148,148)),(340,k*160+12));ImageDraw.Draw(sheet).text((500,k*160+25),f'frame {i}  actual kN {F[i]/1000}\nindicated kN {G[i]/1000}',fill='black')
  assert not proc.stdout.read(1) and proc.wait()==0
  observed=np.unwrap(np.array(observed),axis=0);jump=float(np.degrees(np.max(np.abs(np.diff(observed,axis=0)))));assert jump<12,jump
  film.save(O/(case.name+'-'+branch+'-needles-all120.jpg'),quality=94);sheet.save(O/(case.name+'-'+branch+'-unloading.jpg'),quality=94)
  branch_records.append(dict(branch=branch,first_fracture=first,equal_actual_and_indicated_before_fracture=True,max_model_angular_step_degrees=max_step,max_decoded_angular_step_degrees=jump,max_decoded_direction_error_degrees=max(errors),video_sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 records.append(dict(case_id=case.name,head_sha=H[N],branches=branch_records));print('GAUGE_DECODED_PASS',case.name,flush=True)
assert len(records)==2
(O/'audit.json').write_text(json.dumps(dict(status='PASS',scope='Independent force equality, closed-form damped response, unload tails and all120 decoded red-needle directions; same actual force only while both specimens intact',cases=records),indent=2))
