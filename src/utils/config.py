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

# -------------------------------------------------------------------------------------------------
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
# AI_OUTPUT_DIR = os.path.join(DATA_DIR, 'ai_filtered')  # Directory for AI filtered data
# DEPT_OUTPUT_DIR = os.path.join(DATA_DIR, 'dept_classified')  # Directory for department classified data


# # And update your directory creation section to include the new directory:
# # Create directories if they don't exist
# for directory in [DATA_DIR, INPUT_DIR, PROCESSED_DIR, OUTPUT_DIR, AI_OUTPUT_DIR, DEPT_OUTPUT_DIR]:
#     os.makedirs(directory, exist_ok=True)


# # AI Processing settings
# AI_MODEL_ENABLED = True
# AI_MODEL_NAME = "grok-3"
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

# ---------------------------------------------------------------------------------------------------


"""
Configuration settings for the tender extraction system.
"""
import os
from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Main data directories
DATA_DIR = os.path.join(BASE_DIR, 'data')
INPUT_DIR = os.path.join(DATA_DIR, 'input')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
BACKUP_DIR = os.path.join(DATA_DIR, 'backup')

# Output subdirectories
AI_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'ai_filtered')
DEPT_OUTPUT_DIR = os.path.join(OUTPUT_DIR, 'dept_classified')

# Backup subdirectories
BACKUP_PROCESSED_DIR = os.path.join(BACKUP_DIR, 'processed')
BACKUP_CONS_FILTER_DIR = os.path.join(BACKUP_DIR, 'cons_filter')
BACKUP_DEPT_CLASS_DIR = os.path.join(BACKUP_DIR, 'dept_class_filter')

# Create all directories if they don't exist
ALL_DIRECTORIES = [
    DATA_DIR,
    INPUT_DIR,
    PROCESSED_DIR,
    OUTPUT_DIR,
    BACKUP_DIR,
    AI_OUTPUT_DIR,
    DEPT_OUTPUT_DIR,
    BACKUP_PROCESSED_DIR,
    BACKUP_CONS_FILTER_DIR,
    BACKUP_DEPT_CLASS_DIR
]

for directory in ALL_DIRECTORIES:
    os.makedirs(directory, exist_ok=True)

# AI Processing settings
AI_MODEL_ENABLED = True
AI_MODEL_NAME = "gpt-5-mini"
AI_API_KEY = ""  # Set this through environment variable

# Email settings
EMAIL_ENABLED = False  # Set to True when implementing email functionality
EMAIL_SENDER = ""  # Your email address
EMAIL_RECIPIENTS = []  # List of recipient email addresses
EMAIL_SUBJECT = "Tender Information Report"
EMAIL_BODY = "Please find attached the processed tender information."

# Logging settings
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')

# Create logs directory
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)