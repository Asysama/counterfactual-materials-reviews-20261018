# 固定总伸长后应力反增

A standard linear solid (equilibrium stiffness k_inf parallel to a Maxwell arm, instantaneous stiffness k0 and material relaxation time tau) is in series with a measuring spring ks. The actuator prescribes total extension D then locks. Force obeys Fdot+aF=bDdot+cD with a=(ks+k_inf)/(tau(ks+k0)), b=ks*k0/(ks+k0), c=ks*k_inf/(tau(ks+k0)). True relaxes to ks*k_inf*D/(ks+k_inf). The sole counterfactual reflects the post-lock force about F_at_lock. The passive measuring spring still obeys Hooke law; polymer length follows total-length compatibility. No inertia, heating or changing external displacement is modeled.

No correctness or scale PASS is claimed until exact-head artifacts have been independently checked.
