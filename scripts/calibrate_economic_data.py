import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sp=ROOT/'data'/'nodes'/'suppliers.json'; pp=ROOT/'data'/'products.json'
sup=json.loads(sp.read_text(encoding='utf-8')); products=json.loads(pp.read_text(encoding='utf-8'))
product_specs={
'movement': {'quantity':1000,'weight_kg_per_unit':0.045,'material_cost':31.0,'labor_hours':0.28},
'battery': {'quantity':1000,'weight_kg_per_unit':0.004,'material_cost':1.10,'labor_hours':0.035},
'glass': {'quantity':1000,'weight_kg_per_unit':0.030,'material_cost':8.50,'labor_hours':0.18},
'case': {'quantity':1000,'weight_kg_per_unit':0.075,'material_cost':11.50,'labor_hours':0.32},
'strap': {'quantity':1000,'weight_kg_per_unit':0.030,'material_cost':9.00,'labor_hours':0.48},
'packaging': {'quantity':1000,'weight_kg_per_unit':0.090,'material_cost':2.80,'labor_hours':0.12}}
for p in products:p.update(product_specs[p['id']])
# Supplier premiums represent quality, scale and sourcing maturity, not verified quotes.
premiums={
'supplier_miyota':(1.00,.985,1400),'supplier_movement_backup_jp':(1.10,.975,800),'supplier_movement_backup_ch':(.82,.920,700),
'supplier_panasonic':(1.00,.990,5000),'supplier_battery_backup_kr':(.96,.975,2500),'supplier_battery_backup_de':(1.25,.995,1200),
'supplier_lens':(.92,.965,2200),'supplier_glass_backup_jp':(1.12,.985,900),'supplier_glass_backup_de':(1.28,.990,700),
'supplier_jabil':(.95,.970,1800),'supplier_case_backup_pl':(1.08,.980,1000),'supplier_case_backup_de':(1.22,.990,700),
'supplier_hlp':(.90,.955,1200),'supplier_strap_backup_it':(1.22,.990,800),'supplier_strap_backup_es':(1.12,.980,900),
'supplier_klabin':(.88,.970,4000),'supplier_packaging_backup_de':(1.25,.992,1800),'supplier_packaging_backup_pl':(1.08,.985,2200)}
by_supplier={sid:pid for p in products for sid in p['supplier_ids'] for pid in [p['id']]}
for s in sup:
 pid=by_supplier.get(s['id'])
 if not pid: continue
 factor,quality,capacity=premiums.get(s['id'],(1.0,.96,1000)); spec=product_specs[pid]
 s.update({'component_id':pid,'material_cost_per_unit_eur':round(spec['material_cost']*factor,2),'labor_hours_per_unit':spec['labor_hours'],'quality_yield':quality,'capacity_units_per_day':capacity,'economic_values_are_model_assumptions':True})
sp.write_text(json.dumps(sup,ensure_ascii=False,indent=2),encoding='utf-8');pp.write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf-8')
print('Economic calibration applied to',sum('component_id' in s for s in sup),'qualified suppliers')
