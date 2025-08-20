# """
# Configuration settings for the tender extraction system.
# """
# import os
# from pathlib import Path

# # Base project directory
# BASE_DIR = Path(__file__).resolve().parent.parent.parent

# # Data directories
# DATA_DIR = os.path.join(BASE_DIR, 'data')
# INPUT_DIR = os.path.join(DATA_DIR, 'input')
# PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
# OUTPUT_DIR = os.path.join(DATA_DIR, 'output')

# # Create directories if they don't exist
# for directory in [DATA_DIR, INPUT_DIR, PROCESSED_DIR, OUTPUT_DIR]:
#     os.makedirs(directory, exist_ok=True)

# # AI Processing settings
# AI_MODEL_ENABLED = False  # Set to True when implementing AI processing

# # Email settings
# EMAIL_ENABLED = False  # Set to True when implementing email functionality
# EMAIL_SENDER = ""  # Your email address
# EMAIL_RECIPIENTS = []  # List of recipient email addresses
# EMAIL_SUBJECT = "Tender Information Report"
# EMAIL_BODY = "Please find attached the processed tender information."

# # Logging settings
# LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
# LOG_FILE = os.path.join(BASE_DIR, 'app.log')
# --------------------------------------------------------------------------------------------


# """
# Configuration settings for the tender extraction system.
# """
# import os
# from pathlib import Path

# # Base project directory
# BASE_DIR = Path(__file__).resolve().parent.parent.parent

# # Data directories
# DATA_DIR = os.path.join(BASE_DIR, 'data')
# INPUT_DIR = os.path.join(DATA_DIR, 'input')
# PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
# OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
# AI_OUTPUT_DIR = os.path.join(DATA_DIR, 'ai_filtered')  # New directory for AI filtered data

# # Create directories if they don't exist
# for directory in [DATA_DIR, INPUT_DIR, PROCESSED_DIR, OUTPUT_DIR, AI_OUTPUT_DIR]:
#     os.makedirs(directory, exist_ok=True)

# # AI Processing settings
# AI_MODEL_ENABLED = True
# AI_MODEL_NAME = "gpt-4o-mini"
# AI_API_KEY = ""  # Set this through environment variable or command line arg

# # Email settings
# EMAIL_ENABLED = False  # Set to True when implementing email functionality
# EMAIL_SENDER = ""  # Your email address
# EMAIL_RECIPIENTS = []  # List of recipient email addresses
# EMAIL_SUBJECT = "Tender Information Report"
# EMAIL_BODY = "Please find attached the processed tender information."

# # Logging settings
# LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
# LOG_FILE = os.path.join(BASE_DIR, 'app.log')
"""
Configuration settings for the tender extraction system.
"""
import os
from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data directories
DATA_DIR = os.path.join(BASE_DIR, 'data')
INPUT_DIR = os.path.join(DATA_DIR, 'input')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
AI_OUTPUT_DIR = os.path.join(DATA_DIR, 'ai_filtered')  # Directory for AI filtered data
DEPT_OUTPUT_DIR = os.path.join(DATA_DIR, 'dept_classified')  # Directory for department classified data

# Create directories if they don't exist
for directory in [DATA_DIR, INPUT_DIR, PROCESSED_DIR, OUTPUT_DIR, AI_OUTPUT_DIR, DEPT_OUTPUT_DIR]:
    os.makedirs(directory, exist_ok=True)

# AI Processing settings
AI_MODEL_ENABLED = True
AI_MODEL_NAME = "gpt-4o-mini"
AI_API_KEY = ""  # Set this through environment variable or command line arg

# Email settings
EMAIL_ENABLED = False  # Set to True when implementing email functionality
EMAIL_SENDER = ""  # Your email address
EMAIL_RECIPIENTS = []  # List of recipient email addresses
EMAIL_SUBJECT = "Tender Information Report"
EMAIL_BODY = "Please find attached the processed tender information."

# Logging settings
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = os.path.join(BASE_DIR, 'app.log')