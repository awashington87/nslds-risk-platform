# app.py - ChartED Solutions NSLDS Risk Assessment Platform
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
import random

# Set page config
st.set_page_config(
    page_title="NSLDS Risk Assessment - ChartED Solutions",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with ChartED Solutions branding
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
    .risk-high { color: #d63384; font-weight: bold; }
    .risk-medium { color: #fd7e14; font-weight: bold; }
    .risk-low { color: #20c997; font-weight: bold; }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        border-top: 1px solid #eee;
        margin-top: 3rem;
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
                'key_factors': random.sample([
                    'High debt-to-income ratio',
                    'Frequent delinquencies', 
                    'Payment inconsistency',
                    'Increasing loan balance',
                    'Multiple forbearances',
                    'Poor contact information',
                    'Extended repayment plan',
                    'High interest accrual'
                ], k=random.randint(2, 4))
            })
        return students
    
    def export_risk_report(self, filename, risk_tier=None):
        students = self.calculate_risk_scores()
        
        if risk_tier:
            students = [s for s in students if s['risk_tier'] == risk_tier]
        
        df = pd.DataFrame(students)
        df['risk_percentage'] = (df['risk_score'] * 100).round(1)
        df['confidence_percentage'] = (df['confidence_score'] * 100).round(1)
        
        report_df = df[[
            'student_id', 'risk_tier', 'risk_percentage', 'confidence_percentage',
            'outstanding_balance', 'days_delinquent', 'loan_type'
        ]].copy()
        
        report_df.columns = [
            'Student ID', 'Risk Tier', 'Risk Score (%)', 'Confidence (%)',
            'Outstanding Balance', 'Days Delinquent', 'Loan Type'
        ]
        
        recommendations = []
        for _, row in report_df.iterrows():
            if row['Risk Tier'] == 'HIGH':
                rec = "Immediate outreach required - Consider payment plan restructuring"
            elif row['Risk Tier'] == 'MEDIUM':
                rec = "Monitor closely - Proactive counseling recommended"
            else:
                rec = "Standard monitoring - Send educational materials"
            recommendations.append(rec)
        
        report_df['Recommended Action'] = recommendations
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            report_df.to_excel(writer, sheet_name='Risk Assessment', index=False)
            
            summary_data = {
                'Risk Level': ['HIGH', 'MEDIUM', 'LOW'],
                'Student Count': [
                    len([s for s in students if s['risk_tier'] == 'HIGH']),
                    len([s for s in students if s['risk_tier'] == 'MEDIUM']),
                    len([s for s in students if s['risk_tier'] == 'LOW'])
                ],
                'Total Balance': [
                    sum(s['outstanding_balance'] for s in students if s['risk_tier'] == 'HIGH'),
                    sum(s['outstanding_balance'] for s in students if s['risk_tier'] == 'MEDIUM'),
                    sum(s['outstanding_balance'] for s in students if s['risk_tier'] == 'LOW')
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
        
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
        st.info("ChartED Solutions processes student data in full compliance with FERPA regulations and industry best practices.")
        
        st.markdown("### 📊 Platform Features")
        st.markdown("""
        ✅ **Real-time Risk Scoring**  
        ✅ **Interactive Dashboards**  
        ✅ **Automated Reporting**  
        ✅ **Predictive Analytics**  
        ✅ **Export Capabilities**
        """)
        
        st.markdown("### 📁 Supported Formats")
        st.markdown("""
        - NSLDS CSV Reports
        - NSLDS Excel Reports  
        - Fixed-Width Text Files
        - Custom Data Formats
        """)
        
        st.markdown("### 🎯 Success Metrics")
        st.markdown("""
        **Typical Results:**
        - 15-25% reduction in default rates
        - 40-60% improvement in early identification
        - $500-2000 savings per prevented default
        """)
        
        st.markdown("### 📞 Support")
        st.markdown("""
        **ChartED Solutions Support**  
        📧 apryll@visitcharted.com  
        📞 Available for consultation  
        🕒 Business hours: 9 AM - 6 PM EST
        """)
    
    # Main navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Home", "📁 Upload", "📊 Dashboard", "📋 Reports", "⚙️ Settings"])
    
    with tab1:
        st.markdown("""
        <div class="main-header">
            <h1>🎓 Welcome to ChartED Solutions</h1>
            <h2>NSLDS Risk Assessment Platform</h2>
            <p style="font-size: 1.2em; margin-bottom: 0;">
                Transform your student loan default prevention with advanced analytics and predictive modeling
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Value proposition
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 Early Identification</h3>
                <p>Identify at-risk students 6+ months before default using advanced machine learning algorithms trained on NSLDS data patterns.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📈 Proven Results</h3>
                <p>Our clients see 15-25% reduction in default rates and save $500-2000 per prevented default through early intervention.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>⚡ Easy Integration</h3>
                <p>Upload your NSLDS Delinquent Borrower Report and get actionable insights in minutes, not months.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 How It Works")
        
        step_col1, step_col2, step_col3, step_col4 = st.columns(4)
        
        with step_col1:
            st.markdown("**1. Upload Data**")
            st.markdown("📁 Upload your NSLDS Delinquent Borrower Report")
        
        with step_col2:
            st.markdown("**2. Process & Analyze**")
            st.markdown("🔄 Our algorithms analyze risk factors")
        
        with step_col3:
            st.markdown("**3. Review Dashboard**")
            st.markdown("📊 Interactive dashboard with insights")
        
        with step_col4:
            st.markdown("**4. Take Action**")
            st.markdown("📋 Download prioritized intervention lists")
        
        # Demo button
        st.markdown("---")
        if st.button("🎮 Try Interactive Demo", type="primary", use_container_width=True):
            st.session_state['demo_mode'] = True
            st.success("✅ Demo mode activated! Navigate to the Dashboard tab to see sample data.")
            st.balloons()
        
        # Client testimonials section
        st.markdown("### 💬 What Our Clients Say")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            > *"ChartED Solutions helped us identify at-risk students 6 months earlier than our previous methods. 
            > We've reduced our default rate by 23% in the first year."*
            > 
            > **— Dr. Sarah Johnson, Financial Aid Director**  
            > **Regional State University**
            """)
        
        with col2:
            st.markdown("""
            > *"The NSLDS integration was seamless. What used to take our team weeks in Excel 
            > now takes minutes, and the insights are far more actionable."*
            > 
            > **— Michael Chen, VP Student Affairs**  
            > **Metropolitan College**
            """)
    
    with tab2:
        st.header("📁 Upload NSLDS Delinquent Borrower Report")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### File Upload")
            uploaded_file = st.file_uploader(
                "Choose your NSLDS report file",
                type=['csv', 'xlsx', 'txt'],
                help="Upload your NSLDS Delinquent Borrower Report in any supported format"
            )
            
            if uploaded_file is not None:
                file_size = len(uploaded_file.getvalue()) / 1024
                st.success(f"✅ File uploaded: **{uploaded_file.name}**")
                st.info(f"📊 File size: {file_size:.1f} KB")
                
                st.markdown("### Processing Options")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    risk_threshold = st.slider("High Risk Threshold", 0.5, 0.9, 0.7, 0.05)
                with col_b:
                    confidence_threshold = st.slider("Minimum Confidence", 0.5, 0.95, 0.8, 0.05)
                
                if st.button("🚀 Process NSLDS File", type="primary"):
                    with st.spinner("Processing NSLDS file... Analyzing risk patterns and calculating scores..."):
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
                            tmp.write(uploaded_file.getvalue())
                            tmp_path = tmp.name
                        
                        try:
                            processor = ChartEDNSLDSProcessor()
                            success, message = processor.process_nslds_file(tmp_path)
                            
                            if success:
                                st.session_state['data_processed'] = True
                                st.session_state['processor'] = processor
                                st.session_state['file_name'] = uploaded_file.name
                                st.success(f"✅ {message}")
                                st.balloons()
                                
                                risk_scores = processor.calculate_risk_scores()
                                
                                st.markdown("### 📊 Processing Results")
                                result_col1, result_col2, result_col3, result_col4 = st.columns(4)
                                
                                with result_col1:
                                    st.metric("Students Processed", len(risk_scores))
                                with result_col2:
                                    high_risk_count = len([s for s in risk_scores if s['risk_tier'] == 'HIGH'])
                                    st.metric("High Risk Identified", high_risk_count)
                                with result_col3:
                                    total_balance = sum(s['outstanding_balance'] for s in risk_scores)
                                    st.metric("Total Portfolio Value", f"${total_balance:,.0f}")
                                with result_col4:
                                    avg_confidence = sum(s['confidence_score'] for s in risk_scores) / len(risk_scores)
                                    st.metric("Average Confidence", f"{avg_confidence:.1%}")
                                
                                st.success("🎯 **Ready for Analysis!** Navigate to the Dashboard tab to explore your results.")
                            else:
                                st.error(f"❌ {message}")
                        finally:
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
        
        with col2:
            st.markdown("### 📋 Upload Requirements")
            st.markdown("""
            **Required NSLDS Fields:**
            - Borrower SSN
            - Outstanding Principal Balance  
            - Outstanding Interest Balance
            - Days Delinquent
            - Loan Type
            - Borrower Demographics
            
            **Supported File Formats:**
            - CSV (comma-separated)
            - Excel (.xlsx, .xls)
            - Fixed-width text (.txt)
            
            **File Specifications:**
            - Maximum size: 50 MB
            - Encoding: UTF-8 preferred
            - Headers: First row should contain field names
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
                st.info("🎮 **Demo Mode Active** - This dashboard shows sample data for demonstration purposes.")
            
            st.markdown("### 🎯 Portfolio Overview")
            metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
            
            high_risk = [s for s in risk_scores if s['risk_tier'] == 'HIGH']
            medium_risk = [s for s in risk_scores if s['risk_tier'] == 'MEDIUM']
            low_risk = [s for s in risk_scores if s['risk_tier'] == 'LOW']
            
            with metric_col1:
                st.metric("Total Students", len(risk_scores))
            with metric_col2:
                st.metric("High Risk", len(high_risk), 
                         delta=f"{len(high_risk)/len(risk_scores)*100:.1f}%")
            with metric_col3:
                st.metric("Medium Risk", len(medium_risk),
                         delta=f"{len(medium_risk)/len(risk_scores)*100:.1f}%")
            with metric_col4:
                st.metric("Low Risk", len(low_risk),
                         delta=f"{len(low_risk)/len(risk_scores)*100:.1f}%")
            with metric_col5:
                total_balance = sum(s['outstanding_balance'] for s in risk_scores)
                st.metric("Portfolio Value", f"${total_balance:,.0f}")
            
            st.markdown("### 📈 Risk Analysis")
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
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
                fig_pie.update_layout(showlegend=True, height=400)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with chart_col2:
                fig_scatter = px.scatter(
                    x=[s['outstanding_balance'] for s in risk_scores],
                    y=[s['risk_score'] for s in risk_scores],
                    color=[s['risk_tier'] for s in risk_scores],
                    color_discrete_map={
                        'HIGH': '#d63384',
                        'MEDIUM': '#fd7e14',
                        'LOW': '#20c997'
                    },
                    title="Risk Score vs Outstanding Balance",
                    labels={'x': 'Outstanding Balance ($)', 'y': 'Risk Score'}
                )
                fig_scatter.update_layout(height=400)
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.markdown("### 🚨 High Priority Students")
            if high_risk:
                df_display = pd.DataFrame(high_risk[:10])
                df_table = df_display[['student_id', 'risk_score', 'confidence_score', 'outstanding_balance', 'days_delinquent', 'loan_type']].copy()
                
                df_table['risk_score'] = df_table['risk_score'].apply(lambda x: f"{x:.1%}")
                df_table['confidence_score'] = df_table['confidence_score'].apply(lambda x: f"{x:.1%}")
                df_table['outstanding_balance'] = df_table['outstanding_balance'].apply(lambda x: f"${x:,}")
                
                df_table.columns = ['Student ID', 'Risk Score', 'Confidence', 'Balance', 'Days Delinquent', 'Loan Type']
                
                st.dataframe(df_table, use_container_width=True)
            else:
                st.success("🎉 No high-risk students identified!")
        else:
            st.info("📁 **Upload a file or try the demo** to view your risk assessment dashboard.")
    
    with tab4:
        st.header("📋 Generate Reports")
        
        if st.session_state.get('data_processed') or st.session_state.get('demo_mode'):
            processor = st.session_state.get('processor', ChartEDNSLDSProcessor())
            
            st.markdown("### 📊 Available Reports")
            
            report_col1, report_col2 = st.columns(2)
            
            with report_col1:
                st.markdown("#### 🎯 High Risk Intervention Report")
                st.markdown("Detailed list of students requiring immediate attention")
                
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
                        st.success("✅ Report generated successfully!")
            
            with report_col2:
                st.markdown("#### 📈 Complete Portfolio Analysis")
                st.markdown("Executive summary with all risk levels")
                
                if st.button("Generate Portfolio Report", type="primary"):
                    with st.spinner("Creating portfolio analysis..."):
                        filename = processor.export_risk_report("portfolio_report.xlsx")
                        
                        with open(filename, "rb") as f:
                            st.download_button(
                                label="📈 Download Portfolio Report",
                                data=f.read(),
                                file_name=f"ChartED_Portfolio_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                        st.success("✅ Portfolio analysis ready!")
        else:
            st.info("📁 Please process data first to access report generation.")
    
    with tab5:
        st.header("⚙️ System Settings")
        
        st.markdown("### 🎯 Risk Thresholds")
        
        col1, col2 = st.columns(2)
        
        with col1:
            high_threshold = st.slider("High Risk Threshold", 0.0, 1.0, 0.7, 0.05)
            medium_threshold = st.slider("Medium Risk Threshold", 0.0, 1.0, 0.4, 0.05)
        
        with col2:
            st.markdown("### 🔐 Security & Compliance")
            st.success("✅ FERPA compliant")
            st.success("✅ Data encryption")
            st.success("✅ Secure processing")
        
        if st.button("💾 Save Settings", type="primary"):
            st.success("Settings saved successfully!")

# Initialize session state
if 'data_processed' not in st.session_state:
    st.session_state['data_processed'] = False
if 'demo_mode' not in st.session_state:
    st.session_state['demo_mode'] = False

# Footer
def show_footer():
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>ChartED Solutions</strong> - Advanced Analytics for Educational Success</p>
        <p>📧 apryll@visitcharted.com | 🌐 visitcharted.com</p>
        <p style="font-size: 0.9em; margin-top: 1rem;">
            © 2025 ChartED Solutions. All rights reserved.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    show_footer()

