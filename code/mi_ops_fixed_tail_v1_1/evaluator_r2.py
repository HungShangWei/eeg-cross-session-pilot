"""Post-seal evaluator. Only ScientificBackend calls this after registered E3 permission.
No random generation: indices are a supplied, separately accounted fixed matrix.
"""
from contracts_r1 import Indexed,SEEDS,BUDGETS,ValidityStop,join_exact
from row_identity_r2 import row_id
def evaluate(seal,labels,artifacts,states,label_events,indices,record):
 seal.verify()
 if set(labels)!=set(range(1,10)):raise ValidityStop('NINE_Q_LABEL_CAPABILITIES')
 from statistics_recipe import score_synthetic
 from inference_contract import hp1
 from inference_r1 import hp2_checked,audited_descriptive
 from magnitude_r1b import magnitude,changes,near_inactive
 by={tuple(r['key']):r for r in seal.records};scores={};mags={};people={p:{'T':{},'H':{}} for p in range(1,10)}
 for key,r in by.items():
  person,seed,op,d=key;y=labels[person];a=artifacts[r['prediction_ref']]
  if not isinstance(y,Indexed):raise ValidityStop('INDEXED_Q_LABELS')
  join_exact(r['row_ids'],y.ordinals,a['ordinals'])
  # None denotes technical deferral, not a probability or a zero-valued prediction.
  gap=[z if m else float('nan') for z,m in zip(a['gap'],a['valid'])]
  scores[key]={cost:score_synthetic(gap,y.values,a['valid'],r['temperature'],cost,partition='Q',sealed=True) for cost in (.1,.25,.4)}
  if op in ('T','H') and d>0:
   k=by[(person,seed,'K',0)];ka=artifacts[k['prediction_ref']]
   s=states[r['prediction_ref']];s0=states[k['prediction_ref']];ch=s['choices']
   selection={'N_k':ch['N']['selected'][0],'T_R':ch['T']['selected'][0],'T_penalty':ch['T']['selected'][1],
    'H_penalty':ch['H']['selected'][0],'EA_penalty':ch['EA_source']['selected'][0],'EA_rho':ch['EA_L']['selected'][0]}
   item=magnitude(s['Ts'],s0['Ts'],s['W'].tolist(),s0['W'].tolist(),s['b'].tolist(),s0['b'].tolist(),selection,s['status'])
   change=changes(r['row_ids'],ka['ordinals'],a['ordinals'],ka['gap'],a['gap'],ka['valid'],a['valid'],k['temperature'],r['temperature'],op)
   mags[row_id(key)]={'magnitude':item,'change':change}
   if d==10:people[person][op][seed]=change
 def person_vector(op,d,metric,cost=.25):
  return [sum(scores[(p,s,op,d)][cost][metric] for s in (SEEDS if not op.startswith('EA') else (None,)))/(3 if not op.startswith('EA') else 1) for p in range(1,10)]
 def fits(op):
  vals=[[bool(states[by[(p,s,op,10)]['prediction_ref']]['status'].get('active')) for s in (SEEDS if not op.startswith('EA') else (None,))] for p in range(1,10)]
  return [x[0] for x in vals] if op.startswith('EA') else vals
 primary={}
 jt,jh,ct,ch=[person_vector(op,10,metric) for op,metric in [('T','J'),('H','J'),('T','C'),('H','C')]]
 primary['HP1']=hp1(jt,jh,ct,ch,fits('T'),fits('H'),indices)
 controls={op:person_vector(op,10,'J') for op in ('K','N','EA-U')}
 primary['HP2']={op:hp2_checked(person_vector(op,10,'J'),person_vector(op,10,'C'),controls,fits(op),indices,ea=op=='EA-L') for op in ('T','H','EA-L')}
 recipients={op:[by[(p,s,op,10)]['prediction_ref'] for p in range(1,10) for s in (SEEDS if op=='N' else (None,))] for op in ('N','EA-U')}
 primary['descriptive_no_label']=audited_descriptive(jh,{op:controls[op] for op in ('N','EA-U')},{op:person_vector(op,10,'C') for op in ('N','EA-U')},indices,label_events,recipients)
 primary['near_inactive']=near_inactive(people)
 result={'seal_sha256':seal.sha256,'primary_d':10,'primary_cost':.25,'primary':primary,
  'rows':[{'key':key,'scores':value} for key,value in scores.items()],'magnitude':mags,
  'resampling_generated_here':False,'EA_independent_people':9,'neural_seed_summary':'arithmetic mean within person'}
 seal.verify();record('post_seal_evaluation',result);return result
