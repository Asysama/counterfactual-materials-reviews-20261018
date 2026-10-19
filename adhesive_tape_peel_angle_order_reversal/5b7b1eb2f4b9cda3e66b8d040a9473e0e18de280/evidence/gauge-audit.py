"""Independent gauge evidence from final trajectories and decoded native pixels."""
from pathlib import Path
import json,subprocess,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;B=R/'backups';N='adhesive_tape_peel_angle_order_reversal';O=B/'gauge-audit-v8';O.mkdir(exist_ok=True);(O/'README.md').write_text('# Force gauge audit\n\nIndependent decoded needle and force checks for revised tape generator; derived review images only.\n')
H=json.loads((R/'2026-10-19_heads-v8.json').read_text());records=[]
for mf in sorted((B/'formal-v8'/N).glob('*/metadata.json')):
 m=json.loads(mf.read_text());assert m['generation']['git']==H[N];p=m['phenomenon_data']['scene_params'];case=mf.parent
 branch_records=[]
 for branch in ['true','counterfactual']:
  q=dict(np.load(case/m['paths'][branch]['trajectory']));F=q['measured_force'];G=F;first=p['onset']+24
  assert np.array_equal(F[:,0],F[:,1])
  assert np.allclose(F,q['force_per_width'][:,None]*p['tape_width'])
  assert np.all(F[-12:]==0)
  max_step=float(np.abs(np.diff(G,axis=0)).max()/40*180);assert max_step<9
  cam0=np.array(m['camera']['pos']);target=np.array(m['camera']['lookat']);observed=[];errors=[]
  def project(world,frame):
   cam=cam0+np.array([.025*frame/119,0,0]);fwd=target-cam;fwd/=np.linalg.norm(fwd);right=np.cross(fwd,[0,0,1]);right/=np.linalg.norm(right);up=np.cross(right,fwd);d=np.asarray(world)-cam
   z=np.dot(d,fwd);return np.array([1024+2730.6666666666665*np.dot(d,right)/z,1024-2730.6666666666665*np.dot(d,up)/z])
  f=case/m['paths'][branch]['video'];proc=subprocess.Popen(['ffmpeg','-v','error','-threads','1','-i',str(f),'-f','rawvideo','-pix_fmt','rgb24','-threads','1','-'],stdout=subprocess.PIPE)
  film=Image.new('RGB',(1600,1680),'white');selected=sorted(set([first-3,first-2,first-1,first,first+1,first+2,first+3,first+5,first+8,first+12,90,119]));sheet=Image.new('RGB',(1100,len(selected)*160),'white')
  motion_frames=[0,p['onset']+20,p['onset']+28,75,95,119];motion_sheet=Image.new('RGB',(3*800,2*660),'white')
  motion_points=[]
  for i in range(120):
   size=2048*2048*3;buf=bytearray()
   while len(buf)<size:
    d=proc.stdout.read(size-len(buf));assert d;buf.extend(d)
   im=np.frombuffer(buf,np.uint8).reshape(2048,2048,3);row=[];crops=[]
   for j,x in enumerate([-1.27,1.27]):
    hub=project([x,-.687,.43],i);xx,yy=np.round(hub).astype(int);patch=im[yy-105:yy+80,xx-105:xx+105];assert patch.shape==(185,210,3)
    red=(patch[:,:,0].astype(float)>patch[:,:,1].astype(float)*1.6)&(patch[:,:,0]>70)&(patch[:,:,1]<160)
    ry,rx=np.where(red);assert len(rx)>15,(case.name,branch,i,j,'missing red needle')
    points=np.column_stack([rx+xx-105,ry+yy-105]);direction=points.mean(axis=0)-hub
    angle=math.pi*G[i,j]/40;end=project([x-.151*math.cos(angle),-.687,.43+.151*math.sin(angle)],i);expected=end-hub
    cosine=np.dot(direction,expected)/(np.linalg.norm(direction)*np.linalg.norm(expected));err=math.degrees(math.acos(np.clip(cosine,-1,1)));errors.append(err);assert err<8,(case.name,branch,i,j,err)
    row.append(float(math.atan2(-direction[1],-direction[0])));crops.append(Image.fromarray(patch))
   observed.append(row)
   if i in motion_frames:
    # Unscaled native crop of the shallow-angle grip, tape, front, and ruler.
    anchor=project([1.05,0,1.0],i);left=max(0,min(1248,int(anchor[0]-400)));top=max(0,min(1408,int(anchor[1]-320)))
    slot=motion_frames.index(i);motion_sheet.paste(Image.fromarray(im[top:top+640,left:left+800]),((slot%3)*800,(slot//3)*660+20));ImageDraw.Draw(motion_sheet).text(((slot%3)*800+8,(slot//3)*660+3),f'{branch} shallow-angle frame {i}',fill='black')
    a=q['advance'][i,1];theta=p['angles'][1];free=(p['initial_free_length']+a)*(1+q['force_per_width'][i]/p['extensional_stiffness'])
    front=project([1.27-.55+a,0,.568],0);grip=project([1.27-.55+a-free*math.cos(theta),0,.568+free*math.sin(theta)],0)
    motion_points.append({'frame':i,'advance':float(a),'front_fixed_camera_native_xy':front.tolist(),'grip_fixed_camera_native_xy':grip.tolist()})
   pair=Image.new('RGB',(420,185),'white');pair.paste(crops[0],(0,0));pair.paste(crops[1],(210,0))
   x0=(i%8)*200;y0=(i//8)*112;film.paste(pair.resize((200,88)),(x0,y0+22));ImageDraw.Draw(film).text((x0+3,y0+3),str(i),fill='black')
   if i in selected:
    k=selected.index(i);sheet.paste(pair.resize((336,148)),(0,k*160+12));sheet.paste(Image.fromarray(im).resize((148,148)),(340,k*160+12));ImageDraw.Draw(sheet).text((500,k*160+25),f'frame {i}  actual N {F[i]}',fill='black')
  assert not proc.stdout.read(1) and proc.wait()==0
  observed=np.unwrap(np.array(observed),axis=0);jump=float(np.degrees(np.max(np.abs(np.diff(observed,axis=0)))));assert jump<12,jump
  film.save(O/(case.name+'-'+branch+'-needles-all120.jpg'),quality=94);sheet.save(O/(case.name+'-'+branch+'-unloading.jpg'),quality=94)
  motion_sheet.save(O/(case.name+'-'+branch+'-shallow-motion-native.png'))
  front_pixels=float(np.linalg.norm(np.array(motion_points[-1]['front_fixed_camera_native_xy'])-motion_points[0]['front_fixed_camera_native_xy']));grip_pixels=float(np.linalg.norm(np.array(motion_points[-1]['grip_fixed_camera_native_xy'])-motion_points[0]['grip_fixed_camera_native_xy']));assert front_pixels>30 and grip_pixels>20
  branch_records.append(dict(projected_shallow_front_travel_native_pixels=front_pixels,projected_shallow_grip_travel_native_pixels=grip_pixels,native_motion_crop_frames=motion_frames,projection_note='Computed from stored geometry with fixed initial camera; actual unscaled decoded crops retained for visual confirmation.',branch=branch,peak_load_frame=first,equal_actual_force_all_frames=True,max_model_angular_step_degrees=max_step,max_decoded_angular_step_degrees=jump,max_decoded_direction_error_degrees=max(errors),video_sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 records.append(dict(case_id=case.name,head_sha=H[N],branches=branch_records));print('GAUGE_DECODED_PASS',case.name,flush=True)
assert len(records)==2
(O/'audit.json').write_text(json.dumps(dict(status='PASS',scope='Independent all-frame force equality, continuous load/unload and all120 decoded red-needle directions',cases=records),indent=2))
