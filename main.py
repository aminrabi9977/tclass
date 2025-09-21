# """
# Main entry point for the tender extraction system.
# """
# import os
# import sys
# import argparse
# import logging
# from datetime import datetime

# # Add src directory to path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from src.extraction.html_parser import TenderHTMLParser
# from src.extraction.excel_manager import ExcelManager
# from src.utils.config import INPUT_DIR, PROCESSED_DIR, OUTPUT_DIR, LOG_LEVEL, LOG_FILE

# # Configure logging
# logging.basicConfig(
#     level=getattr(logging, LOG_LEVEL),
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler()
#     ]
# )

# logger = logging.getLogger(__name__)

# def test_extraction(html_file_path, output_dir=None):
#     """
#     Test HTML extraction and saving to Excel.
    
#     Args:
#         html_file_path: Path to the HTML file to test
#         output_dir: Directory to save the Excel file (default: PROCESSED_DIR)
#     """
#     if not os.path.exists(html_file_path):
#         logger.error(f"File not found: {html_file_path}")
#         return
    
#     # Default output directory is processed directory
#     if output_dir is None:
#         output_dir = PROCESSED_DIR
    
#     # Make sure output directory exists
#     os.makedirs(output_dir, exist_ok=True)
    
#     logger.info(f"Testing extraction from: {html_file_path}")
#     logger.info(f"Excel will be saved to: {output_dir}")
    
#     # Initialize the parser and Excel manager
#     parser = TenderHTMLParser()
#     excel_mgr = ExcelManager(output_dir)
    
#     try:
#         # Parse the HTML file
#         tenders = parser.parse_file(html_file_path)
        
#         if not tenders:
#             logger.warning("No tender information found in the file.")
#             return
        
#         logger.info(f"Found {len(tenders)} tenders in the file.")
        
#         # Print all extracted data for each tender
#         for i, tender in enumerate(tenders, 1):
#             logger.info(f"\nTender #{i}:")
#             for field in parser.fields:
#                 value = tender.get(field, "")
#                 # Truncate long values for display
#                 if isinstance(value, str) and len(value) > 100:
#                     display_value = value[:97] + "..."
#                 else:
#                     display_value = value
#                 logger.info(f"  {field}: {display_value}")
        
#         # Save to Excel
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         basename = os.path.basename(html_file_path).split('.')[0]
#         excel_filename = f"test_{basename}_{timestamp}.xlsx"
        
#         excel_path = excel_mgr.save_to_excel(tenders, excel_filename)
        
#         logger.info(f"\nSaved tender information to Excel: {excel_path}")
#         logger.info(f"Total tenders saved: {len(tenders)}")
        
#         return excel_path
    
#     except Exception as e:
#         logger.error(f"Error during extraction or Excel saving: {str(e)}")
#         import traceback
#         logger.error(traceback.format_exc())
#         return None

# def process_html_files(input_dir=INPUT_DIR, process_all=False):
#     """
#     Process HTML files in the input directory.
    
#     Args:
#         input_dir: Directory containing HTML files
#         process_all: If True, process all files; otherwise, process only new files
        
#     Returns:
#         List of paths to generated Excel files
#     """
#     logger.info(f"Processing HTML files from {input_dir}")
    
#     # Get list of HTML files
#     html_files = [f for f in os.listdir(input_dir) if f.endswith('.html')]
    
#     if not html_files:
#         logger.warning(f"No HTML files found in {input_dir}")
#         return []
    
#     logger.info(f"Found {len(html_files)} HTML files")
    
#     # Initialize parser and Excel manager
#     parser = TenderHTMLParser()
#     excel_mgr = ExcelManager(PROCESSED_DIR)
    
#     excel_files = []
    
#     for html_file in html_files:
#         file_path = os.path.join(input_dir, html_file)
        
#         try:
#             # Parse HTML file
#             logger.info(f"Parsing {html_file}")
#             tenders = parser.parse_file(file_path)
            
#             if not tenders:
#                 logger.warning(f"No tender information found in {html_file}")
#                 continue
            
#             # Save to Excel
#             excel_name = f"{os.path.splitext(html_file)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
#             excel_path = excel_mgr.save_to_excel(tenders, excel_name)
            
#             logger.info(f"Saved tender information to {excel_path}")
#             excel_files.append(excel_path)
            
#         except Exception as e:
#             logger.error(f"Error processing {html_file}: {str(e)}")
    
#     return excel_files

# def main():
#     """Main entry point."""
#     parser = argparse.ArgumentParser(description='Tender Extraction System')
#     parser.add_argument('--input-dir', help='Directory containing HTML files', default=INPUT_DIR)
#     parser.add_argument('--all', action='store_true', help='Process all HTML files, not just new ones')
#     parser.add_argument('--test', help='Test extraction on a single HTML file')
#     parser.add_argument('--output-dir', help='Directory to save output files for test mode')
#     args = parser.parse_args()
    
#     try:
#         # If test mode is enabled, run the test function
#         if args.test:
#             output_dir = args.output_dir or PROCESSED_DIR
#             excel_path = test_extraction(args.test, output_dir)
            
#             if excel_path:
#                 logger.info(f"Test completed successfully. Excel file saved to: {excel_path}")
#                 logger.info("Please open the Excel file to verify that the data was extracted correctly.")
#             else:
#                 logger.error("Test failed. See error messages above.")
#                 return 1
            
#         else:
#             # Regular processing mode
#             excel_files = process_html_files(args.input_dir, args.all)
            
#             if excel_files:
#                 logger.info(f"Successfully processed {len(excel_files)} HTML files")
                
#                 # Placeholder for AI processing and email sending
#                 # This will be implemented in future steps
#                 logger.info("AI processing and email sending not yet implemented")
                
#             else:
#                 logger.info("No files were processed")
            
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")
#         return 1
    
#     return 0

# if __name__ == "__main__":
#     sys.exit(main())

# -----------------------------------------------------------------------------------------------

"""
Main orchestrator for the complete tender extraction and processing pipeline.
Handles HTML extraction, AI filtering, and department classification automatically.
"""
import os
import sys
import argparse
import logging
import shutil
from datetime import datetime
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.extraction.html_parser import TenderHTMLParser
from src.extraction.excel_manager import ExcelManager
from src.utils.config import (
    INPUT_DIR, PROCESSED_DIR, AI_OUTPUT_DIR, DEPT_OUTPUT_DIR,
    BACKUP_PROCESSED_DIR, BACKUP_CONS_FILTER_DIR, BACKUP_DEPT_CLASS_DIR,
    LOG_LEVEL, LOG_FILE
)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging with UTF-8 encoding to handle Persian text and emojis
import logging.handlers

# Create logs directory if it doesn't exist
log_dir = os.path.dirname(LOG_FILE)
os.makedirs(log_dir, exist_ok=True)

# Configure logging with proper encoding
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.handlers.RotatingFileHandler(
            LOG_FILE, 
            maxBytes=10*1024*1024,  # 10MB max file size
            backupCount=5,
            encoding='utf-8'
        ),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def process_html_files():
    """
    Process all HTML files in the input directory.
    
    Returns:
        List of paths to generated Excel files
    """
    logger.info("="*60)
    logger.info("STEP 1: HTML EXTRACTION")
    logger.info("="*60)
    
    if not os.path.exists(INPUT_DIR):
        logger.error(f"Input directory not found: {INPUT_DIR}")
        return []
    
    # Get list of HTML files
    html_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.html')]
    
    if not html_files:
        logger.warning(f"No HTML files found in {INPUT_DIR}")
        return []
    
    logger.info(f"Found {len(html_files)} HTML files")
    
    # Initialize parser and Excel manager
    parser = TenderHTMLParser()
    excel_mgr = ExcelManager(PROCESSED_DIR)
    
    excel_files = []
    processed_files = []
    
    for html_file in html_files:
        file_path = os.path.join(INPUT_DIR, html_file)
        
        try:
            # Parse HTML file
            logger.info(f"📄 Processing {html_file}")
            tenders = parser.parse_file(file_path)
            
            if not tenders:
                logger.warning(f"No tender information found in {html_file}")
                continue
            
            # Save to Excel with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            excel_name = f"{os.path.splitext(html_file)[0]}_{timestamp}.xlsx"
            excel_path = excel_mgr.save_to_excel(tenders, excel_name)
            
            # Save backup copy
            backup_path = save_to_backup(excel_path, BACKUP_PROCESSED_DIR, "processed")
            
            logger.info(f"✅ Saved {len(tenders)} tenders to {excel_path}")
            logger.info(f"💾 Backup saved to {backup_path}")
            
            excel_files.append(excel_path)
            processed_files.append(html_file)
            
        except Exception as e:
            logger.error(f"❌ Error processing {html_file}: {str(e)}")
    
    # Delete successfully processed HTML files
    for html_file in processed_files:
        try:
            html_path = os.path.join(INPUT_DIR, html_file)
            os.remove(html_path)
            logger.info(f"🗑️ Deleted processed HTML file: {html_file}")
        except Exception as e:
            logger.error(f"Error deleting {html_file}: {e}")
    
    logger.info(f"📊 Successfully processed {len(excel_files)} HTML files")
    return excel_files

def save_to_backup(source_path, backup_dir, backup_type):
    """
    Save file to backup directory with timestamp.
    
    Args:
        source_path: Source file path
        backup_dir: Backup directory path
        backup_type: Type of backup (for filename prefix)
        
    Returns:
        Path to backup file
    """
    try:
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        basename = os.path.basename(source_path)
        backup_filename = f"{backup_type}_{timestamp}_{basename}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        shutil.copy2(source_path, backup_path)
        return backup_path
        
    except Exception as e:
        logger.error(f"Error backing up file: {e}")
        raise

def run_ai_processing():
    """
    Run AI processing on the latest processed file.
    
    Returns:
        Path to the filtered file or None if failed
    """
    logger.info("="*60)
    logger.info("STEP 2: AI FILTERING")
    logger.info("="*60)
    
    try:
        # Import the processing function
        from process_tenders import process_tenders_auto
        
        # Run AI processing
        result_path = process_tenders_auto()
        
        if result_path:
            logger.info(f"AI processing completed: {result_path}")
            
            # Look for full_filtered files in AI_OUTPUT_DIR
            full_filtered_files = []
            if os.path.exists(AI_OUTPUT_DIR):
                full_filtered_files = [
                    os.path.join(AI_OUTPUT_DIR, f)
                    for f in os.listdir(AI_OUTPUT_DIR)
                    if f.startswith("full_filtered_") and f.endswith('.xlsx')
                ]
            
            if full_filtered_files:
                # Get the most recent full_filtered file
                full_filtered_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                latest_full_filtered = full_filtered_files[0]
                
                logger.info(f"Found full filtered file: {latest_full_filtered}")
                
                # Save to backup
                save_to_backup(latest_full_filtered, BACKUP_CONS_FILTER_DIR, "cons_filtered")
                
                # Delete processed files after successful AI processing
                cleanup_processed_files()
                
                return latest_full_filtered
            else:
                logger.error("No full_filtered file found in AI output directory")
                # List what files are actually there
                if os.path.exists(AI_OUTPUT_DIR):
                    files = os.listdir(AI_OUTPUT_DIR)
                    logger.info(f"Files in {AI_OUTPUT_DIR}: {files}")
                return None
        else:
            logger.error("AI processing function returned None")
            return None
            
    except Exception as e:
        logger.error(f"Error in AI processing: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

def run_department_classification():
    """
    Run department classification on the latest AI filtered file.
    
    Returns:
        Path to the classified file or None if failed
    """
    logger.info("="*60)
    logger.info("STEP 3: DEPARTMENT CLASSIFICATION")
    logger.info("="*60)
    
    try:
        # Import the classification function
        from classify_departments import classify_departments_auto
        
        # Run department classification
        result_path = classify_departments_auto()
        
        if result_path:
            logger.info(f"✅ Department classification completed: {result_path}")
            
            # Delete AI filtered files after successful classification
            cleanup_ai_filtered_files()
            
            return result_path
        else:
            logger.error("❌ Department classification failed")
            return None
            
    except Exception as e:
        logger.error(f"Error in department classification: {e}")
        return None

def cleanup_processed_files():
    """Clean up processed files after successful AI filtering."""
    try:
        if os.path.exists(PROCESSED_DIR):
            for file in os.listdir(PROCESSED_DIR):
                if file.endswith('.xlsx'):
                    file_path = os.path.join(PROCESSED_DIR, file)
                    os.remove(file_path)
                    logger.info(f"🗑️ Deleted processed file: {file}")
    except Exception as e:
        logger.error(f"Error cleaning up processed files: {e}")

def cleanup_ai_filtered_files():
    """Clean up AI filtered files after successful department classification."""
    try:
        if os.path.exists(AI_OUTPUT_DIR):
            for file in os.listdir(AI_OUTPUT_DIR):
                if file.endswith('.xlsx'):
                    file_path = os.path.join(AI_OUTPUT_DIR, file)
                    os.remove(file_path)
                    logger.info(f"🗑️ Deleted AI filtered file: {file}")
    except Exception as e:
        logger.error(f"Error cleaning up AI filtered files: {e}")

def test_extraction(html_file_path, output_dir=None):
    """
    Test HTML extraction and saving to Excel (original functionality).
    
    Args:
        html_file_path: Path to the HTML file to test
        output_dir: Directory to save the Excel file (default: PROCESSED_DIR)
    """
    if not os.path.exists(html_file_path):
        logger.error(f"File not found: {html_file_path}")
        return
    
    # Default output directory is processed directory
    if output_dir is None:
        output_dir = PROCESSED_DIR
    
    # Make sure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info(f"Testing extraction from: {html_file_path}")
    logger.info(f"Excel will be saved to: {output_dir}")
    
    # Initialize the parser and Excel manager
    parser = TenderHTMLParser()
    excel_mgr = ExcelManager(output_dir)
    
    try:
        # Parse the HTML file
        tenders = parser.parse_file(html_file_path)
        
        if not tenders:
            logger.warning("No tender information found in the file.")
            return
        
        logger.info(f"Found {len(tenders)} tenders in the file.")
        
        # Print all extracted data for each tender
        for i, tender in enumerate(tenders, 1):
            logger.info(f"\nTender #{i}:")
            for field in parser.fields:
                value = tender.get(field, "")
                # Truncate long values for display
                if isinstance(value, str) and len(value) > 100:
                    display_value = value[:97] + "..."
                else:
                    display_value = value
                logger.info(f"  {field}: {display_value}")
        
        # Save to Excel
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        basename = os.path.basename(html_file_path).split('.')[0]
        excel_filename = f"test_{basename}_{timestamp}.xlsx"
        
        excel_path = excel_mgr.save_to_excel(tenders, excel_filename)
        
        logger.info(f"\nSaved tender information to Excel: {excel_path}")
        logger.info(f"Total tenders saved: {len(tenders)}")
        
        return excel_path
    
    except Exception as e:
        logger.error(f"Error during extraction or Excel saving: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Complete Tender Processing System')
    parser.add_argument('--test', help='Test extraction on a single HTML file')
    parser.add_argument('--output-dir', help='Directory to save output files for test mode')
    parser.add_argument('--skip-ai', action='store_true', help='Skip AI processing step')
    parser.add_argument('--skip-dept', action='store_true', help='Skip department classification step')
    parser.add_argument('--html-only', action='store_true', help='Only process HTML files (skip AI and department steps)')
    args = parser.parse_args()
    
    try:
        # Check for required environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key and not args.html_only:
            logger.warning("OPENAI_API_KEY not found in environment variables.")
            logger.warning("Only HTML extraction will be performed.")
            args.html_only = True
        
        # Test mode - single file extraction
        if args.test:
            output_dir = args.output_dir or PROCESSED_DIR
            excel_path = test_extraction(args.test, output_dir)
            
            if excel_path:
                logger.info(f"✅ Test completed successfully. Excel file saved to: {excel_path}")
                logger.info("Please open the Excel file to verify that the data was extracted correctly.")
            else:
                logger.error("❌ Test failed. See error messages above.")
                return 1
            
            return 0
        
        # Full pipeline execution
        logger.info("🚀 STARTING COMPLETE TENDER PROCESSING PIPELINE")
        logger.info("="*60)
        
        # Step 1: Process HTML files
        excel_files = process_html_files()
        
        if not excel_files:
            logger.warning("No HTML files were processed. Pipeline stopped.")
            return 0
        
        if args.html_only:
            logger.info("✅ HTML processing completed. Stopping here (--html-only flag)")
            return 0
        
        # Step 2: AI Processing
        if not args.skip_ai:
            ai_result = run_ai_processing()
            if not ai_result:
                logger.error("AI processing failed. Pipeline stopped.")
                return 1
        else:
            logger.info("⏭️ Skipping AI processing (--skip-ai flag)")
        
        # Step 3: Department Classification
        if not args.skip_dept and not args.skip_ai:
            dept_result = run_department_classification()
            if not dept_result:
                logger.error("Department classification failed. Pipeline stopped.")
                return 1
        else:
            if args.skip_dept:
                logger.info("⏭️ Skipping department classification (--skip-dept flag)")
            else:
                logger.info("⏭️ Skipping department classification (AI was skipped)")
        
        # Pipeline completed successfully
        logger.info("="*60)
        logger.info("🎉 COMPLETE PIPELINE EXECUTED SUCCESSFULLY!")
        logger.info("="*60)
        logger.info("📂 Check the following directories for outputs:")
        logger.info(f"   📊 AI Filtered: {AI_OUTPUT_DIR}")
        logger.info(f"   🏢 Department Classified: {DEPT_OUTPUT_DIR}")
        logger.info(f"   💾 Backups: data/backup/")
        logger.info("="*60)
        
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred in main pipeline: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())