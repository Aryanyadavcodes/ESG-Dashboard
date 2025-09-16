"""
Automated ESG Dashboard Portal
=============================
Web-based portal to upload multiple Excel files and generate comprehensive ESG dashboard
Built with Streamlit for easy deployment and use
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import os
import zipfile
import io

# Page configuration
st.set_page_config(
    page_title="ESG Dashboard Portal",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        padding: 1rem 0;
    }
    .kpi-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #2E8B57;
    }
</style>
""", unsafe_allow_html=True)

class ESGDashboardPortal:
    def __init__(self):
        self.processed_data = None
        self.kpis = {}

    def process_excel_file(self, uploaded_file, site_name):
        """Process a single uploaded Excel file"""
        try:
            # Read Excel file
            excel_data = pd.read_excel(uploaded_file, sheet_name=None)

            # Find the main data sheet
            main_sheet_names = ['Project 1', 'Site_Template', 'Consolidated_Data', 'Data']
            main_sheet = None

            for sheet_name in main_sheet_names:
                if sheet_name in excel_data:
                    main_sheet = excel_data[sheet_name]
                    break

            if main_sheet is None:
                main_sheet = list(excel_data.values())[0]

            # Extract site information and KPIs
            site_kpis = self.extract_site_kpis(main_sheet, site_name)

            return site_kpis

        except Exception as e:
            st.error(f"Error processing {site_name}: {str(e)}")
            return None

    def extract_site_kpis(self, data_sheet, site_name):
        """Extract KPIs from a single site's data"""
        kpis = {
            'Site_Name': site_name,
            'Report_Date': datetime.now().strftime('%Y-%m-%d')
        }

        try:
            # Extract diesel consumption
            diesel_total = 0
            water_total = 0
            concrete_total = 0
            steel_total = 0

            # Look for specific rows and extract monthly data
            for idx, row in data_sheet.iterrows():
                row_str = str(row.iloc[2]).lower() if len(row) > 2 else ""

                if 'diesel' in row_str:
                    monthly_values = self.extract_monthly_values(row)
                    diesel_total += sum(monthly_values)

                elif 'water' in row_str:
                    monthly_values = self.extract_monthly_values(row)
                    water_total += sum(monthly_values)

                elif 'concrete' in row_str:
                    monthly_values = self.extract_monthly_values(row)
                    concrete_total += sum(monthly_values)

                elif 'steel' in row_str or 'metal' in row_str:
                    monthly_values = self.extract_monthly_values(row)
                    steel_total += sum(monthly_values)

            # Calculate KPIs
            kpis['Diesel_Consumption_Liters'] = diesel_total
            kpis['Water_Consumption_Liters'] = water_total
            kpis['Concrete_Usage_Tons'] = concrete_total
            kpis['Steel_Usage_Tons'] = steel_total

            # Emission calculations (using standard emission factors)
            kpis['Scope1_Emissions_tCO2e'] = diesel_total * 0.00268  # 2.68 kg CO2e/liter
            kpis['Scope3_Materials_tCO2e'] = (concrete_total * 0.52) + (steel_total * 2.3)  # Material emission factors
            kpis['Total_Emissions_tCO2e'] = kpis['Scope1_Emissions_tCO2e'] + kpis['Scope3_Materials_tCO2e']

            # Assume 100MW capacity (can be extracted from site master data)
            site_capacity = 100
            kpis['Site_Capacity_MW'] = site_capacity
            kpis['Emission_Intensity_tCO2e_per_MW'] = kpis['Total_Emissions_tCO2e'] / site_capacity
            kpis['Water_Intensity_L_per_MW'] = water_total / site_capacity
            kpis['Fuel_Intensity_L_per_MW'] = diesel_total / site_capacity

        except Exception as e:
            st.warning(f"Error extracting KPIs for {site_name}: {str(e)}")

        return kpis

    def extract_monthly_values(self, row):
        """Extract numeric values from monthly columns"""
        values = []
        # Check columns 5-16 for monthly data
        for i in range(5, min(17, len(row))):
            try:
                val = row.iloc[i]
                if pd.isna(val):
                    values.append(0)
                elif isinstance(val, (int, float)):
                    values.append(val)
                elif isinstance(val, str):
                    # Extract numbers from strings like "8500 Litre"
                    import re
                    numbers = re.findall(r'\d+', val)
                    if numbers:
                        values.append(float(numbers[0]))
                    else:
                        values.append(0)
                else:
                    values.append(0)
            except:
                values.append(0)

        return values

    def create_portfolio_dashboard(self, all_site_kpis):
        """Create comprehensive portfolio dashboard"""

        # Convert to DataFrame
        df = pd.DataFrame(all_site_kpis)

        # Portfolio Summary KPIs
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_sites = len(df)
            st.markdown("""
            <div class="kpi-card">
                <h3>Total Sites</h3>
                <div class="metric-value">{}</div>
            </div>
            """.format(total_sites), unsafe_allow_html=True)

        with col2:
            total_capacity = df['Site_Capacity_MW'].sum()
            st.markdown("""
            <div class="kpi-card">
                <h3>Portfolio Capacity</h3>
                <div class="metric-value">{} MW</div>
            </div>
            """.format(total_capacity), unsafe_allow_html=True)

        with col3:
            total_emissions = df['Total_Emissions_tCO2e'].sum()
            st.markdown("""
            <div class="kpi-card">
                <h3>Total GHG Emissions</h3>
                <div class="metric-value">{:.1f} tCO2e</div>
            </div>
            """.format(total_emissions), unsafe_allow_html=True)

        with col4:
            avg_intensity = df['Emission_Intensity_tCO2e_per_MW'].mean()
            st.markdown("""
            <div class="kpi-card">
                <h3>Avg. Emission Intensity</h3>
                <div class="metric-value">{:.2f} tCO2e/MW</div>
            </div>
            """.format(avg_intensity), unsafe_allow_html=True)

        # Create visualizations
        st.markdown("## 📊 Portfolio Analysis")

        # Site-wise emissions chart
        col1, col2 = st.columns(2)

        with col1:
            fig_emissions = px.bar(
                df, 
                x='Site_Name', 
                y='Total_Emissions_tCO2e',
                title='GHG Emissions by Site',
                color='Total_Emissions_tCO2e',
                color_continuous_scale='Reds'
            )
            fig_emissions.update_layout(xaxis=dict(tickangle=45))
            st.plotly_chart(fig_emissions, use_container_width=True)

        with col2:
            # Scope-wise breakdown
            scope_data = {
                'Scope': ['Scope 1', 'Scope 3'],
                'Emissions': [df['Scope1_Emissions_tCO2e'].sum(), df['Scope3_Materials_tCO2e'].sum()]
            }
            fig_scope = px.pie(
                pd.DataFrame(scope_data),
                values='Emissions',
                names='Scope',
                title='Portfolio Emissions by Scope'
            )
            st.plotly_chart(fig_scope, use_container_width=True)

        # Intensity comparison
        col1, col2 = st.columns(2)

        with col1:
            fig_intensity = px.bar(
                df,
                x='Site_Name',
                y='Emission_Intensity_tCO2e_per_MW',
                title='Emission Intensity by Site (tCO2e/MW)',
                color='Emission_Intensity_tCO2e_per_MW',
                color_continuous_scale='Greens'
            )
            fig_intensity.update_layout(xaxis=dict(tickangle=45))
            st.plotly_chart(fig_intensity, use_container_width=True)

        with col2:
            # Resource consumption
            fig_resources = go.Figure()
            fig_resources.add_trace(go.Bar(
                name='Diesel (Liters)',
                x=df['Site_Name'],
                y=df['Diesel_Consumption_Liters'],
                yaxis='y'
            ))
            fig_resources.add_trace(go.Bar(
                name='Water (Liters)',
                x=df['Site_Name'],
                y=df['Water_Consumption_Liters'],
                yaxis='y2'
            ))

            fig_resources.update_layout(
                title='Resource Consumption by Site',
                xaxis=dict(tickangle=45),
                yaxis=dict(title='Diesel (Liters)', side='left'),
                yaxis2=dict(title='Water (Liters)', side='right', overlaying='y'),
                barmode='group'
            )
            st.plotly_chart(fig_resources, use_container_width=True)

        # Data table
        st.markdown("## 📋 Detailed KPI Table")

        # Format the dataframe for display
        display_df = df.copy()
        numeric_columns = ['Diesel_Consumption_Liters', 'Water_Consumption_Liters', 
                          'Total_Emissions_tCO2e', 'Emission_Intensity_tCO2e_per_MW',
                          'Water_Intensity_L_per_MW', 'Fuel_Intensity_L_per_MW']

        for col in numeric_columns:
            if col in display_df.columns:
                if 'Emissions' in col or 'Intensity' in col:
                    display_df[col] = display_df[col].round(2)
                else:
                    display_df[col] = display_df[col].round(0).astype(int)

        st.dataframe(display_df, use_container_width=True)

        # Export functionality
        st.markdown("## 💾 Export Results")

        col1, col2 = st.columns(2)

        with col1:
            # Create Excel export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Portfolio_KPIs', index=False)

            st.download_button(
                label="📊 Download Excel Report",
                data=output.getvalue(),
                file_name=f"ESG_Portfolio_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        with col2:
            # Create CSV export
            csv = df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV Data",
                data=csv,
                file_name=f"ESG_Portfolio_Data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

def main():
    """Main Streamlit app"""

    # Header
    st.markdown('<h1 class="main-header">🌱 ESG Dashboard Portal</h1>', unsafe_allow_html=True)
    st.markdown("### Upload your site Excel files to generate comprehensive ESG KPIs")

    # Initialize the portal
    portal = ESGDashboardPortal()

    # Sidebar for file uploads
    with st.sidebar:
        st.header("📁 File Upload")
        st.markdown("Upload Excel files for each site:")

        uploaded_files = st.file_uploader(
            "Choose Excel files",
            type=['xlsx', 'xls'],
            accept_multiple_files=True,
            help="Upload one Excel file per site"
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} files uploaded")

            process_button = st.button("🚀 Process Files & Generate Dashboard")
        else:
            st.info("Please upload Excel files to continue")
            process_button = False

    # Main content area
    if uploaded_files and process_button:

        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        all_site_kpis = []

        # Process each file
        for i, uploaded_file in enumerate(uploaded_files):

            status_text.text(f"Processing {uploaded_file.name}...")
            progress_bar.progress((i + 1) / len(uploaded_files))

            # Extract site name from filename
            site_name = uploaded_file.name.replace('.xlsx', '').replace('.xls', '')

            # Process the file
            site_kpis = portal.process_excel_file(uploaded_file, site_name)

            if site_kpis:
                all_site_kpis.append(site_kpis)

        status_text.text("✅ All files processed successfully!")

        if all_site_kpis:
            # Create the dashboard
            portal.create_portfolio_dashboard(all_site_kpis)
        else:
            st.error("❌ No data could be extracted from the uploaded files")

    elif not uploaded_files:
        # Landing page content
        st.markdown("""
        ## 🎯 How to Use This Portal

        1. **Upload Excel Files**: Use the sidebar to upload Excel files for each site
        2. **Process Data**: Click "Process Files & Generate Dashboard" 
        3. **View Results**: Comprehensive ESG dashboard will be generated automatically
        4. **Export Reports**: Download Excel or CSV reports for presentations

        ## 📊 What You'll Get

        - **Portfolio Overview**: Total capacity, emissions, and key metrics
        - **Site Comparisons**: Performance across all sites
        - **Emission Analysis**: Scope-wise breakdown and trends
        - **Intensity Metrics**: Per MW performance indicators
        - **Resource Tracking**: Fuel, water, and material consumption
        - **Export Options**: Ready-to-present reports

        ## 🔧 Supported File Formats

        - Excel files (.xlsx, .xls)
        - Should follow the GHG accounting template structure
        - Monthly data in columns 5-16
        - Standard emission source categories

        ## 📋 Sample KPIs Generated

        - Total GHG Emissions (tCO2e)
        - Emission Intensity (tCO2e/MW)
        - Fuel Consumption (Liters)
        - Water Usage (Liters)
        - Material Consumption (Tons)
        - Resource Efficiency Metrics
        """)

        # Demo section
        with st.expander("🔍 See Sample Dashboard"):
            # Create sample data for demo
            sample_data = [
                {'Site_Name': 'Sample Solar Site 1', 'Site_Capacity_MW': 100, 'Total_Emissions_tCO2e': 45.2, 'Emission_Intensity_tCO2e_per_MW': 0.452},
                {'Site_Name': 'Sample Solar Site 2', 'Site_Capacity_MW': 75, 'Total_Emissions_tCO2e': 38.7, 'Emission_Intensity_tCO2e_per_MW': 0.516},
                {'Site_Name': 'Sample Wind Site 1', 'Site_Capacity_MW': 80, 'Total_Emissions_tCO2e': 32.1, 'Emission_Intensity_tCO2e_per_MW': 0.401}
            ]

            sample_df = pd.DataFrame(sample_data)

            fig_sample = px.bar(
                sample_df,
                x='Site_Name',
                y='Total_Emissions_tCO2e',
                title='Sample: GHG Emissions by Site',
                color='Total_Emissions_tCO2e',
                color_continuous_scale='Greens'
            )

            st.plotly_chart(fig_sample, use_container_width=True)

if __name__ == "__main__":
    main()
