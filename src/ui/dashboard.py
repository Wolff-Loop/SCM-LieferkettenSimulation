from PySide6.QtWidgets import QGridLayout,QLabel,QWidget
KPI_NAMEN={'total_cost':'Gesamtkosten (€)','purchase_cost':'Einkauf inkl. Arbeit (€)','material_cost':'Materialkosten (€)','labor_cost':'Arbeitskosten (€)','transport_cost':'Transportkosten (€)','customs_cost':'Zollkosten (€)','inventory_cost':'Kapitalbindung (€)','quality_cost':'Qualitätskosten (€)','carbon_cost':'CO₂-Kosten (€)','co2_emissions':'CO₂ (kg)','lead_time':'Lieferzeit (Tage)','risk_score':'Risikoscore','service_level':'OTIF (%)'}
class Dashboard(QWidget):
 def __init__(self):
  super().__init__();layout=QGridLayout(self);self.werte={}
  for row,(key,name) in enumerate(KPI_NAMEN.items()):
   layout.addWidget(QLabel(name),row,0);v=QLabel('–');v.setStyleSheet('font-weight:bold;');layout.addWidget(v,row,1);self.werte[key]=v
 def update_kpis(self,kpis):
  for key,label in self.werte.items():
   if key in kpis: label.setText(f'{kpis[key]:,.2f}' if isinstance(kpis[key],float) else str(kpis[key]))
