import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import base64
import os
import re
import io
from datetime import datetime

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
    .site-selection-card {{
        background: #fff;
        border: 2px solid {SUNSURE_GREEN};
        border-radius: 15px;
        box-shadow: 0 3px 12px rgba(10,70,53,0.12);
        padding: 2rem 1.5rem;
        margin: 1rem auto;
        max-width: 800px;
        text-align: center;
    }}
    .site-button {{
        background: linear-gradient(135deg, {SUNSURE_GREEN} 0%, #2d7a5f 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        margin: 0.5rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(10,70,53,0.2);
    }}
    .site-button:hover {{
        background: linear-gradient(135deg, #0d5a42 0%, {SUNSURE_GREEN} 100%);
        box-shadow: 0 4px 12px rgba(10,70,53,0.3);
    }}
    .category-button {{
        background: linear-gradient(135deg, {SUNSURE_RED} 0%, #ff6b54 100%);
        color: white !important;
        border: none;
        border-radius: 18px;
        padding: 1.8rem 2.5rem;
        margin: 1rem;
        font-weight: 700;
        font-size: 1.4rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 18px rgba(253,58,32,0.25);
        min-width: 280px;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .category-button:hover {{
        background: linear-gradient(135deg, #e03426 0%, {SUNSURE_RED} 100%);
        box-shadow: 0 8px 25px rgba(253,58,32,0.35);
        transform: translateY(-2px);
    }}
    .site-section {{
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid #e8e8e8;
    }}
    .section-header {{
        color: {SUNSURE_GREEN};
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 1rem;
        border-bottom: 2px solid {SUNSURE_GREEN};
        padding-bottom: 0.5rem;
    }}
    .esia-card {{
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #dee2e6;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
    }}
    .consultant-logo-placeholder {{
        background: #f8f9fa;
        border: 2px dashed #adb5bd;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        color: #6c757d;
        font-style: italic;
    }}
    .grievance-metric {{
        text-align: center;
        padding: 1rem;
        border-radius: 12px;
        background: #fff;
        box-shadow: 0 1.5px 8px rgba(0,0,0,0.05);
    }}
    .grievance-metric h3 {{
        margin: 0.3rem 0;
        color: {SUNSURE_GREEN};
    }}
    .back-button {{
        background: #6c757d;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        margin: 0.5rem;
        font-weight: 500;
        cursor: pointer;
    }}
    .back-button:hover {{
        background: #5a6268;
    }}
    .risk-category-item {{
        background: #fff;
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 4px solid;
    }}
    .risk-high {{
        border-left-color: #dc3545;
    }}
    .risk-medium {{
        border-left-color: #ffc107;
    }}
    .risk-low {{
        border-left-color: #28a745;
    }}
    </style>
    """
    st.markdown(page_bg_css, unsafe_allow_html=True)

OM_SITES = ["Pailani 1", "Pailani 2", "Pinahat", "Gursarai", "Panwari", "Augasi", "Solapur", "Erandol"]
CONSTRUCTION_SITES = ["Niwali", "Dhule", "Mau", "Erach", "Illayangudi", "Bikaner IV", "Bikaner III", "Kabrai", "Charkhari", "Jath", "Bijapur", "Mundsar"]

if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'site_category' not in st.session_state:
    st.session_state.site_category = None
if 'selected_site' not in st.session_state:
    st.session_state.selected_site = None

with st.sidebar:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, {SUNSURE_RED} 0%, #ff6b54 100%);
                    color: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; text-align: center;">
            <h2 style="margin: 0; font-family: 'Inter', sans-serif;">
                <img src="sunsure_sidebar_icon.png" style="height:32px;vertical-align:middle;margin-bottom:6px;margin-right:7px;">
                SUNSURE ENERGY
            </h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">ESG Data Upload Portal</p>
        </div>
    """, unsafe_allow_html=True)
    if st.session_state.page != 'main':
        if st.button("🏠 Back to Main", key="sidebar_home"):
            st.session_state.page = 'main'
            st.session_state.site_category = None
            st.session_state.selected_site = None
            st.rerun()
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
        sheets = ['Project 1','Site_Template','Consolidated_Data','Data']
        sheet = next((excel_data[s] for s in sheets if s in excel_data), list(excel_data.values())[0])
        state = identify_state(uploaded_file.name)
        cap = 100
        tech = 'Solar' if 'solar' in uploaded_file.name.lower() else 'Wind' if 'wind' in uploaded_file.name.lower() else 'Hybrid'
        match = re.search(r'(\d+)\s*mwp?', uploaded_file.name.lower())
        if match:
            cap = int(match.group(1))
        totals = dict(Water=0, Diesel=0, Elec=0, Cement=0)
        emis = dict(S1=0,S2=0,S3=0)
        month_vals = dict(Water=[0]*12, Diesel=[0]*12, Elec=[0]*12, Cement=[0]*12)
        for _,r in sheet.iterrows():
            desc = str(r.iloc[2]).lower()
            if 'water' in desc:
                _,v=extract_monthly_values(r,['water']); month_vals['Water']=[x+y for x,y in zip(month_vals['Water'],v)]; totals['Water']+=sum(v)
            elif 'diesel' in desc or 'fuel' in desc:
                _,v=extract_monthly_values(r,['diesel']); month_vals['Diesel']=[x+y for x,y in zip(month_vals['Diesel'],v)]; totals['Diesel']+=sum(v); emis['S1']+=sum(v)*0.00268
            elif 'electricity' in desc:
                _,v=extract_monthly_values(r,['electricity']); month_vals['Elec']=[x+y for x,y in zip(month_vals['Elec'],v)]; totals['Elec']+=sum(v); emis['S2']+=sum(v)*0.82/1000
            elif 'cement' in desc:
                _,v=extract_monthly_values(r,['cement']); month_vals['Cement']=[x+y for x,y in zip(month_vals['Cement'],v)]; totals['Cement']+=sum(v); emis['S3']+=sum(v)*0.52/1000
        total_ghg=emis['S1']+emis['S2']+emis['S3']
        return {
            'Site_Name':site_name,'State':state,'Capacity_MW':cap,'Technology':tech,
            'Water_Total':totals['Water'],'Diesel_Total':totals['Diesel'],
            'Electricity_Total':totals['Elec'],'Cement_Total':totals['Cement'],
            'Water_Monthly':month_vals['Water'],'Diesel_Monthly':month_vals['Diesel'],
            'Elec_Monthly':month_vals['Elec'],'Cement_Monthly':month_vals['Cement'],
            'GHG_Total_Scope1':emis['S1'],'GHG_Total_Scope2':emis['S2'],
            'GHG_Total_Scope3':emis['S3'],'GHG_Total':total_ghg
        }
    except Exception as e:
        st.warning(f"Error processing {site_name}: {e}")
        return None

def kpi_card_white(title,value,unit):
    return f"""
    <div class="kpi-card-white">
        <div class="kpi-title-black">{title}</div>
        <div class="kpi-value-red">{value}</div>
        <div class="kpi-unit-gray">{unit}</div>
    </div>"""

def download_buttons(df,state_summary):
    buf=io.BytesIO()
    with pd.ExcelWriter(buf,engine='xlsxwriter') as w:
        df.to_excel(w,sheet_name='Portfolio',index=False)
        state_summary.to_excel(w,sheet_name='States',index=False)
    st.download_button("📊 Download Portfolio (Excel)",buf.getvalue(),
                       "portfolio_report.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.download_button("📋 Download Summary (CSV)",pd.DataFrame([{
        "Sites":len(df),"Capacity_MW":df['Capacity_MW'].sum(),
        "Water_L":df['Water_Total'].sum(),"Diesel_L":df['Diesel_Total'].sum(),
        "GHG_tCO2e":df['GHG_Total'].sum()
    }]).to_csv(index=False),"exec_summary.csv","text/csv")

def render_site_dashboard(site,cat):
    st.markdown(f"<div style='text-align:center; margin-bottom:2rem;'><h1 style='color:{SUNSURE_GREEN};'>"
                f"{site} - {cat}</h1></div>",unsafe_allow_html=True)
    if st.button("⬅️ Back to Sites"):
        st.session_state.page='site_selection';st.session_state.selected_site=None;st.rerun()
    # GHG
    st.markdown("<div class='site-section'><h3 class='section-header'>🌍 GHG Data</h3>",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    c1.markdown(kpi_card_white("Scope1 Emissions","12.5","tCO₂e"),unsafe_allow_html=True)
    c2.markdown(kpi_card_white("Water","45k","L"),unsafe_allow_html=True)
    c3.markdown(kpi_card_white("Diesel","5.2k","L"),unsafe_allow_html=True)
    c4.markdown(kpi_card_white("Clean Gen","8.5k","MWh"),unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)
    # ESIA
    st.markdown("<div class='site-section'><h3 class='section-header'>📋 ESIA Status</h3>",unsafe_allow_html=True)
    col1,col2=st.columns([2,1])
    col1.markdown("<div class='esia-card'><p>Status: Completed ✓</p></div>",unsafe_allow_html=True)
    if col1.button("📄 Download ESIA"):
        st.info("Download link")
    col2.markdown("<div class='consultant-logo-placeholder'>ESIA Logo</div>",unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)
    # Risks
    st.markdown("<div class='site-section'><h3 class='section-header'>⚠️ E&S Risks Callout</h3>",unsafe_allow_html=True)
    b,a,c=st.columns([5,1,5])
    with b:
        st.markdown("<h4>Before Mitigation</h4>" +
                    "<p>Total Risks: <span style='color:#fd3a20;'>22</span></p>" + 
                    "<div class='risk-category-item risk-high'><strong>High:3</strong></div>" +
                    "<div class='risk-category-item risk-medium'><strong>Medium:7</strong></div>" +
                    "<div class='risk-category-item risk-low'><strong>Low:12</strong></div>",
                    unsafe_allow_html=True)
    with a:
        st.markdown("<div style='text-align:center;font-size:2rem;color:#0a4635;margin-top:2rem;'>➡️</div>",unsafe_allow_html=True)
    with c:
        st.markdown("<h4>After Mitigation</h4>" +
                    "<p>Total Risks: <span style='color:#28a745;'>22</span></p>" +
                    "<div class='risk-category-item risk-high' style='opacity:0.3;'><strong>High:0</strong></div>" +
                    "<div class='risk-category-item risk-medium'><strong>Medium:2</strong></div>" +
                    "<div class='risk-category-item risk-low'><strong>Low:20</strong></div>",
                    unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)
    # Approvals
    st.markdown("<div class='site-section'><h3 class='section-header'>📜 Regulatory Approvals</h3>",unsafe_allow_html=True)
    for doc,iss,exp in [("CTE","Jan15,24","Jan14,26"),("CTO","Mar22,24","Mar21,27"),("Intimation","Feb08,24","N/A")]:
        st.markdown(f"<div class='approval-card'><p><strong>{doc}</strong> Issued:{iss} Valid:{exp}</p></div>",unsafe_allow_html=True)
    if st.button("📁 Download Certs"):
        st.info("Download")
    st.markdown("</div>",unsafe_allow_html=True)
    # Grievances
    st.markdown("<div class='site-section'><h3 class='section-header'>📢 Grievances Management</h3>",unsafe_allow_html=True)
    # metrics
    total,resolved,pending,avg=3,1,2,"5 days"
    st.markdown("<div class='grievance-metric'><h3>Total</h3><p>"+str(total)+"</p></div>",unsafe_allow_html=True)
    st.markdown("<div class='grievance-metric'><h3>Resolved</h3><p>"+str(resolved)+"</p></div>",unsafe_allow_html=True)
    st.markdown("<div class='grievance-metric'><h3>Pending</h3><p>"+str(pending)+"</p></div>",unsafe_allow_html=True)
    st.markdown("<div class='grievance-metric'><h3>Avg Resolution</h3><p>"+avg+"</p></div>",unsafe_allow_html=True)
    # by category
    st.markdown("<h4>By Category</h4>",unsafe_allow_html=True)
    cat_df=pd.DataFrame({
        "Category":["EmployeesIt seems the message was cut off. Please request any final adjustments or clarifications!
