# """
# Test script for the extraction functionality.
# """
# import os
# import sys
# import logging
# from datetime import datetime

# # Configure basic logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[logging.StreamHandler()]
# )
# logger = logging.getLogger(__name__)

# # Import our modules
# from src.data_extraction.html_parser import TenderHTMLParser
# from src.data_extraction.excel_manager import ExcelManager

# def test_extraction(html_file_path, output_dir=None):
#     """
#     Test HTML extraction and saving to Excel.
    
#     Args:
#         html_file_path: Path to the HTML file to test
#         output_dir: Directory to save the Excel file (default: current directory)
#     """
#     if not os.path.exists(html_file_path):
#         logger.error(f"File not found: {html_file_path}")
#         return
    
#     # Default output directory is current directory
#     if output_dir is None:
#         output_dir = os.getcwd()
    
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

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         logger.error("Please provide the path to an HTML file.")
#         logger.info("Usage: python test_extraction.py path/to/html/file.html [output_directory]")
#         sys.exit(1)
    
#     html_file_path = sys.argv[1]
    
#     # Optional output directory
#     output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
#     excel_path = test_extraction(html_file_path, output_dir)
    
#     if excel_path:
#         logger.info(f"\nTest completed successfully. Excel file saved to: {excel_path}")
#         logger.info("Please open the Excel file to verify that the data was extracted correctly.")
#     else:
#         logger.error("Test failed. See error messages above.")

# ----------------------------------------------------------------------------------

"""
Test script for the extraction functionality.
"""
import os
import sys
import logging
from datetime import datetime

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Import our modules
from src.data_extraction.html_parser import TenderHTMLParser
from src.data_extraction.excel_manager import ExcelManager

def test_extraction(html_file_path, output_dir=None):
    """
    Test HTML extraction and saving to Excel.
    
    Args:
        html_file_path: Path to the HTML file to test
        output_dir: Directory to save the Excel file (default: current directory)
    """
    if not os.path.exists(html_file_path):
        logger.error(f"File not found: {html_file_path}")
        return
    
    # Default output directory is current directory
    if output_dir is None:
        output_dir = os.getcwd()
    
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
            
            # Print raw HTML for the region field to debug
            region_value = tender.get("منطقه", "")
            logger.info(f"  DEBUG - منطقه field: '{region_value}'")
        
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

def debug_html_structure(html_file_path):
    """
    Debug the HTML structure to find where the region field is located.
    """
    from bs4 import BeautifulSoup
    
    if not os.path.exists(html_file_path):
        logger.error(f"File not found: {html_file_path}")
        return
    
    # Read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all tender notices
    tender_tables = soup.find_all('table', class_='rp-notice-content')
    
    for i, table in enumerate(tender_tables, 1):
        logger.info(f"\nAnalyzing Tender Table #{i}:")
        
        # Find all rows
        rows = table.find_all('tr')
        
        for j, row in enumerate(rows, 1):
            # Find cells with "منطقه" label
            cells = row.find_all('td')
            
            for k, cell in enumerate(cells, 1):
                b_tag = cell.find('b')
                if b_tag and "منطقه" in b_tag.text:
                    logger.info(f"  Found 'منطقه' in Row {j}, Cell {k}:")
                    logger.info(f"  - B tag text: '{b_tag.text}'")
                    logger.info(f"  - Cell full text: '{cell.get_text(strip=True)}'")
                    logger.info(f"  - Cell HTML: {cell}")
                    
                    # Try to extract value
                    cell_copy = BeautifulSoup(str(cell), 'html.parser')
                    b_element = cell_copy.find('b')
                    if b_element:
                        b_element.extract()
                    value = cell_copy.get_text(strip=True)
                    logger.info(f"  - Extracted value: '{value}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Please provide the path to an HTML file.")
        logger.info("Usage: python test_extraction.py path/to/html/file.html [output_directory]")
        sys.exit(1)
    
    html_file_path = sys.argv[1]
    
    # Optional output directory
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Debug HTML structure to find the region field
    logger.info("Debugging HTML structure to locate the region field...")
    debug_html_structure(html_file_path)
    
    # Run the regular extraction test
    logger.info("\nRunning regular extraction test...")
    excel_path = test_extraction(html_file_path, output_dir)
    
    if excel_path:
        logger.info(f"\nTest completed successfully. Excel file saved to: {excel_path}")
        logger.info("Please open the Excel file to verify that the data was extracted correctly.")
    else:
        logger.error("Test failed. See error messages above.")