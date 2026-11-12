import networkx as nx
from src.routing.network_loader import NetworkLoader
from src.routing.graph_builder import GraphBuilder
from src.routing.routing_engine import RoutingEngine
from src.analytics.cost_engine import CostEngine

class Application:
    def __init__(self): self.reload_network()
    def reload_network(self):
        self.network_data=NetworkLoader().load_network_data(); self.graph=GraphBuilder().build(self.network_data)
        self.routing_engine=RoutingEngine(self.graph); self.products=self.network_data['products']
        self.country_economics=self.network_data['country_economics']; self.economic_config=self.network_data['economic_config']
        self.cost_engine=CostEngine(self.country_economics,self.economic_config)
    def calculate_route(self,source,target,strategy='FASTEST'): return self.routing_engine.calculate_route(source,target,strategy)
    def calculate_product_route(self,product,strategy='FASTEST'):
        candidates=[]
        for sid in product.get('supplier_ids',[product.get('supplier_id')]):
            if not sid or sid not in self.graph: continue
            try:
                route=self.calculate_route(sid,product['destination_id'],strategy)
                supplier=self.graph.nodes[sid]; breakdown=self.cost_engine.calculate(product,supplier,route)
                route.update({'selected_supplier_id':sid,'selected_supplier_name':supplier.get('name',sid),'supplier_country':supplier.get('country'),'cost_breakdown':breakdown,'economic_total_cost':breakdown['total_cost']})
                candidates.append(route)
            except (nx.NetworkXNoPath,nx.NodeNotFound): pass
        if not candidates: raise nx.NetworkXNoPath(f'Kein qualifizierter Lieferant für {product["name"]} erreichbar')
        metric={'FASTEST':'total_time_h','CHEAPEST':'economic_total_cost','LOWEST_CO2':'total_co2','MOST_RESILIENT':'total_risk'}[strategy]
        return min(candidates,key=lambda x:x[metric])
    def calculate_all_product_routes(self,strategy='FASTEST'): return [{**p,**self.calculate_product_route(p,strategy)} for p in self.products]
    def set_country_economics(self,country,labor_cost=None,duty_rate=None,risk_rate=None):
        values=self.country_economics[country]
        if labor_cost is not None: values['loaded_labor_cost_eur_h']=float(labor_cost)
        if duty_rate is not None: values['duty_rate']=float(duty_rate)
        if risk_rate is not None: values['risk_surcharge_rate']=float(risk_rate)
    def get_country_economics(self): return self.country_economics
    def get_map_nodes(self):
        mp={'SUPPLIER':'LIEFERANT','PORT':'HAFEN','AIRPORT':'FLUGHAFEN','FACTORY':'FABRIK','WAREHOUSE':'LAGER','RAIL_TERMINAL':'TERMINAL','BOTTLENECK':'ENGPASS'}
        return [{'id':n,'name':d.get('name',n),'country':d.get('country','Unknown'),'lat':d['latitude'],'lon':d['longitude'],'typ':mp.get(d.get('node_type'),'TERMINAL'),'status':d.get('status','ACTIVE')} for n,d in self.graph.nodes(data=True) if 'latitude' in d and 'longitude' in d]
    def get_network_statistics(self): return {'nodes':self.graph.number_of_nodes(),'edges':self.graph.number_of_edges()}
    def node_ids_for_name_or_country(self,target): return [n for n,d in self.graph.nodes(data=True) if d.get('name')==target or d.get('country')==target] if target else []
