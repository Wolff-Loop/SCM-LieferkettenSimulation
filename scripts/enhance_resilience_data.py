import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; N=ROOT/'data'/'nodes'; R=ROOT/'data'/'routes'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
def nd(i,n,c,lat,lon,t): return {'id':i,'name':n,'country':c,'latitude':lat,'longitude':lon,'node_type':t,'status':'ACTIVE'}
sup=load(N/'suppliers.json'); ports=load(N/'ports.json'); air=load(N/'airports.json'); rail=load(N/'rail_terminals.json'); edges=load(R/'edges.json'); geo=load(R/'geometries.json')
new_sup=[
nd('supplier_movement_backup_jp','Seiko Instruments Backup','Japan',36.2,138.1,'SUPPLIER'),nd('supplier_movement_backup_ch','Hong Kong Movement Backup','China',22.32,114.17,'SUPPLIER'),
nd('supplier_battery_backup_kr','Korea Battery Backup','South Korea',37.45,126.7,'SUPPLIER'),nd('supplier_battery_backup_de','German Battery Backup','Germany',48.8,9.2,'SUPPLIER'),
nd('supplier_glass_backup_jp','Japan Glass Backup','Japan',35.2,136.9,'SUPPLIER'),nd('supplier_glass_backup_de','German Glass Backup','Germany',50.1,8.7,'SUPPLIER'),
nd('supplier_case_backup_pl','Poland Case Backup','Poland',51.1,17.0,'SUPPLIER'),nd('supplier_case_backup_de','German Case Backup','Germany',48.1,11.6,'SUPPLIER'),
nd('supplier_strap_backup_it','Italy Strap Backup','Italy',45.4,11.9,'SUPPLIER'),nd('supplier_strap_backup_es','Spain Strap Backup','Spain',40.4,-3.7,'SUPPLIER'),
nd('supplier_packaging_backup_de','German Packaging Backup','Germany',49.5,8.5,'SUPPLIER'),nd('supplier_packaging_backup_pl','Poland Packaging Backup','Poland',52.2,21.0,'SUPPLIER')]
existing={x['id'] for x in sup}; sup += [x for x in new_sup if x['id'] not in existing]
# Guaranteed rail backbone nodes
rail_add=[nd('rail_tokyo','Tokyo Freight Terminal','Japan',35.62,139.75,'RAIL_TERMINAL'),nd('rail_kobe','Kobe Freight Terminal','Japan',34.70,135.20,'RAIL_TERMINAL'),nd('rail_shanghai','Shanghai Rail Hub','China',31.20,121.40,'RAIL_TERMINAL'),nd('rail_duisburg','Duisburg Rail Terminal','Germany',51.4344,6.7623,'RAIL_TERMINAL'),nd('rail_hamburg','Hamburg Rail Terminal','Germany',53.54,10.0,'RAIL_TERMINAL'),nd('rail_heilbronn','Heilbronn Rail Terminal','Germany',49.1427,9.2109,'RAIL_TERMINAL')]
rex={x['id'] for x in rail}; rail += [x for x in rail_add if x['id'] not in rex]
alln={x['id']:x for x in sup+ports+air+rail+load(N/'warehouses.json')+load(N/'factories.json')}
seen={(e['source'],e['target'],e['transport_mode']) for e in edges}
def add(a,b,m,dist,points=None,risk=.2):
 key=(a,b,m)
 if key in seen or a not in alln or b not in alln:return
 seen.add(key); edges.append({'source':a,'target':b,'transport_mode':m,'distance_km':dist,'risk':risk,'status':'ACTIVE'})
 A,B=alln[a],alln[b]; points=points or [[A['latitude'],A['longitude']],[B['latitude'],B['longitude']]]
 geo[f'{a}_{b}']={'source':a,'target':b,'transport_mode':m,'ui_mode':{'TRUCK':'LKW','RAIL':'ZUG','SHIP':'SEESCHIFF','AIR':'FLUGZEUG'}[m],'geometry':points}
# suppliers to terrestrial and maritime choices
links={
'supplier_miyota':['port_yokohama','port_kobe','port_tokyo','port_nagoya','rail_tokyo','rail_kobe'],
'supplier_panasonic':['port_kobe','port_yokohama','port_osaka','port_nagoya','rail_kobe','rail_tokyo'],
'supplier_movement_backup_jp':['port_tokyo','port_nagoya','rail_tokyo'], 'supplier_movement_backup_ch':['port_shanghai','port_ningbo','rail_shanghai'],
'supplier_battery_backup_kr':['port_demo_001','airport_demo_001','rail_demo_001'], 'supplier_battery_backup_de':['rail_heilbronn','factory_heilbronn'],
'supplier_glass_backup_jp':['port_nagoya','port_kobe','rail_kobe'], 'supplier_glass_backup_de':['rail_heilbronn','factory_heilbronn'],
'supplier_case_backup_pl':['rail_heilbronn','factory_heilbronn'], 'supplier_case_backup_de':['rail_heilbronn','factory_heilbronn'],
'supplier_strap_backup_it':['rail_heilbronn','port_valencia'], 'supplier_strap_backup_es':['port_valencia','rail_heilbronn'],
'supplier_packaging_backup_de':['rail_heilbronn','factory_heilbronn'], 'supplier_packaging_backup_pl':['rail_heilbronn','factory_heilbronn']}
for s,targets in links.items():
 for t in targets:add(s,t,'TRUCK',300)
# explicit maritime backbone, all directions needed for rerouting
sea=[('port_yokohama','port_singapore'),('port_kobe','port_singapore'),('port_tokyo','port_singapore'),('port_nagoya','port_singapore'),('port_shanghai','port_singapore'),('port_ningbo','port_singapore'),('port_singapore','port_rotterdam'),('port_singapore','port_hamburg'),('port_singapore','port_antwerp'),('port_singapore','port_durban'),('port_durban','port_rotterdam'),('port_durban','port_hamburg'),('port_veracruz','port_rotterdam'),('port_veracruz','port_hamburg'),('port_santos','port_rotterdam'),('port_santos','port_antwerp')]
for a,b in sea:
 if a in alln and b in alln:add(a,b,'SHIP',9000, risk=.22)
# rail connections from ports to Heilbronn
for a,b,d in [('port_rotterdam','rail_duisburg',230),('port_hamburg','rail_hamburg',20),('port_antwerp','rail_duisburg',190),('rail_duisburg','rail_heilbronn',340),('rail_hamburg','rail_heilbronn',610),('rail_heilbronn','factory_heilbronn',10),('rail_tokyo','port_tokyo',25),('rail_kobe','port_kobe',15),('rail_shanghai','port_shanghai',25)]: add(a,b,'RAIL',d,risk=.12)
save(N/'suppliers.json',sup);save(N/'rail_terminals.json',rail);save(R/'edges.json',edges);save(R/'geometries.json',geo)
print('Resilienz ergänzt:',len(sup),'Lieferanten,',len(rail),'Bahnterminals,',len(edges),'Kanten')
