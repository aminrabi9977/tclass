"""
Test script for the department classifier.
"""
import os
import sys
import argparse
import logging
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.processing.department_classifier import DepartmentClassifier
from src.utils.config import AI_OUTPUT_DIR, DEPT_OUTPUT_DIR, LOG_LEVEL, LOG_FILE

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def test_department_classifier(input_path, api_key, base_url=None):
    """
    Test the department classifier with a sample Excel file.
    
    Args:
        input_path: Path to the input Excel file
        api_key: OpenAI API key
        base_url: Base URL for the OpenAI API (optional)
    """
    try:
        logger.info(f"Testing department classifier with {input_path}")
        
        # Initialize department classifier
        classifier = DepartmentClassifier(api_key=api_key, base_url=base_url)
        
        # Set output paths
        output_dir = DEPT_OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        
        basename = os.path.basename(input_path)
        output_path = os.path.join(output_dir, f"test_dept_classified_{basename}")
        
        # Process the Excel file
        result_path = classifier.process_excel(
            input_path=input_path,
            full_data_path=input_path,
            output_path=output_path
        )
        
        logger.info(f"Test completed successfully. Results saved to: {result_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Test the department classifier')
    parser.add_argument('--input', help='Path to the input Excel file')
    parser.add_argument('--api-key', help='OpenAI API key')
    parser.add_argument('--base-url', help='Base URL for the OpenAI API (optional)')
    args = parser.parse_args()
    
    # Check for input file
    input_path = args.input
    if not input_path:
        logger.error("No input file specified. Use --input to specify the Excel file.")
        return 1
    
    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return 1
    
    # Check for API key
    api_key = args.api_key
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("No API key provided. Use --api-key or set OPENAI_API_KEY environment variable.")
            return 1
    
    # Run the test
    success = test_department_classifier(input_path, api_key, args.base_url)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

# --------------------------------------------------------------
