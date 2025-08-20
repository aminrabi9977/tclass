"""
Script to process tender data using the AI processor.
"""
import os
import sys
import argparse
import logging
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.processing.ai_processor import TenderAIProcessor
from src.utils.config import PROCESSED_DIR, OUTPUT_DIR, LOG_LEVEL, LOG_FILE

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

def prepare_data_for_ai(input_path, output_path=None):
    """
    Prepare data for AI processing by extracting required columns.
    
    Args:
        input_path: Path to the input Excel file
        output_path: Path to save the extracted data
        
    Returns:
        Path to the extracted data
    """
    try:
        logger.info(f"Preparing data from {input_path}")
        
        # Read the Excel file
        df = pd.read_excel(input_path)
        
        # Extract required columns for AI
        required_columns = ["شماره مناقصه در هزاره", "عنوان", "شرح آگهی", "دسته بندی"]
        
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
            output_path = os.path.join(dirname, f"extracted_{basename}")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to Excel
        extracted_df.to_excel(output_path, index=False)
        
        logger.info(f"Extracted data saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error preparing data: {e}")
        raise

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Process tender data using AI')
    parser.add_argument('--input', help='Path to the input Excel file')
    parser.add_argument('--api-key', help='OpenAI API key')
    parser.add_argument('--base-url', help='Base URL for the OpenAI API (optional)')
    parser.add_argument('--output-dir', help='Directory to save output files', default=OUTPUT_DIR)
    args = parser.parse_args()
    
    try:
        # Use the latest Excel file in PROCESSED_DIR if input not specified
        input_path = args.input
        if not input_path:
            logger.info(f"No input file specified, looking for the latest Excel file in {PROCESSED_DIR}")
            excel_files = [
                os.path.join(PROCESSED_DIR, f) 
                for f in os.listdir(PROCESSED_DIR) 
                if f.endswith('.xlsx')
            ]
            
            if not excel_files:
                logger.error(f"No Excel files found in {PROCESSED_DIR}")
                return 1
            
            # Sort by modification time (latest first)
            excel_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            input_path = excel_files[0]
            logger.info(f"Using latest Excel file: {input_path}")
        
        # Check if the input file exists
        if not os.path.exists(input_path):
            logger.error(f"Input file not found: {input_path}")
            return 1
        
        # Create subdirectory for AI output
        ai_output_dir = os.path.join(args.output_dir, "ai_filtered")
        os.makedirs(ai_output_dir, exist_ok=True)
        
        # Prepare timestamp for output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare data for AI processing
        extracted_data_path = os.path.join(ai_output_dir, f"extracted_{timestamp}.xlsx")
        extracted_path = prepare_data_for_ai(input_path, extracted_data_path)
        
        # Check if API key is provided
        api_key = args.api_key
        if not api_key:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                logger.error("No API key provided. Use --api-key or set OPENAI_API_KEY environment variable.")
                return 1
        
        # Initialize AI processor
        processor = TenderAIProcessor(api_key=api_key, base_url=args.base_url)
        
        # Process data
        output_path = os.path.join(ai_output_dir, f"filtered_{timestamp}.xlsx")
        full_output_path = os.path.join(ai_output_dir, f"full_filtered_{timestamp}.xlsx")
        
        # Process data and get consulting tenders
        result_path = processor.process_excel(
            input_path=extracted_path,
            output_path=output_path,
            full_data_path=input_path
        )
        
        logger.info(f"Processing completed. Results saved to: {result_path}")
        logger.info(f"Full filtered data saved to: {os.path.join(ai_output_dir, f'full_filtered_{os.path.basename(input_path)}')}")
        
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())