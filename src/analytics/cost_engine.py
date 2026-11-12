class CostEngine:
    def __init__(self, countries, config):
        self.countries = countries
        self.config = config

    def calculate(self, product, supplier, route):
        qty=float(product.get('quantity',1)); weight_t=qty*float(product.get('weight_kg_per_unit',0))/1000
        country=self.countries.get(supplier.get('country'),self.countries['Unknown'])
        material=qty*float(supplier.get('material_cost_per_unit_eur',0))
        labor=qty*float(supplier.get('labor_hours_per_unit',0))*float(country['loaded_labor_cost_eur_h'])
        purchase=material+labor
        quality_loss=qty*(1-float(supplier.get('quality_yield',1.0)))*float(self.config['quality_failure_cost_eur_per_unit'])
        transport=float(route['total_cost'])*weight_t + len(route['segments'])*float(self.config['handling_cost_per_segment_eur'])
        customs=(purchase+transport)*float(country['duty_rate'])
        risk=(purchase+transport)*float(country['risk_surcharge_rate'])
        lead_days=float(route['total_time_h'])/24
        inventory=(purchase+transport)*float(self.config['inventory_carrying_rate_per_year'])*(lead_days/365)
        carbon=float(route['total_co2'])*weight_t/1000*float(self.config['carbon_price_eur_per_tonne'])
        total=purchase+quality_loss+transport+customs+risk+inventory+carbon
        return {k:round(v,2) for k,v in {
            'material_cost':material,'labor_cost':labor,'purchase_cost':purchase,
            'quality_cost':quality_loss,'transport_cost':transport,'customs_cost':customs,
            'risk_surcharge':risk,'inventory_cost':inventory,'carbon_cost':carbon,
            'total_cost':total}.items()}
