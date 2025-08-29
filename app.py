# Enhanced ChartED Solutions Portal - Unified Financial Aid Platform
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import tempfile
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set page config
st.set_page_config(
    page_title="ChartED Solutions - Unified Financial Aid Portal",
    page_icon="🎓",
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
        margin-bottom: 1rem;
    }
    .email-template {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .major-risk-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced Data Processor
class UnifiedDataProcessor:
    def __init__(self):
        self.processed_data = {}
        
    def process_nslds_file(self, file):
        """Process NSLDS delinquent borrower report"""
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # Standardize NSLDS column names
            nslds_mapping = {
                'Borrower SSN': 'ssn',
                'Borrower First Name': 'first_name',
                'Borrower Last Name': 'last_name',
                'E-mail': 'email',
                'Days Delinquent': 'days_delinquent',
                'OPB': 'outstanding_balance',
                'Loan Type': 'loan_type'
            }
            
            # Apply mapping for existing columns
            existing_cols = {k: v for k, v in nslds_mapping.items() if k in df.columns}
            df = df.rename(columns=existing_cols)
            
            # Create student ID
            df['student_id'] = df.index.map(lambda x: f'STU{x+1000:06d}')
            
            # Add risk scoring
            df['risk_score'] = df.get('days_delinquent', 0).apply(self.calculate_risk_score)
            df['risk_tier'] = df['risk_score'].apply(self.get_risk_tier)
            
            self.processed_data['nslds'] = df
            return True, f"Processed {len(df)} NSLDS records"
            
        except Exception as e:
            return False, f"Error processing NSLDS file: {str(e)}"
    
    def process_sis_file(self, file):
        """Process Student Information System data"""
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # Standardize SIS column names
            sis_mapping = {
                'Student ID': 'student_id',
                'SSN': 'ssn',
                'First Name': 'first_name',
                'Last Name': 'last_name',
                'Email': 'email',
                'Major': 'major',
                'Program': 'program',
                'CIP Code': 'cip_code',
                'Academic Standing': 'academic_standing',
                'GPA': 'gpa',
                'Credit Hours': 'credit_hours',
                'Enrollment Status': 'enrollment_status'
            }
            
            existing_cols = {k: v for k, v in sis_mapping.items() if k in df.columns}
            df = df.rename(columns=existing_cols)
            
            self.processed_data['sis'] = df
            return True, f"Processed {len(df)} SIS records"
            
        except Exception as e:
            return False, f"Error processing SIS file: {str(e)}"
    
    def merge_datasets(self):
        """Merge NSLDS and SIS data"""
        if 'nslds' not in self.processed_data or 'sis' not in self.processed_data:
            return None
            
        nslds_df = self.processed_data['nslds']
        sis_df = self.processed_data['sis']
        
        # Merge on SSN or student_id
        if 'ssn' in nslds_df.columns and 'ssn' in sis_df.columns:
            merged = pd.merge(nslds_df, sis_df, on='ssn', how='inner', suffixes=('_nslds', '_sis'))
        else:
            merged = pd.merge(nslds_df, sis_df, on='student_id', how='inner', suffixes=('_nslds', '_sis'))
        
        return merged
    
    def calculate_risk_score(self, days_delinquent):
        """Calculate risk score based on delinquency"""
        if pd.isna(days_delinquent) or days_delinquent < 30:
            return random.uniform(0, 0.3)
        elif days_delinquent < 90:
            return random.uniform(0.3, 0.6)
        elif days_delinquent < 180:
            return random.uniform(0.6, 0.8)
        else:
            return random.uniform(0.8, 1.0)
    
    def get_risk_tier(self, score):
        """Convert risk score to tier"""
        if score >= 0.7:
            return 'HIGH'
        elif score >= 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'

# Email Management System
class EmailManager:
    def __init__(self):
        self.templates = {
            'default_prevention': {
                'subject': 'Important: Student Loan Payment Information',
                'body': '''Dear {first_name} {last_name},

We hope this message finds you well. We are reaching out regarding your federal student loan account that shows a past-due balance.

Account Information:
- Outstanding Balance: ${outstanding_balance:,.2f}
- Days Past Due: {days_delinquent}
- Loan Type: {loan_type}

We want to help you avoid default and protect your credit. Please contact our office within 10 business days to discuss payment options, including:
- Income-driven repayment plans
- Temporary payment reductions
- Loan rehabilitation programs

Contact our Financial Aid Office at:
Phone: (555) 123-4567
Email: finaid@yourschool.edu

Best regards,
Financial Aid Office
Your Institution Name
''',
                'compliance_level': 'FERPA_COMPLIANT'
            },
            'payment_plan': {
                'subject': 'Payment Plan Options Available',
                'body': '''Dear {first_name} {last_name},

Based on your current loan status, you may qualify for alternative payment arrangements.

Current Status:
- Outstanding Balance: ${outstanding_balance:,.2f}
- Program of Study: {major}

We offer several options to help manage your student loan payments:
1. Income-Based Repayment Plans
2. Extended Payment Terms
3. Temporary Forbearance Options

Please schedule an appointment with our office to discuss these options.

Financial Aid Office
(555) 123-4567
finaid@yourschool.edu
''',
                'compliance_level': 'FERPA_COMPLIANT'
            },
            'counseling_invitation': {
                'subject': 'Financial Counseling Services Available',
                'body': '''Dear {first_name} {last_name},

Our Financial Aid Office offers free financial counseling services to help you manage your student loans and plan for successful repayment.

Services Include:
- Loan counseling and education
- Budget planning assistance
- Repayment strategy development
- Default prevention guidance

To schedule a confidential consultation, please contact:
Phone: (555) 123-4567
Email: finaid@yourschool.edu

We're here to help you succeed.

Financial Aid Office
''',
                'compliance_level': 'FERPA_COMPLIANT'
            }
        }
    
    def validate_ferpa_compliance(self, template_content, student_data):
        """Validate FERPA compliance of email content"""
        # Basic FERPA validation rules
        ferpa_violations = []
        
        # Check for sensitive information exposure
        sensitive_fields = ['ssn', 'grades', 'disciplinary_records']
        for field in sensitive_fields:
            if field in template_content.lower():
                ferpa_violations.append(f"Contains sensitive field: {field}")
        
        return len(ferpa_violations) == 0, ferpa_violations
    
    def generate_email(self, template_key, student_data):
        """Generate personalized email from template"""
        template = self.templates.get(template_key)
        if not template:
            return None
        
        # Validate FERPA compliance
        is_compliant, violations = self.validate_ferpa_compliance(template['body'], student_data)
        if not is_compliant:
            return {'error': f'FERPA violations detected: {violations}'}
        
        # Format email content
        try:
            formatted_subject = template['subject'].format(**student_data)
            formatted_body = template['body'].format(**student_data)
            
            return {
                'subject': formatted_subject,
                'body': formatted_body,
                'compliance_status': 'FERPA_COMPLIANT',
                'template_used': template_key
            }
        except KeyError as e:
            return {'error': f'Missing data field: {e}'}
    
    def send_bulk_emails(self, student_list, template_key):
        """Simulate sending bulk emails (in production, integrate with actual email service)"""
        sent_count = 0
        failed_count = 0
        results = []
        
        for student in student_list:
            email_content = self.generate_email(template_key, student)
            if 'error' not in email_content:
                # In production, send via SMTP or email API
                results.append({
                    'student_id': student.get('student_id', 'Unknown'),
                    'email': student.get('email', 'No email'),
                    'status': 'sent',
                    'timestamp': datetime.now()
                })
                sent_count += 1
            else:
                results.append({
                    'student_id': student.get('student_id', 'Unknown'),
                    'status': 'failed',
                    'error': email_content['error']
                })
                failed_count += 1
        
        return {
            'sent': sent_count,
            'failed': failed_count,
            'details': results
        }

# Major Analytics Engine
class MajorAnalyticsEngine:
    def __init__(self):
        pass
    
    def analyze_by_major(self, merged_data):
        """Analyze risk patterns by academic major"""
        if merged_data is None or merged_data.empty:
            return None
        
        # Group by major
        major_analysis = merged_data.groupby('major').agg({
            'risk_score': ['mean', 'count'],
            'outstanding_balance': ['mean', 'sum'],
            'days_delinquent': 'mean'
        }).round(2)
        
        # Flatten column names
        major_analysis.columns = ['avg_risk', 'student_count', 'avg_balance', 'total_balance', 'avg_delinquent_days']
        major_analysis = major_analysis.reset_index()
        
        # Add risk tier classification
        major_analysis['risk_tier'] = major_analysis['avg_risk'].apply(
            lambda x: 'HIGH' if x >= 0.7 else 'MEDIUM' if x >= 0.4 else 'LOW'
        )
        
        return major_analysis.sort_values('avg_risk', ascending=False)

def main():
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="charted-logo">🎓 ChartED Solutions</div>', unsafe_allow_html=True)
        st.markdown("**Unified Financial Aid Portal** - Integrated Data Analysis & Communication Platform")
    with col2:
        st.markdown("**Contact Us:**")
        st.markdown("📧 apryll@visitcharted.com")
        st.markdown("🌐 visitcharted.com")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔒 FERPA Compliant System")
        st.info("All communications and data processing maintain strict FERPA compliance with built-in validation.")
        
        st.markdown("### 📊 Integrated Features")
        st.markdown("""
        ✅ **Multi-File Processing**  
        ✅ **Major-Based Analytics**  
        ✅ **Integrated Communications**  
        ✅ **FERPA-Compliant Templates**  
        ✅ **Unified Dashboard**
        """)
        
        st.markdown("### 📞 Support")
        st.markdown("""
        **ChartED Solutions**  
        📧 apryll@visitcharted.com  
        📞 Consultation available  
        🕒 9 AM - 6 PM EST
        """)
    
    # Initialize session state
    if 'data_processor' not in st.session_state:
        st.session_state['data_processor'] = UnifiedDataProcessor()
    if 'email_manager' not in st.session_state:
        st.session_state['email_manager'] = EmailManager()
    if 'analytics_engine' not in st.session_state:
        st.session_state['analytics_engine'] = MajorAnalyticsEngine()
    
    # Main navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Dashboard", 
        "📁 Data Upload", 
        "📊 Major Analytics", 
        "📧 Communications", 
        "📋 Reports",
        "⚙️ Settings"
    ])
    
    with tab1:
        st.markdown("""
        <div class="main-header">
            <h1>Unified Financial Aid Portal</h1>
            <p style="font-size: 1.2em; margin-bottom: 0;">
                Streamline your workflow with integrated data analysis, major-based insights, and communication tools
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 System Integration</h3>
                <p>Eliminate switching between multiple systems. Upload NSLDS and SIS data in one place for comprehensive analysis.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Major-Based Insights</h3>
                <p>Identify risk patterns by academic program. Target interventions based on program-specific default trends.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📧 Integrated Communications</h3>
                <p>Send FERPA-compliant emails directly from the platform. No need to switch to separate email systems.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick action buttons
        st.markdown("### Quick Actions")
        action_col1, action_col2, action_col3, action_col4 = st.columns(4)
        
        with action_col1:
            if st.button("📁 Upload Files", use_container_width=True):
                st.switch_page("Data Upload")
        
        with action_col2:
            if st.button("📊 View Analytics", use_container_width=True):
                st.switch_page("Major Analytics")
        
        with action_col3:
            if st.button("📧 Send Communications", use_container_width=True):
                st.switch_page("Communications")
        
        with action_col4:
            if st.button("📋 Generate Reports", use_container_width=True):
                st.switch_page("Reports")
    
    with tab2:
        st.header("📁 Multi-File Data Upload")
        st.markdown("Upload multiple data sources for comprehensive analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### NSLDS Delinquent Borrower Report")
            nslds_file = st.file_uploader(
                "Upload NSLDS Report",
                type=['csv', 'xlsx'],
                key="nslds_upload",
                help="Upload your NSLDS Delinquent Borrower Report"
            )
            
            if nslds_file:
                st.success(f"✅ NSLDS file uploaded: {nslds_file.name}")
                if st.button("Process NSLDS Data", type="primary"):
                    with st.spinner("Processing NSLDS data..."):
                        success, message = st.session_state['data_processor'].process_nslds_file(nslds_file)
                        if success:
                            st.success(message)
                            st.session_state['nslds_processed'] = True
                        else:
                            st.error(message)
        
        with col2:
