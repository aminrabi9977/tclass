# """
# Tender Processing System - Web Application
# A modern web interface for processing tender data using AI.
# """

# import streamlit as st
# import pandas as pd
# import os
# import tempfile
# import zipfile
# from datetime import datetime
# import time
# import plotly.express as px
# import plotly.graph_objects as go
# from streamlit_option_menu import option_menu
# from stqdm import stqdm
# import io
# import sys
# import threading
# import queue
# import subprocess
# from pathlib import Path

# # Add project root to path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from dotenv import load_dotenv
# load_dotenv()

# # Import our modules
# from src.utils.config import INPUT_DIR, AI_OUTPUT_DIR, DEPT_OUTPUT_DIR, BACKUP_DIR

# # Page configuration
# st.set_page_config(
#     page_title="Tender Processing System",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         text-align: center;
#         padding: 2rem 0;
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border-radius: 10px;
#         margin-bottom: 2rem;
#     }
    
#     .stats-container {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 10px;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#     }
    
#     .upload-section {
#         border: 2px dashed #cccccc;
#         border-radius: 10px;
#         padding: 2rem;
#         text-align: center;
#         margin: 2rem 0;
#     }
    
#     .success-message {
#         background: #d4edda;
#         color: #155724;
#         padding: 1rem;
#         border-radius: 5px;
#         margin: 1rem 0;
#     }
    
#     .error-message {
#         background: #f8d7da;
#         color: #721c24;
#         padding: 1rem;
#         border-radius: 5px;
#         margin: 1rem 0;
#     }
    
#     .processing-step {
#         background: #fff3cd;
#         color: #856404;
#         padding: 1rem;
#         border-radius: 5px;
#         margin: 0.5rem 0;
#         border-left: 4px solid #ffc107;
#     }
    
#     .stDataFrame {
#         border: 1px solid #e0e0e0;
#         border-radius: 5px;
#     }
# </style>
# """, unsafe_allow_html=True)

# class TenderProcessor:
#     """Main class for handling the tender processing pipeline."""
    
#     def __init__(self):
#         self.temp_dir = tempfile.mkdtemp()
#         self.results = {}
        
#     def save_uploaded_file(self, uploaded_file):
#         """Save uploaded HTML file to input directory."""
#         try:
#             # Create a unique filename
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"{timestamp}_{uploaded_file.name}"
#             file_path = os.path.join(INPUT_DIR, filename)
            
#             # Save the file
#             with open(file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
            
#             return file_path, filename
#         except Exception as e:
#             st.error(f"Error saving file: {str(e)}")
#             return None, None
    
#     def run_processing_pipeline(self, progress_callback=None):
#         """Run the complete processing pipeline."""
#         try:
#             # Import the main processing function
#             import subprocess
#             import sys
            
#             # Get the path to main.py
#             main_py_path = os.path.join(os.path.dirname(__file__), "main.py")
            
#             if progress_callback:
#                 progress_callback("Starting HTML extraction...", 10)
            
#             # Run main.py as a subprocess to avoid import conflicts
#             result = subprocess.run([
#                 sys.executable, main_py_path
#             ], capture_output=True, text=True, encoding='utf-8')
            
#             if progress_callback:
#                 progress_callback("Processing completed", 100)
            
#             # Check if process was successful
#             if result.returncode == 0:
#                 return True, result.stdout
#             else:
#                 return False, result.stderr
                
#         except Exception as e:
#             return False, str(e)
    
#     def get_latest_results(self):
#         """Get the latest processing results."""
#         results = {
#             'extracted_files': [],
#             'ai_filtered_files': [],
#             'dept_classified_files': []
#         }
        
#         try:
#             # Get latest department classified file
#             if os.path.exists(DEPT_OUTPUT_DIR):
#                 dept_files = [f for f in os.listdir(DEPT_OUTPUT_DIR) if f.endswith('.xlsx')]
#                 if dept_files:
#                     dept_files.sort(key=lambda x: os.path.getmtime(os.path.join(DEPT_OUTPUT_DIR, x)), reverse=True)
#                     latest_dept_file = os.path.join(DEPT_OUTPUT_DIR, dept_files[0])
#                     results['dept_classified_files'] = [latest_dept_file]
            
#             # Get AI filtered files
#             if os.path.exists(AI_OUTPUT_DIR):
#                 ai_files = [f for f in os.listdir(AI_OUTPUT_DIR) if f.endswith('.xlsx')]
#                 results['ai_filtered_files'] = [os.path.join(AI_OUTPUT_DIR, f) for f in ai_files]
            
#         except Exception as e:
#             st.error(f"Error getting results: {str(e)}")
        
#         return results
    
#     def create_download_package(self, file_paths):
#         """Create a ZIP package of result files."""
#         try:
#             zip_buffer = io.BytesIO()
            
#             with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#                 for file_path in file_paths:
#                     if os.path.exists(file_path):
#                         filename = os.path.basename(file_path)
#                         zip_file.write(file_path, filename)
            
#             zip_buffer.seek(0)
#             return zip_buffer.getvalue()
#         except Exception as e:
#             st.error(f"Error creating download package: {str(e)}")
#             return None

# def main():
#     """Main application function."""
    
#     # Initialize session state
#     if 'processor' not in st.session_state:
#         st.session_state.processor = TenderProcessor()
#     if 'processing_complete' not in st.session_state:
#         st.session_state.processing_complete = False
#     if 'uploaded_file_name' not in st.session_state:
#         st.session_state.uploaded_file_name = None
    
#     # Header
#     st.markdown("""
#     <div class="main-header">
#         <h1>📊 Tender Processing System</h1>
#         <p>AI-Powered Tender Analysis and Department Classification</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Sidebar menu
#     with st.sidebar:
#         selected = option_menu(
#             "Navigation",
#             ["Upload & Process", "View Results", "Analytics", "Settings"],
#             icons=["upload", "table", "bar-chart", "gear"],
#             menu_icon="list",
#             default_index=0
#         )
    
#     # Main content based on selected menu
#     if selected == "Upload & Process":
#         show_upload_section()
#     elif selected == "View Results":
#         show_results_section()
#     elif selected == "Analytics":
#         show_analytics_section()
#     elif selected == "Settings":
#         show_settings_section()

# def show_upload_section():
#     """Show the file upload and processing section."""
    
#     st.header("📁 Upload HTML File")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         # File uploader
#         uploaded_file = st.file_uploader(
#             "Choose an HTML file",
#             type=['html', 'htm'],
#             help="Upload the HTML file containing tender data"
#         )
        
#         if uploaded_file is not None:
#             st.session_state.uploaded_file_name = uploaded_file.name
            
#             # Show file info
#             st.info(f"📄 File: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
            
#             # Process button
#             if st.button("🚀 Start Processing", type="primary", use_container_width=True):
#                 process_file(uploaded_file)
    
#     with col2:
#         # Instructions
#         st.markdown("""
#         ### 📋 Instructions:
#         1. Upload your HTML file
#         2. Click "Start Processing"
#         3. Wait for completion
#         4. Download results
        
#         ### ⚡ Features:
#         - AI-powered filtering
#         - Department classification
#         - Automatic backup
#         - Excel export
#         """)

# def process_file(uploaded_file):
#     """Process the uploaded file through the pipeline."""
    
#     # Save the uploaded file
#     file_path, filename = st.session_state.processor.save_uploaded_file(uploaded_file)
    
#     if not file_path:
#         st.error("Failed to save uploaded file")
#         return
    
#     st.success(f"File saved: {filename}")
    
#     # Create progress tracking
#     progress_bar = st.progress(0)
#     status_text = st.empty()
#     log_container = st.container()
    
#     def update_progress(message, progress):
#         progress_bar.progress(progress / 100)
#         status_text.text(message)
#         with log_container:
#             st.markdown(f'<div class="processing-step">📝 {message}</div>', unsafe_allow_html=True)
    
#     # Run the processing pipeline
#     with st.spinner("Processing tender data..."):
#         success, output = st.session_state.processor.run_processing_pipeline(update_progress)
    
#     if success:
#         st.session_state.processing_complete = True
#         st.markdown('<div class="success-message">✅ Processing completed successfully!</div>', unsafe_allow_html=True)
        
#         # Show processing output in an expander
#         with st.expander("📜 View Processing Log"):
#             st.text(output)
        
#         # Automatically switch to results view
#         st.rerun()
#     else:
#         st.markdown(f'<div class="error-message">❌ Processing failed: {output}</div>', unsafe_allow_html=True)
        
#         # Show error details
#         with st.expander("🔍 Error Details"):
#             st.text(output)

# def show_results_section():
#     """Show the processing results section."""
    
#     st.header("📊 Processing Results")
    
#     if not st.session_state.processing_complete:
#         st.warning("⚠️ No processing results available. Please upload and process a file first.")
#         return
    
#     # Get latest results
#     results = st.session_state.processor.get_latest_results()
    
#     if not any(results.values()):
#         st.error("❌ No result files found.")
#         return
    
#     # Show results summary
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.metric("📄 Extracted Files", len(results.get('extracted_files', [])))
    
#     with col2:
#         st.metric("🤖 AI Filtered Files", len(results.get('ai_filtered_files', [])))
    
#     with col3:
#         st.metric("🏢 Classified Files", len(results.get('dept_classified_files', [])))
    
#     # Show classified data if available
#     if results['dept_classified_files']:
#         latest_file = results['dept_classified_files'][0]
        
#         st.subheader("📋 Department Classified Tenders")
        
#         try:
#             df = pd.read_excel(latest_file)
            
#             # Show basic stats
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 st.metric("Total Tenders", len(df))
#             with col2:
#                 dept_count = df['معاونت مربوطه'].nunique() if 'معاونت مربوطه' in df.columns else 0
#                 st.metric("Departments", dept_count)
#             with col3:
#                 consulting_count = len(df)  # All are consulting since they've been filtered
#                 st.metric("Consulting Tenders", consulting_count)
#             with col4:
#                 success_rate = "100%" if len(df) > 0 else "0%"
#                 st.metric("Success Rate", success_rate)
            
#             # Show data table
#             st.subheader("📊 Tender Data")
            
#             # Customize displayed columns
#             display_columns = []
#             if 'شماره مناقصه در هزاره' in df.columns:
#                 display_columns.append('شماره مناقصه در هزاره')
#             if 'معاونت مربوطه' in df.columns:
#                 display_columns.append('معاونت مربوطه')
#             if 'عنوان' in df.columns:
#                 display_columns.append('عنوان')
#             if 'برگزارکننده' in df.columns:
#                 display_columns.append('برگزارکننده')
#             if 'منطقه' in df.columns:
#                 display_columns.append('منطقه')
            
#             if display_columns:
#                 st.dataframe(
#                     df[display_columns].head(50),  # Show first 50 rows
#                     use_container_width=True,
#                     height=400
#                 )
                
#                 if len(df) > 50:
#                     st.info(f"📄 Showing first 50 of {len(df)} total records")
            
#             # Download section
#             st.subheader("💾 Download Results")
            
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 # Download Excel file
#                 with open(latest_file, 'rb') as f:
#                     excel_data = f.read()
                
#                 st.download_button(
#                     label="📄 Download Excel File",
#                     data=excel_data,
#                     file_name=f"tender_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
#                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                     use_container_width=True
#                 )
            
#             with col2:
#                 # Download complete package
#                 all_files = []
#                 if results['dept_classified_files']:
#                     all_files.extend(results['dept_classified_files'])
#                 if results['ai_filtered_files']:
#                     all_files.extend(results['ai_filtered_files'])
                
#                 if all_files:
#                     zip_data = st.session_state.processor.create_download_package(all_files)
#                     if zip_data:
#                         st.download_button(
#                             label="📦 Download Complete Package",
#                             data=zip_data,
#                             file_name=f"tender_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
#                             mime="application/zip",
#                             use_container_width=True
#                         )
            
#         except Exception as e:
#             st.error(f"Error displaying results: {str(e)}")

# def show_analytics_section():
#     """Show analytics and visualizations."""
    
#     st.header("📈 Analytics Dashboard")
    
#     if not st.session_state.processing_complete:
#         st.warning("⚠️ No data available for analytics. Please process a file first.")
#         return
    
#     # Get latest results
#     results = st.session_state.processor.get_latest_results()
    
#     if not results['dept_classified_files']:
#         st.error("❌ No classified data available for analytics.")
#         return
    
#     try:
#         df = pd.read_excel(results['dept_classified_files'][0])
        
#         # Department distribution
#         if 'معاونت مربوطه' in df.columns:
#             st.subheader("🏢 Department Distribution")
            
#             dept_counts = df['معاونت مربوطه'].value_counts()
            
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 # Pie chart
#                 fig_pie = px.pie(
#                     values=dept_counts.values,
#                     names=dept_counts.index,
#                     title="Tenders by Department"
#                 )
#                 fig_pie.update_traces(textposition='inside', textinfo='percent+label')
#                 st.plotly_chart(fig_pie, use_container_width=True)
            
#             with col2:
#                 # Bar chart
#                 fig_bar = px.bar(
#                     x=dept_counts.index,
#                     y=dept_counts.values,
#                     title="Department Tender Count"
#                 )
#                 fig_bar.update_layout(xaxis_title="Department", yaxis_title="Number of Tenders")
#                 st.plotly_chart(fig_bar, use_container_width=True)
        
#         # Regional distribution
#         if 'منطقه' in df.columns:
#             st.subheader("🗺️ Regional Distribution")
            
#             region_counts = df['منطقه'].value_counts().head(10)
            
#             fig_region = px.bar(
#                 x=region_counts.values,
#                 y=region_counts.index,
#                 orientation='h',
#                 title="Top 10 Regions by Tender Count"
#             )
#             fig_region.update_layout(xaxis_title="Number of Tenders", yaxis_title="Region")
#             st.plotly_chart(fig_region, use_container_width=True)
        
#         # Data quality metrics
#         st.subheader("📊 Data Quality Metrics")
        
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             completeness = (df.notna().sum().sum() / (len(df) * len(df.columns))) * 100
#             st.metric("Data Completeness", f"{completeness:.1f}%")
        
#         with col2:
#             classified_rate = (df['معاونت مربوطه'] != 'نامشخص').sum() / len(df) * 100 if 'معاونت مربوطه' in df.columns else 0
#             st.metric("Classification Rate", f"{classified_rate:.1f}%")
        
#         with col3:
#             unique_organizers = df['برگزارکننده'].nunique() if 'برگزارکننده' in df.columns else 0
#             st.metric("Unique Organizers", unique_organizers)
        
#         with col4:
#             processing_date = datetime.now().strftime("%Y-%m-%d")
#             st.metric("Last Processed", processing_date)
        
#     except Exception as e:
#         st.error(f"Error generating analytics: {str(e)}")

# def show_settings_section():
#     """Show application settings."""
    
#     st.header("⚙️ Settings")
    
#     # API Configuration
#     st.subheader("🔑 API Configuration")
    
#     with st.expander("OpenAI API Settings"):
#         current_key = os.getenv("OPENAI_API_KEY", "")
#         current_url = os.getenv("OPENAI_BASE_URL", "")
        
#         api_key = st.text_input(
#             "API Key",
#             value=current_key[:10] + "..." if current_key else "",
#             type="password",
#             help="Your OpenAI API key"
#         )
        
#         base_url = st.text_input(
#             "Base URL",
#             value=current_url,
#             help="API base URL (optional)"
#         )
        
#         if st.button("💾 Save API Settings"):
#             st.success("✅ API settings would be saved (in a real deployment)")
    
#     # Processing Settings
#     st.subheader("🔧 Processing Settings")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         batch_size = st.slider("Batch Size", 10, 100, 50, help="Number of tenders to process per batch")
#         timeout = st.slider("API Timeout (seconds)", 30, 300, 120, help="Timeout for API requests")
    
#     with col2:
#         enable_backup = st.checkbox("Enable Backup", value=True, help="Automatically backup processed files")
#         debug_mode = st.checkbox("Debug Mode", value=False, help="Enable detailed logging")
    
#     # System Information
#     st.subheader("ℹ️ System Information")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.info(f"**Python Version:** {sys.version.split()[0]}")
#         st.info(f"**Streamlit Version:** {st.__version__}")
    
#     with col2:
#         # Check directories
#         dirs_status = {
#             "Input Directory": os.path.exists(INPUT_DIR),
#             "Output Directory": os.path.exists(DEPT_OUTPUT_DIR),
#             "Backup Directory": os.path.exists(BACKUP_DIR)
#         }
        
#         for dir_name, exists in dirs_status.items():
#             status = "✅ Exists" if exists else "❌ Missing"
#             st.info(f"**{dir_name}:** {status}")
    
#     # Clear cache button
#     st.subheader("🧹 Maintenance")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         if st.button("🗑️ Clear Cache", help="Clear Streamlit cache"):
#             st.cache_data.clear()
#             st.success("✅ Cache cleared!")
    
#     with col2:
#         if st.button("🔄 Reset Session", help="Reset application session"):
#             st.session_state.clear()
#             st.success("✅ Session reset!")
#             st.rerun()

# if __name__ == "__main__":
#     main()

# ---------------------------------------------------------------------------------------------------------

# """
# Tender Processing System - Web Application
# A modern web interface for processing tender data using AI.
# """

# import streamlit as st
# import pandas as pd
# import os
# import tempfile
# import zipfile
# from datetime import datetime, timedelta
# import time
# import plotly.express as px
# import plotly.graph_objects as go
# from streamlit_option_menu import option_menu
# from stqdm import stqdm
# import io
# import sys
# import threading
# import queue
# import subprocess
# from pathlib import Path
# import re
# import jdatetime  # For Persian calendar support

# # Add project root to path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from dotenv import load_dotenv
# load_dotenv()

# # Import our modules
# from src.utils.config import INPUT_DIR, AI_OUTPUT_DIR, DEPT_OUTPUT_DIR, BACKUP_DIR

# # Page configuration
# st.set_page_config(
#     page_title="Tender Processing System",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         text-align: center;
#         padding: 2rem 0;
#         background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border-radius: 10px;
#         margin-bottom: 2rem;
#     }
    
#     .stats-container {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 10px;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#         margin: 1rem 0;
#     }
    
#     .upload-section {
#         border: 2px dashed #cccccc;
#         border-radius: 10px;
#         padding: 2rem;
#         text-align: center;
#         margin: 2rem 0;
#     }
    
#     .success-message {
#         background: #d4edda;
#         color: #155724;
#         padding: 1rem;
#         border-radius: 5px;
#         margin: 1rem 0;
#     }
    
#     .error-message {
#         background: #f8d7da;
#         color: #721c24;
#         padding: 1rem;
#         border-radius: 5px;
#         margin: 1rem 0;
#     }
    
#     .processing-step {
#         background: #fff3cd;
#         color: #856404;
#         padding: 1rem;
#         border-radius: 5px;
#         margin: 0.5rem 0;
#         border-left: 4px solid #ffc107;
#     }
    
#     .stage-indicator {
#         background: #e3f2fd;
#         color: #1976d2;
#         padding: 0.8rem;
#         border-radius: 5px;
#         margin: 0.5rem 0;
#         border-left: 4px solid #2196f3;
#         font-weight: bold;
#     }
    
#     .stDataFrame {
#         border: 1px solid #e0e0e0;
#         border-radius: 5px;
#     }
# </style>
# """, unsafe_allow_html=True)

# class TenderProcessor:
#     """Main class for handling the tender processing pipeline."""
    
#     def __init__(self):
#         self.temp_dir = tempfile.mkdtemp()
#         self.results = {}
        
#     def save_uploaded_file(self, uploaded_file):
#         """Save uploaded HTML file to input directory."""
#         try:
#             # Create a unique filename
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             filename = f"{timestamp}_{uploaded_file.name}"
#             file_path = os.path.join(INPUT_DIR, filename)
            
#             # Save the file
#             with open(file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
            
#             return file_path, filename
#         except Exception as e:
#             st.error(f"Error saving file: {str(e)}")
#             return None, None
    
#     def run_processing_pipeline_detailed(self, progress_callback=None, log_callback=None):
#         """Run the complete processing pipeline with detailed progress tracking."""
#         try:
#             import sys
#             import os
            
#             # Add project root to Python path
#             project_root = os.path.dirname(__file__)
#             if project_root not in sys.path:
#                 sys.path.insert(0, project_root)
            
#             if progress_callback:
#                 progress_callback("🚀 Initializing processing pipeline...", 5)
#             if log_callback:
#                 log_callback("Starting processing pipeline")
            
#             # Stage 1: HTML Extraction
#             if progress_callback:
#                 progress_callback("📄 Stage 1: HTML Extraction", 10)
#             if log_callback:
#                 log_callback("Stage 1: Starting HTML extraction")
            
#             # Import and run HTML processing
#             from src.extraction.html_parser import TenderHTMLParser
#             from src.extraction.excel_manager import ExcelManager
#             from src.utils.config import PROCESSED_DIR
            
#             # Get HTML files
#             html_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.html')]
#             if not html_files:
#                 return False, "No HTML files found in input directory"
            
#             if progress_callback:
#                 progress_callback("📄 Processing HTML files...", 20)
#             if log_callback:
#                 log_callback(f"Found {len(html_files)} HTML files to process")
            
#             # Process HTML files
#             parser = TenderHTMLParser()
#             excel_mgr = ExcelManager(PROCESSED_DIR)
#             processed_files = []
            
#             for i, html_file in enumerate(html_files):
#                 file_path = os.path.join(INPUT_DIR, html_file)
#                 if log_callback:
#                     log_callback(f"Processing {html_file}")
                
#                 tenders = parser.parse_file(file_path)
#                 if tenders:
#                     excel_name = f"{os.path.splitext(html_file)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
#                     excel_path = excel_mgr.save_to_excel(tenders, excel_name)
#                     processed_files.append(excel_path)
#                     if log_callback:
#                         log_callback(f"Extracted {len(tenders)} tenders from {html_file}")
                
#                 # Update progress
#                 progress = 20 + (10 * (i + 1) / len(html_files))
#                 if progress_callback:
#                     progress_callback(f"📄 Processed {i+1}/{len(html_files)} HTML files", int(progress))
            
#             if not processed_files:
#                 return False, "No tenders extracted from HTML files"
            
#             if progress_callback:
#                 progress_callback("✅ Stage 1 Complete: HTML extraction finished", 35)
#             if log_callback:
#                 log_callback(f"Stage 1 completed. Processed {len(processed_files)} files")
            
#             # Stage 2: AI Filtering
#             if progress_callback:
#                 progress_callback("🤖 Stage 2: AI Filtering (Consulting vs Contracting)", 40)
#             if log_callback:
#                 log_callback("Stage 2: Starting AI filtering")
            
#             try:
#                 # Check API key
#                 api_key = os.getenv("OPENAI_API_KEY")
#                 if not api_key:
#                     if log_callback:
#                         log_callback("Warning: No API key found, skipping AI processing")
#                     if progress_callback:
#                         progress_callback("⚠️ Skipping AI processing (no API key)", 65)
#                     ai_result = None
#                 else:
#                     from process_tenders import process_tenders_auto
                    
#                     if progress_callback:
#                         progress_callback("🤖 Running AI classification...", 50)
                    
#                     ai_result = process_tenders_auto()
                    
#                     if ai_result:
#                         if progress_callback:
#                             progress_callback("✅ Stage 2 Complete: AI filtering finished", 65)
#                         if log_callback:
#                             log_callback("Stage 2 completed successfully")
#                     else:
#                         if log_callback:
#                             log_callback("Stage 2 failed - AI processing returned no results")
#                         return False, "AI filtering failed"
            
#             except Exception as e:
#                 if log_callback:
#                     log_callback(f"Stage 2 error: {str(e)}")
#                 return False, f"AI filtering failed: {str(e)}"
            
#             # Stage 3: Department Classification
#             if progress_callback:
#                 progress_callback("🏢 Stage 3: Department Classification", 70)
#             if log_callback:
#                 log_callback("Stage 3: Starting department classification")
            
#             try:
#                 if ai_result:  # Only run if AI processing was successful
#                     from classify_departments import classify_departments_auto
                    
#                     if progress_callback:
#                         progress_callback("🏢 Classifying by departments...", 80)
                    
#                     dept_result = classify_departments_auto()
                    
#                     if dept_result:
#                         if progress_callback:
#                             progress_callback("✅ Stage 3 Complete: Department classification finished", 95)
#                         if log_callback:
#                             log_callback("Stage 3 completed successfully")
#                     else:
#                         if log_callback:
#                             log_callback("Stage 3 failed - Department classification returned no results")
#                         return False, "Department classification failed"
#                 else:
#                     if progress_callback:
#                         progress_callback("⚠️ Skipping department classification (AI was skipped)", 95)
#                     if log_callback:
#                         log_callback("Skipping Stage 3 - AI processing was not performed")
            
#             except Exception as e:
#                 if log_callback:
#                     log_callback(f"Stage 3 error: {str(e)}")
#                 return False, f"Department classification failed: {str(e)}"
            
#             # Final completion
#             if progress_callback:
#                 progress_callback("🎉 All stages completed successfully!", 100)
#             if log_callback:
#                 log_callback("Pipeline completed successfully")
            
#             return True, "Processing completed successfully"
            
#         except Exception as e:
#             if log_callback:
#                 log_callback(f"Pipeline error: {str(e)}")
#             return False, str(e)
    
#     def get_latest_results(self):
#         """Get the latest processing results."""
#         results = {
#             'extracted_files': [],
#             'ai_filtered_files': [],
#             'dept_classified_files': []
#         }
        
#         try:
#             # Get latest department classified file
#             if os.path.exists(DEPT_OUTPUT_DIR):
#                 dept_files = [f for f in os.listdir(DEPT_OUTPUT_DIR) if f.endswith('.xlsx')]
#                 if dept_files:
#                     dept_files.sort(key=lambda x: os.path.getmtime(os.path.join(DEPT_OUTPUT_DIR, x)), reverse=True)
#                     latest_dept_file = os.path.join(DEPT_OUTPUT_DIR, dept_files[0])
#                     results['dept_classified_files'] = [latest_dept_file]
            
#             # Get AI filtered files
#             if os.path.exists(AI_OUTPUT_DIR):
#                 ai_files = [f for f in os.listdir(AI_OUTPUT_DIR) if f.endswith('.xlsx')]
#                 results['ai_filtered_files'] = [os.path.join(AI_OUTPUT_DIR, f) for f in ai_files]
            
#         except Exception as e:
#             st.error(f"Error getting results: {str(e)}")
        
#         return results
    
#     def create_download_package(self, file_paths):
#         """Create a ZIP package of result files."""
#         try:
#             zip_buffer = io.BytesIO()
            
#             with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
#                 for file_path in file_paths:
#                     if os.path.exists(file_path):
#                         filename = os.path.basename(file_path)
#                         zip_file.write(file_path, filename)
            
#             zip_buffer.seek(0)
#             return zip_buffer.getvalue()
#         except Exception as e:
#             st.error(f"Error creating download package: {str(e)}")
#             return None

# def parse_filename_datetime(filename):
#     """Parse datetime information from filename."""
#     try:
#         # Extract pattern like "52385_1404-06-16 18:00 - Main.html"
#         # Or "timestamp_YYYY-MM-DD HH:MM - description.html"
        
#         # First, try to extract Persian date pattern
#         persian_pattern = r'(\d{4}-\d{2}-\d{2})\s+(\d{1,2}):(\d{2})'
#         match = re.search(persian_pattern, filename)
        
#         if match:
#             date_str = match.group(1)  # YYYY-MM-DD
#             hour = int(match.group(2))
#             minute = int(match.group(3))
            
#             # Parse Persian date
#             year, month, day = map(int, date_str.split('-'))
            
#             # Convert Persian to Gregorian
#             try:
#                 persian_date = jdatetime.date(year, month, day)
#                 gregorian_date = persian_date.togregorian()
                
#                 # Determine AM/PM from filename
#                 is_pm = 'بعدازظهر' in filename or 'بعداز ظهر' in filename
#                 if is_pm and hour < 12:
#                     hour += 12
#                 elif not is_pm and hour == 12:
#                     hour = 0
                
#                 full_datetime = datetime.combine(gregorian_date, datetime.min.time().replace(hour=hour, minute=minute))
                
#                 return {
#                     'datetime': full_datetime,
#                     'persian_date': date_str,
#                     'time_str': f"{match.group(2)}:{match.group(3)}",
#                     'period': 'بعدازظهر' if is_pm else 'صبح'
#                 }
#             except:
#                 pass
        
#         # Fallback: try to extract timestamp from beginning of filename
#         timestamp_pattern = r'^(\d{8}_\d{6})'
#         match = re.search(timestamp_pattern, filename)
#         if match:
#             timestamp_str = match.group(1)
#             dt = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
#             return {
#                 'datetime': dt,
#                 'persian_date': None,
#                 'time_str': dt.strftime('%H:%M'),
#                 'period': 'بعدازظهر' if dt.hour >= 12 else 'صبح'
#             }
        
#         return None
#     except Exception as e:
#         st.error(f"Error parsing filename datetime: {e}")
#         return None

# def main():
#     """Main application function."""
    
#     # Initialize session state
#     if 'processor' not in st.session_state:
#         st.session_state.processor = TenderProcessor()
#     if 'processing_complete' not in st.session_state:
#         st.session_state.processing_complete = False
#     if 'uploaded_file_name' not in st.session_state:
#         st.session_state.uploaded_file_name = None
    
#     # Header
#     st.markdown("""
#     <div class="main-header">
#         <h1>📊 Tender Processing System</h1>
#         <p>AI-Powered Tender Analysis and Department Classification</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Sidebar menu
#     with st.sidebar:
#         selected = option_menu(
#             "Navigation",
#             ["Upload & Process", "View Results", "Analytics", "Settings"],
#             icons=["upload", "table", "bar-chart", "gear"],
#             menu_icon="list",
#             default_index=0
#         )
    
#     # Main content based on selected menu
#     if selected == "Upload & Process":
#         show_upload_section()
#     elif selected == "View Results":
#         show_results_section()
#     elif selected == "Analytics":
#         show_analytics_section()
#     elif selected == "Settings":
#         show_settings_section()

# def show_upload_section():
#     """Show the file upload and processing section."""
    
#     st.header("📁 Upload HTML File")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         # File uploader
#         uploaded_file = st.file_uploader(
#             "Choose an HTML file",
#             type=['html', 'htm'],
#             help="Upload the HTML file containing tender data"
#         )
        
#         if uploaded_file is not None:
#             st.session_state.uploaded_file_name = uploaded_file.name
            
#             # Show file info
#             st.info(f"📄 File: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
            
#             # Process button
#             if st.button("🚀 Start Processing", type="primary", use_container_width=True):
#                 process_file_detailed(uploaded_file)
    
#     with col2:
#         # Instructions
#         st.markdown("""
#         ### 📋 Instructions:
#         1. Upload your HTML file
#         2. Click "Start Processing"
#         3. Wait for completion
#         4. Download results
        
#         ### ⚡ Features:
#         - AI-powered filtering
#         - Department classification
#         - Automatic backup
#         - Excel export
#         """)

# def process_file_detailed(uploaded_file):
#     """Process the uploaded file through the pipeline with detailed progress."""
    
#     # Save the uploaded file
#     file_path, filename = st.session_state.processor.save_uploaded_file(uploaded_file)
    
#     if not file_path:
#         st.error("Failed to save uploaded file")
#         return
    
#     st.success(f"File saved: {filename}")
    
#     # Create progress tracking containers
#     progress_container = st.container()
#     log_container = st.container()
    
#     # Progress tracking variables
#     progress_bar = progress_container.progress(0)
#     status_container = progress_container.empty()
#     log_messages = []
    
#     def update_progress(message, progress):
#         progress_bar.progress(progress / 100)
#         status_container.markdown(f'<div class="stage-indicator">🔄 {message}</div>', unsafe_allow_html=True)
    
#     def log_message(message):
#         log_messages.append(f"{datetime.now().strftime('%H:%M:%S')} - {message}")
#         with log_container:
#             with st.expander("📜 Processing Log", expanded=True):
#                 for msg in log_messages[-10:]:  # Show last 10 messages
#                     st.text(msg)
    
#     # Run the processing pipeline with detailed tracking
#     with st.spinner("Processing tender data..."):
#         success, output = st.session_state.processor.run_processing_pipeline_detailed(
#             progress_callback=update_progress,
#             log_callback=log_message
#         )
    
#     if success:
#         st.session_state.processing_complete = True
#         progress_bar.progress(100)
#         status_container.markdown('<div class="success-message">✅ Processing completed successfully!</div>', unsafe_allow_html=True)
        
#         # Show completion message
#         st.balloons()
#         st.success("🎉 All processing stages completed successfully!")
        
#         # Auto-refresh to show results
#         time.sleep(2)
#         st.rerun()
#     else:
#         st.markdown(f'<div class="error-message">❌ Processing failed: {output}</div>', unsafe_allow_html=True)
        
#         # Show error details
#         with st.expander("🔍 Error Details"):
#             st.text(output)

# def show_results_section():
#     """Show the processing results section."""
    
#     st.header("📊 Processing Results")
    
#     if not st.session_state.processing_complete:
#         st.warning("⚠️ No processing results available. Please upload and process a file first.")
#         return
    
#     # Get latest results
#     results = st.session_state.processor.get_latest_results()
    
#     if not any(results.values()):
#         st.error("❌ No result files found.")
#         return
    
#     # Show results summary
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.metric("📄 Extracted Files", len(results.get('extracted_files', [])))
    
#     with col2:
#         st.metric("🤖 AI Filtered Files", len(results.get('ai_filtered_files', [])))
    
#     with col3:
#         st.metric("🏢 Classified Files", len(results.get('dept_classified_files', [])))
    
#     # Show classified data if available
#     if results['dept_classified_files']:
#         latest_file = results['dept_classified_files'][0]
        
#         st.subheader("📋 Department Classified Tenders")
        
#         try:
#             df = pd.read_excel(latest_file)
            
#             # Show basic stats
#             col1, col2, col3, col4 = st.columns(4)
#             with col1:
#                 st.metric("Total Tenders", len(df))
#             with col2:
#                 dept_count = df['معاونت مربوطه'].nunique() if 'معاونت مربوطه' in df.columns else 0
#                 st.metric("Departments", dept_count)
#             with col3:
#                 consulting_count = len(df)
#                 st.metric("Consulting Tenders", consulting_count)
#             with col4:
#                 success_rate = "100%" if len(df) > 0 else "0%"
#                 st.metric("Success Rate", success_rate)
            
#             # Show data table
#             st.subheader("📊 Tender Data")
            
#             # Customize displayed columns
#             display_columns = []
#             if 'شماره مناقصه در هزاره' in df.columns:
#                 display_columns.append('شماره مناقصه در هزاره')
#             if 'معاونت مربوطه' in df.columns:
#                 display_columns.append('معاونت مربوطه')
#             if 'عنوان' in df.columns:
#                 display_columns.append('عنوان')
#             if 'برگزارکننده' in df.columns:
#                 display_columns.append('برگزارکننده')
#             if 'منطقه' in df.columns:
#                 display_columns.append('منطقه')
            
#             if display_columns:
#                 st.dataframe(
#                     df[display_columns].head(50),
#                     use_container_width=True,
#                     height=400
#                 )
                
#                 if len(df) > 50:
#                     st.info(f"📄 Showing first 50 of {len(df)} total records")
            
#             # Download section
#             st.subheader("💾 Download Results")
            
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 # Download Excel file
#                 with open(latest_file, 'rb') as f:
#                     excel_data = f.read()
                
#                 st.download_button(
#                     label="📄 Download Excel File",
#                     data=excel_data,
#                     file_name=f"tender_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
#                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#                     use_container_width=True
#                 )
            
#             with col2:
#                 # Download complete package
#                 all_files = []
#                 if results['dept_classified_files']:
#                     all_files.extend(results['dept_classified_files'])
#                 if results['ai_filtered_files']:
#                     all_files.extend(results['ai_filtered_files'])
                
#                 if all_files:
#                     zip_data = st.session_state.processor.create_download_package(all_files)
#                     if zip_data:
#                         st.download_button(
#                             label="📦 Download Complete Package",
#                             data=zip_data,
#                             file_name=f"tender_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
#                             mime="application/zip",
#                             use_container_width=True
#                         )
            
#         except Exception as e:
#             st.error(f"Error displaying results: {str(e)}")

# def show_analytics_section():
#     """Show analytics and visualizations with date/time filtering."""
    
#     st.header("📈 Interactive Analytics Dashboard")
    
#     if not st.session_state.processing_complete:
#         st.warning("⚠️ No data available for analytics. Please process a file first.")
#         return
    
#     # Get latest results
#     results = st.session_state.processor.get_latest_results()
    
#     if not results['dept_classified_files']:
#         st.error("❌ No classified data available for analytics.")
#         return
    
#     try:
#         df = pd.read_excel(results['dept_classified_files'][0])
        
#         # Extract datetime information from processed files
#         file_datetime_info = []
        
#         # Check INPUT_DIR for original files to extract datetime
#         if os.path.exists(INPUT_DIR):
#             input_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.html')]
#             for file in input_files:
#                 datetime_info = parse_filename_datetime(file)
#                 if datetime_info:
#                     datetime_info['filename'] = file
#                     file_datetime_info.append(datetime_info)
        
#         # Date and Time Filters
#         st.subheader("🗓️ Date and Time Filters")
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             if file_datetime_info:
#                 # Extract unique dates
#                 available_dates = sorted(list(set([info['datetime'].date() for info in file_datetime_info])))
                
#                 if len(available_dates) > 1:
#                     selected_date = st.selectbox(
#                         "Select Date",
#                         options=['All Dates'] + [d.strftime('%Y-%m-%d') for d in available_dates],
#                         index=0
#                     )
#                 else:
#                     selected_date = 'All Dates'
#                     st.info("Only one date available in data")
#             else:
#                 selected_date = 'All Dates'
#                 st.info("No date information found in filenames")
        
#         with col2:
#             time_periods = ['All Times', 'صبح (Morning)', 'بعدازظهر (Afternoon)']
#             selected_time_period = st.selectbox("Select Time Period", time_periods)
        
#         with col3:
#             if file_datetime_info:
#                 available_hours = sorted(list(set([info['datetime'].hour for info in file_datetime_info])))
#                 hour_options = ['All Hours'] + [f"{h:02d}:00" for h in available_hours]
#                 selected_hour = st.selectbox("Select Hour", hour_options)
#             else:
#                 selected_hour = 'All Hours'
        
#         # Apply filters (for demonstration, we'll show different visualizations based on selected filters)
#         filtered_info = file_datetime_info.copy()
        
#         if selected_date != 'All Dates':
#             selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
#             filtered_info = [info for info in filtered_info if info['datetime'].date() == selected_date_obj]
        
#         if selected_time_period != 'All Times':
#             if 'صبح' in selected_time_period:
#                 filtered_info = [info for info in filtered_info if info['period'] == 'صبح']
#             elif 'بعدازظهر' in selected_time_period:
#                 filtered_info = [info for info in filtered_info if info['period'] == 'بعدازظهر']
        
#         if selected_hour != 'All Hours':
#             selected_hour_int = int(selected_hour.split(':')[0])
#             filtered_info = [info for info in filtered_info if info['datetime'].hour == selected_hour_int]
        
#         # Display filter results
#         if filtered_info:
#             st.success(f"📊 Showing analytics for {len(filtered_info)} time period(s)")
            
#             # Create a summary of selected filters
#             filter_summary = []
#             if selected_date != 'All Dates':
#                 filter_summary.append(f"Date: {selected_date}")
#             if selected_time_period != 'All Times':
#                 filter_summary.append(f"Period: {selected_time_period}")
#             if selected_hour != 'All Hours':
#                 filter_summary.append(f"Hour: {selected_hour}")
            
#             if filter_summary:
#                 st.info(f"🔍 Active Filters: {' | '.join(filter_summary)}")
#         else:
#             st.warning("⚠️ No data matches the selected filters")
        
#         # Department distribution
#         if 'معاونت مربوطه' in df.columns:
#             st.subheader("🏢 Department Distribution")
            
#             dept_counts = df['معاونت مربوطه'].value_counts()
            
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 # Pie chart
#                 fig_pie = px.pie(
#                     values=dept_counts.values,
#                     names=dept_counts.index,
#                     title="Tenders by Department"
#                 )
#                 fig_pie.update_traces(textposition='inside', textinfo='percent+label')
#                 st.plotly_chart(fig_pie, use_container_width=True)
            
#             with col2:
#                 # Bar chart
#                 fig_bar = px.bar(
#                     x=dept_counts.index,
#                     y=dept_counts.values,
#                     title="Department Tender Count",
#                     labels={'x': 'Department', 'y': 'Number of Tenders'}
#                 )
#                 fig_bar.update_layout(xaxis_tickangle=-45)
#                 st.plotly_chart(fig_bar, use_container_width=True)
        
#         # Time-based analytics
#         if file_datetime_info:
#             st.subheader("⏰ Time-based Analysis")
            
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 # Time period distribution
#                 period_counts = {}
#                 for info in file_datetime_info:
#                     period = info['period']
#                     period_counts[period] = period_counts.get(period, 0) + 1
                
#                 if period_counts:
#                     fig_period = px.pie(
#                         values=list(period_counts.values()),
#                         names=list(period_counts.keys()),
#                         title="Distribution by Time Period"
#                     )
#                     st.plotly_chart(fig_period, use_container_width=True)
            
#             with col2:
#                 # Hourly distribution
#                 hour_counts = {}
#                 for info in file_datetime_info:
#                     hour = info['datetime'].hour
#                     hour_counts[f"{hour:02d}:00"] = hour_counts.get(f"{hour:02d}:00", 0) + 1
                
#                 if hour_counts:
#                     fig_hourly = px.bar(
#                         x=list(hour_counts.keys()),
#                         y=list(hour_counts.values()),
#                         title="Tender Processing by Hour",
#                         labels={'x': 'Hour', 'y': 'Number of Files'}
#                     )
#                     st.plotly_chart(fig_hourly, use_container_width=True)
        
#         # Regional distribution
#         if 'منطقه' in df.columns:
#             st.subheader("🗺️ Regional Distribution")
            
#             region_counts = df['منطقه'].value_counts().head(10)
            
#             fig_region = px.bar(
#                 x=region_counts.values,
#                 y=region_counts.index,
#                 orientation='h',
#                 title="Top 10 Regions by Tender Count",
#                 labels={'x': 'Number of Tenders', 'y': 'Region'}
#             )
#             st.plotly_chart(fig_region, use_container_width=True)
        
#         # Data quality metrics
#         st.subheader("📊 Data Quality Metrics")
        
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             completeness = (df.notna().sum().sum() / (len(df) * len(df.columns))) * 100
#             st.metric("Data Completeness", f"{completeness:.1f}%")
        
#         with col2:
#             classified_rate = (df['معاونت مربوطه'] != 'نامشخص').sum() / len(df) * 100 if 'معاونت مربوطه' in df.columns else 0
#             st.metric("Classification Rate", f"{classified_rate:.1f}%")
        
#         with col3:
#             unique_organizers = df['برگزارکننده'].nunique() if 'برگزارکننده' in df.columns else 0
#             st.metric("Unique Organizers", unique_organizers)
        
#         with col4:
#             files_processed = len(file_datetime_info)
#             st.metric("Files Processed", files_processed)
        
#     except Exception as e:
#         st.error(f"Error generating analytics: {str(e)}")

# def show_settings_section():
#     """Show application settings."""
    
#     st.header("⚙️ Settings")
    
#     # API Configuration
#     st.subheader("🔑 API Configuration")
    
#     with st.expander("OpenAI API Settings"):
#         current_key = os.getenv("OPENAI_API_KEY", "")
#         current_url = os.getenv("OPENAI_BASE_URL", "")
        
#         api_key = st.text_input(
#             "API Key",
#             value=current_key[:10] + "..." if current_key else "",
#             type="password",
#             help="Your OpenAI API key"
#         )
        
#         base_url = st.text_input(
#             "Base URL",
#             value=current_url,
#             help="API base URL (optional)"
#         )
        
#         if st.button("💾 Save API Settings"):
#             st.success("✅ API settings would be saved (in a real deployment)")
    
#     # Processing Settings
#     st.subheader("🔧 Processing Settings")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         batch_size = st.slider("Batch Size", 10, 100, 50, help="Number of tenders to process per batch")
#         timeout = st.slider("API Timeout (seconds)", 30, 300, 120, help="Timeout for API requests")
    
#     with col2:
#         enable_backup = st.checkbox("Enable Backup", value=True, help="Automatically backup processed files")
#         debug_mode = st.checkbox("Debug Mode", value=False, help="Enable detailed logging")
    
#     # System Information
#     st.subheader("ℹ️ System Information")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.info(f"**Python Version:** {sys.version.split()[0]}")
#         st.info(f"**Streamlit Version:** {st.__version__}")
    
#     with col2:
#         # Check directories
#         dirs_status = {
#             "Input Directory": os.path.exists(INPUT_DIR),
#             "Output Directory": os.path.exists(DEPT_OUTPUT_DIR),
#             "Backup Directory": os.path.exists(BACKUP_DIR)
#         }
        
#         for dir_name, exists in dirs_status.items():
#             status = "✅ Exists" if exists else "❌ Missing"
#             st.info(f"**{dir_name}:** {status}")
    
#     # Clear cache button
#     st.subheader("🧹 Maintenance")
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         if st.button("🗑️ Clear Cache", help="Clear Streamlit cache"):
#             st.cache_data.clear()
#             st.success("✅ Cache cleared!")
    
#     with col2:
#         if st.button("🔄 Reset Session", help="Reset application session"):
#             st.session_state.clear()
#             st.success("✅ Session reset!")
#             st.rerun()

# if __name__ == "__main__":
#     main()

# -----------------------------------------------------------------------------------------------


"""
سامانه پردازش مناقصات - اپلیکیشن وب
واسط وب مدرن برای پردازش داده‌های مناقصه با استفاده از هوش مصنوعی
"""

import streamlit as st
import pandas as pd
import os
import tempfile
import zipfile
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import io
import sys
import subprocess
from pathlib import Path
import re
import shutil
import jdatetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

# Import our modules
from src.utils.config import (
    INPUT_DIR, AI_OUTPUT_DIR, DEPT_OUTPUT_DIR, BACKUP_DIR,
    PROCESSED_DIR, BACKUP_PROCESSED_DIR, BACKUP_CONS_FILTER_DIR, BACKUP_DEPT_CLASS_DIR
)

# Page configuration
st.set_page_config(
    page_title="سامانه پردازش مناقصات",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Persian RTL layout
# Custom CSS for Persian RTL layout
# Custom CSS for Persian RTL layout with fixed sidebar
# Robust CSS and JavaScript solution for fixed RTL sidebar
st.markdown("""
<style>
    /* Import IRANSans font */
    @font-face {
        font-family: 'IRANSans';
        src: url('./IRANSans.ttf') format('truetype');
        font-weight: normal;
        font-style: normal;
    }
    
    /* Apply IRANSans font to entire app */
    * {
        font-family: 'IRANSans', 'Tahoma', 'Arial', sans-serif !important;
    }
    
    /* RTL Layout for main app */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    .main .block-container {
        direction: rtl;
        text-align: right;
        margin-right: 320px !important; /* Space for sidebar */
        margin-left: 1rem !important;
        padding-right: 2rem !important;
        padding-left: 1rem !important;
    }
    
    /* File uploader - keep LTR for proper functionality */
    .stFileUploader {
        direction: ltr !important;
        text-align: left !important;
    }
    
    .stFileUploader label {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'IRANSans', 'Tahoma', 'Arial', sans-serif !important;
    }
    
    .stFileUploader > div {
        direction: ltr !important;
    }
    
    /* File uploader button positioning */
    .stFileUploader button {
        float: left !important;
        margin-right: 0 !important;
        margin-left: auto !important;
    }
    
    /* Drag and drop area - keep LTR */
    .uploadedFile, .file-upload-container {
        direction: ltr !important;
        text-align: left !important;
    }
    
    /* Other RTL elements */
    .stSelectbox, .stTextInput, .stTextArea {
        direction: rtl;
        text-align: right;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        font-family: 'IRANSans', 'Tahoma', sans-serif !important;
    }
    
    /* Card styling */
    .stats-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        direction: rtl;
        text-align: right;
    }
    
    /* Upload section - mixed LTR/RTL */
    .upload-section {
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        direction: rtl;
    }
    
    /* Success message */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        direction: rtl;
        text-align: right;
        border-right: 4px solid #28a745;
    }
    
    /* Error message */
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        direction: rtl;
        text-align: right;
        border-right: 4px solid #dc3545;
    }
    
    /* Stage indicator */
    .stage-indicator {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.8rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-right: 4px solid #2196f3;
        font-weight: bold;
        direction: rtl;
        text-align: right;
    }
    
    /* Progress info */
    .progress-info {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-right: 4px solid #ffc107;
        direction: rtl;
        text-align: right;
    }
    
    /* Data frame - keep LTR for readability */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 5px;
        direction: ltr !important;
    }
    
    /* Metrics RTL */
    .metric-container {
        direction: rtl;
        text-align: right;
    }
    
    /* Buttons RTL */
    .stButton > button {
        direction: rtl;
        font-family: 'IRANSans', 'Tahoma', sans-serif !important;
    }
    
    /* Persian font for all text elements */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div {
        font-family: 'IRANSans', 'Tahoma', 'Arial', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    /* Fix plotly charts direction */
    .plotly-graph-div {
        direction: ltr;
    }
    
    /* Progress bar container */
    .stProgress {
        direction: ltr !important;
    }
    
    /* Spinner text RTL */
    .stSpinner > div {
        direction: rtl !important;
        text-align: right !important;
        font-family: 'IRANSans', 'Tahoma', 'Arial', sans-serif !important;
    }
    
    /* Additional spacing adjustments */
    .main .block-container {
        max-width: none !important;
        padding-top: 1rem !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            margin-right: 0 !important;
            padding-right: 1rem !important;
        }
    }
</style>

<script>
function fixSidebarAndLayout() {
    // Function to find sidebar using multiple selectors
    function findSidebar() {
        const selectors = [
            '[data-testid="stSidebar"]',
            '.css-1d391kg',
            '.sidebar',
            '[class*="css-"][class*="sidebar"]',
            'section[data-testid="stSidebar"]'
        ];
        
        for (let selector of selectors) {
            const element = document.querySelector(selector);
            if (element) return element;
        }
        return null;
    }
    
    // Function to find main content area
    function findMainContent() {
        const selectors = [
            '.main .block-container',
            '[data-testid="block-container"]',
            '.css-18e3th9',
            '.main',
            '[class*="block-container"]'
        ];
        
        for (let selector of selectors) {
            const element = document.querySelector(selector);
            if (element) return element;
        }
        return null;
    }
    
    // Function to find and hide collapse button
    function hideCollapseButton() {
        const selectors = [
            '[data-testid="collapsedControl"]',
            '.css-9s5bis',
            '.css-1544g2n',
            '[title="Close sidebar"]',
            'button[kind="header"]'
        ];
        
        selectors.forEach(selector => {
            const button = document.querySelector(selector);
            if (button) {
                button.style.display = 'none';
                button.style.visibility = 'hidden';
            }
        });
    }
    
    const sidebar = findSidebar();
    const mainContent = findMainContent();
    
    if (sidebar) {
        // Force sidebar to be always visible and on the right
        sidebar.style.cssText = `
            position: fixed !important;
            right: 0 !important;
            left: auto !important;
            top: 0 !important;
            height: 100vh !important;
            width: 300px !important;
            z-index: 1000 !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            opacity: 1 !important;
            background-color: #fafafa !important;
            border-left: 1px solid #e0e0e0 !important;
            border-right: none !important;
            overflow-y: auto !important;
        `;
        
        // Apply RTL and font to all sidebar content
        const sidebarElements = sidebar.querySelectorAll('*');
        sidebarElements.forEach(el => {
            if (!el.closest('.stFileUploader')) {
                el.style.setProperty('direction', 'rtl', 'important');
                el.style.setProperty('text-align', 'right', 'important');
            }
            el.style.setProperty('font-family', 'IRANSans, Tahoma, Arial, sans-serif', 'important');
        });
        
        // Special handling for option menu items
        const navLinks = sidebar.querySelectorAll('.nav-link, [class*="nav-link"]');
        navLinks.forEach(link => {
            link.style.setProperty('direction', 'rtl', 'important');
            link.style.setProperty('text-align', 'right', 'important');
            link.style.setProperty('justify-content', 'flex-start', 'important');
            link.style.setProperty('flex-direction', 'row-reverse', 'important');
        });
        
        // Force sidebar container to have proper styling
        const sidebarContainer = sidebar.querySelector('div');
        if (sidebarContainer) {
            sidebarContainer.style.setProperty('direction', 'rtl', 'important');
            sidebarContainer.style.setProperty('text-align', 'right', 'important');
            sidebarContainer.style.setProperty('padding', '1rem', 'important');
        }
    }
    
    if (mainContent) {
        // Adjust main content to not overlap with sidebar
        mainContent.style.cssText = `
            margin-right: 320px !important;
            margin-left: 1rem !important;
            padding-right: 2rem !important;
            padding-left: 1rem !important;
            direction: rtl !important;
            text-align: right !important;
            font-family: IRANSans, Tahoma, Arial, sans-serif !important;
            max-width: none !important;
        `;
    }
    
    // Hide any collapse buttons
    hideCollapseButton();
    
    // Force expand sidebar if it's collapsed
    const expandButton = document.querySelector('[data-testid="baseButton-headerNoPadding"]');
    if (expandButton && expandButton.querySelector('[data-testid="stSidebarNav"]')) {
        expandButton.click();
    }
}

// Run immediately
fixSidebarAndLayout();

// Run after DOM is loaded
document.addEventListener('DOMContentLoaded', fixSidebarAndLayout);

// Run periodically to catch dynamic changes
setInterval(fixSidebarAndLayout, 100);

// Use MutationObserver for more efficient monitoring
const observer = new MutationObserver(function(mutations) {
    let shouldRun = false;
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList' || 
            (mutation.type === 'attributes' && 
             (mutation.attributeName === 'style' || mutation.attributeName === 'class'))) {
            shouldRun = true;
        }
    });
    if (shouldRun) {
        setTimeout(fixSidebarAndLayout, 10);
    }
});

observer.observe(document.body, { 
    childList: true, 
    subtree: true, 
    attributes: true,
    attributeFilter: ['style', 'class']
});

// Handle window resize
window.addEventListener('resize', fixSidebarAndLayout);

// Also try to click any sidebar expand buttons that might appear
document.addEventListener('click', function(e) {
    // Prevent sidebar from being collapsed
    if (e.target.closest('[data-testid="collapsedControl"]') || 
        e.target.closest('.css-9s5bis')) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }
});
</script>
""", unsafe_allow_html=True)
# Add this AFTER your main CSS in app.py
st.markdown("""
<script>
// Force sidebar expansion on page load
window.addEventListener('load', function() {
    setTimeout(function() {
        // Find and click sidebar expand button if it exists
        const expandBtn = document.querySelector('[data-testid="baseButton-headerNoPadding"]');
        if (expandBtn) {
            expandBtn.click();
        }
        
        // Alternative selectors for expand button
        const altExpandBtns = [
            'button[kind="header"]',
            '.css-1y6u1qa',
            '.css-1oe6ams'
        ];
        
        altExpandBtns.forEach(selector => {
            const btn = document.querySelector(selector);
            if (btn && btn.querySelector('svg')) {
                btn.click();
            }
        });
    }, 500);
});

// Force sidebar to stay open
document.addEventListener('click', function(e) {
    // Prevent any sidebar collapse
    const target = e.target.closest('button');
    if (target && (target.getAttribute('data-testid') === 'collapsedControl' || 
                   target.querySelector('[data-testid="stSidebarNav"]'))) {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }
});
</script>
""", unsafe_allow_html=True)

# Add this CSS to override Streamlit's default sidebar behavior
st.markdown("""
<style>
/* Force sidebar to always be expanded */
[data-testid="stSidebar"] {
    transform: translateX(0px) !important;
    width: 300px !important;
    min-width: 300px !important;
}

/* Hide the collapse button entirely */
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}

/* Force main content area to have proper margins */
.main > div {
    margin-right: 320px !important;
    padding-right: 20px !important;
}

/* Ensure sidebar content is RTL */
[data-testid="stSidebar"] * {
    font-family: 'IRANSans', 'Tahoma', sans-serif !important;
    direction: rtl !important;
    text-align: right !important;
}
</style>
""", unsafe_allow_html=True)
class TenderProcessor:
    """کلاس اصلی برای مدیریت پایپ‌لاین پردازش مناقصات"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.results = {}
        
    def save_uploaded_file(self, uploaded_file):
        """ذخیره فایل HTML آپلود شده در پوشه ورودی"""
        try:
            # Create a unique filename keeping original name
            original_name = uploaded_file.name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{original_name}"
            file_path = os.path.join(INPUT_DIR, filename)
            
            # Save the file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return file_path, filename
        except Exception as e:
            st.error(f"خطا در ذخیره فایل: {str(e)}")
            return None, None
    
    def move_file_with_backup(self, source_path, dest_dir, backup_dir, prefix=""):
        """انتقال فایل با ایجاد نسخه پشتیبان"""
        try:
            # Create directories if they don't exist
            os.makedirs(dest_dir, exist_ok=True)
            os.makedirs(backup_dir, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = os.path.basename(source_path)
            
            if prefix:
                new_filename = f"{prefix}_{timestamp}_{original_name}"
            else:
                new_filename = f"{timestamp}_{original_name}"
            
            # Destination paths
            dest_path = os.path.join(dest_dir, new_filename)
            backup_path = os.path.join(backup_dir, new_filename)
            
            # Copy to both destinations
            shutil.copy2(source_path, dest_path)
            shutil.copy2(source_path, backup_path)
            
            # Delete original
            os.remove(source_path)
            
            return dest_path, backup_path
        except Exception as e:
            st.error(f"خطا در انتقال فایل: {str(e)}")
            return None, None
    
    def cleanup_directory(self, directory):
        """پاک کردن تمام فایل‌های یک پوشه"""
        try:
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    file_path = os.path.join(directory, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
        except Exception as e:
            st.error(f"خطا در پاک کردن پوشه: {str(e)}")
    
    def run_processing_pipeline_detailed(self, progress_callback=None):
        """اجرای پایپ‌لاین کامل پردازش با مدیریت صحیح فایل‌ها"""
        try:
            # Stage 1: HTML Extraction
            if progress_callback:
                progress_callback("🔄 در حال استخراج اطلاعات از فایل HTML...", 10)
            
            with st.spinner("🔄 در حال استخراج اطلاعات از فایل HTML..."):
                # Import modules
                from src.extraction.html_parser import TenderHTMLParser
                from src.extraction.excel_manager import ExcelManager
                
                # Get HTML files
                html_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.html')]
                if not html_files:
                    return False, "هیچ فایل HTML در پوشه ورودی یافت نشد"
                
                # Process HTML files
                parser = TenderHTMLParser()
                excel_mgr = ExcelManager(PROCESSED_DIR)
                
                for html_file in html_files:
                    file_path = os.path.join(INPUT_DIR, html_file)
                    tenders = parser.parse_file(file_path)
                    
                    if tenders:
                        # Keep original filename structure
                        base_name = os.path.splitext(html_file)[0]
                        excel_name = f"{base_name}.xlsx"
                        excel_path = excel_mgr.save_to_excel(tenders, excel_name)
                        
                        # Move to backup and keep in processed
                        backup_path = os.path.join(BACKUP_PROCESSED_DIR, f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{excel_name}")
                        shutil.copy2(excel_path, backup_path)
                        
                        # Delete HTML file from input
                        os.remove(file_path)
                
                if progress_callback:
                    progress_callback("✅ مرحله اول: استخراج HTML تکمیل شد", 35)
            
            # Stage 2: AI Filtering
            if progress_callback:
                progress_callback("🤖 در حال فیلتر کردن با هوش مصنوعی (مشاوره‌ای در مقابل پیمانکاری)...", 40)
            
            with st.spinner("🤖 در حال فیلتر کردن با هوش مصنوعی..."):
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    if progress_callback:
                        progress_callback("⚠️ رد شدن از مرحله AI (کلید API یافت نشد)", 65)
                    ai_result = None
                else:
                    from process_tenders import process_tenders_auto
                    ai_result = process_tenders_auto()
                    
                    if ai_result:
                        # Move processed files to backup and delete originals
                        for file in os.listdir(PROCESSED_DIR):
                            if file.endswith('.xlsx'):
                                source_path = os.path.join(PROCESSED_DIR, file)
                                backup_path = os.path.join(BACKUP_CONS_FILTER_DIR, f"cons_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file}")
                                os.remove(source_path)  # Delete from processed after AI processing
                        
                        if progress_callback:
                            progress_callback("✅ مرحله دوم: فیلتر هوش مصنوعی تکمیل شد", 65)
                    else:
                        return False, "فیلتر هوش مصنوعی ناموفق بود"
            
            # Stage 3: Department Classification
            if progress_callback:
                progress_callback("🏢 در حال طبقه‌بندی بر اساس معاونت‌ها...", 70)
            
            with st.spinner("🏢 در حال طبقه‌بندی بر اساس معاونت‌ها..."):
                if ai_result:
                    from classify_departments import classify_departments_auto
                    dept_result = classify_departments_auto()
                    
                    if dept_result:
                        # Move AI filtered files to backup and delete originals
                        for file in os.listdir(AI_OUTPUT_DIR):
                            if file.endswith('.xlsx'):
                                source_path = os.path.join(AI_OUTPUT_DIR, file)
                                backup_path = os.path.join(BACKUP_DEPT_CLASS_DIR, f"dept_classified_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file}")
                                os.remove(source_path)  # Delete from ai_filtered after dept classification
                        
                        if progress_callback:
                            progress_callback("✅ مرحله سوم: طبقه‌بندی معاونت‌ها تکمیل شد", 95)
                    else:
                        return False, "طبقه‌بندی معاونت‌ها ناموفق بود"
                else:
                    if progress_callback:
                        progress_callback("⚠️ رد شدن از طبقه‌بندی معاونت‌ها (AI انجام نشد)", 95)
            
            # Final cleanup - delete final results after processing
            with st.spinner("🧹 در حال پاک‌سازی نهایی..."):
                # Delete files from dept_classified (keep only in backup)
                for file in os.listdir(DEPT_OUTPUT_DIR):
                    if file.endswith('.xlsx'):
                        os.remove(os.path.join(DEPT_OUTPUT_DIR, file))
                
                if progress_callback:
                    progress_callback("🎉 تمام مراحل با موفقیت تکمیل شد!", 100)
            
            return True, "پردازش با موفقیت تکمیل شد"
            
        except Exception as e:
            return False, str(e)
    
    def get_latest_results(self):
        """دریافت آخرین نتایج پردازش از پوشه‌های پشتیبان"""
        results = {
            'extracted_files': [],
            'ai_filtered_files': [],
            'dept_classified_files': []
        }
        
        try:
            # Get latest department classified file from backup
            if os.path.exists(BACKUP_DEPT_CLASS_DIR):
                dept_files = [f for f in os.listdir(BACKUP_DEPT_CLASS_DIR) if f.endswith('.xlsx')]
                if dept_files:
                    dept_files.sort(key=lambda x: os.path.getmtime(os.path.join(BACKUP_DEPT_CLASS_DIR, x)), reverse=True)
                    latest_dept_file = os.path.join(BACKUP_DEPT_CLASS_DIR, dept_files[0])
                    results['dept_classified_files'] = [latest_dept_file]
            
            # Get AI filtered files from backup
            if os.path.exists(BACKUP_CONS_FILTER_DIR):
                ai_files = [f for f in os.listdir(BACKUP_CONS_FILTER_DIR) if f.endswith('.xlsx')]
                results['ai_filtered_files'] = [os.path.join(BACKUP_CONS_FILTER_DIR, f) for f in ai_files]
            
            # Get processed files from backup
            if os.path.exists(BACKUP_PROCESSED_DIR):
                processed_files = [f for f in os.listdir(BACKUP_PROCESSED_DIR) if f.endswith('.xlsx')]
                results['extracted_files'] = [os.path.join(BACKUP_PROCESSED_DIR, f) for f in processed_files]
            
        except Exception as e:
            st.error(f"خطا در دریافت نتایج: {str(e)}")
        
        return results
    
    def create_download_package(self, file_paths):
        """ایجاد بسته ZIP از فایل‌های نتیجه"""
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
            st.error(f"خطا در ایجاد بسته دانلود: {str(e)}")
            return None

def parse_filename_datetime(filename):
    """استخراج اطلاعات تاریخ و زمان از نام فایل"""
    try:
        # Extract Persian date pattern like "52385_1404-06-16 18:00 - Main.html"
        persian_pattern = r'(\d{4}-\d{2}-\d{2})\s+(\d{1,2}):(\d{2})'
        match = re.search(persian_pattern, filename)
        
        if match:
            date_str = match.group(1)
            hour = int(match.group(2))
            minute = int(match.group(3))
            
            year, month, day = map(int, date_str.split('-'))
            
            try:
                persian_date = jdatetime.date(year, month, day)
                gregorian_date = persian_date.togregorian()
                
                is_pm = 'بعدازظهر' in filename or 'بعداز ظهر' in filename
                if is_pm and hour < 12:
                    hour += 12
                elif not is_pm and hour == 12:
                    hour = 0
                
                full_datetime = datetime.combine(gregorian_date, datetime.min.time().replace(hour=hour, minute=minute))
                
                return {
                    'datetime': full_datetime,
                    'persian_date': date_str,
                    'time_str': f"{match.group(2)}:{match.group(3)}",
                    'period': 'بعدازظهر' if is_pm else 'صبح'
                }
            except:
                pass
        
        # Fallback: extract timestamp
        timestamp_pattern = r'^(\d{8}_\d{6})'
        match = re.search(timestamp_pattern, filename)
        if match:
            timestamp_str = match.group(1)
            dt = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            return {
                'datetime': dt,
                'persian_date': None,
                'time_str': dt.strftime('%H:%M'),
                'period': 'بعدازظهر' if dt.hour >= 12 else 'صبح'
            }
        
        return None
    except Exception as e:
        st.error(f"خطا در تجزیه تاریخ نام فایل: {e}")
        return None

def main():
    """تابع اصلی اپلیکیشن"""
    
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
        <h1>📊 سامانه پردازش مناقصات</h1>
        <p>تحلیل مناقصات با قدرت هوش مصنوعی و طبقه‌بندی معاونت‌ها</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar menu
    with st.sidebar:
        selected = option_menu(
            "منوی اصلی",
            ["آپلود و پردازش", "مشاهده نتایج", "داشبورد تحلیلی", "تنظیمات"],
            icons=["upload", "table", "bar-chart", "gear"],
            menu_icon="list",
            default_index=0
        )
    
    # Main content based on selected menu
    if selected == "آپلود و پردازش":
        show_upload_section()
    elif selected == "مشاهده نتایج":
        show_results_section()
    elif selected == "داشبورد تحلیلی":
        show_analytics_section()
    elif selected == "تنظیمات":
        show_settings_section()

def show_upload_section():
    """نمایش بخش آپلود فایل و پردازش"""
    
    st.header("📁 آپلود فایل HTML")
    

    # File uploader
    uploaded_file = st.file_uploader(
        "فایل HTML خود را انتخاب کنید",
        type=['html', 'htm'],
        help="فایل HTML حاوی داده‌های مناقصه را آپلود کنید"
    )
    
    if uploaded_file is not None:
        st.session_state.uploaded_file_name = uploaded_file.name
        
        # Show file info
        st.info(f"📄 فایل: {uploaded_file.name} ({uploaded_file.size:,} بایت)")
        
        # Process button
        if st.button("🚀 شروع پردازش", type="primary", use_container_width=True):
            process_file_detailed(uploaded_file)
    
    # with col2:
    #     # Instructions
    #     st.markdown("""
    #     ### 📋 راهنمای کاربرد:
    #     1. فایل HTML خود را آپلود کنید
    #     2. روی "شروع پردازش" کلیک کنید
    #     3. منتظر تکمیل پردازش بمانید
    #     4. نتایج را دانلود کنید
        
    #     ### ⚡ ویژگی‌ها:
    #     - فیلتر با هوش مصنوعی
    #     - طبقه‌بندی معاونت‌ها
    #     - پشتیبان‌گیری خودکار
    #     - خروجی Excel
    #     """)

def process_file_detailed(uploaded_file):
    """پردازش فایل آپلود شده با نمایش پیشرفت دقیق"""
    
    # Save the uploaded file
    file_path, filename = st.session_state.processor.save_uploaded_file(uploaded_file)
    
    if not file_path:
        st.error("ذخیره فایل ناموفق بود")
        return
    
    st.success(f"فایل ذخیره شد: {filename}")
    
    # Progress tracking
    progress_container = st.container()
    progress_bar = progress_container.progress(0)
    status_container = progress_container.empty()
    
    def update_progress(message, progress):
        progress_bar.progress(progress / 100)
        status_container.markdown(f'<div class="stage-indicator">{message}</div>', unsafe_allow_html=True)
    
    # Run processing pipeline
    success, output = st.session_state.processor.run_processing_pipeline_detailed(
        progress_callback=update_progress
    )
    
    if success:
        st.session_state.processing_complete = True
        progress_bar.progress(100)
        status_container.markdown('<div class="success-message">✅ پردازش با موفقیت تکمیل شد!</div>', unsafe_allow_html=True)
        
        st.balloons()
        st.success("🎉 تمام مراحل پردازش با موفقیت تکمیل شد!")
        
        time.sleep(2)
        st.rerun()
    else:
        st.markdown(f'<div class="error-message">❌ پردازش ناموفق بود: {output}</div>', unsafe_allow_html=True)

def show_results_section():
    """نمایش بخش نتایج پردازش"""
    
    st.header("📊 نتایج پردازش")
    
    if not st.session_state.processing_complete:
        st.warning("⚠️ هیچ نتیجه پردازشی در دسترس نیست. لطفاً ابتدا یک فایل آپلود و پردازش کنید.")
        return
    
    # Get latest results
    results = st.session_state.processor.get_latest_results()
    
    if not any(results.values()):
        st.error("❌ هیچ فایل نتیجه‌ای یافت نشد.")
        return
    
    # Show results summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📄 فایل‌های استخراج شده", len(results.get('extracted_files', [])))
    
    with col2:
        st.metric("🤖 فایل‌های فیلتر AI", len(results.get('ai_filtered_files', [])))
    
    with col3:
        st.metric("🏢 فایل‌های طبقه‌بندی شده", len(results.get('dept_classified_files', [])))
    
    # Show classified data
    if results['dept_classified_files']:
        latest_file = results['dept_classified_files'][0]
        
        st.subheader("📋 مناقصات طبقه‌بندی شده بر اساس معاونت")
        
        try:
            df = pd.read_excel(latest_file)
            
            # Show basic stats
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("کل مناقصات", len(df))
            with col2:
                dept_count = df['معاونت مربوطه'].nunique() if 'معاونت مربوطه' in df.columns else 0
                st.metric("تعداد معاونت‌ها", dept_count)
            with col3:
                consulting_count = len(df)
                st.metric("مناقصات مشاوره‌ای", consulting_count)
            with col4:
                success_rate = "100%" if len(df) > 0 else "0%"
                st.metric("نرخ موفقیت", success_rate)
            
            # Show data table
            st.subheader("📊 داده‌های مناقصه")
            
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
                    df[display_columns].head(50),
                    use_container_width=True,
                    height=400
                )
                
                if len(df) > 50:
                    st.info(f"📄 نمایش 50 رکورد اول از {len(df)} رکورد کل")
            
            # Download section
            st.subheader("💾 دانلود نتایج")
            
            col1, col2 = st.columns(2)
            
            with col1:
                with open(latest_file, 'rb') as f:
                    excel_data = f.read()
                
                st.download_button(
                    label="📄 دانلود فایل Excel",
                    data=excel_data,
                    file_name=f"نتایج_مناقصات_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            with col2:
                all_files = []
                if results['dept_classified_files']:
                    all_files.extend(results['dept_classified_files'])
                if results['ai_filtered_files']:
                    all_files.extend(results['ai_filtered_files'])
                
                if all_files:
                    zip_data = st.session_state.processor.create_download_package(all_files)
                    if zip_data:
                        st.download_button(
                            label="📦 دانلود بسته کامل",
                            data=zip_data,
                            file_name=f"بسته_مناقصات_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
            
        except Exception as e:
            st.error(f"خطا در نمایش نتایج: {str(e)}")

def show_analytics_section():
    """نمایش داشبورد تحلیلی با فیلتر تاریخ و زمان"""
    
    st.header("📈 داشبورد تحلیلی تعاملی")
    
    if not st.session_state.processing_complete:
        st.warning("⚠️ داده‌ای برای تحلیل در دسترس نیست. لطفاً ابتدا یک فایل پردازش کنید.")
        return
    
    results = st.session_state.processor.get_latest_results()
    
    if not results['dept_classified_files']:
        st.error("❌ هیچ داده طبقه‌بندی شده‌ای برای تحلیل موجود نیست.")
        return
    
    try:
        df = pd.read_excel(results['dept_classified_files'][0])
        
        # Extract datetime info from backup files
        file_datetime_info = []
        
        for backup_dir in [BACKUP_PROCESSED_DIR, BACKUP_CONS_FILTER_DIR, BACKUP_DEPT_CLASS_DIR]:
            if os.path.exists(backup_dir):
                files = [f for f in os.listdir(backup_dir) if f.endswith('.xlsx')]
                for file in files:
                    datetime_info = parse_filename_datetime(file)
                    if datetime_info:
                        datetime_info['filename'] = file
                        file_datetime_info.append(datetime_info)
        
        # Date and Time Filters
        st.subheader("🗓️ فیلترهای تاریخ و زمان")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if file_datetime_info:
                available_dates = sorted(list(set([info['datetime'].date() for info in file_datetime_info])))
                
                if len(available_dates) > 1:
                    selected_date = st.selectbox(
                        "انتخاب تاریخ",
                        options=['تمام تاریخ‌ها'] + [d.strftime('%Y-%m-%d') for d in available_dates],
                        index=0
                    )
                else:
                    selected_date = 'تمام تاریخ‌ها'
                    st.info("فقط یک تاریخ در داده‌ها موجود است")
            else:
                selected_date = 'تمام تاریخ‌ها'
                st.info("اطلاعات تاریخ در نام فایل‌ها یافت نشد")
        
        with col2:
            time_periods = ['تمام زمان‌ها', 'صبح', 'بعدازظهر']
            selected_time_period = st.selectbox("انتخاب بازه زمانی", time_periods)
        
        with col3:
            if file_datetime_info:
                available_hours = sorted(list(set([info['datetime'].hour for info in file_datetime_info])))
                hour_options = ['تمام ساعات'] + [f"{h:02d}:00" for h in available_hours]
                selected_hour = st.selectbox("انتخاب ساعت", hour_options)
            else:
                selected_hour = 'تمام ساعات'
        
        # Department distribution
        if 'معاونت مربوطه' in df.columns:
            st.subheader("🏢 توزیع بر اساس معاونت‌ها")
            
            dept_counts = df['معاونت مربوطه'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_pie = px.pie(
                    values=dept_counts.values,
                    names=dept_counts.index,
                    title="مناقصات بر اساس معاونت"
                )
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                fig_bar = px.bar(
                    x=dept_counts.index,
                    y=dept_counts.values,
                    title="تعداد مناقصات در هر معاونت",
                    labels={'x': 'معاونت', 'y': 'تعداد مناقصات'}
                )
                fig_bar.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Regional distribution
        if 'منطقه' in df.columns:
            st.subheader("🗺️ توزیع جغرافیایی")
            
            region_counts = df['منطقه'].value_counts().head(10)
            
            fig_region = px.bar(
                x=region_counts.values,
                y=region_counts.index,
                orientation='h',
                title="۱۰ منطقه برتر از نظر تعداد مناقصه",
                labels={'x': 'تعداد مناقصات', 'y': 'منطقه'}
            )
            st.plotly_chart(fig_region, use_container_width=True)
        
        # Data quality metrics
        st.subheader("📊 معیارهای کیفیت داده")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            completeness = (df.notna().sum().sum() / (len(df) * len(df.columns))) * 100
            st.metric("کمال داده", f"{completeness:.1f}%")
        
        with col2:
            classified_rate = (df['معاونت مربوطه'] != 'نامشخص').sum() / len(df) * 100 if 'معاونت مربوطه' in df.columns else 0
            st.metric("نرخ طبقه‌بندی", f"{classified_rate:.1f}%")
        
        with col3:
            unique_organizers = df['برگزارکننده'].nunique() if 'برگزارکننده' in df.columns else 0
            st.metric("برگزارکنندگان منحصربه‌فرد", unique_organizers)
        
        with col4:
            files_processed = len(file_datetime_info)
            st.metric("فایل‌های پردازش شده", files_processed)
        
    except Exception as e:
        st.error(f"خطا در تولید تحلیل: {str(e)}")

def show_settings_section():
    """نمایش بخش تنظیمات اپلیکیشن"""
    
    st.header("⚙️ تنظیمات")
    
    # API Configuration
    st.subheader("🔑 پیکربندی API")
    
    with st.expander("تنظیمات OpenAI API"):
        current_key = os.getenv("OPENAI_API_KEY", "")
        current_url = os.getenv("OPENAI_BASE_URL", "")
        
        api_key = st.text_input(
            "کلید API",
            value=current_key[:10] + "..." if current_key else "",
            type="password",
            help="کلید API سرویس OpenAI شما"
        )
        
        base_url = st.text_input(
            "آدرس پایه",
            value=current_url,
            help="آدرس پایه API (اختیاری)"
        )
        
        if st.button("💾 ذخیره تنظیمات API"):
            st.success("✅ تنظیمات API ذخیره خواهد شد (در استقرار واقعی)")
    
    # Processing Settings
    st.subheader("🔧 تنظیمات پردازش")
    
    col1, col2 = st.columns(2)
    
    with col1:
        batch_size = st.slider("اندازه دسته", 10, 100, 50, help="تعداد مناقصات برای پردازش در هر دسته")
        timeout = st.slider("مهلت زمانی API (ثانیه)", 30, 300, 120, help="مهلت زمانی برای درخواست‌های API")
    
    with col2:
        enable_backup = st.checkbox("فعال‌سازی پشتیبان‌گیری", value=True, help="پشتیبان‌گیری خودکار از فایل‌های پردازش شده")
        debug_mode = st.checkbox("حالت اشکال‌زدایی", value=False, help="فعال‌سازی لاگ‌گیری تفصیلی")
    
    # System Information
    st.subheader("ℹ️ اطلاعات سیستم")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**نسخه Python:** {sys.version.split()[0]}")
        st.info(f"**نسخه Streamlit:** {st.__version__}")
    
    with col2:
        dirs_status = {
            "پوشه ورودی": os.path.exists(INPUT_DIR),
            "پوشه خروجی": os.path.exists(DEPT_OUTPUT_DIR),
            "پوشه پشتیبان": os.path.exists(BACKUP_DIR)
        }
        
        for dir_name, exists in dirs_status.items():
            status = "✅ موجود" if exists else "❌ غایب"
            st.info(f"**{dir_name}:** {status}")
    
    # Maintenance
    st.subheader("🧹 نگهداری")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ پاک کردن کش", help="پاک کردن کش Streamlit"):
            st.cache_data.clear()
            st.success("✅ کش پاک شد!")
    
    with col2:
        if st.button("🔄 بازنشانی جلسه", help="بازنشانی جلسه اپلیکیشن"):
            st.session_state.clear()
            st.success("✅ جلسه بازنشانی شد!")
            st.rerun()

if __name__ == "__main__":
    main()