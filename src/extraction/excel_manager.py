"""
Excel Manager module for handling Excel operations.
"""
import os
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

class ExcelManager:
    """Manages Excel operations for tender data with specified field order."""
    
    def __init__(self, output_dir: str = None):
        """
        Initialize the Excel manager.
        
        Args:
            output_dir: Directory where Excel files will be saved
        """
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'data', 'processed')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Define the field order for the Excel file
        self.field_order = [
            "شماره مناقصه در هزاره",   # Tender number in Hezareh
            "عنوان",                   # Title
            "برگزارکننده",              # Organizer
            "منطقه",                   # Region
            "تاریخ انتشار",             # Publication date
            "تهیه اسناد تا",            # Document preparation deadline
            "منبع",                    # Source
            "ارسال اسناد تا",           # Document submission deadline
            "شرح آگهی",                # Description
            "شرایط آگهی",               # Conditions
            "دسته بندی",                # Category
            "مشاهده تصویر آگهی"         # View advertisement image
        ]
    
    def save_to_excel(self, tenders: List[Dict[str, Any]], file_name: Optional[str] = None) -> str:
        """
        Save tender data to an Excel file.
        
        Args:
            tenders: List of dictionaries containing tender information
            file_name: Name of the Excel file (default: tenders_YYYY-MM-DD_HHMMSS.xlsx)
            
        Returns:
            Path to the saved Excel file
        """
        if not tenders:
            raise ValueError("No tender data to save")
        
        # Create DataFrame from tender data
        df = pd.DataFrame(tenders)
        
        # Ensure all required fields are present
        for field in self.field_order:
            if field not in df.columns:
                df[field] = ""  # Add empty column if field is missing
        
        # Reorder columns based on field_order
        # Only include columns that are in both field_order and df.columns
        ordered_columns = [col for col in self.field_order if col in df.columns]
        
        # Add any additional columns that might be present but not in field_order
        extra_columns = [col for col in df.columns if col not in self.field_order]
        all_columns = ordered_columns + extra_columns
        
        # Reorder the DataFrame columns
        df = df[all_columns]
        
        # Generate file name if not provided
        if not file_name:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            file_name = f"tenders_{timestamp}.xlsx"
        
        # Ensure file has .xlsx extension
        if not file_name.endswith('.xlsx'):
            file_name += '.xlsx'
        
        # Save to Excel
        file_path = os.path.join(self.output_dir, file_name)
        df.to_excel(file_path, index=False, engine='openpyxl')
        
        return file_path
    
    def read_excel(self, file_path: str) -> pd.DataFrame:
        """
        Read tender data from an Excel file.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            DataFrame containing tender data
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return pd.read_excel(file_path, engine='openpyxl')