"""
Main entry point for the tender extraction system.
"""
import os
import sys
import argparse
import logging
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.extraction.html_parser import TenderHTMLParser
from src.extraction.excel_manager import ExcelManager
from src.utils.config import INPUT_DIR, PROCESSED_DIR, OUTPUT_DIR, LOG_LEVEL, LOG_FILE

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_extraction(html_file_path, output_dir=None):
    """
    Test HTML extraction and saving to Excel.
    
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

def process_html_files(input_dir=INPUT_DIR, process_all=False):
    """
    Process HTML files in the input directory.
    
    Args:
        input_dir: Directory containing HTML files
        process_all: If True, process all files; otherwise, process only new files
        
    Returns:
        List of paths to generated Excel files
    """
    logger.info(f"Processing HTML files from {input_dir}")
    
    # Get list of HTML files
    html_files = [f for f in os.listdir(input_dir) if f.endswith('.html')]
    
    if not html_files:
        logger.warning(f"No HTML files found in {input_dir}")
        return []
    
    logger.info(f"Found {len(html_files)} HTML files")
    
    # Initialize parser and Excel manager
    parser = TenderHTMLParser()
    excel_mgr = ExcelManager(PROCESSED_DIR)
    
    excel_files = []
    
    for html_file in html_files:
        file_path = os.path.join(input_dir, html_file)
        
        try:
            # Parse HTML file
            logger.info(f"Parsing {html_file}")
            tenders = parser.parse_file(file_path)
            
            if not tenders:
                logger.warning(f"No tender information found in {html_file}")
                continue
            
            # Save to Excel
            excel_name = f"{os.path.splitext(html_file)[0]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            excel_path = excel_mgr.save_to_excel(tenders, excel_name)
            
            logger.info(f"Saved tender information to {excel_path}")
            excel_files.append(excel_path)
            
        except Exception as e:
            logger.error(f"Error processing {html_file}: {str(e)}")
    
    return excel_files

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Tender Extraction System')
    parser.add_argument('--input-dir', help='Directory containing HTML files', default=INPUT_DIR)
    parser.add_argument('--all', action='store_true', help='Process all HTML files, not just new ones')
    parser.add_argument('--test', help='Test extraction on a single HTML file')
    parser.add_argument('--output-dir', help='Directory to save output files for test mode')
    args = parser.parse_args()
    
    try:
        # If test mode is enabled, run the test function
        if args.test:
            output_dir = args.output_dir or PROCESSED_DIR
            excel_path = test_extraction(args.test, output_dir)
            
            if excel_path:
                logger.info(f"Test completed successfully. Excel file saved to: {excel_path}")
                logger.info("Please open the Excel file to verify that the data was extracted correctly.")
            else:
                logger.error("Test failed. See error messages above.")
                return 1
            
        else:
            # Regular processing mode
            excel_files = process_html_files(args.input_dir, args.all)
            
            if excel_files:
                logger.info(f"Successfully processed {len(excel_files)} HTML files")
                
                # Placeholder for AI processing and email sending
                # This will be implemented in future steps
                logger.info("AI processing and email sending not yet implemented")
                
            else:
                logger.info("No files were processed")
            
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())