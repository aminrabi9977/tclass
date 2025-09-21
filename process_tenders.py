# """
# Script to process tender data using the AI processor with JSON input.
# """
# import os
# import sys
# import argparse
# import logging
# import pandas as pd
# from datetime import datetime

# # Add project root to path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from src.processing.ai_processor import TenderAIProcessor
# from src.utils.config import PROCESSED_DIR, OUTPUT_DIR, LOG_LEVEL, LOG_FILE

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

# def prepare_data_for_ai(input_path, output_path=None):
#     """
#     Prepare data for AI processing by extracting required columns.
#     Now only extracts 3 columns instead of 4.
    
#     Args:
#         input_path: Path to the input Excel file
#         output_path: Path to save the extracted data
        
#     Returns:
#         Path to the extracted data
#     """
#     try:
#         logger.info(f"Preparing data from {input_path}")
        
#         # Read the Excel file
#         df = pd.read_excel(input_path)
        
#         # Extract required columns for AI (now only 3 columns)
#         required_columns = ["شماره مناقصه در هزاره", "عنوان", "شرح آگهی"]
        
#         # Check if all required columns exist
#         missing_columns = [col for col in required_columns if col not in df.columns]
#         if missing_columns:
#             logger.error(f"Missing columns in the Excel file: {missing_columns}")
#             raise ValueError(f"Missing columns in the Excel file: {missing_columns}")
        
#         # Create a new DataFrame with only the required columns
#         extracted_df = df[required_columns]
        
#         # Generate output path if not provided
#         if not output_path:
#             dirname = os.path.dirname(input_path) if os.path.dirname(input_path) else "."
#             basename = os.path.basename(input_path)
#             output_path = os.path.join(dirname, f"extracted_{basename}")
        
#         # Create output directory if it doesn't exist
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
#         # Save to Excel
#         extracted_df.to_excel(output_path, index=False)
        
#         logger.info(f"Extracted data saved to {output_path}")
#         logger.info(f"Extracted {len(extracted_df)} records with {len(required_columns)} columns")
#         return output_path
        
#     except Exception as e:
#         logger.error(f"Error preparing data: {e}")
#         raise

# def main():
#     """Main entry point."""
#     parser = argparse.ArgumentParser(description='Process tender data using AI with JSON input')
#     parser.add_argument('--input', help='Path to the input Excel file')
#     parser.add_argument('--api-key', help='OpenAI API key')
#     parser.add_argument('--base-url', help='Base URL for the OpenAI API (optional)')
#     parser.add_argument('--output-dir', help='Directory to save output files', default=OUTPUT_DIR)
#     args = parser.parse_args()
    
#     try:
#         # Use the latest Excel file in PROCESSED_DIR if input not specified
#         input_path = args.input
#         if not input_path:
#             logger.info(f"No input file specified, looking for the latest Excel file in {PROCESSED_DIR}")
#             excel_files = [
#                 os.path.join(PROCESSED_DIR, f) 
#                 for f in os.listdir(PROCESSED_DIR) 
#                 if f.endswith('.xlsx')
#             ]
            
#             if not excel_files:
#                 logger.error(f"No Excel files found in {PROCESSED_DIR}")
#                 return 1
            
#             # Sort by modification time (latest first)
#             excel_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
#             input_path = excel_files[0]
#             logger.info(f"Using latest Excel file: {input_path}")
        
#         # Check if the input file exists
#         if not os.path.exists(input_path):
#             logger.error(f"Input file not found: {input_path}")
#             return 1
        
#         # Create subdirectory for AI output
#         ai_output_dir = os.path.join(args.output_dir, "ai_filtered")
#         os.makedirs(ai_output_dir, exist_ok=True)
        
#         # Prepare timestamp for output files
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
#         # Prepare data for AI processing (extract 3 columns)
#         extracted_data_path = os.path.join(ai_output_dir, f"extracted_{timestamp}.xlsx")
#         extracted_path = prepare_data_for_ai(input_path, extracted_data_path)
        
#         # Check if API key is provided
#         api_key = args.api_key
#         if not api_key:
#             api_key = os.environ.get("OPENAI_API_KEY")
#             if not api_key:
#                 logger.error("No API key provided. Use --api-key or set OPENAI_API_KEY environment variable.")
#                 return 1
        
#         # Initialize AI processor
#         processor = TenderAIProcessor(api_key=api_key, base_url=args.base_url)
        
#         # Process data with JSON input
#         output_path = os.path.join(ai_output_dir, f"filtered_{timestamp}.xlsx")
        
#         # Process data and get consulting tenders
#         result_path = processor.process_excel(
#             input_path=extracted_path,
#             output_path=output_path,
#             full_data_path=input_path
#         )
        
#         logger.info(f"Processing completed successfully!")
#         logger.info(f"Extracted data (3 columns): {extracted_path}")
#         logger.info(f"Filtered consulting tenders: {result_path}")
#         logger.info(f"Full filtered data: {os.path.join(ai_output_dir, f'full_filtered_{os.path.basename(input_path)}')}")
        
#         return 0
        
#     except Exception as e:
#         logger.error(f"An error occurred: {str(e)}")
#         import traceback
#         logger.error(traceback.format_exc())
#         return 1

# if __name__ == "__main__":
#     sys.exit(main())
    # ----------------------------------------------------------------------------------------------------------

"""
Script to process tender data using the AI processor with JSON input.
Supports both manual and automatic execution modes.
"""
import os
import sys
import argparse
import logging
import pandas as pd
from datetime import datetime
import shutil

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.processing.ai_processor import TenderAIProcessor
from src.utils.config import (
    PROCESSED_DIR, AI_OUTPUT_DIR, BACKUP_CONS_FILTER_DIR, 
    LOG_LEVEL, LOG_FILE
)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

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

def get_latest_processed_file():
    """
    Get the latest processed Excel file.
    
    Returns:
        Path to the latest file or None if no files found
    """
    try:
        if not os.path.exists(PROCESSED_DIR):
            return None
        
        excel_files = [
            os.path.join(PROCESSED_DIR, f) 
            for f in os.listdir(PROCESSED_DIR) 
            if f.endswith('.xlsx')
        ]
        
        if not excel_files:
            return None
        
        # Sort by modification time (latest first)
        excel_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return excel_files[0]
        
    except Exception as e:
        logger.error(f"Error finding latest processed file: {e}")
        return None

def save_to_backup(source_path, backup_dir, backup_type="ai_filtered"):
    """
    Save file to backup directory.
    
    Args:
        source_path: Source file path
        backup_dir: Backup directory path  
        backup_type: Type of backup (for filename)
    """
    try:
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        basename = os.path.basename(source_path)
        backup_filename = f"{backup_type}_{timestamp}_{basename}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy file to backup
        shutil.copy2(source_path, backup_path)
        
        logger.info(f"File backed up to: {backup_path}")
        return backup_path
        
    except Exception as e:
        logger.error(f"Error backing up file: {e}")
        raise

def prepare_data_for_ai(input_path, output_path=None):
    """
    Prepare data for AI processing by extracting required columns.
    Now only extracts 3 columns instead of 4.
    
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
        
        # Extract required columns for AI (now only 3 columns with updated names)
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
            output_path = os.path.join(dirname, f"extracted_{basename}")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to Excel
        extracted_df.to_excel(output_path, index=False)
        
        logger.info(f"Extracted data saved to {output_path}")
        logger.info(f"Extracted {len(extracted_df)} records with {len(required_columns)} columns")
        return output_path
        
    except Exception as e:
        logger.error(f"Error preparing data: {e}")
        raise

def process_tenders_auto(input_file=None):
    """
    Automatically process the latest file from processed directory.
    
    Args:
        input_file: Optional specific input file path
        
    Returns:
        Path to the full filtered file or None if failed
    """
    try:
        # Get API credentials from environment
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            return None
        
        # Find input file
        if not input_file:
            input_file = get_latest_processed_file()
            if not input_file:
                logger.error(f"No processed files found in {PROCESSED_DIR}")
                return None
        
        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return None
        
        logger.info(f"Processing file: {input_file}")
        
        # Create output directories
        os.makedirs(AI_OUTPUT_DIR, exist_ok=True)
        os.makedirs(BACKUP_CONS_FILTER_DIR, exist_ok=True)
        
        # Prepare timestamp for output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare temporary extracted data
        temp_dir = os.path.join(AI_OUTPUT_DIR, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        extracted_data_path = os.path.join(temp_dir, f"extracted_{timestamp}.xlsx")
        extracted_path = prepare_data_for_ai(input_file, extracted_data_path)
        
        # Initialize AI processor
        processor = TenderAIProcessor(api_key=api_key, base_url=base_url)
        
        # Process data with JSON input
        result_path = processor.process_excel(
            input_path=extracted_path,
            output_path=None,  # Let the processor decide the path
            full_data_path=input_file
        )
        
        # Find the full_filtered file that should have been created
        # Look in both main directory and temp directory
        full_filtered_files = []
        
        # First check main AI_OUTPUT_DIR
        if os.path.exists(AI_OUTPUT_DIR):
            for f in os.listdir(AI_OUTPUT_DIR):
                if f.startswith("full_filtered_") and f.endswith('.xlsx'):
                    full_filtered_files.append(os.path.join(AI_OUTPUT_DIR, f))
        
        # Also check temp directory as fallback
        temp_dir = os.path.join(AI_OUTPUT_DIR, "temp")
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                if f.startswith("full_filtered_") and f.endswith('.xlsx'):
                    full_filtered_files.append(os.path.join(temp_dir, f))
        
        if full_filtered_files:
            # Get the most recent full_filtered file
            full_filtered_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            full_filtered_path = full_filtered_files[0]
            
            # If file is in temp directory, move it to main directory
            if "/temp/" in full_filtered_path.replace("\\", "/"):
                main_filename = os.path.basename(full_filtered_path)
                main_path = os.path.join(AI_OUTPUT_DIR, main_filename)
                shutil.move(full_filtered_path, main_path)
                full_filtered_path = main_path
                logger.info(f"Moved file from temp to main directory: {main_path}")
            
            # Save to backup
            save_to_backup(full_filtered_path, BACKUP_CONS_FILTER_DIR, "cons_filtered")
            
            logger.info(f"AI processing completed successfully!")
            logger.info(f"Full filtered output: {full_filtered_path}")
            
            # Clean up temporary files
            try:
                if os.path.exists(extracted_data_path):
                    os.remove(extracted_data_path)
                # Clean up any other temp files
                if os.path.exists(temp_dir):
                    temp_files = [f for f in os.listdir(temp_dir) if f.startswith("extracted_")]
                    for temp_file in temp_files:
                        temp_file_path = os.path.join(temp_dir, temp_file)
                        if os.path.exists(temp_file_path):
                            os.remove(temp_file_path)
                    # Remove temp dir if empty
                    if not os.listdir(temp_dir):
                        os.rmdir(temp_dir)
            except Exception as cleanup_error:
                logger.warning(f"Cleanup error (non-critical): {cleanup_error}")
            
            return full_filtered_path
        else:
            logger.error("No full_filtered file was created")
            # Log what files are actually in both directories
            main_files = os.listdir(AI_OUTPUT_DIR) if os.path.exists(AI_OUTPUT_DIR) else []
            temp_files = os.listdir(temp_dir) if os.path.exists(temp_dir) else []
            logger.info(f"Files in main AI directory: {main_files}")
            logger.info(f"Files in temp directory: {temp_files}")
            return None
        
    except Exception as e:
        logger.error(f"Error in automatic tender processing: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Process tender data using AI with JSON input')
    parser.add_argument('--input', help='Path to the input Excel file (optional - will use latest processed file)')
    parser.add_argument('--api-key', help='OpenAI API key (optional - will use environment variable)')
    parser.add_argument('--base-url', help='Base URL for the OpenAI API (optional - will use environment variable)')
    args = parser.parse_args()
    
    try:
        # Use provided API key or fall back to environment
        api_key = args.api_key or os.getenv("OPENAI_API_KEY")
        base_url = args.base_url or os.getenv("OPENAI_BASE_URL")
        
        if not api_key:
            logger.error("No API key provided. Set OPENAI_API_KEY environment variable or use --api-key")
            return 1
        
        # Find input file
        input_path = args.input
        if not input_path:
            input_path = get_latest_processed_file()
            if not input_path:
                logger.error(f"No processed files found in {PROCESSED_DIR}")
                return 1
            logger.info(f"Using latest processed file: {input_path}")
        
        # Check if the input file exists
        if not os.path.exists(input_path):
            logger.error(f"Input file not found: {input_path}")
            return 1
        
        # Create output directories
        os.makedirs(AI_OUTPUT_DIR, exist_ok=True)
        os.makedirs(BACKUP_CONS_FILTER_DIR, exist_ok=True)
        
        # Prepare timestamp for output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare data for AI processing (extract 3 columns)
        temp_dir = os.path.join(AI_OUTPUT_DIR, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        extracted_data_path = os.path.join(temp_dir, f"extracted_{timestamp}.xlsx")
        extracted_path = prepare_data_for_ai(input_path, extracted_data_path)
        
        # Initialize AI processor
        processor = TenderAIProcessor(api_key=api_key, base_url=base_url)
        
        # Process data with JSON input - only save full_filtered output
        full_filtered_filename = f"full_filtered_{timestamp}.xlsx"
        full_filtered_path = os.path.join(AI_OUTPUT_DIR, full_filtered_filename)
        
        # Process data and get consulting tenders
        result_path = processor.process_excel(
            input_path=extracted_path,
            output_path=None,  # We don't need the basic filtered output
            full_data_path=input_path
        )
        
        # The processor creates full_filtered file automatically, find it
        full_filtered_files = [
            os.path.join(AI_OUTPUT_DIR, f)
            for f in os.listdir(AI_OUTPUT_DIR)
            if f.startswith("full_filtered_") and f.endswith('.xlsx')
        ]
        
        if full_filtered_files:
            # Get the most recent full_filtered file
            full_filtered_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            actual_output_path = full_filtered_files[0]
            
            # Rename to our desired filename if different
            if actual_output_path != full_filtered_path:
                os.rename(actual_output_path, full_filtered_path)
            
            # Save to backup
            save_to_backup(full_filtered_path, BACKUP_CONS_FILTER_DIR, "cons_filtered")
            
            logger.info("="*60)
            logger.info("AI PROCESSING COMPLETED SUCCESSFULLY!")
            logger.info("="*60)
            logger.info(f"📊 Full filtered output: {full_filtered_path}")
            logger.info(f"💾 Backup saved to: {BACKUP_CONS_FILTER_DIR}")
            logger.info("="*60)
            
            # Clean up temporary files
            try:
                if os.path.exists(extracted_data_path):
                    os.remove(extracted_data_path)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
            except:
                pass
        else:
            logger.error("No full_filtered file was created")
            return 1
        
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())