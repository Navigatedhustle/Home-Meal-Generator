from __future__ import annotations
import random
from typing import List, Dict, Any

MEAL_TYPES=['breakfast','lunch','dinner','snack']
ACTIVITY_FACTORS={'sedentary':1.2,'light':1.375,'moderate':1.55,'very':1.725,'athlete':1.9}

def mifflin_st_jeor(sex:str,age:int,height_cm:float,weight_kg:float)->float:
    return 10*weight_kg+6.25*height_cm-5*age+(5 if sex.lower()=='male' else -161)

def compute_tdee(bmr:float,activity:str)->float:
    return bmr*ACTIVITY_FACTORS.get(activity,1.2)

def grams_from_kcal(k:float,p_ratio=0.35,f_ratio=0.25,c_ratio=0.40):
    return round(k*p_ratio/4), round(k*c_ratio/4), round(k*f_ratio/9)

def filter_meals(meals:List[Dict[str,Any]],prefs:Dict[str,Any])->List[Dict[str,Any]]:
    out=[];ex=set([x.strip().lower() for x in prefs.get('excludes','').split(',') if x.strip()])
    for m in meals:
        t=set(m.get('tags',[]))
        if prefs.get('vegetarian') and not(('vegetarian'in t)or('vegan'in t)): continue
        if prefs.get('vegan') and 'vegan' not in t: continue
        if prefs.get('dairy_free') and ('dairy_free' not in t and 'vegan' not in t): continue
        if prefs.get('gluten_free') and 'gluten_free' not in t: pass
        if ex:
            hay=(m.get('name','')+' '+' '.join(m.get('ingredients',[]))).lower()
            if any(x in hay for x in ex):
                continue
        out.append(m)
    return out

def pick_day_plan(target:int, meals_db:List[Dict[str,Any]], meals_per_day:int):
    by={mt:[m for m in meals_db if m.get('meal_type')==mt] for mt in MEAL_TYPES}
    if meals_per_day>=3: seq=['breakfast','lunch','dinner']+['snack']*(meals_per_day-3)
    else: seq=['lunch','dinner'][:meals_per_day]
    random.shuffle(seq)
    picks=[]; total=0
    for mt in seq:
        bucket=by.get(mt) or meals_db
        c=random.choice(bucket); picks.append(c); total+=c['K']
    lo,hi=int(target*0.95),int(target*1.05); tries=300
    while tries>0 and not(lo<=total<=hi):
        tries-=1
        i=random.randrange(0,len(picks)); mt=picks[i]['meal_type']; bucket=by.get(mt) or meals_db
        cand=random.choice(bucket); new_total=total-picks[i]['K']+cand['K']
        if abs(new_total-target)<abs(total-target): picks[i]=cand; total=new_total
    return picks,total

def aggregate_grocery(plan:List[List[Dict[str,Any]]])->Dict[str,int]:
    g={}
    for day in plan:
        for meal in day:
            for it in meal.get('ingredients',[]): g[it]=g.get(it,0)+1
    return g
