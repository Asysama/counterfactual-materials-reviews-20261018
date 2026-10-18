import sys,json,itertools,importlib.util
from pathlib import Path
import numpy as np
G=Path(sys.argv[1]);out=Path(sys.argv[2]);sys.path.insert(0,str(G))
from src import scaling,violation as v
sp=importlib.util.spec_from_file_location('checks',Path(__file__).with_name('2026-10-18_mechanics.py'));m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
base=scaling.sample_params(None,42,scaling.profile_for_seed(42));records=[]
for length,response,onset,depth in itertools.product([1.,1.36],[.85,1.12],[20,29],[.75,1.11]):
 p=v.resolve(base|dict(length=length,response=response,onset=onset,depth=depth));assert not v.validate(p)
 t=v.trajectory(p,'true');c=v.trajectory(p,'counterfactual');r=m.mechanics(G.name,p,t,c);e=v.predicate(p,t,c)
 records.append(dict(parameters={k:p[k] for k in ['length','response','onset','depth']},physics=r,evidence_frame=e))
out.write_text(json.dumps(dict(status='PASS',scope='16 independent combined physical-axis corners, non-rendering',cases=records),indent=2));print(G.name,'16 boundary profiles PASS')
