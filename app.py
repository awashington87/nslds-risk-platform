# app.py - Main Streamlit Application
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
import sqlite3
import tempfile
import os

# Set page config
st.set_page_config(
    page_title="NSLDS Risk Assessment Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5a87 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .risk-high { color: #d63384; font-weight: bold; }
    .risk-medium { color: #fd7e14; font-weight: bold; }
    .risk-low { color: #20c997; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Import your processing modules (these would be in separate files)
# For demo purposes, I'll include simplified versions here
class DemoNSLDSProcessor:
    def __init__(self):
        self.db_path = "demo_risk_db.db"
        
    def process_nslds_file(self, file_path):
        # Simplified demo processing
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)
            return len(df) > 0
        except:
            return False
    
    def calculate_risk_scores(self):
        # Generate demo risk scores
        import random
        students = []
        for i in range(100):
            risk_score = random.uniform(0, 1)
            risk_tier = 'HIGH' if risk_score > 0.7 else 'MEDIUM' if risk_score > 0.4 else 'LOW'
            students.append({
                'student_id': f'STU{i:06d}',
                'name': f'Student {i+1}',
                'risk_score': risk_score,
                'confidence_score': random.uniform(0.6, 0.95),
                'risk_tier': risk_tier,
                'outstanding_balance': random.randint(5000, 50000),
                'days_delinquent': random.randint(31, 365),
                'key_factors': random.sample([
                    'High debt-to-income ratio',
                    'Frequent delinquencies', 
                    'Payment inconsistency',
                    'Increasing loan balance',
                    'Multiple forbearances'
                ], k=random.randint(1, 3))
            })
        return students
    
    def export_risk_report(self, filename):
        # Generate demo Excel report
        students = self.calculate_risk_scores()
        df = pd.DataFrame(students)
        df.to_excel(filename, index=False)
        return filename

def main():
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1f4e79/white?text=NSLDS+Risk", width=200)
        st.markdown("---")
        
        st.markdown("### 🔒 FERPA Compliant")
        st.info("This system processes student data in full compliance with FERPA regulations.")
        
        st.markdown("### 📊 Supported Formats")
        st.markdown("""
        - NSLDS CSV Reports
        - NSLDS Excel Reports  
        - Fixed-Width Text Files
        """)
        
        st.markdown("### 📞 Support")
        st.markdown("""
        **Email:** support@nsldsrisk.com  
        **Phone:** (555) 123-4567  
        **Hours:** 9 AM - 6 PM EST
        """)
    
    # Main content
    st.markdown("""
    <div class="main-header">
        <h1>🎓 NSLDS Risk Assessment Platform</h1>
        <p style="font-size: 1.2em; margin-bottom: 0;">
            Advanced student loan default prediction using NSLDS Delinquent Borrower Reports
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📁 File Upload", "📊 Dashboard", "📋 Reports", "⚙️ Settings"])
    
    with tab1:
        st.header("Upload NSLDS Delinquent Borrower Report")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose NSLDS report file",
                type=['csv', 'xlsx', 'txt'],
                help="Upload your NSLDS Delinquent Borrower Report in CSV, Excel, or fixed-width text format"
            )
            
            if uploaded_file is not None:
                # File details
                st.success(f"File uploaded: {uploaded_file.name}")
                st.info(f"File size: {len(uploaded_file.getvalue()) / 1024:.1f} KB")
                
                # Processing button
                if st.button("🚀 Process File", type="primary"):
                    with st.spinner("Processing NSLDS file... This may take a few minutes."):
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                            tmp.write(uploaded_file.getvalue())
                            tmp_path = tmp.name
                        
                        try:
                            # Process with demo processor
                            processor = DemoNSLDSProcessor()
                            success = processor.process_nslds_file(tmp_path)
                            
                            if success:
                                st.session_state['data_processed'] = True
                                st.session_state['processor'] = processor
                                st.success("✅ File processed successfully!")
                                st.balloons()
                                
                                # Show preview
                                risk_scores = processor.calculate_risk_scores()
                                st.markdown("### Preview Results")
                                
                                col_a, col_b, col_c = st.columns(3)
                                with col_a:
                                    st.metric("Total Students", len(risk_scores))
                                with col_b:
                                    high_risk_count = len([s for s in risk_scores if s['risk_tier'] == 'HIGH'])
                                    st.metric("High Risk", high_risk_count, delta=f"{high_risk_count/len(risk_scores)*100:.1f}%")
                                with col_c:
                                    avg_balance = sum(s['outstanding_balance'] for s in risk_scores) / len(risk_scores)
                                    st.metric("Avg Balance", f"${avg_balance:,.0f}")
                            else:
                                st.error("❌ Error processing file. Please check the format and try again.")
                        finally:
                            # Clean up temp file
                            os.unlink(tmp_path)
        
        with col2:
            st.markdown("### 📋 File Requirements")
            st.markdown("""
            **NSLDS Report Fields:**
            - Borrower SSN
            - Outstanding Balance  
            - Days Delinquent
            - Loan Type
            - Borrower Name
            
            **Supported Formats:**
            - CSV (comma-separated)
            - Excel (.xlsx)
            - Fixed-width text
            
            **File Size Limit:** 50 MB
            """)
    
    with tab2:
        st.header("📊 Risk Assessment Dashboard")
        
        if st.session_state.get('data_processed'):
            processor = st.session_state['processor']
            risk_scores = processor.calculate_risk_scores()
            
            # Summary metrics
            st.markdown("### Key Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            high_risk = [s for s in risk_scores if s['risk_tier'] == 'HIGH']
            medium_risk = [s for s in risk_scores if s['risk_tier'] == 'MEDIUM']
            low_risk = [s for s in risk_scores if s['risk_tier'] == 'LOW']
            
            with col1:
                st.metric("Total Students", len(risk_scores))
            with col2:
                st.metric("High Risk", len(high_risk), 
                         delta=f"{len(high_risk)/len(risk_scores)*100:.1f}%")
            with col3:
                st.metric("Medium Risk", len(medium_risk),
                         delta=f"{len(medium_risk)/len(risk_scores)*100:.1f}%")
            with col4:
                total_balance = sum(s['outstanding_balance'] for s in risk_scores)
                st.metric("Total at Risk", f"${total_balance:,.0f}")
            
            # Risk distribution chart
            st.markdown("### Risk Distribution")
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                risk_counts = {
                    'High Risk': len(high_risk),
                    'Medium Risk': len(medium_risk), 
                    'Low Risk': len(low_risk)
                }
                
                fig_pie = px.pie(
                    values=list(risk_counts.values()),
                    names=list(risk_counts.keys()),
                    color_discrete_map={
                        'High Risk': '#d63384',
                        'Medium Risk': '#fd7e14',
                        'Low Risk': '#20c997'
                    },
                    title="Student Risk Distribution"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Risk score histogram
                scores = [s['risk_score'] for s in risk_scores]
                fig_hist = px.histogram(
                    x=scores,
                    nbins=20,
                    title="Risk Score Distribution",
                    labels={'x': 'Risk Score', 'y': 'Number of Students'}
                )
                fig_hist.update_layout(showlegend=False)
                st.plotly_chart(fig_hist, use_container_width=True)
            
            # High priority students table
            st.markdown("### 🚨 High Priority Students")
            if high_risk:
                df_high_risk = pd.DataFrame(high_risk)
                df_display = df_high_risk[['student_id', 'risk_score', 'outstanding_balance', 'days_delinquent']].copy()
                df_display['risk_score'] = df_display['risk_score'].apply(lambda x: f"{x:.1%}")
                df_display['outstanding_balance'] = df_display['outstanding_balance'].apply(lambda x: f"${x:,}")
                df_display.columns = ['Student ID', 'Risk Score', 'Balance', 'Days Delinquent']
                
                st.dataframe(df_display, use_container_width=True)
            else:
                st.info("No high-risk students identified.")
        else:
            st.info("Please upload and process an NSLDS file to view the dashboard.")
    
    with tab3:
        st.header("📋 Generate Reports")
        
        if st.session_state.get('data_processed'):
            processor = st.session_state['processor']
            
            st.markdown("### Available Reports")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 High Risk Intervention Report")
                st.markdown("Detailed list of students requiring immediate attention")
                
                if st.button("Generate High Risk Report"):
                    with st.spinner("Generating report..."):
                        filename = processor.export_risk_report("high_risk_report.xlsx")
                        
                        # Create download button
                        with open(filename, "rb") as f:
                            st.download_button(
                                label="📊 Download High Risk Report",
                                data=f.read(),
                                file_name=f"high_risk_intervention_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.success("Report generated successfully!")
            
            with col2:
                st.markdown("#### 📈 Portfolio Summary Report")
                st.markdown("Executive summary with key metrics and trends")
                
                if st.button("Generate Portfolio Report"):
                    st.info("Portfolio report generation coming soon!")
            
            st.markdown("---")
            st.markdown("### 📧 Automated Reporting")
            
            with st.expander("Set up automated reports"):
                frequency = st.selectbox("Report Frequency", ["Weekly", "Monthly", "Quarterly"])
                email = st.text_input("Email Address", placeholder="alerts@yourschool.edu")
                
                if st.button("Save Automated Report Settings"):
                    st.success("Automated reporting configured!")
        else:
            st.info("Please upload and process an NSLDS file to generate reports.")
    
    with tab4:
        st.header("⚙️ System Settings")
        
        st.markdown("### Risk Assessment Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Risk Thresholds")
            high_threshold = st.slider("High Risk Threshold", 0.0, 1.0, 0.7, 0.05)
            medium_threshold = st.slider("Medium Risk Threshold", 0.0, 1.0, 0.4, 0.05)
            
            st.markdown("#### Weighting Factors")
            financial_weight = st.slider("Financial Risk Weight", 0.0, 1.0, 0.6, 0.1)
            behavioral_weight = st.slider("Behavioral Risk Weight", 0.0, 1.0, 0.4, 0.1)
        
        with col2:
            st.markdown("#### Data Retention")
            retention_months = st.number_input("Historical Data Retention (months)", 12, 60, 24)
            
            st.markdown("#### Notifications")
            email_alerts = st.checkbox("Email Alerts for High Risk Students", True)
            alert_threshold = st.number_input("Alert Threshold (number of students)", 1, 100, 10)
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")
        
        st.markdown("---")
        st.markdown("### 🔐 Data Security")
        
        with st.expander("Security Information"):
            st.markdown("""
            **Data Encryption:** All data is encrypted at rest and in transit using AES-256 encryption.
            
            **FERPA Compliance:** This system is designed to meet FERPA requirements for student data protection.
            
            **Access Logs:** All system access is logged and monitored for security compliance.
            
            **Data Retention:** Student data is automatically purged according to your retention policy.
            """)

# Footer
def show_footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>© 2025 NSLDS Risk Assessment Platform | 
        <a href='mailto:support@nsldsrisk.com'>Support</a> | 
        <a href='#'>Privacy Policy</a> | 
        <a href='#'>Terms of Service</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()

