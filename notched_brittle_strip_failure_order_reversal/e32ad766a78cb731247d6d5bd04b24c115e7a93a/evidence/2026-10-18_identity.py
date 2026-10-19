"""Reviewer-selected object identity replay; independent of generator mask tags."""
import sys,json,subprocess,hashlib,math
from pathlib import Path
import numpy as np
from PIL import Image
G=Path(sys.argv[1]);batch=Path(sys.argv[2]);out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=False);sys.path.insert(0,str(G))
from src import violation as v
from engine import geometry as geo
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
N=G.name
prefixes={'notched_brittle_strip_failure_order_reversal':('sharp_upper','sharp_lower'),'locked_extension_viscoelastic_stress_growth':('viscoelastic_strip','rubber_paint_'),'rubber_torsion_poynting_axial_contraction':('rubber_plain','rubber_stripes'),'adhesive_tape_low_angle_subthreshold_peeling':('peeling_tape_1',),'braided_sleeve_extension_radial_expansion':('fiber_',)}[N]
def selected_mask_frames(file,frames):
 p=subprocess.Popen(['ffmpeg','-v','error','-threads','1','-i',str(file),'-f','rawvideo','-pix_fmt','rgb24','-threads','1','-'],stdout=subprocess.PIPE)
 out={};size=2048*2048*3
 for i in range(120):
  data=bytearray()
  while len(data)<size:
   b=p.stdout.read(size-len(data));assert b;data.extend(b)
  if i in frames:out[i]=np.frombuffer(data,np.uint8).reshape(2048,2048,3).copy()
 assert p.stdout.read(1)==b'' and p.wait()==0
 return out
records=[]
for mf in sorted(batch.glob('*/metadata.json')):
 m=json.loads(mf.read_text());case=mf.parent;p=m['phenomenon_data']['scene_params'];states=dict(np.load(case/m['paths']['counterfactual']['trajectory']))
 frames=sorted(set([0,m['first_changed_frame'],m['evidence_frame'],m['evidence_frame']+1,90,119]));masks=selected_mask_frames(case/m['paths']['counterfactual']['mask'],frames)
 look,dist=v.camera(p);scene,cam,pos,target=geo.setup(p,look,dist,2048);v.scene(p);assert not scene.display.shading.show_shadows
 checks=[]
 for i in frames:
  cam.location=Vector(m['camera']['pos']);cam.location.x+=.025*i/119;cam.rotation_euler=(Vector(m['camera']['lookat'])-cam.location).to_track_quat('-Z','Y').to_euler()
  geo.clear_dynamic();v.frame(p,states,i);bpy.context.view_layer.update()
  targets=[];all_bounds=[];target_bounds=[]
  for o in bpy.data.objects:
   if o.type=='FONT':
    # Calibrated physical markings are allowed; arbitrary/floating annotations fail.
    assert N=='notched_brittle_strip_failure_order_reversal'
    parts=o.name.split('_');assert parts[:2] in [['gauge','label'],['gauge','unit']]
    j=int(parts[2]);assert j in [0,1];x=[-.95,.95][j]*p['scale'];ss=p['scale']
    if parts[1]=='label':
     assert len(parts)==4;value=int(parts[3]);assert value in [0,100,200,300] and o.data.body==str(value)
     ang=math.pi*value/300;loc=[x-.135*ss*math.cos(ang),-.333*ss,.43*ss+.135*ss*math.sin(ang)];size=.034*ss
    else:
     assert len(parts)==3 and o.data.body=='kN';loc=[x,-.333*ss,.35*ss];size=.046*ss
    assert np.allclose(o.location,loc,atol=1e-7) and np.allclose(o.rotation_euler,[math.pi/2,0,0],atol=1e-7)
    assert abs(o.data.size-size)<1e-7 and not o.get('target',False) and not o.get('dynamic',False)
    face=bpy.data.objects['gauge_face_'+str(j)];assert not face.get('target',False)
    assert np.linalg.norm(np.array(o.location)[[0,2]]-np.array([x,.43*ss]))<.19*ss

   o['target']=o.type=='MESH' and o.name.startswith(prefixes)
   if o['target']:targets.append(o.name)
   if o.type=='MESH' and o.name!='floor' and not o.hide_render:
    coords=[world_to_camera_view(scene,cam,o.matrix_world@Vector(x)) for x in o.bound_box]
    bounds=[min(x.x for x in coords),min(x.y for x in coords),max(x.x for x in coords),max(x.y for x in coords)]
    all_bounds.append(bounds)
    if o['target']:target_bounds.append(bounds);assert all(x.z>0 for x in coords)
  fonts=sorted(o.name for o in bpy.data.objects if o.type=='FONT')
  expected=sorted([f'gauge_label_{j}_{v}' for j in [0,1] for v in [0,100,200,300]]+[f'gauge_unit_{j}' for j in [0,1]]) if N.startswith('notched') else []
  assert fonts==expected
  assert targets and target_bounds
  bb=np.array(target_bounds);assert bb[:,:2].min()>.005 and bb[:,2:].max()<.995,(N,i,bb)
  f=out/(case.name+'-identity-'+str(i)+'.png');geo.render_mask(scene,f);expected=np.asarray(Image.open(f).convert('RGB'))
  if i<m['mask_start_frame']:expected=np.zeros_like(expected)
  assert np.array_equal(masks[i],expected),(N,i,'mask not selected object projection')
  checks.append(dict(frame=i,objects=sorted(targets),target_bounds=[bb[:,:2].min(axis=0).tolist(),bb[:,2:].max(axis=0).tolist()],apparatus_bounds=[np.array(all_bounds)[:,:2].min(axis=0).tolist(),np.array(all_bounds)[:,2:].max(axis=0).tolist()],exact_identity_match=True))
 records.append(dict(case_id=case.name,head_sha=m['generation']['git'],no_floating_annotations=True,attached_calibration_markings=fonts,shadows_disabled=True,frames=checks))
(out/'identity-audit.json').write_text(json.dumps(dict(status='PASS',scope='Reviewer-named object sets, exact native decoded projection at six frames; visual review separate',cases=records),indent=2))
print('INDEPENDENT_IDENTITY_PASS',N)
