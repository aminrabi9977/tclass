"""
Script to classify tender data by department.
Complete version with environment variables support.
"""
import os
import sys
import argparse
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.processing.department_classifier import DepartmentClassifier
from src.utils.config import AI_OUTPUT_DIR, OUTPUT_DIR, LOG_LEVEL, LOG_FILE

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

def get_latest_ai_filtered_file(directory):
    """
    Get the latest AI filtered file from directory.
    
    Args:
        directory: Directory to search for files
        
    Returns:
        Path to the latest file or None if no files found
    """
    try:
        ai_filtered_files = [
            os.path.join(directory, f) 
            for f in os.listdir(directory) 
            if f.startswith("full_filtered_") and f.endswith('.xlsx')
        ]
        
        if not ai_filtered_files:
            return None
        
        # Sort by modification time (latest first)
        ai_filtered_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return ai_filtered_files[0]
        
    except Exception as e:
        logger.error(f"Error finding latest AI filtered file: {e}")
        return None

def save_to_backup(source_path, backup_dir, backup_type="dept_classified"):
    """
    Save file to backup directory.
    
    Args:
        source_path: Source file path
        backup_dir: Backup directory path
        backup_type: Type of backup (for folder structure)
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
        import shutil
        shutil.copy2(source_path, backup_path)
        
        logger.info(f"File backed up to: {backup_path}")
        return backup_path
        
    except Exception as e:
        logger.error(f"Error backing up file: {e}")
        raise

def classify_departments_auto(input_file=None):
    """
    Automatically classify departments from the latest AI filtered file.
    
    Args:
        input_file: Optional specific input file path
        
    Returns:
        Path to the department classified file or None if failed
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
            input_file = get_latest_ai_filtered_file(AI_OUTPUT_DIR)
            if not input_file:
                logger.error(f"No AI filtered files found in {AI_OUTPUT_DIR}")
                return None
        
        if not os.path.exists(input_file):
            logger.error(f"Input file not found: {input_file}")
            return None
        
        logger.info(f"Using input file: {input_file}")
        
        # Create output directories
        dept_output_dir = os.path.join(OUTPUT_DIR, "dept_classified")
        backup_dept_dir = os.path.join("data", "backup", "dept_class_filter")
        os.makedirs(dept_output_dir, exist_ok=True)
        os.makedirs(backup_dept_dir, exist_ok=True)
        
        # Prepare timestamp for output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare data for department classification
        temp_dir = os.path.join(OUTPUT_DIR, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        extracted_data_path = os.path.join(temp_dir, f"dept_extract_{timestamp}.xlsx")
        extracted_path = prepare_data_for_classification(input_file, extracted_data_path)
        
        # Initialize department classifier
        classifier = DepartmentClassifier(api_key=api_key, base_url=base_url)
        
        # Process data
        output_filename = f"dept_classified_{timestamp}.xlsx"
        output_path = os.path.join(dept_output_dir, output_filename)
        
        # Classify departments and add to full data
        result_path = classifier.process_excel(
            input_path=extracted_path,
            full_data_path=input_file,
            output_path=output_path
        )
        
        # Save to backup
        save_to_backup(result_path, backup_dept_dir, "dept_classified")
        
        # Clean up temporary files
        try:
            os.remove(extracted_data_path)
            if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                os.rmdir(temp_dir)
        except:
            pass
        
        logger.info(f"Department classification completed successfully!")
        logger.info(f"Output saved to: {result_path}")
        
        return result_path
        
    except Exception as e:
        logger.error(f"Error in automatic department classification: {e}")
        return None

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Classify tender data by department')
    parser.add_argument('--input', help='Path to the input Excel file (optional - will use latest AI filtered file)')
    parser.add_argument('--api-key', help='OpenAI API key (optional - will use environment variable)')
    parser.add_argument('--base-url', help='Base URL for the OpenAI API (optional - will use environment variable)')
    parser.add_argument('--output-dir', help='Directory to save output files', default=OUTPUT_DIR)
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
            input_path = get_latest_ai_filtered_file(AI_OUTPUT_DIR)
            if not input_path:
                logger.error(f"No AI filtered files found in {AI_OUTPUT_DIR}")
                return 1
            logger.info(f"Using latest AI filtered file: {input_path}")
        
        # Check if the input file exists
        if not os.path.exists(input_path):
            logger.error(f"Input file not found: {input_path}")
            return 1
        
        # Create output directories
        dept_output_dir = os.path.join(args.output_dir, "dept_classified")
        backup_dept_dir = os.path.join("data", "backup", "dept_class_filter")
        os.makedirs(dept_output_dir, exist_ok=True)
        os.makedirs(backup_dept_dir, exist_ok=True)
        
        # Prepare timestamp for output files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Prepare data for department classification
        temp_dir = os.path.join(args.output_dir, "temp")
        os.makedirs(temp_dir, exist_ok=True)
        extracted_data_path = os.path.join(temp_dir, f"dept_extract_{timestamp}.xlsx")
        extracted_path = prepare_data_for_classification(input_path, extracted_data_path)
        
        # Initialize department classifier
        classifier = DepartmentClassifier(api_key=api_key, base_url=base_url)
        
        # Process data
        output_filename = f"dept_classified_{timestamp}.xlsx"
        output_path = os.path.join(dept_output_dir, output_filename)
        
        # Classify departments and add to full data
        result_path = classifier.process_excel(
            input_path=extracted_path,
            full_data_path=input_path,
            output_path=output_path
        )
        
        # Save to backup
        save_to_backup(result_path, backup_dept_dir, "dept_classified")
        
        # Clean up temporary files
        try:
            os.remove(extracted_data_path)
            if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                os.rmdir(temp_dir)
        except:
            pass
        
        logger.info("="*60)
        logger.info("DEPARTMENT CLASSIFICATION COMPLETED SUCCESSFULLY!")
        logger.info("="*60)
        logger.info(f"📊 Output saved to: {result_path}")
        logger.info(f"💾 Backup saved to: {backup_dept_dir}")
        logger.info("="*60)
        
        return 0
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())