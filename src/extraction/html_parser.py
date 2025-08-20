
"""
HTML Parser module for extracting tender information from HTML files.
"""
from bs4 import BeautifulSoup
import os
import re
from typing import Dict, List, Any, Optional

class TenderHTMLParser:
    """Parser for extracting tender information from HTML files according to specified requirements."""
    
    def __init__(self):
        """Initialize the HTML parser."""
        # Define the fields to extract
        self.fields = [
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
    
    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse an HTML file and extract tender information.
        
        Args:
            file_path: Path to the HTML file
            
        Returns:
            List of dictionaries containing tender information
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all tender notices (tables with class 'rp-notice-content')
        tender_tables = soup.find_all('table', class_='rp-notice-content')
        
        tenders = []
        for table in tender_tables:
            tender_data = self._extract_tender_data(table)
            if tender_data:
                tenders.append(tender_data)
        return tenders
    
    def _extract_tender_data(self, table) -> Dict[str, Any]:
        """
        Extract tender data from a table element.
        
        Args:
            table: BeautifulSoup table element
            
        Returns:
            Dictionary containing tender information
        """
        tender_data = {field: "" for field in self.fields}
        
        try:
            # 1. Extract tender number in Hezareh
            number_div = table.select_one('div.rp-divrelative div.rp-div-bb')
            if number_div:
                tender_data["شماره مناقصه در هزاره"] = number_div.text.strip()
            
            # 2. Extract title
            title_element = table.find('strong', class_='cd-noticetitle')
            if title_element:
                tender_data["عنوان"] = title_element.text.strip()
            
            # Find all rows with field labels
            rows = table.find_all('tr')
            
            # Extract organizer and region from the first row that contains them
            for row in rows:
                organizer_cell = row.find('td', class_='rp-td-50p rp-back1a')
                region_cell = row.find('td', class_='rp-back1a')
                
                if organizer_cell and region_cell:
                    organizer_b = organizer_cell.find('b')
                    region_b = region_cell.find('b')
                    
                    if organizer_b and "برگزار کننده" in organizer_b.text:
                        tender_data["برگزارکننده"] = self._extract_specific_field_value(organizer_cell)
                    
                    # if region_b and "منطقه" in region_b.text:
                    #     tender_data["منطقه"] = self._extract_specific_field_value(region_cell)
            
            # Extract other fields from their specific rows
            for row in rows:
                cells = row.find_all('td')
                for cell in cells:
                    b_tag = cell.find('b')
                    if not b_tag:
                        continue
                    
                    label = b_tag.text.strip()
                    
                    if "تاریخ انتشار" in label:
                        tender_data["تاریخ انتشار"] = self._extract_specific_field_value(cell)
                    elif "منطقه" in label:
                        tender_data["منطقه"] = self._extract_specific_field_value(cell)
                    elif "تهیه اسناد تا" in label:
                        tender_data["تهیه اسناد تا"] = self._extract_specific_field_value(cell)
                    
                    elif "منبع" in label:
                        tender_data["منبع"] = self._extract_specific_field_value(cell)
                    
                    elif "ارسال اسناد تا" in label:
                        tender_data["ارسال اسناد تا"] = self._extract_specific_field_value(cell)
                    
                    elif "شرح آگهی" in label:
                        description_span = cell.find('span', class_='cd-noticedescription')
                        if description_span:
                            tender_data["شرح آگهی"] = description_span.text.strip()
                    
                    elif "شرایط آگهی" in label:
                        tender_data["شرایط آگهی"] = self._extract_specific_field_value(cell)
                    
                    elif "دسته بندی" in label or "کلیدواژه" in label:
                        tender_data["دسته بندی"] = self._extract_specific_field_value(cell)
            
            # Extract image link
            for row in rows:
                image_cell = row.find('td', class_='rp-back2a')
                if image_cell and image_cell.find('a'):
                    link = image_cell.find('a')
                    if "مشاهده تصویر آگهی" in link.text:
                        tender_data["مشاهده تصویر آگهی"] = link['href']
            
        except Exception as e:
            print(f"Error extracting tender data: {str(e)}")
        
        return tender_data
    
    def _extract_specific_field_value(self, cell):
        """
        Extract only the specific value for a field, not all subsequent text.
        This handles cells like <td><b>Field:</b> Value</td>
        """
        # Get the b tag which contains the label
        b_tag = cell.find('b')
        if not b_tag:
            return ""
        
        # Remove the b tag from a copy of the cell to get just the value
        cell_copy = BeautifulSoup(str(cell), 'html.parser')
        b_element = cell_copy.find('b')
        if b_element:
            b_element.extract()
        
        # Get the text and clean it up
        value = cell_copy.get_text(strip=True)
        
        # Remove any leading colon
        if value.startswith(':'):
            value = value[1:].strip()
        
        # Extract only the first part of the value (before any potential field labels)
        field_labels = ["برگزار کننده", "منطقه", "نوبت اعلام", "تاریخ انتشار", "شماره آگهی", 
                        "تهیه اسناد تا", "منبع", "ارسال اسناد تا", "کد هزاره", "بازگشایی", 
                        "شرح آگهی", "شرایط آگهی", "آدرس", "تلفن", "وبسایت", "فکس", "ایمیل", 
                        "دسته بندی", "تهیه اسناد"]
        
        # For each potential field label, check if it appears in the value and cut at that point
        for label in field_labels:
            label_pattern = f":{label}"  # Look for ":label"
            if label_pattern in value:
                value = value.split(label_pattern)[0].strip()
            elif label in value:  # Also check without the colon
                value = value.split(label)[0].strip()
        
        return value

