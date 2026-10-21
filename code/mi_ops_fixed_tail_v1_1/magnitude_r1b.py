"""Protocol 7.6 pure diagnostics, no fitting and no real data access."""
import math
from contracts_r1 import ValidityStop,join_exact,SEEDS
def _flat(x):
 if isinstance(x,(list,tuple)):
  return [v for a in x for v in _flat(a)]
 return [float(x)]
def magnitude(T,Ts,W,Ws,b,bs,selection,status):
 if not all(math.isfinite(v) and v>0 for v in (T,Ts)):raise ValidityStop('TEMPERATURE_MAGNITUDE')
 w,w0,bv,b0=map(_flat,(W,Ws,b,bs))
 if len(w)!=len(w0) or len(bv)!=len(b0) or not all(math.isfinite(v) for v in w+w0+bv+b0):raise ValidityStop('MAGNITUDE_SHAPE_FINITE')
 num=math.hypot(*(a-z for a,z in zip(w,w0)));norm=math.hypot(*w0);den=max(norm,1e-12);bd=math.hypot(*(a-z for a,z in zip(bv,b0)));bn=math.hypot(*b0)
 v=math.log(T/Ts);R=selection['T_R']
 return dict(m_T=abs(v),m_W=num/den,weight_absolute_change=num,source_weight_norm=norm,weight_denominator=den,
  zero_source_weight_norm=norm==0,weight_norm_floor=norm<1e-12,bias_change_norm=bd,source_bias_norm=bn,bias_relative_change=bd/max(bn,1e-12),
  zero_source_bias_norm=bn==0,bias_denominator=max(bn,1e-12),T=T,Ts=Ts,v=v,
  T_at_lower_bound=v<=-math.log(R)+1e-12,T_at_upper_bound=v>=math.log(R)-1e-12,
  conservative={'N_k160':selection['N_k']==160,'T_penalty1':selection['T_penalty']==1,'T_R2':R==2,
   'H_penalty1':selection['H_penalty']==1,'EA_source_penalty1':selection['EA_penalty']==1,'EA_L_rho025':selection['EA_rho']==.25},
  selected_grid=dict(selection),fit_record=dict(status),active_fit=bool(status.get('active')),fallback=bool(status.get('fallback')),fit_status=status['status'])
def changes(ids,k_ids,o_ids,k_gap,o_gap,k_mask,o_mask,kT,oT,operation):
 ids=join_exact(ids,k_ids,o_ids);n=len(ids)
 if not all(len(x)==n for x in (k_gap,o_gap,k_mask,o_mask)):raise ValidityStop('CHANGE_LENGTH')
 if not all(type(x) is bool for x in (*k_mask,*o_mask)) or min(kT,oT)<=0:raise ValidityStop('MASK_OR_TEMPERATURE')
 if any(m and not math.isfinite(z) for z,m in zip(k_gap,k_mask)) or any(m and not math.isfinite(z) for z,m in zip(o_gap,o_mask)):raise ValidityStop('FINITE_MASK_CONTRACT')
 common=[i for i,(a,b) in enumerate(zip(k_mask,o_mask)) if a and b];threshold=math.log(3.)
 cls=acc=union=0
 for i in common:
  cc=(k_gap[i]>0)!=(o_gap[i]>0);ac=(abs(k_gap[i])/kT>=threshold)!=(abs(o_gap[i])/oT>=threshold)
  cls+=cc;acc+=ac;union+=cc or ac
 if operation=='T' and cls:raise ValidityStop('T_CLASS_INVARIANCE')
 reasons=[]
 if tuple(k_mask)!=tuple(o_mask):reasons.append('missing_mask_mismatch')
 if not common:reasons.append('no_common_valid')
 return dict(status='EVALUABLE' if not reasons else 'UNKNOWN',reasons=reasons,ordinals=ids,K_valid=tuple(k_mask),operation_valid=tuple(o_mask),
  common_valid_ordinals=tuple(ids[i] for i in common),denominator=len(common),class_numerator=cls,accept_numerator=acc,union_numerator=union,
  q=union/len(common) if common else None,technical_deferral_changes=sum(a!=b for a,b in zip(k_mask,o_mask)),cost=.25)
def seed_mean(records):
 reasons=[];observed=[]
 if set(records)!=set(SEEDS):reasons.append('three_fixed_seeds_required')
 for seed in SEEDS:
  r=records.get(seed)
  if r is None:continue
  if r['q'] is not None:observed.append(r['q'])
  if r['status']!='EVALUABLE':reasons.extend(f'{seed}:{x}' for x in r['reasons'])
 return dict(evaluable=not reasons,reasons=reasons,observed_seed_count=len(observed),
  observed_q=sum(observed)/len(observed) if observed else None,q=sum(observed)/3 if not reasons else None)
def near_inactive(people,d=10):
 if d!=10 or set(people)!=set(range(1,10)):raise ValidityStop('INTENDED_NINE_PRIMARY10')
 yes=unknown=0;per={}
 for person,arms in people.items():
  T=seed_mean(arms.get('T',{}));H=seed_mean(arms.get('H',{}));ok=T['evaluable'] and H['evaluable']
  value=(T['q']<.02 and H['q']<.02) if ok else None
  yes+=value is True;unknown+=value is None;per[person]={'T':T,'H':H,'jointly_near_inactive':value}
 status='NEAR_INACTIVE' if yes>=5 else 'NOT_NEAR_INACTIVE' if yes+unknown<5 else 'UNKNOWN'
 return dict(status=status,qualifying_people=yes,unknown_people=unknown,people=per,
  adaptation_interpretation='near_inactive_uninformative' if status=='NEAR_INACTIVE' else 'unknown' if status=='UNKNOWN' else 'not_near_inactive',
  modifies_hypothesis_base_label=False)
