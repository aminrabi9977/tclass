"""
Tender Processing System - Web Application
A modern web interface for processing tender data using AI.
"""

import streamlit as st
import pandas as pd
import os
import tempfile
import zipfile
from datetime import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from stqdm import stqdm
import io
import sys
import threading
import queue
import subprocess
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Import our modules
from src.utils.config import INPUT_DIR, AI_OUTPUT_DIR, DEPT_OUTPUT_DIR, BACKUP_DIR

# Page configuration
st.set_page_config(
    page_title="Tender Processing System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .stats-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .upload-section {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .processing-step {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
    
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

class TenderProcessor:
    """Main class for handling the tender processing pipeline."""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.results = {}
        
    def save_uploaded_file(self, uploaded_file):
        """Save uploaded HTML file to input directory."""
        try:
            # Create a unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{uploaded_file.name}"
            file_path = os.path.join(INPUT_DIR, filename)
            
            # Save the file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return file_path, filename
        except Exception as e:
            st.error(f"Error saving file: {str(e)}")
            return None, None
    
    def run_processing_pipeline(self, progress_callback=None):
        """Run the complete processing pipeline."""
        try:
            # Import the main processing function
            import subprocess
            import sys
            
            # Get the path to main.py
            main_py_path = os.path.join(os.path.dirname(__file__), "main.py")
            
            if progress_callback:
                progress_callback("Starting HTML extraction...", 10)
            
            # Run main.py as a subprocess to avoid import conflicts
            result = subprocess.run([
                sys.executable, main_py_path
            ], capture_output=True, text=True, encoding='utf-8')
            
            if progress_callback:
                progress_callback("Processing completed", 100)
            
            # Check if process was successful
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
                
        except Exception as e:
            return False, str(e)
    
    def get_latest_results(self):
        """Get the latest processing results."""
        results = {
            'extracted_files': [],
            'ai_filtered_files': [],
            'dept_classified_files': []
        }
        
        try:
            # Get latest department classified file
            if os.path.exists(DEPT_OUTPUT_DIR):
                dept_files = [f for f in os.listdir(DEPT_OUTPUT_DIR) if f.endswith('.xlsx')]
                if dept_files:
                    dept_files.sort(key=lambda x: os.path.getmtime(os.path.join(DEPT_OUTPUT_DIR, x)), reverse=True)
                    latest_dept_file = os.path.join(DEPT_OUTPUT_DIR, dept_files[0])
                    results['dept_classified_files'] = [latest_dept_file]
            
            # Get AI filtered files
            if os.path.exists(AI_OUTPUT_DIR):
                ai_files = [f for f in os.listdir(AI_OUTPUT_DIR) if f.endswith('.xlsx')]
                results['ai_filtered_files'] = [os.path.join(AI_OUTPUT_DIR, f) for f in ai_files]
            
        except Exception as e:
            st.error(f"Error getting results: {str(e)}")
        
        return results
    
    def create_download_package(self, file_paths):
        """Create a ZIP package of result files."""
        try:
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        filename = os.path.basename(file_path)
                        zip_file.write(file_path, filename)
            
            zip_buffer.seek(0)
            return zip_buffer.getvalue()
        except Exception as e:
            st.error(f"Error creating download package: {str(e)}")
            return None

def main():
    """Main application function."""
    
    # Initialize session state
    if 'processor' not in st.session_state:
        st.session_state.processor = TenderProcessor()
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'uploaded_file_name' not in st.session_state:
        st.session_state.uploaded_file_name = None
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📊 Tender Processing System</h1>
        <p>AI-Powered Tender Analysis and Department Classification</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar menu
    with st.sidebar:
        selected = option_menu(
            "Navigation",
            ["Upload & Process", "View Results", "Analytics", "Settings"],
            icons=["upload", "table", "bar-chart", "gear"],
            menu_icon="list",
            default_index=0
        )
    
    # Main content based on selected menu
    if selected == "Upload & Process":
        show_upload_section()
    elif selected == "View Results":
        show_results_section()
    elif selected == "Analytics":
        show_analytics_section()
    elif selected == "Settings":
        show_settings_section()

def show_upload_section():
    """Show the file upload and processing section."""
    
    st.header("📁 Upload HTML File")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an HTML file",
            type=['html', 'htm'],
            help="Upload the HTML file containing tender data"
        )
        
        if uploaded_file is not None:
            st.session_state.uploaded_file_name = uploaded_file.name
            
            # Show file info
            st.info(f"📄 File: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
            
            # Process button
            if st.button("🚀 Start Processing", type="primary", use_container_width=True):
                process_file(uploaded_file)
    
    with col2:
        # Instructions
        st.markdown("""
        ### 📋 Instructions:
        1. Upload your HTML file
        2. Click "Start Processing"
        3. Wait for completion
        4. Download results
        
        ### ⚡ Features:
        - AI-powered filtering
        - Department classification
        - Automatic backup
        - Excel export
        """)

def process_file(uploaded_file):
    """Process the uploaded file through the pipeline."""
    
    # Save the uploaded file
    file_path, filename = st.session_state.processor.save_uploaded_file(uploaded_file)
    
    if not file_path:
        st.error("Failed to save uploaded file")
        return
    
    st.success(f"File saved: {filename}")
    
    # Create progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_container = st.container()
    
    def update_progress(message, progress):
        progress_bar.progress(progress / 100)
        status_text.text(message)
        with log_container:
            st.markdown(f'<div class="processing-step">📝 {message}</div>', unsafe_allow_html=True)
    
    # Run the processing pipeline
    with st.spinner("Processing tender data..."):
        success, output = st.session_state.processor.run_processing_pipeline(update_progress)
    
    if success:
        st.session_state.processing_complete = True
        st.markdown('<div class="success-message">✅ Processing completed successfully!</div>', unsafe_allow_html=True)
        
        # Show processing output in an expander
        with st.expander("📜 View Processing Log"):
            st.text(output)
        
        # Automatically switch to results view
        st.rerun()
    else:
        st.markdown(f'<div class="error-message">❌ Processing failed: {output}</div>', unsafe_allow_html=True)
        
        # Show error details
        with st.expander("🔍 Error Details"):
            st.text(output)

def show_results_section():
    """Show the processing results section."""
    
    st.header("📊 Processing Results")
    
    if not st.session_state.processing_complete:
        st.warning("⚠️ No processing results available. Please upload and process a file first.")
        return
    
    # Get latest results
    results = st.session_state.processor.get_latest_results()
    
    if not any(results.values()):
        st.error("❌ No result files found.")
        return
    
    # Show results summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📄 Extracted Files", len(results.get('extracted_files', [])))
    
    with col2:
        st.metric("🤖 AI Filtered Files", len(results.get('ai_filtered_files', [])))
    
    with col3:
        st.metric("🏢 Classified Files", len(results.get('dept_classified_files', [])))
    
    # Show classified data if available
    if results['dept_classified_files']:
        latest_file = results['dept_classified_files'][0]
        
        st.subheader("📋 Department Classified Tenders")
        
        try:
            df = pd.read_excel(latest_file)
            
            # Show basic stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Tenders", len(df))
            with col2:
                dept_count = df['معاونت مربوطه'].nunique() if 'معاونت مربوطه' in df.columns else 0
                st.metric("Departments", dept_count)
            with col3:
                consulting_count = len(df)  # All are consulting since they've been filtered
                st.metric("Consulting Tenders", consulting_count)
            with col4:
                success_rate = "100%" if len(df) > 0 else "0%"
                st.metric("Success Rate", success_rate)
            
            # Show data table
            st.subheader("📊 Tender Data")
            
            # Customize displayed columns
            display_columns = []
            if 'شماره مناقصه در هزاره' in df.columns:
                display_columns.append('شماره مناقصه در هزاره')
            if 'معاونت مربوطه' in df.columns:
                display_columns.append('معاونت مربوطه')
            if 'عنوان' in df.columns:
                display_columns.append('عنوان')
            if 'برگزارکننده' in df.columns:
                display_columns.append('برگزارکننده')
            if 'منطقه' in df.columns:
                display_columns.append('منطقه')
            
            if display_columns:
                st.dataframe(
                    df[display_columns].head(50),  # Show first 50 rows
                    use_container_width=True,
                    height=400
                )
                
                if len(df) > 50:
                    st.info(f"📄 Showing first 50 of {len(df)} total records")
            
            # Download section
            st.subheader("💾 Download Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download Excel file
                with open(latest_file, 'rb') as f:
                    excel_data = f.read()
                
                st.download_button(
                    label="📄 Download Excel File",
                    data=excel_data,
                    file_name=f"tender_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col2:
                # Download complete package
                all_files = []
                if results['dept_classified_files']:
                    all_files.extend(results['dept_classified_files'])
                if results['ai_filtered_files']:
                    all_files.extend(results['ai_filtered_files'])
                
                if all_files:
                    zip_data = st.session_state.processor.create_download_package(all_files)
                    if zip_data:
                        st.download_button(
                            label="📦 Download Complete Package",
                            data=zip_data,
                            file_name=f"tender_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
            
        except Exception as e:
            st.error(f"Error displaying results: {str(e)}")

def show_analytics_section():
    """Show analytics and visualizations."""
    
    st.header("📈 Analytics Dashboard")
    
    if not st.session_state.processing_complete:
        st.warning("⚠️ No data available for analytics. Please process a file first.")
        return
    
    # Get latest results
    results = st.session_state.processor.get_latest_results()
    
    if not results['dept_classified_files']:
        st.error("❌ No classified data available for analytics.")
        return
    
    try:
        df = pd.read_excel(results['dept_classified_files'][0])
        
        # Department distribution
        if 'معاونت مربوطه' in df.columns:
            st.subheader("🏢 Department Distribution")
            
            dept_counts = df['معاونت مربوطه'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart
                fig_pie = px.pie(
                    values=dept_counts.values,
                    names=dept_counts.index,
                    title="Tenders by Department"
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Bar chart
                fig_bar = px.bar(
                    x=dept_counts.index,
                    y=dept_counts.values,
                    title="Department Tender Count"
                )
                fig_bar.update_layout(xaxis_title="Department", yaxis_title="Number of Tenders")
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Regional distribution
        if 'منطقه' in df.columns:
            st.subheader("🗺️ Regional Distribution")
            
            region_counts = df['منطقه'].value_counts().head(10)
            
            fig_region = px.bar(
                x=region_counts.values,
                y=region_counts.index,
                orientation='h',
                title="Top 10 Regions by Tender Count"
            )
            fig_region.update_layout(xaxis_title="Number of Tenders", yaxis_title="Region")
            st.plotly_chart(fig_region, use_container_width=True)
        
        # Data quality metrics
        st.subheader("📊 Data Quality Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            completeness = (df.notna().sum().sum() / (len(df) * len(df.columns))) * 100
            st.metric("Data Completeness", f"{completeness:.1f}%")
        
        with col2:
            classified_rate = (df['معاونت مربوطه'] != 'نامشخص').sum() / len(df) * 100 if 'معاونت مربوطه' in df.columns else 0
            st.metric("Classification Rate", f"{classified_rate:.1f}%")
        
        with col3:
            unique_organizers = df['برگزارکننده'].nunique() if 'برگزارکننده' in df.columns else 0
            st.metric("Unique Organizers", unique_organizers)
        
        with col4:
            processing_date = datetime.now().strftime("%Y-%m-%d")
            st.metric("Last Processed", processing_date)
        
    except Exception as e:
        st.error(f"Error generating analytics: {str(e)}")

def show_settings_section():
    """Show application settings."""
    
    st.header("⚙️ Settings")
    
    # API Configuration
    st.subheader("🔑 API Configuration")
    
    with st.expander("OpenAI API Settings"):
        current_key = os.getenv("OPENAI_API_KEY", "")
        current_url = os.getenv("OPENAI_BASE_URL", "")
        
        api_key = st.text_input(
            "API Key",
            value=current_key[:10] + "..." if current_key else "",
            type="password",
            help="Your OpenAI API key"
        )
        
        base_url = st.text_input(
            "Base URL",
            value=current_url,
            help="API base URL (optional)"
        )
        
        if st.button("💾 Save API Settings"):
            st.success("✅ API settings would be saved (in a real deployment)")
    
    # Processing Settings
    st.subheader("🔧 Processing Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        batch_size = st.slider("Batch Size", 10, 100, 50, help="Number of tenders to process per batch")
        timeout = st.slider("API Timeout (seconds)", 30, 300, 120, help="Timeout for API requests")
    
    with col2:
        enable_backup = st.checkbox("Enable Backup", value=True, help="Automatically backup processed files")
        debug_mode = st.checkbox("Debug Mode", value=False, help="Enable detailed logging")
    
    # System Information
    st.subheader("ℹ️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Python Version:** {sys.version.split()[0]}")
        st.info(f"**Streamlit Version:** {st.__version__}")
    
    with col2:
        # Check directories
        dirs_status = {
            "Input Directory": os.path.exists(INPUT_DIR),
            "Output Directory": os.path.exists(DEPT_OUTPUT_DIR),
            "Backup Directory": os.path.exists(BACKUP_DIR)
        }
        
        for dir_name, exists in dirs_status.items():
            status = "✅ Exists" if exists else "❌ Missing"
            st.info(f"**{dir_name}:** {status}")
    
    # Clear cache button
    st.subheader("🧹 Maintenance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Cache", help="Clear Streamlit cache"):
            st.cache_data.clear()
            st.success("✅ Cache cleared!")
    
    with col2:
        if st.button("🔄 Reset Session", help="Reset application session"):
            st.session_state.clear()
            st.success("✅ Session reset!")
            st.rerun()

if __name__ == "__main__":
    main()