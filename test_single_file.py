import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def process_single_site_file(excel_file_path):
    excel_data = pd.read_excel(excel_file_path, sheet_name=None)
    return excel_data

def extract_ghg_data(excel_data):
    main_sheet = None
    for sheet in ['Project 1', 'Site_Template', 'Consolidated_Data', 'Data']:
        if sheet in excel_data:
            main_sheet = excel_data[sheet]
            break
    if main_sheet is None:
        main_sheet = list(excel_data.values())[0]
    return main_sheet

def calculate_kpis(data_sheet):
    # Simplified diesel extraction from Project 1 sheet format
    diesel_rows = data_sheet[data_sheet.iloc[:,2].astype(str).str.contains('Diesel', na=False)]
    diesel_total = 0
    for col in data_sheet.columns[5:17]:
        values = diesel_rows[col].fillna(0)
        for val in values:
            val_str = str(val)
            if val_str.isdigit():
                diesel_total += float(val)
            else:
                try:
                    diesel_total += float(''.join(filter(str.isdigit, val_str)))
                except:
                    continue
    scope1_emissions = diesel_total * 0.00268  # tCO2e
    print(f"Total Diesel Consumption (Liters): {diesel_total:.2f}")
    print(f"Estimated Scope 1 Emissions (tCO2e): {scope1_emissions:.2f}")

def main():
    file = '7.GHG_Data_July-2025_100MW-Solar-project-Solapur-M.xlsx'
    if not os.path.exists(file):
        print(f"❌ File not found: {file}")
        return
    excel_data = process_single_site_file(file)
    main_sheet = extract_ghg_data(excel_data)
    calculate_kpis(main_sheet)

if __name__ == '__main__':
    main()
