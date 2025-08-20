"""
Script to classify tender data by department.
"""
import os
import sys
import argparse
import logging
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.processing.department_classifier import DepartmentClassifier
from src.utils.config import AI_OUTPUT_DIR, OUTPUT_DIR, LOG_LEVEL, LOG_FILE

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

def prepare_data_for_classification(input_path, output_path=None):
    """
    Prepare data for department classification by extracting required columns.
    
    Args:
        input_path: Path to the input Excel file
        output_path: Path to save the extracted data
        
    Returns:
        Path to the extracted data
    """
    try:
        logger.info(f"Preparing data for classification from {input_path}")
        
        # Read the Excel file
        df = pd.read_excel(input_path)
        
        # Extract required columns for classification
        required_columns = ["شماره مناقصه در هزاره", "عنوان", "شرح آگهی"]
        
        # Check if all required columns exist
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logger.error(f"Missing columns in the Excel file: {missing_columns}")
            raise ValueError(f"Missing columns in the Excel file: {missing_columns}")
        
        # Create a new DataFrame with only the required columns
        extracted_df = df[required_columns]
        
        # Generate output path if not provided
        if not output_path:
            dirname = os.path.dirname(input_path) if os.path.dirname(input_path) else "."
            basename = os.path.basename(input_path)
            output_path = os.path.join(dirname, f"dept_extract_{basename}")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to Excel
        extracted_df.to_excel(output_path, index=False)
        
        logger.info(f"Data for classification saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error preparing data for classification: {e}")
        raise

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Classify tender data by department')
    parser.add_argument('--input', help='Path to the input Excel file (full filtered data)')
    parser.add_argument('--api-key', help='OpenAI API key')
    parser.add_argument('--base-url', help='Base URL for the OpenAI API (optional)')
    parser.add_argument('--output-dir', help='Directory to save output files', default=OUTPUT_DIR)
    args = parser.parse_args()
    
    try:
        # Find the most recent full filtered file in AI_OUTPUT_DIR if input not specified
        input_path = args.input
        if not input_path:
            logger.info(f"No input file specified, looking for the latest full filtered Excel file in {AI_OUTPUT_DIR}")
            full_filtered_files = [
                os.path.join(AI_OUTPUT_DIR, f) 
                for f in os.listdir(AI_OUTPUT_DIR) 
                if f.startswith("full_filtered_") and f.endswith('.xlsx')
            ]
            
            if not full_filtered_files:
                logger.error(f"No full filtered Excel files found in {AI_OUTPUT_DIR}")
                return 1
            
            # Sort by modification time (latest first)
            full_filtered_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            input_path = full_filtered_files[0]
            logger.info(f"Using latest full filtered Excel file: {input_path}")
        
        # Check if the input file exists
        if not os.path.exists(input_path):
            logger.error(f"Input file not found: {input_path}")
            return 1
        
        # Create subdirectory for department classified output
        dept_output_dir = os.path.join(args.output_dir, "dept_classified")
        os.makedirs(dept_output_dir, exist_ok=True)
        
        # Prepare timestamp for output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare data for department classification
        extracted_data_path = os.path.join(dept_output_dir, f"dept_extract_{timestamp}.xlsx")
        extracted_path = prepare_data_for_classification(input_path, extracted_data_path)
        
        # Check if API key is provided
        api_key = args.api_key
        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                logger.error("No API key provided. Use --api-key or set OPENAI_API_KEY environment variable.")
                return 1
        
        # Initialize department classifier
        classifier = DepartmentClassifier(api_key=api_key, base_url=args.base_url)
        
        # Process data
        output_path = os.path.join(dept_output_dir, f"dept_classified_{timestamp}.xlsx")
        
        # Classify departments and add to full data
        result_path = classifier.process_excel(
            input_path=extracted_path,
            full_data_path=input_path,
            output_path=output_path
        )
        
        logger.info(f"Department classification completed. Results saved to: {result_path}")
        
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())