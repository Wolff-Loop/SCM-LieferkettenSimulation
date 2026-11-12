"""Erzeugt einen reproduzierbaren multimodalen Demo-Graphen.

WICHTIG: Die erzeugten Zusatzknoten sind synthetische, plausible Benchmarkdaten.
Die bekannten Lieferanten, Häfen, Flughäfen und das Werk bleiben reale Ankerpunkte.
"""

import json
import math
import random
from pathlib import Path

SEED = 20261111
RNG = random.Random(SEED)
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
NODES = DATA / "nodes"
ROUTES = DATA / "routes"

REGIONS = {
    "Japan": (35.68, 139.76), "China": (31.23, 121.47), "Southeast Asia": (1.35, 103.82),
    "India": (19.08, 72.88), "Middle East": (25.20, 55.27), "Germany": (50.11, 8.68),
    "Benelux": (51.92, 4.48), "France": (48.86, 2.35), "Iberia": (38.72, -9.14),
    "Scandinavia": (57.71, 11.97), "Eastern Europe": (52.23, 21.01),
    "Mexico": (19.17, -96.13), "US East": (40.71, -74.01), "US West": (34.05, -118.24),
    "Brazil": (-23.96, -46.33), "South Africa": (-29.86, 31.02),
    "East Africa": (-4.04, 39.67), "Australia": (-32.06, 115.74),
}

ANCHOR_SUPPLIERS = [
    {"id":"supplier_miyota","name":"Citizen Miyota","country":"Japan","latitude":31.8344,"longitude":131.3078,"node_type":"SUPPLIER","status":"ACTIVE"},
    {"id":"supplier_panasonic","name":"Panasonic Energy","country":"Japan","latitude":34.7381,"longitude":135.5633,"node_type":"SUPPLIER","status":"ACTIVE"},
    {"id":"supplier_lens","name":"Lens Technology","country":"China","latitude":28.2282,"longitude":113.0020,"node_type":"SUPPLIER","status":"ACTIVE"},
    {"id":"supplier_jabil","name":"Jabil Mexico","country":"Mexico","latitude":20.7211,"longitude":-103.3918,"node_type":"SUPPLIER","status":"ACTIVE"},
    {"id":"supplier_hlp","name":"HLP Leather","country":"South Africa","latitude":-33.0153,"longitude":27.9116,"node_type":"SUPPLIER","status":"ACTIVE"},
    {"id":"supplier_klabin","name":"Klabin","country":"Brazil","latitude":-24.3244,"longitude":-50.6158,"node_type":"SUPPLIER","status":"ACTIVE"},
]

ANCHOR_PORTS = [
    ("port_yokohama","Port of Yokohama","Japan",35.4437,139.6380),
    ("port_kobe","Port of Kobe","Japan",34.6901,135.1955),
    ("port_tokyo","Port of Tokyo","Japan",35.6175,139.7956),
    ("port_nagoya","Port of Nagoya","Japan",35.0474,136.8430),
    ("port_shanghai","Port of Shanghai","China",31.2304,121.4737),
    ("port_ningbo","Port of Ningbo-Zhoushan","China",29.8683,121.5440),
    ("port_shenzhen","Port of Shenzhen","China",22.5431,114.0579),
    ("port_singapore","Port of Singapore","Singapore",1.3521,103.8198),
    ("port_dubai","Port of Jebel Ali","United Arab Emirates",25.0113,55.0612),
    ("port_mumbai","Port of Mumbai","India",18.9388,72.8354),
    ("port_rotterdam","Port of Rotterdam","Netherlands",51.9244,4.4777),
    ("port_hamburg","Port of Hamburg","Germany",53.5511,9.9937),
    ("port_antwerp","Port of Antwerp","Belgium",51.2667,4.4000),
    ("port_le_havre","Port of Le Havre","France",49.4944,0.1079),
    ("port_valencia","Port of Valencia","Spain",39.4481,-0.3167),
    ("port_veracruz","Port of Veracruz","Mexico",19.1738,-96.1342),
    ("port_santos","Port of Santos","Brazil",-23.9608,-46.3336),
    ("port_durban","Port of Durban","South Africa",-29.8587,31.0218),
    ("port_mombasa","Port of Mombasa","Kenya",-4.0435,39.6682),
    ("port_fremantle","Port of Fremantle","Australia",-32.0569,115.7439),
]

ANCHOR_AIRPORTS = [
    ("airport_tokyo","Tokyo Haneda Cargo Airport","Japan",35.5494,139.7798),
    ("airport_kansai","Kansai Cargo Airport","Japan",34.4347,135.2440),
    ("airport_shanghai","Shanghai Pudong Cargo Airport","China",31.1443,121.8083),
    ("airport_singapore","Singapore Changi Cargo Airport","Singapore",1.3644,103.9915),
    ("airport_frankfurt","Frankfurt Cargo Airport","Germany",50.0379,8.5622),
    ("airport_amsterdam","Amsterdam Schiphol Cargo Airport","Netherlands",52.3105,4.7683),
    ("airport_mexico","Mexico City Cargo Airport","Mexico",19.4361,-99.0719),
    ("airport_sao_paulo","São Paulo Cargo Airport","Brazil",-23.4356,-46.4731),
    ("airport_johannesburg","Johannesburg Cargo Airport","South Africa",-26.1337,28.2420),
]

SEA_CORRIDORS = {
    ("Asia", "Europe"): [[1.3,103.8],[6.5,92],[8,76],[12.1,60],[12.6,43.5],[29.9,32.55],[31.3,32.3],[35.9,-5.6],[43.5,-9.8],[50.5,0.5]],
    ("Africa", "Europe"): [[-34.5,25],[-35,18],[-24,3],[-5,-6],[15,-16],[35,-18],[43.5,-9.8],[50.5,0.5]],
    ("America", "Europe"): [[25,-80],[31,-68],[38,-50],[45,-25],[49,-8],[50.5,0.5]],
    ("Australia", "Asia"): [[-27,112],[-18,108],[-8,105],[1.3,103.8]],
}


def jitter(center, lat_span=3.0, lon_span=4.0):
    return center[0] + RNG.uniform(-lat_span, lat_span), center[1] + RNG.uniform(-lon_span, lon_span)


def node(node_id, name, country, lat, lon, node_type):
    return {"id":node_id,"name":name,"country":country,"latitude":round(lat,5),"longitude":round(lon,5),"node_type":node_type,"status":"ACTIVE"}


def haversine(a, b):
    lat1, lon1, lat2, lon2 = map(math.radians, [a["latitude"], a["longitude"], b["latitude"], b["longitude"]])
    dlat, dlon = lat2-lat1, lon2-lon1
    value = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371 * 2 * math.asin(math.sqrt(value))


def straight_geometry(a, b, bends=2):
    points = [[a["latitude"], a["longitude"]]]
    for i in range(1, bends+1):
        t=i/(bends+1)
        points.append([round(a["latitude"]*(1-t)+b["latitude"]*t,5), round(a["longitude"]*(1-t)+b["longitude"]*t,5)])
    points.append([b["latitude"], b["longitude"]])
    return points


def maritime_group(port):
    lon, lat = port["longitude"], port["latitude"]
    if lon > 90 and lat < -10: return "Australia"
    if lon > 60: return "Asia"
    if lat < 5 and -25 < lon < 55: return "Africa"
    if lon < -30: return "America"
    return "Europe"


def sea_geometry(a, b):
    ga, gb = maritime_group(a), maritime_group(b)
    if ga == gb:
        return straight_geometry(a,b,4)
    key=(ga,gb); reverse=False
    if key not in SEA_CORRIDORS:
        key=(gb,ga); reverse=True
    corridor=SEA_CORRIDORS.get(key, [])
    if reverse: corridor=list(reversed(corridor))
    return [[a["latitude"],a["longitude"]], *corridor, [b["latitude"],b["longitude"]]]


def nearest(nodes, origin, count, max_km=None):
    candidates=sorted((haversine(origin,n),n) for n in nodes if n["id"]!=origin["id"])
    if max_km is not None: candidates=[item for item in candidates if item[0] <= max_km]
    return candidates[:count]


def add_edge(edges, geometries, seen, a, b, mode, risk=None):
    key=(a["id"],b["id"],mode)
    if key in seen: return
    seen.add(key)
    distance=max(1.0,haversine(a,b) * ({"TRUCK":1.22,"RAIL":1.15,"SHIP":1.10,"AIR":1.0,"BARGE":1.18}[mode]))
    edges.append({"source":a["id"],"target":b["id"],"transport_mode":mode,"distance_km":round(distance,1),"risk":risk if risk is not None else {"TRUCK":0.36,"RAIL":0.18,"SHIP":0.24,"AIR":0.62,"BARGE":0.16}[mode],"status":"ACTIVE"})
    geo = sea_geometry(a,b) if mode=="SHIP" else straight_geometry(a,b,3 if mode in {"ROAD","RAIL"} else 1)
    geometries[f'{a["id"]}_{b["id"]}']={"source":a["id"],"target":b["id"],"transport_mode":mode,"ui_mode":{"TRUCK":"LKW","RAIL":"ZUG","SHIP":"SEESCHIFF","AIR":"FLUGZEUG","BARGE":"BINNENSCHIFF"}[mode],"geometry":geo}


def main():
    NODES.mkdir(parents=True, exist_ok=True); ROUTES.mkdir(parents=True, exist_ok=True)
    suppliers=list(ANCHOR_SUPPLIERS)
    ports=[node(*p,"PORT") for p in ANCHOR_PORTS]
    airports=[node(*p,"AIRPORT") for p in ANCHOR_AIRPORTS]
    rail=[]; warehouses=[]; factories=[]

    # 500+ Knoten: verteilt auf 18 Logistikregionen.
    for i in range(84):
        region=list(REGIONS)[i % len(REGIONS)]; lat,lon=jitter(REGIONS[region])
        suppliers.append(node(f"supplier_demo_{i:03d}",f"{region} Supplier {i+1:03d}",region,lat,lon,"SUPPLIER"))
    for i in range(70):
        region=list(REGIONS)[i % len(REGIONS)]; lat,lon=jitter(REGIONS[region],2.0,2.5)
        ports.append(node(f"port_demo_{i:03d}",f"{region} Regional Port {i+1:03d}",region,lat,lon,"PORT"))
    for i in range(71):
        region=list(REGIONS)[i % len(REGIONS)]; lat,lon=jitter(REGIONS[region],3.5,4.5)
        airports.append(node(f"airport_demo_{i:03d}",f"{region} Cargo Airport {i+1:03d}",region,lat,lon,"AIRPORT"))
    for i in range(130):
        region=list(REGIONS)[i % len(REGIONS)]; lat,lon=jitter(REGIONS[region],2.8,3.5)
        rail.append(node(f"rail_demo_{i:03d}",f"{region} Rail Terminal {i+1:03d}",region,lat,lon,"RAIL_TERMINAL"))
    for i in range(130):
        region=list(REGIONS)[i % len(REGIONS)]; lat,lon=jitter(REGIONS[region],2.5,3.0)
        warehouses.append(node(f"warehouse_demo_{i:03d}",f"{region} Distribution Center {i+1:03d}",region,lat,lon,"WAREHOUSE"))
    factories.append(node("factory_heilbronn","Watch Factory Heilbronn","Germany",49.1427,9.2187,"FACTORY"))
    for i in range(9):
        region=list(REGIONS)[i % len(REGIONS)]; lat,lon=jitter(REGIONS[region],2.0,2.0)
        factories.append(node(f"factory_demo_{i:03d}",f"{region} Assembly Plant {i+1:03d}",region,lat,lon,"FACTORY"))

    all_nodes=suppliers+ports+airports+rail+warehouses+factories
    by_id={n["id"]:n for n in all_nodes}
    edges=[]; geometries={}; seen=set()

    # Lokale Redundanz: jeder Lieferant erreicht mehrere Häfen, Flughäfen und Bahnterminals.
    for supplier in suppliers:
        for _,target in nearest(ports,supplier,3): add_edge(edges,geometries,seen,supplier,target,"TRUCK")
        for _,target in nearest(airports,supplier,2): add_edge(edges,geometries,seen,supplier,target,"TRUCK")
        for _,target in nearest(rail,supplier,2): add_edge(edges,geometries,seen,supplier,target,"TRUCK")

    # Straßen-/Schienennetz mit bidirektionalen Nachbarschaftsverbindungen.
    land_nodes=rail+warehouses+factories+ports+airports
    for origin in land_nodes:
        for distance,target in nearest(land_nodes,origin,4,max_km=900):
            mode="RAIL" if origin["node_type"]=="RAIL_TERMINAL" and target["node_type"]=="RAIL_TERMINAL" else "TRUCK"
            add_edge(edges,geometries,seen,origin,target,mode); add_edge(edges,geometries,seen,target,origin,mode)

    # Seehubs: jeder Hafen hat mehrere Alternativen statt nur einer einzigen Route.
    for origin in ports:
        for _,target in nearest(ports,origin,4):
            add_edge(edges,geometries,seen,origin,target,"SHIP")
            add_edge(edges,geometries,seen,target,origin,"SHIP")

    # Luftfrachtnetz: regionale und interkontinentale Redundanz.
    for origin in airports:
        for _,target in nearest(airports,origin,3):
            add_edge(edges,geometries,seen,origin,target,"AIR")
            add_edge(edges,geometries,seen,target,origin,"AIR")
    anchor_air=[by_id[x] for x in ["airport_tokyo","airport_shanghai","airport_singapore","airport_frankfurt","airport_amsterdam","airport_mexico","airport_sao_paulo","airport_johannesburg"]]
    for a in anchor_air:
        for b in anchor_air:
            if a["id"]!=b["id"]: add_edge(edges,geometries,seen,a,b,"AIR")

    # Garantierte Zielanbindung und japanische Redundanz.
    factory=by_id["factory_heilbronn"]
    for target_id in ["port_rotterdam","port_hamburg","port_antwerp","airport_frankfurt","airport_amsterdam"]:
        add_edge(edges,geometries,seen,by_id[target_id],factory,"TRUCK")
    for target_id in ["rail_demo_005","rail_demo_023","rail_demo_041"]:
        if target_id in by_id: add_edge(edges,geometries,seen,by_id[target_id],factory,"RAIL")
    for supplier_id in ["supplier_miyota","supplier_panasonic"]:
        for port_id in ["port_yokohama","port_kobe","port_tokyo","port_nagoya"]:
            add_edge(edges,geometries,seen,by_id[supplier_id],by_id[port_id],"TRUCK")
        for airport_id in ["airport_tokyo","airport_kansai"]:
            add_edge(edges,geometries,seen,by_id[supplier_id],by_id[airport_id],"TRUCK")

    # Dateien schreiben.
    files={"suppliers.json":suppliers,"ports.json":ports,"airports.json":airports,
           "rail_terminals.json":rail,"warehouses.json":warehouses,"factories.json":factories}
    for filename,data in files.items():
        (NODES/filename).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    (ROUTES/"edges.json").write_text(json.dumps(edges,ensure_ascii=False,indent=2),encoding="utf-8")
    (ROUTES/"geometries.json").write_text(json.dumps(geometries,ensure_ascii=False),encoding="utf-8")
    print(f"Erzeugt: {len(all_nodes)} Knoten, {len(edges)} gerichtete Kanten, Seed={SEED}")


if __name__ == "__main__":
    main()
