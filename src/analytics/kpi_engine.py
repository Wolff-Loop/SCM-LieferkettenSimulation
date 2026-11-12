class KPIEngine:
    @staticmethod
    def calculate(routes=None,event_count=0,day=0,expected_chains=6):
        routes=routes or []
        keys=['material_cost','labor_cost','purchase_cost','quality_cost','transport_cost','customs_cost','risk_surcharge','inventory_cost','carbon_cost','total_cost']
        totals={k:sum(r.get('cost_breakdown',{}).get(k,0) for r in routes) for k in keys}
        if not routes:
            return {**totals,'co2_emissions':0,'lead_time':0,'risk_score':100 if event_count else 0,'service_level':0}
        lead=max(r['total_time_h'] for r in routes)/24; risk=sum(r['total_risk'] for r in routes)/len(routes)
        completeness=len(routes)/expected_chains
        return {**{k:round(v,2) for k,v in totals.items()},'co2_emissions':round(sum(r['total_co2']*(r.get('quantity',1)*r.get('weight_kg_per_unit',0)/1000) for r in routes),2),'lead_time':round(lead,1),'risk_score':round(min(100,risk*10+event_count*10),1),'service_level':round(max(0,98*completeness-event_count*5),1)}
