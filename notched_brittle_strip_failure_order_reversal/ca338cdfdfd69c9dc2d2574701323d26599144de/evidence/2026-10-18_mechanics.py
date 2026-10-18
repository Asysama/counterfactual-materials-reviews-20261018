"""External acceptance predicates: no calls to generator predicate/scoring code."""
import numpy as np, math

def mechanics(n,p,t,c):
 assert all(np.isfinite(a).all() and len(a)==120 for q in [t,c] for a in q.values())
 assert np.array_equal(t['time'],c['time']) and np.allclose(t['time'],np.arange(120)/24)
 if n.startswith('notched'):
  fs=[]
  for q in [t,c]:fs.append([(int(np.flatnonzero(q['broken'][:,j])[0]) if q['broken'][:,j].any() else 120) for j in range(2)])
  assert fs[0][0]<fs[0][1]==fs[1][1]<90 and fs[1][0]==120
  for j,K in enumerate([1+2*math.sqrt(p['notch_depth']/p['rho_sharp']),1+2*math.sqrt(p['notch_depth']/p['rho_round'])]):
   f=fs[0][j];assert t['nominal_stress'][f-1]*K<p['material_strength']<=t['nominal_stress'][f]*K
  assert np.array_equal(t['opening'][:,1],c['opening'][:,1]) and np.array_equal(t['nominal_stress'],c['nominal_stress'])
  assert np.all(t['opening'][-1]>.20) and c['opening'][-1,1]>.20 and c['opening'][-1,0]==0
  return {'fracture_frames_true_cf':fs,'single_change':'sharp_notch_strength'}
 if n.startswith('locked'):
  lock=p['onset']+p['ramp_frames'];eq=p['ks']*p['kinf']*p['total_extension']/(p['ks']+p['kinf'])
  tau=p['tau']*(p['ks']+p['k0'])/(p['ks']+p['kinf'])
  expected=eq+(t['force'][lock]-eq)*np.exp(-np.arange(120-lock)/24/tau)
  assert np.allclose(t['force'][lock:],expected) and np.all(np.diff(c['force'][lock:])>0)
  assert np.array_equal(t['total_extension'],c['total_extension'])
  for q in [t,c]:
   assert np.allclose(q['spring_extension']*p['ks'],q['force'])
   assert np.allclose(q['spring_extension']+q['rubber_extension'],q['total_extension']) and np.min(q['rubber_extension'])>=-1e-9
   assert np.max(np.abs(np.diff(q['total_extension'][lock:])))==0
  return {'lock_frame':lock,'force_at_lock':float(t['force'][lock]),'final_true_force':float(t['force'][-1]),'final_cf_force':float(c['force'][-1]),'equilibrium_force':eq}
 if n.startswith('rubber'):
  A=2+(t['twist']*p['reference_radius']/p['reference_length'])**2/2
  residual=2*t['stretch']-A/t['stretch']**2
  assert np.max(abs(residual))<1e-10 and np.all(2+2*A/t['stretch']**3>0)
  assert np.array_equal(t['twist'],c['twist'])
  for q in [t,c]:assert np.allclose(q['radius']**2*q['length'],p['reference_radius']**2*p['reference_length'])
  assert t['length'][-1]>p['reference_length']>c['length'][-1]
  return {'zero_force_energy_derivative_max':float(np.max(abs(residual))),'true_final_length':float(t['length'][-1]),'cf_final_length':float(c['length'][-1]),'reference_length':p['reference_length']}
 if n.startswith('adhesive'):
  f=t['force_per_width'];angles=np.array(p['angles']);G=f[:,None]*(1-np.cos(angles))+f[:,None]**2/(2*p['extensional_stiffness'])
  assert np.allclose(G,t['energy_release']) and np.array_equal(f,c['force_per_width'])
  assert np.max(G[:,1])<p['adhesion_energy'] and np.max(G[:,0])>p['adhesion_energy']
  assert np.all(t['advance'][:,1]==0) and np.array_equal(t['advance'][:,0],c['advance'][:,0])
  velocity=p['mobility']*48*np.maximum(0,G-p['adhesion_energy'])
  assert np.allclose(np.diff(t['advance'],axis=0),(velocity[:-1]+velocity[1:])/48)
  assert c['advance'][-1,1]>.28 and np.max(c['advance'])<1.25 and np.max(np.diff(t['advance'][-10:],axis=0))==0
  return {'adhesion_threshold':p['adhesion_energy'],'maximum_energy_release':G.max(axis=0).tolist(),'final_true_peel':t['advance'][-1].tolist(),'final_cf_peel':c['advance'][-1].tolist()}
 if n.startswith('braided'):
  # Reconstruct actual discretized centerlines independently of generator mesh functions.
  def lengths(q):
   u=np.linspace(0,1,481);out=[]
   for L,R in zip(q['length'],q['radius']):
    r=R+p['weave_amplitude']*np.cos(p['strand_count']*2*np.pi*u)
    xyz=np.column_stack([L*u,r*np.cos(2*np.pi*u),r*np.sin(2*np.pi*u)])
    out.append(np.linalg.norm(np.diff(xyz,axis=0),axis=1).sum())
   return np.array(out)
  lt,lc=lengths(t),lengths(c)
  assert np.allclose(lt,p['fiber_length'],rtol=1e-8) and lc[-1]>p['fiber_length']*1.05
  assert np.array_equal(t['length'],c['length']) and t['radius'][-1]<p['initial_radius']<c['radius'][-1]
  return {'true_max_fiber_length_error':float(np.max(abs(lt-p['fiber_length']))),'cf_fiber_length_ratio':float(lc[-1]/p['fiber_length']),'true_final_radius':float(t['radius'][-1]),'cf_final_radius':float(c['radius'][-1])}
 raise AssertionError('Unknown phenomenon')
