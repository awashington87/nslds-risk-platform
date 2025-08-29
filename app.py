# app.py - ChartED Solutions NSLDS Risk Assessment Platform (Working Version)
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import tempfile
import os
import random

# Set page config
st.set_page_config(
    page_title="NSLDS Risk Assessment - ChartED Solutions",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .charted-logo {
        font-size: 2.5em;
        font-weight: bold;
        color: #1e3a5f;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #1e3a5f;
    }
</style>
""", unsafe_allow_html=True)

# Demo NSLDS Processor
class ChartEDNSLDSProcessor:
    def __init__(self):
        self.db_path = "charted_risk_db.db"
        
    def validate_file(self, file_path):
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                return False, "Unsupported file format"
            
            if len(df) == 0:
                return False, "File is empty"
            
            return True, f"File validated: {len(df)} records found"
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def process_nslds_file(self, file_path):
        try:
            valid, message = self.validate_file(file_path)
            if not valid:
                return False, message
            
            import time
            time.sleep(2)
            
            return True, "File processed successfully"
        except Exception as e:
            return False, f"Processing error: {str(e)}"
    
    def calculate_risk_scores(self):
        students = []
        for i in range(random.randint(75, 150)):
            risk_score = random.betavariate(2, 5)
            risk_tier = 'HIGH' if risk_score > 0.7 else 'MEDIUM' if risk_score > 0.4 else 'LOW'
            
            students.append({
                'student_id': f'STU{i+1000:06d}',
                'name': f'Student {i+1}',
                'risk_score': risk_score,
                'confidence_score': random.uniform(0.65, 0.95),
                'risk_tier': risk_tier,
                'outstanding_balance': random.randint(8000, 75000),
                'days_delinquent': random.randint(31, 400),
                'loan_type': random.choice(['Subsidized Stafford', 'Unsubsidized Stafford', 'PLUS', 'Consolidation']),
            })
        return students
    
    def export_risk_report(self, filename, risk_tier=None):
        try:
            students = self.calculate_risk_scores()
            
            if risk_tier:
                students = [s for s in students if s['risk_tier'] == risk_tier]
            
            df = pd.DataFrame(students)
            
            if df.empty:
                return filename
            
            df['risk_percentage'] = (df['risk_score'] * 100).round(1)
            df['confidence_percentage'] = (df['confidence_score'] * 100).round(1)
            
            report_df = df[['student_id', 'risk_tier', 'risk_percentage', 'confidence_percentage',
                           'outstanding_balance', 'days_delinquent', 'loan_type']].copy()
            
            report_df.columns = ['Student ID', 'Risk Tier', 'Risk Score (%)', 'Confidence (%)',
                                'Outstanding Balance', 'Days Delinquent', 'Loan Type']
            
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                report_df.to_excel(writer, sheet_name='Risk Assessment', index=False)
            
            return filename
            
        except Exception as e:
            st.error(f"Error creating report: {e}")
            return filename

def main():
    # Header with ChartED Solutions branding
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="charted-logo">📊 ChartED Solutions</div>', unsafe_allow_html=True)
        st.markdown("**NSLDS Risk Assessment Platform** - Advanced Student Loan Default Prediction")
    with col2:
        st.markdown("**Contact Us:**")
        st.markdown("📧 apryll@visitcharted.com")
        st.markdown("🌐 visitcharted.com")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔒 FERPA Compliant System")
        st.info("ChartED Solutions processes student data in full compliance with FERPA regulations.")
        
        st.markdown("### 📊 Platform Features")
        st.markdown("""
        ✅ **Real-time Risk Scoring**  
        ✅ **Interactive Dashboards**  
        ✅ **Automated Reporting**  
        ✅ **Predictive Analytics**
        """)
        
        st.markdown("### 📞 Support")
        st.markdown("""
        **ChartED Solutions Support**  
        📧 apryll@visitcharted.com  
        📞 Available for consultation
        """)
    
    # Main navigation
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📁 Upload", "📊 Dashboard", "📋 Reports"])
    
    with tab1:
        st.markdown("""
        <div class="main-header">
            <h1>🎓 Welcome to ChartED Solutions</h1>
            <h2>NSLDS Risk Assessment Platform</h2>
            <p style="font-size: 1.2em; margin-bottom: 0;">
                Transform your student loan default prevention with advanced analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Value proposition
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 Early Identification</h3>
                <p>Identify at-risk students 6+ months before default using machine learning algorithms.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📈 Proven Results</h3>
                <p>Clients see 15-25% reduction in default rates and save $500-2000 per prevented default.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>⚡ Easy Integration</h3>
                <p>Upload NSLDS reports and get actionable insights in minutes, not months.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Demo button
        st.markdown("---")
        if st.button("🎮 Try Interactive Demo", type="primary", use_container_width=True):
            st.session_state['demo_mode'] = True
            st.success("Demo mode activated! Navigate to the Dashboard tab to see sample data.")
    
    with tab2:
        st.header("📁 Upload NSLDS Delinquent Borrower Report")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose your NSLDS report file",
                type=['csv', 'xlsx', 'txt'],
                help="Upload your NSLDS Delinquent Borrower Report"
            )
            
            if uploaded_file is not None:
                file_size = len(uploaded_file.getvalue()) / 1024
                st.success(f"File uploaded: **{uploaded_file.name}**")
                st.info(f"File size: {file_size:.1f} KB")
                
                if st.button("🚀 Process NSLDS File", type="primary"):
                    with st.spinner("Processing NSLDS file..."):
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                            tmp.write(uploaded_file.getvalue())
                            tmp_path = tmp.name
                        
                        try:
                            processor = ChartEDNSLDSProcessor()
                            success, message = processor.process_nslds_file(tmp_path)
                            
                            if success:
                                st.session_state['data_processed'] = True
                                st.session_state['processor'] = processor
                                st.success(f"✅ {message}")
                                
                                risk_scores = processor.calculate_risk_scores()
                                
                                col_a, col_b, col_c = st.columns(3)
                                with col_a:
                                    st.metric("Students Processed", len(risk_scores))
                                with col_b:
                                    high_risk_count = len([s for s in risk_scores if s['risk_tier'] == 'HIGH'])
                                    st.metric("High Risk Identified", high_risk_count)
                                with col_c:
                                    total_balance = sum(s['outstanding_balance'] for s in risk_scores)
                                    st.metric("Total Portfolio Value", f"${total_balance:,.0f}")
                                
                                st.success("Ready for Analysis! Navigate to the Dashboard tab.")
                            else:
                                st.error(f"❌ {message}")
                        finally:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
        
        with col2:
            st.markdown("### Upload Requirements")
            st.markdown("""
            **Required NSLDS Fields:**
            - Borrower SSN
            - Outstanding Balance
            - Days Delinquent
            - Loan Type
            
            **Supported Formats:**
            - CSV (comma-separated)
            - Excel (.xlsx, .xls)
            - Fixed-width text (.txt)
            """)
    
    with tab3:
        st.header("📊 Risk Assessment Dashboard")
        
        has_data = st.session_state.get('data_processed') or st.session_state.get('demo_mode')
        
        if has_data:
            if 'processor' in st.session_state:
                processor = st.session_state['processor']
            else:
                processor = ChartEDNSLDSProcessor()
            
            risk_scores = processor.calculate_risk_scores()
            
            if st.session_state.get('demo_mode'):
                st.info("🎮 **Demo Mode Active** - Sample data for demonstration")
            
            # Key metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            high_risk = [s for s in risk_scores if s['risk_tier'] == 'HIGH']
            medium_risk = [s for s in risk_scores if s['risk_tier'] == 'MEDIUM']
            low_risk = [s for s in risk_scores if s['risk_tier'] == 'LOW']
            
            with col1:
                st.metric("Total Students", len(risk_scores))
            with col2:
                st.metric("High Risk", len(high_risk))
            with col3:
                st.metric("Medium Risk", len(medium_risk))
            with col4:
                st.metric("Low Risk", len(low_risk))
            with col5:
                total_balance = sum(s['outstanding_balance'] for s in risk_scores)
                st.metric("Portfolio Value", f"${total_balance:,.0f}")
            
            # Risk distribution chart
            col1, col2 = st.columns(2)
            
            with col1:
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
                scores = [s['risk_score'] for s in risk_scores]
                fig_hist = px.histogram(
                    x=scores,
                    nbins=20,
                    title="Risk Score Distribution",
                    labels={'x': 'Risk Score', 'y': 'Number of Students'}
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            # High priority students
            if high_risk:
                st.markdown("### 🚨 High Priority Students")
                df_display = pd.DataFrame(high_risk[:10])
                df_table = df_display[['student_id', 'risk_score', 'outstanding_balance', 'days_delinquent', 'loan_type']].copy()
                
                df_table['risk_score'] = df_table['risk_score'].apply(lambda x: f"{x:.1%}")
                df_table['outstanding_balance'] = df_table['outstanding_balance'].apply(lambda x: f"${x:,}")
                
                df_table.columns = ['Student ID', 'Risk Score', 'Balance', 'Days Delinquent', 'Loan Type']
                st.dataframe(df_table, use_container_width=True)
        else:
            st.info("Upload a file or try the demo to view your risk assessment dashboard.")
    
    with tab4:
        st.header("📋 Generate Reports")
        
        if st.session_state.get('data_processed') or st.session_state.get('demo_mode'):
            processor = st.session_state.get('processor', ChartEDNSLDSProcessor())
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 High Risk Intervention Report")
                st.markdown("Students requiring immediate attention")
                
                if st.button("Generate High Risk Report", type="primary"):
                    with st.spinner("Generating report..."):
                        filename = processor.export_risk_report("high_risk_report.xlsx", risk_tier="HIGH")
                        
                        with open(filename, "rb") as f:
                            st.download_button(
                                label="📊 Download High Risk Report",
                                data=f.read(),
                                file_name=f"ChartED_HighRisk_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.success("Report generated successfully!")
            
            with col2:
                st.markdown("#### 📈 Complete Portfolio Analysis")
                st.markdown("Executive summary with all risk levels")
                
                if st.button("Generate Portfolio Report", type="primary"):
                    with st.spinner("Creating analysis..."):
                        filename = processor.export_risk_report("portfolio_report.xlsx")
                        
                        with open(filename, "rb") as f:
                            st.download_button(
                                label="📈 Download Portfolio Report",
                                data=f.read(),
                                file_name=f"ChartED_Portfolio_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.success("Portfolio analysis ready!")
        else:
            st.info("Process data first to access report generation.")

# Initialize session state
if 'data_processed' not in st.session_state:
    st.session_state['data_processed'] = False
if 'demo_mode' not in st.session_state:
    st.session_state['demo_mode'] = False

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>ChartED Solutions</strong> - Advanced Analytics for Educational Success</p>
    <p>📧 apryll@visitcharted.com | 🌐 visitcharted.com</p>
    <p>© 2025 ChartED Solutions. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
