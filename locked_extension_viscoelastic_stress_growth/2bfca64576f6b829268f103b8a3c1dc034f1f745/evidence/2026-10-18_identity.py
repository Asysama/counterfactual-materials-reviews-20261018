"""Reviewer-selected object identity replay; independent of generator mask tags."""
import sys,json,subprocess,hashlib
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
   assert o.type!='FONT'
   o['target']=o.type=='MESH' and o.name.startswith(prefixes)
   if o['target']:targets.append(o.name)
   if o.type=='MESH' and o.name!='floor' and not o.hide_render:
    coords=[world_to_camera_view(scene,cam,o.matrix_world@Vector(x)) for x in o.bound_box]
    bounds=[min(x.x for x in coords),min(x.y for x in coords),max(x.x for x in coords),max(x.y for x in coords)]
    all_bounds.append(bounds)
    if o['target']:target_bounds.append(bounds);assert all(x.z>0 for x in coords)
  assert targets and target_bounds
  bb=np.array(target_bounds);assert bb[:,:2].min()>.005 and bb[:,2:].max()<.995,(N,i,bb)
  f=out/(case.name+'-identity-'+str(i)+'.png');geo.render_mask(scene,f);expected=np.asarray(Image.open(f).convert('RGB'))
  if i<m['mask_start_frame']:expected=np.zeros_like(expected)
  assert np.array_equal(masks[i],expected),(N,i,'mask not selected object projection')
  checks.append(dict(frame=i,objects=sorted(targets),target_bounds=[bb[:,:2].min(axis=0).tolist(),bb[:,2:].max(axis=0).tolist()],apparatus_bounds=[np.array(all_bounds)[:,:2].min(axis=0).tolist(),np.array(all_bounds)[:,2:].max(axis=0).tolist()],exact_identity_match=True))
 records.append(dict(case_id=case.name,head_sha=m['generation']['git'],no_scene_text_objects=True,shadows_disabled=True,frames=checks))
(out/'identity-audit.json').write_text(json.dumps(dict(status='PASS',scope='Reviewer-named object sets, exact native decoded projection at six frames; visual review separate',cases=records),indent=2))
print('INDEPENDENT_IDENTITY_PASS',N)
