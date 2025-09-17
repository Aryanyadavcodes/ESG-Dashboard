import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64
import os
import re
import io

SUNSURE_GREEN = "#0a4635"
SUNSURE_RED = "#fd3a20"
SUNSURE_BLACK = "#111111"

st.set_page_config(
    page_title="Sunsure Energy | ESG Performance Dashboard",
    page_icon="Logo_Icon_red.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_path = "homepage-flyer1.jpg"
if os.path.exists(img_path):
    img_base64 = get_base64_of_bin_file(img_path)
    page_bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)), url("data:image/jpg;base64,{img_base64}");
        background-size: cover; background-repeat:no-repeat; background-position:center;
    }}
    .feature-card {{
        background: #fff; border-radius: 14px; box-shadow: 0 2.5px 9px rgba(0,0,0,0.04);
        padding: 1.1rem 1rem; text-align:center;
    }}
    .kpi-card-white {{
        background: #fff;
        border: 1.7px solid #ececec;
        border-radius: 16px;
        box-shadow: 0 1.5px 8px rgba(0,0,0,0.09);
        padding: 1.1rem 0.9rem 1rem 0.9rem;
        text-align: center;
        margin-bottom: 0.8rem;
        min-width:118px; max-width:170px; 
        margin-left:auto; margin-right:auto; 
        display:block;
    }}
    .kpi-title-black {{
        font-size: 1.08rem;
        color: {SUNSURE_BLACK};
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-bottom: 0.7rem;
        text-transform: uppercase;
    }}
    .kpi-value-red {{
        font-size: 2.19rem;
        font-weight: bold;
        color: {SUNSURE_RED};
        margin-bottom: 0.18rem;
    }}
    .kpi-unit-gray {{
        font-size: 1.02rem;
        color: #444;
        font-weight: 510;
    }}
    </style>
    """
    st.markdown(page_bg_css, unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, {SUNSURE_RED} 0%, #ff6b54 100%);
                    color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; text-align: center;">
            <h2 style="margin: 0; font-family: 'Inter', sans-serif;">
                SUNSURE ENERGY
            </h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">ESG Data Upload Portal</p>
        </div>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Upload Site Excel Files",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="Upload Excel files from Sunsure Energy sites"
    )
    with st.expander("ℹ️ About Sunsure Energy"):
        st.markdown(
            '<a href="https://sunsure-energy.com/" target="_blank" style="color:#fd3a20;font-weight:600;text-decoration:underline;">Visit the official Sunsure Energy website</a>',
            unsafe_allow_html=True
        )

def identify_state(filename):
    mapping = {
        'solapur': 'Maharashtra', 'augasi': 'Uttar Pradesh', 'panwari': 'Uttar Pradesh',
        'pailani': 'Uttar Pradesh', 'gujarat': 'Gujarat', 'rajasthan': 'Rajasthan',
        'karnataka': 'Karnataka', 'tamil nadu': 'Tamil Nadu', 'telangana': 'Telangana',
        'madhya pradesh': 'Madhya Pradesh', 'haryana': 'Haryana', 'punjab': 'Punjab',
        'odisha': 'Odisha', 'jharkhand': 'Jharkhand', 'chhattisgarh': 'Chhattisgarh'
    }
    filename_lower = filename.lower()
    for key, state in mapping.items():
        if key in filename_lower:
            return state
    return 'Unknown'

def extract_monthly_values(row, resource_keys):
    months = ['January','February','March','April','May','June','July',
              'August','September','October','November','December']
    values = []
    for i, month in enumerate(months, 5):
        try:
            val = row.iloc[i] if i < len(row) else 0
            if pd.isna(val):
                values.append(0)
            elif isinstance(val, (float, int)):
                values.append(val)
            elif isinstance(val, str):
                numbers = re.findall(r'\d+\.?\d*', val)
                values.append(float(numbers[0]) if numbers else 0)
            else:
                values.append(0)
        except Exception:
            values.append(0)
    return months, values

def process_excel_file(uploaded_file, site_name):
    try:
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        main_sheet_names = ['Project 1', 'Site_Template', 'Consolidated_Data', 'Data']
        main_sheet = None
        for sheet_name in main_sheet_names:
            if sheet_name in excel_data:
                main_sheet = excel_data[sheet_name]
                break
        if main_sheet is None:
            main_sheet = list(excel_data.values())[0]
        state = identify_state(uploaded_file.name)
        capacity = 100
        tech = 'Solar' if 'solar' in uploaded_file.name.lower() else (
            'Wind' if 'wind' in uploaded_file.name.lower() else 'Hybrid')
        cap_match = re.search(r'(\d+)\s*mwp?', uploaded_file.name.lower())
        if cap_match:
            capacity = int(cap_match.group(1))
        water_total, diesel_total, elec_total, cement_total, ghg_total_s1, ghg_total_s2, ghg_total_s3 = 0,0,0,0,0,0,0
        water_monthly = [0]*12
        diesel_monthly = [0]*12
        elec_monthly = [0]*12
        cement_monthly = [0]*12
        for idx, row in main_sheet.iterrows():
            if len(row) < 4:
                continue
            desc_str = str(row.iloc[2]).lower()
            if "water" in desc_str:
                m,v = extract_monthly_values(row, 'water')
                water_monthly = [w+val for w,val in zip(water_monthly, v)]
                water_total += sum(v)
            elif "diesel" in desc_str or "fuel" in desc_str:
                m,v = extract_monthly_values(row,"diesel")
                diesel_monthly = [d+val for d, val in zip(diesel_monthly, v)]
                diesel_total += sum(v)
                ghg_total_s1 += sum(v)*0.00268
            elif "electricity" in desc_str:
                m,v = extract_monthly_values(row,"electricity")
                elec_monthly = [e+val for e,val in zip(elec_monthly, v)]
                elec_total += sum(v)
                ghg_total_s2 += sum(v)*0.82/1000
            elif "cement" in desc_str:
                m,v = extract_monthly_values(row,"cement")
                cement_monthly = [c+val for c,val in zip(cement_monthly, v)]
                cement_total += sum(v)
                ghg_total_s3 += sum(v)*0.52/1000
        ghg_total = ghg_total_s1 + ghg_total_s2 + ghg_total_s3

        return {
            'Site_Name': site_name, 'State': state, 'Capacity_MW': capacity, 'Technology': tech,
            'Water_Total': water_total, 'Diesel_Total': diesel_total,
            'Electricity_Total': elec_total, 'Cement_Total': cement_total,
            'Water_Monthly': water_monthly, 'Diesel_Monthly': diesel_monthly,
            'Elec_Monthly': elec_monthly, 'Cement_Monthly': cement_monthly,
            'GHG_Total_Scope1': ghg_total_s1, 'GHG_Total_Scope2': ghg_total_s2,
            'GHG_Total_Scope3': ghg_total_s3, 'GHG_Total': ghg_total
        }
    except Exception as e:
        st.warning(f"Error processing {site_name}: {e}")
        return None

def kpi_card_white(title, value, unit):
    return f"""
    <div class="kpi-card-white">
        <div class="kpi-title-black">{title}</div>
        <div class="kpi-value-red">{value}</div>
        <div class="kpi-unit-gray">{unit}</div>
    </div>"""

def download_buttons(df, state_summary):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Portfolio_KPIs', index=False)
        state_summary.to_excel(writer, sheet_name='State_Summary', index=False)
    st.download_button(
        label="📊 Download Portfolio Report (Excel)",
        data=output.getvalue(),
        file_name="Sunsure_ESG_Portfolio_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.download_button(
        label="🗺️ Download State Analysis (CSV)",
        data=state_summary.to_csv(index=False),
        file_name="Sunsure_State_Analysis.csv",
        mime="text/csv"
    )
    executive_summary = {
        "Portfolio Sites": len(df),
        "Total Capacity (MW)": df['Capacity_MW'].sum(),
        "Total Water (Litres)": df['Water_Total'].sum(),
        "Total Diesel (Litres)": df['Diesel_Total'].sum(),
        "Total GHG Emissions (tCO2e)": df['GHG_Total'].sum()
    }
    exec_df = pd.DataFrame([executive_summary])
    st.download_button(
        label="📋 Download Executive Summary (CSV)",
        data=exec_df.to_csv(index=False),
        file_name="Sunsure_Executive_Summary.csv",
        mime="text/csv"
    )

def main():
    if not uploaded_files:
        try:
            logo = Image.open("Sunsure-Energy_Logo-with-tagline.png")
            st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
            st.image(logo, width=320)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception:
            st.warning("Logo image not found or unable to display.")
        st.markdown("""
        <div style="text-align:center;margin-top:1.7rem; margin-bottom:0.2rem;">
            <h2 style="color: #0a4635; font-family: 'Inter', sans-serif; font-size: 2.0rem; font-weight:900; letter-spacing:0.06em; margin-bottom: 0.42rem; max-width:1400px; margin-left:auto; margin-right:auto; white-space:nowrap;overflow-x:auto;">
                Welcome to Sunsure Energy ESG&nbsp;Dashboard
            </h2>
            <p style="font-size: 1.2rem; color: #111111; font-weight:600; max-width:1280px; margin: 0 auto 2.1rem auto; line-height: 1.7;">
                Professional ESG performance dashboard for Sunsure Energy's renewable energy&nbsp;portfolio.
                <br>Upload your site data to generate comprehensive sustainability reports.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex; gap:1.6rem; justify-content:center; margin-bottom:2.5rem;">
            <div class="feature-card">
                <h3>🎯 Professional ESG Analytics</h3>
                <p>Industry-leading ESG metrics tailored for Sunsure Energy's portfolio with comprehensive KPI tracking</p>
            </div>
            <div class="feature-card">
                <h3>🗺️ Multi-State Operations</h3>
                <p>Track performance across Maharashtra, Uttar Pradesh, and other states with geographic insights</p>
            </div>
            <div class="feature-card">
                <h3>📊 Executive Reporting</h3>
                <p>Boardroom-ready dashboards and reports for Sunsure leadership and stakeholder presentations</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown('<div style="text-align:center; margin-bottom:0.2rem;">', unsafe_allow_html=True)
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
    st.markdown("Click the button below to generate your ESG dashboard:")
    dashboard_trigger = st.button("🚀 Generate Dashboard", key="gen_button")
    st.markdown('</div>', unsafe_allow_html=True)
    if not dashboard_trigger:
        st.stop()

    all_site_kpis = []
    for file in uploaded_files:
        site_dict = process_excel_file(file, file.name.replace('.xlsx','').replace('.xls',''))
        if site_dict:
            all_site_kpis.append(site_dict)
    df = pd.DataFrame(all_site_kpis)

    st.subheader("Executive Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(kpi_card_white("Portfolio Sites", len(df), "Sites"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card_white("Total Capacity", f"{df['Capacity_MW'].sum():,.0f}", "MW"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card_white("Total Water", f"{df['Water_Total'].sum():,.0f}", "Litres"), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_card_white("Total Diesel", f"{df['Diesel_Total'].sum():,.0f}", "Litres"), unsafe_allow_html=True)
    with col5:
        st.markdown(kpi_card_white("Total GHG Emissions", f"{df['GHG_Total'].sum():,.2f}", "tCO₂e"), unsafe_allow_html=True)

    st.subheader("State-wise Performance")
    state_summary = df.groupby('State').agg({
        'Capacity_MW': 'sum',
        'Water_Total': 'sum',
        'Diesel_Total': 'sum',
        'GHG_Total': 'sum',
        'Site_Name': 'count'
    }).reset_index().rename(columns={'Site_Name': 'Num_Sites'})
    st.dataframe(state_summary, use_container_width=True, hide_index=True)

    st.subheader("Performance Analytics")
    months = ['January','February','March','April','May','June','July','August','September','October','November','December']

    st.write("### 💧 Water Supply Consumption")
    if len(df) == 1:
        st.info(f"Monthly water supply data for: {df.iloc[0]['Site_Name']}")
        fig_water = px.bar(
            x=months, y=df.iloc[0]['Water_Monthly'],
            labels={'x': 'Month', 'y': 'Water Supply Consumption (Litres)'},
            title=f"Water Supply Consumption (Monthly) — {df.iloc[0]['Site_Name']}",
            color_discrete_sequence=[SUNSURE_GREEN],
        )
        st.plotly_chart(fig_water, use_container_width=True)
    else:
        st.info("Total water supply consumption for each site (cumulative):")
        fig_water = px.bar(
            x=df['Site_Name'], y=df['Water_Total'],
            labels={'x': 'Site', 'y': 'Total Water Supply Consumption (Litres)'},
            title='Site-wise Cumulative Water Supply Consumption',
            color_discrete_sequence=[SUNSURE_GREEN]
        )
        st.plotly_chart(fig_water, use_container_width=True)

    st.write("### ⛽ Diesel (Fuel) Consumption")
    if len(df) == 1:
        st.info(f"Monthly diesel consumption for: {df.iloc[0]['Site_Name']}")
        fig_diesel = px.bar(
            x=months, y=df.iloc[0]['Diesel_Monthly'],
            labels={'x': 'Month', 'y': 'Diesel Consumption (Litres)'},
            title=f"Diesel Consumption (Monthly) — {df.iloc[0]['Site_Name']}",
            color_discrete_sequence=[SUNSURE_RED]
        )
        st.plotly_chart(fig_diesel, use_container_width=True)
    else:
        st.info("Total diesel consumption for each site (cumulative):")
        fig_diesel = px.bar(
            x=df['Site_Name'], y=df['Diesel_Total'],
            labels={'x': 'Site', 'y': 'Total Diesel Consumption (Litres)'},
            title='Site-wise Cumulative Diesel Consumption',
            color_discrete_sequence=[SUNSURE_RED]
        )
        st.plotly_chart(fig_diesel, use_container_width=True)

    st.write("### 🌍 GHG Emissions (Scope 1 only)")
    if len(df) == 1:
        st.info(f"Monthly scope 1 GHG emissions for: {df.iloc[0]['Site_Name']}")
        scope1 = [x*0.00268 for x in df.iloc[0]['Diesel_Monthly']]
        fig_ghg = px.bar(
            x=months, y=scope1,
            labels={'x':'Month','y':'GHG Emissions Scope 1 (tCO₂e)'},
            title=f"GHG Emissions Scope 1 - Diesel (Monthly) — {df.iloc[0]['Site_Name']}",
            color_discrete_sequence=['#00AF9B']
        )
        st.plotly_chart(fig_ghg, use_container_width=True)
    else:
        st.info("GHG emissions Scope 1 (diesel only) for each site:")
        fig_ghg = px.bar(
            x=df['Site_Name'], y=df['GHG_Total_Scope1'],
            labels={'x': 'Site', 'y': 'GHG Scope 1 Emissions (tCO₂e)'},
            title='Site-wise Scope 1 (Diesel) GHG Emissions',
            color_discrete_sequence=['#00AF9B']
        )
        st.plotly_chart(fig_ghg, use_container_width=True)

    st.subheader("Export / Download Reports")
    download_buttons(df, state_summary)

if __name__ == "__main__":
    main()

