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
    page_icon="sunsure_icon.png",
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
    .grievance-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }}
    .grievance-table th, .grievance-table td {{
        border: 1px solid #dee2e6;
        padding: 0.8rem;
        text-align: left;
    }}
    .grievance-table th {{
        background: {SUNSURE_GREEN};
        color: white;
        font-weight: 600;
    }}
    .approval-card {{
        background: #fff;
        border: 1px solid #e8e8e8;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
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

# Site data structure
OM_SITES = ["Pailani 1", "Pailani 2", "Pinahat", "Gursarai", "Panwari", "Augasi", "Solapur", "Erandol"]
CONSTRUCTION_SITES = ["Niwali", "Dhule", "Mau", "Erach", "Illayangudi", "Bikaner IV", "Bikaner III", "Kabrai", "Charkhari", "Jath", "Bijapur", "Mundsar"]

# Session state management
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

def render_site_dashboard(site_name, site_category):
    st.markdown(f"""
    <div style="text-align:center; margin-bottom:2rem;">
        <h1 style="color: {SUNSURE_GREEN}; font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">
            {site_name} - {site_category}
        </h1>
        <p style="color: #666; font-size: 1.1rem;">Site-Specific ESG Performance Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️ Back to Sites", key="back_to_sites"):
            st.session_state.page = 'site_selection'
            st.session_state.selected_site = None
            st.rerun()
    
    # Section 1: GHG Data
    st.markdown('<div class="site-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">🌍 GHG Data & Environmental Metrics</h3>', unsafe_allow_html=True)
    
    # Demo GHG KPIs for the site
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(kpi_card_white("Scope 1 Emissions", "12.5", "tCO₂e"), unsafe_allow_html=True)
    with col2:
        st.markdown(kpi_card_white("Water Consumption", "45,000", "Litres"), unsafe_allow_html=True)
    with col3:
        st.markdown(kpi_card_white("Diesel Usage", "5,200", "Litres"), unsafe_allow_html=True)
    with col4:
        st.markdown(kpi_card_white("Clean Energy Gen.", "8,500", "MWh"), unsafe_allow_html=True)
    
    # Monthly trends (demo)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    demo_emissions = [10, 8, 12, 15, 18, 20, 22, 19, 16, 14, 11, 9]
    
    fig = px.line(x=months, y=demo_emissions, 
                  title=f"Monthly GHG Emissions Trend - {site_name}",
                  labels={'x': 'Month', 'y': 'GHG Emissions (tCO₂e)'},
                  color_discrete_sequence=[SUNSURE_GREEN])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 2: ESIA Study Status
    st.markdown('<div class="site-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">📋 ESIA Study Status</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        <div class="esia-card">
            <h4 style="color: #0a4635; margin-bottom: 1rem;">Environmental & Social Impact Assessment</h4>
            <p><strong>Status:</strong> <span style="color: green;">Completed ✓</span></p>
            <p><strong>Completion Date:</strong> March 15, 2024</p>
            <p><strong>Next Review:</strong> March 2025</p>
            <p><strong>Compliance Level:</strong> Fully Compliant</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📄 Download ESIA Report", key=f"esia_{site_name}"):
            st.info("ESIA Report download link would be activated here")
    
    with col2:
        st.markdown("""
        <div class="consultant-logo-placeholder">
            <p style="margin: 0; font-size: 0.9rem;">ESIA Consultant Logo</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem;">[Logo would appear here]</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 3: E&S Risks Callout
    st.markdown('<div class="site-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">⚠️ E&S Risks Callout</h3>', unsafe_allow_html=True)
    
    # Show Before/After side by side with Streamlit columns
    col_before, col_arrow, col_after = st.columns([5,1,5])
    
    with col_before:
        st.markdown( """
            <div style="text-align: center;">
              <h4>Before Mitigation</h4>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            '''
            <div class="risk-category-item risk-high">
                <strong style="color: #dc3545;">High Risk: 3</strong>
                <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem;">Soil Erosion, Community Impact, Water Depletion</p>
            </div>
            <div class="risk-category-item risk-medium">
                <strong style="color: #ffc107;">Medium Risk: 7</strong>
                <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem;">Noise Impact, Air Quality, Traffic, Waste Management</p>
            </div>
            <div class="risk-category-item risk-low">
                <strong style="color: #28a745;">Low Risk: 12</strong>
                <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem;">Equipment Safety, Documentation, Minor Compliance Issues</p>
            </div>
            ''', unsafe_allow_html=True
        )
    
    with col_arrow:
        st.markdown('<div style="text-align:center; font-size:2.5rem; margin-top: 3rem; color:#0a4635;">➡️</div>', unsafe_allow_html=True)
    
    with col_after:
        st.markdown(
            """
            <div style="text-align: center;">
                <h4>After Mitigation</h4>
            </div>
            """, unsafe_allow_html=True
        )
        st.markdown(
            '''
            <div class="risk-category-item risk-high" style="opacity: 0.3;">
                <strong style="color: #dc3545;">High Risk: 0</strong>
                <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem;">All high risks successfully mitigated</p>
            </div>
            <div class="risk-category-item risk-medium">
                <strong style="color: #ffc107;">Medium Risk: 2</strong>
                <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem;">Construction Noise, Minor Air Quality Monitoring</p>
            </div>
            <div class="risk-category-item risk-low">
                <strong style="color: #28a745;">Low Risk: 20</strong>
                <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem;">All other risks reduced to low category</p>
            </div>
            ''', unsafe_allow_html=True
        )
    
    # Risk Reduction Summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("High Risk Reduction", "100%", delta="-3 risks", delta_color="normal")
    with col2:
        st.metric("Medium Risk Reduction", "71%", delta="-5 risks", delta_color="normal")
    with col3:
        st.metric("Low Risk Increase", "67%", delta="+8 risks", delta_color="inverse")
    
    # Risk Trend Chart using proper DataFrame format
    risk_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    risk_trend = pd.DataFrame({
        'Month': risk_months,
        'High Risk': [3, 3, 2, 1, 0, 0],
        'Medium Risk': [7, 6, 5, 4, 3, 2],
        'Low Risk': [12, 13, 15, 17, 19, 20]
    })
    if st.button("📑 View E&S Risk Register"):
        st.info("Here you can display or download the E&S Risk Register file, table, or link (functionality to be added).")

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 4: Regulatory Approvals
    st.markdown('<div class="site-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">📜 Regulatory Approvals</h3>', unsafe_allow_html=True)
    
    approvals_data = [
        {"Document": "Consent to Establish (CTE)", "Issue Date": "Jan 15, 2024", "Valid Until": "Jan 14, 2026", "Status": "Active"},
        {"Document": "Consent to Operate (CTO)", "Issue Date": "Mar 22, 2024", "Valid Until": "Mar 21, 2027", "Status": "Active"},
        {"Document": "Intimation Letter", "Issue Date": "Feb 08, 2024", "Valid Until": "N/A", "Status": "Acknowledged"}
    ]
    
    for approval in approvals_data:
        st.markdown(f"""
        <div class="approval-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h5 style="margin: 0; color: {SUNSURE_GREEN};">{approval['Document']}</h5>
                    <p style="margin: 0.2rem 0; color: #666;">Issued: {approval['Issue Date']} | Valid Until: {approval['Valid Until']}</p>
                </div>
                <div>
                    <span style="background: {'green' if approval['Status'] == 'Active' else 'blue'}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">
                        {approval['Status']}
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("📁 Download All Certificates", key=f"certs_{site_name}"):
        st.info("All regulatory certificates download would be initiated here")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section 5: Grievances
    st.markdown('<div class="site-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-header">📢 Grievances Management</h3>', unsafe_allow_html=True)
    
    # Demo grievances data
    grievances_data = {
        'Grievance ID': ['GR001', 'GR002', 'GR003'],
        'Date Received': ['2024-08-15', '2024-09-02', '2024-09-10'],
        'Issue Type': ['Noise Complaint', 'Dust Generation', 'Water Quality'],
        'Source': ['Local Resident', 'Farmer', 'Village Head'],
        'Status': ['Resolved', 'In Progress', 'Under Review'],
        'Resolution Date': ['2024-08-20', 'Pending', 'Pending']
    }
    
    st.markdown("<h4 style='margin-bottom:1.5rem;'>Category-wise Grievances Summary</h4>", unsafe_allow_html=True)

    cat_grievances = [ 
    {   total_grievances == sum(cat["Total"] for cat in cat_grievances)
        total_resolved == sum(cat["Resolved"] for cat in cat_grievances)
        total_pending == sum(cat["Pending"] for cat in cat_grievances) },
    {
        "Category": "Employees",
        "Color": "#003865",
        "Total": 6,
        "Resolved": 5,
        "Pending": 1,
        "AvgTime": "3 days"
    },
    {
        "Category": "Community",
        "Color": SUNSURE_GREEN,  # "#0a4635"
        "Total": 8,
        "Resolved": 6,
        "Pending": 2,
        "AvgTime": "5 days"
    },
    {
        "Category": "Workers",
        "Color": SUNSURE_RED,  # "#fd3a20"
        "Total": 5,
        "Resolved": 4,
        "Pending": 1,
        "AvgTime": "4 days"
    },
]

    cols = st.columns(3)
    for i, info in enumerate(cat_grievances):
      cols[i].markdown(f"""
      <div class='grievance-metric' style='background:#fff;box-shadow:0 2px 10px rgba(0,0,0,0.09);border-top:5px solid {info['Color']};margin-bottom:1rem;'>
        <h3 style='color:{info['Color']};margin-bottom:0.5rem;'>{info['Category']}</h3>
        <p style='margin:0.15rem 0;font-size:1.15rem;'><b>Total:</b> {info['Total']}</p>
        <p style='margin:0.10rem 0;color:#198754;font-weight:600;'><b>Resolved:</b> {info['Resolved']}</p>
        <p style='margin:0.10rem 0;color:#fd7e14;font-weight:600;'><b>Pending:</b> {info['Pending']}</p>
        <p style='margin:0.18rem 0 0 0;'><b>Avg Time:</b> {info['AvgTime']}</p>
        s1, s2, s3 = st.columns(3)
        s1.markdown(f"<div class='grievance-metric' style='background:#fff;'><h4 style='color:#003865'>Total Grievances</h4><h2>{total_grievances}</h2></div>", unsafe_allow_html=True)
        s2.markdown(f"<div class='grievance-metric' style='background:#fff;'><h4 style='color:#198754;'>Total Resolved</h4><h2>{total_resolved}</h2></div>", unsafe_allow_html=True)
        s3.markdown(f"<div class='grievance-metric' style='background:#fff;'><h4 style='color:#fd7e14;'>Total Pending</h4><h2>{total_pending}</h2></div>", unsafe_allow_html=True)
      </div>
      """, unsafe_allow_html=True)


def render_site_selection(category):
    sites = OM_SITES if category == "O&M Sites" else CONSTRUCTION_SITES
    
    st.markdown(f"""
    <div class="site-selection-card">
        <h2 style="color: {SUNSURE_GREEN}; margin-bottom: 2rem;">Select {category}</h2>
        <p style="color: #666; margin-bottom: 2rem;">Choose a site to view detailed ESG performance dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Back button
    if st.button("⬅️ Back to Main Menu", key="back_to_main"):
        st.session_state.page = 'main'
        st.session_state.site_category = None
        st.rerun()
    
    # Site buttons in a grid
    cols = st.columns(4)
    for i, site in enumerate(sites):
        with cols[i % 4]:
            if st.button(site, key=f"site_{site}", help=f"View {site} dashboard"):
                st.session_state.selected_site = site
                st.session_state.page = 'site_dashboard'
                st.rerun()

def main():
    # Main page - Site category selection
    if st.session_state.page == 'main':
        # Logo
        try:
            logo = Image.open("Sunsure-Energy_Logo-with-tagline.png")
            st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
            st.image(logo, width=320)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception:
            st.warning("Logo image not found or unable to display.")
        
        # Welcome section
        st.markdown("""
        <div style="text-align:center;margin-top:1.7rem; margin-bottom:0.2rem;">
            <h2 style="color: #0a4635; font-family: 'Inter', sans-serif; font-size: 2.0rem; font-weight:900; letter-spacing:0.06em; margin-bottom: 0.42rem; max-width:1400px; margin-left:auto; margin-right:auto; white-space:nowrap;overflow-x:auto;">
                Welcome to Sunsure Energy ESG&nbsp;Dashboard
            </h2>
            <p style="font-size: 1.2rem; color: #111111; font-weight:600; max-width:1280px; margin: 0 auto 2.1rem auto; line-height: 1.7;">
                Professional ESG performance dashboard for Sunsure Energy's renewable energy&nbsp;portfolio.
                Upload your site data to generate comprehensive sustainability reports.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
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
        
        # Site category selection
        st.markdown("""
        <div style="text-align:center; margin: 3rem 0;">
            <h2 style="color: #0a4635; margin-bottom: 2.5rem; font-size: 2.2rem; font-weight: 800;">Select Site Category</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔧 O&M Sites", key="om_sites", help="Operations & Maintenance Sites"):
                    st.session_state.site_category = "O&M Sites"
                    st.session_state.page = 'site_selection'
                    st.rerun()
            
            with col_b:
                if st.button("🏗️ Construction Sites", key="construction_sites", help="Under Construction Sites"):
                    st.session_state.site_category = "Construction Sites"
                    st.session_state.page = 'site_selection'
                    st.rerun()
        
        # Portfolio dashboard section (if files uploaded)
        if uploaded_files:
            st.markdown('<hr style="margin: 3rem 0;">', unsafe_allow_html=True)
            
            st.markdown('<div style="text-align:center; margin-bottom:0.2rem;">', unsafe_allow_html=True)
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
            st.markdown("Click the button below to generate your portfolio dashboard:")
            dashboard_trigger = st.button("🚀 Generate Portfolio Dashboard", key="gen_button")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if dashboard_trigger:
                # Process files and show portfolio dashboard
                all_site_kpis = []
                for file in uploaded_files:
                    site_dict = process_excel_file(file, file.name.replace('.xlsx','').replace('.xls',''))
                    if site_dict:
                        all_site_kpis.append(site_dict)
                
                if all_site_kpis:
                    df = pd.DataFrame(all_site_kpis)
                    
                    st.subheader("Portfolio Executive Summary")
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
                    
                    st.subheader("Export / Download Reports")
                    download_buttons(df, state_summary)
    
    # Site selection page
    elif st.session_state.page == 'site_selection':
        render_site_selection(st.session_state.site_category)
    
    # Individual site dashboard
    elif st.session_state.page == 'site_dashboard':
        render_site_dashboard(st.session_state.selected_site, st.session_state.site_category)

if __name__ == "__main__":
    main()















