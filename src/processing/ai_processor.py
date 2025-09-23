# """
# AI Processor module for filtering tender data using a language model with JSON input.
# """
# import os
# import pandas as pd
# import json
# from typing import List, Dict, Any, Optional
# import logging
# from openai import OpenAI

# logger = logging.getLogger(__name__)

# class TenderAIProcessor:
#     """
#     Processes tender data using a language model to filter consulting tenders.
#     Now works with JSON input instead of Excel.
#     """
    
#     def __init__(self, api_key: str, base_url: str = None):
#         """
#         Initialize the AI processor.
        
#         Args:
#             api_key: API key for the OpenAI API
#             base_url: Base URL for the OpenAI API (optional)
#         """
#         try:
#             # Initialize the OpenAI client
#             if base_url:
#                 self.client = OpenAI(api_key=api_key, base_url=base_url)
#             else:
#                 self.client = OpenAI(api_key=api_key)
            
#             self.model = "gpt-5-mini"
#             logger.info("AI processor initialized successfully")
#         except Exception as e:
#             logger.error(f"Error initializing AI processor: {e}")
#             raise
    
#     def get_system_prompt(self) -> str:
#         """
#         Return the system prompt for the language model.
#         Updated to work with JSON input.
#         """
#         return """
#         # هدف
#         از روی «عنوان» (و در صورت وجود «شرح آگهی») تشخیص بده هر آیتم «مشاوره‌ای» است یا نه؛ سپس فقط شمارهٔ «شماره مناقصه در هزاره» آیتم‌های مشاوره‌ای را چاپ کن.

#         # ورودی
#         JSON آبجکت یا آرایه‌ای از آبجکت‌ها با حداقل کلیدهای:
#         - «عنوان»
#         - «شماره مناقصه در هزاره»
#         - (اختیاری) «شرح آگهی»

#         # خروجی (سخت‌گیرانه)
#         فقط شماره‌ها؛ هر کدام در یک سطر مستقل.
#         هیچ متن/علامت/براکت/کاما/برچسب/فاصلهٔ اضافی چاپ نکن.
#         ترتیب ورودی را حفظ کن. آیتم‌های غیرمشاوره‌ای یا با شمارهٔ نامعتبر ⇒ چاپ نکن.

#         # نُرم‌سازی ذهنی (قبل از قضاوت)
#         - ی/ك عربی↔فارسی را یکسان کن؛ «ي→ی»، «ك→ک». «ۀ/ة→ه».
#         - نیم‌فاصله/ZWNJ/کشیده را بردار و فاصله‌ها را یکنواخت کن.
#         - چسبندگی «و» را جدا کن: «…وامنیت→… و امنیت»، «وخطوط→و خطوط».
#         - ارقام فارسی/عربی را برای چاپ به 0–9 تبدیل کن.
#         - شکل‌های جمع/اضافه (ها/های/ِ) را نادیده بگیر.
#         - «شماره مناقصه در هزاره» باید فقط عدد معتبر باشد (بعد از نُرم‌سازی). اگر خالی/نامعتبر بود ⇒ چاپ نکن.

#         # واژگان راهنما
#         ## مشاوره‌ای (سیگنال‌های قوی)
#         مشاوره، خدمات مشاوره، مهندس مشاور، خدمات مهندسی، خدمات طراحی و مهندسی، انتخاب/شناسایی «مشاور»، مطالعه/مطالعات/بررسی/تحلیل، امکان‌سنجی، نظارت (عالیه/مقیم/کارگاهی/بر اجرا)، کنترل پروژه (PM/MC بدون اجرا)، طراحی مفهومی/پایه/تفصیلی (وقتی «طراحی و اجرا» نیامده)، تدوین، تهیه گزارش، راهبرد/استراتژی، تهیه اسناد مناقصه/RFP، مدیریت طرح (بدون اجرا)، عامل سوم/چهارم، آموزش/دوره آموزشی/کارگاه آموزشی، ارزیابی، ممیزی/بازبینی، طرح جامع، نقشه‌برداری، ژئوتکنیک/آزمایشگاه خاک، Business Plan، BCP/طرح تداوم کسب‌وکار، بازرسی فنی، بازرسی، کنترل کیفیت، qc، qa/qc، پایش، ارزیابی فنی، ارزیابی فنی بازرگانی، **پیش‌صلاحیت**، **ارزیابی کیفی**، **تشخیص صلاحیت**، prequalification، pq، ارزیابی کیفی پیمانکاران/مناقصه‌گران»، تهیه اسناد مناقصه، راهبرد/استراتژی، «ارائه مشاوره»، «مشاوره جهت/برای/به‌منظور/در خصوص/در زمینه»، «مشاوره فنی/تخصصی/کارشناسی».

#         ## پیمانکاری/اجرایی (سیگنال رد مشاوره‌ای)
#         ساخت/اجرا/احداث/نصب/راه‌اندازی/توسعه/بهسازی/بازسازی/مرمت/آسفالت/روکش/جدول‌گذاری/لایروبی/حفاری/ابنیه/سیویل/برق‌رسانی/گازرسانی/مخابرات/روشنایی/خط انتقال/شبکه/محوطه‌سازی/فضای سبز (اجرایی)/رنگ‌آمیزی/تعمیرات و نگهداری (O&M)/بهره‌برداری/اپراتوری/EPC/PC/DB/Turnkey/پشتیبانی یا نگهداری عملیاتی سامانه/پایش یا مانیتورینگ عملیاتی.

#         # قواعد تصمیم‌گیری (ترتیب تقدم + «توقف فوری»)
#         ## قدم ۰ — Overrides قطعی
#         ### ۰.A مشاوره‌ای (توقف فوری؛ مگر استثناء)
#         اگر هرکدام از موارد زیر در «عنوان/شرح» بود ⇒ بلافاصله «مشاوره‌ای» و به قواعد بعدی نرو:
#         - «خدمات مشاوره/خدمت مشاوره/مشاوره‌ای»
#         - «انتخاب مشاور» یا «شناسایی مشاور»
#         - «مهندس مشاور»
#         - «انجام خدمات مشاوره»، «RFP مشاوره»
#         - «ارائه مشاوره»
#         - «خدمات مهندسی»
#         - «خدمات طراحی و مهندسی»
#         - «نظارت … بر اجرای …»
#         - «دوره(های) آموزشی» یا «کارگاه آموزشی»
#         - ««طراحی تفصیلی» یا «طراحی پایه» یا «طراحی مفهومی» **مشروط به نبودِ** «طراحی و اجرا
#         - الگوی «مشاوره (جهت|برای|به‌منظور|در خصوص|در زمینه) …»
#         - «مشاوره فنی/تخصصی/کارشناسی»
#         - الگوی ترکیبی با هر فاصله تا ۸۰ نویسه:
#         (خرید|خریداری|استعلام|تأمین|تدارک|انعقاد\s*قرارداد|واگذاری|برگزاری\s*مناقصه).{0,80}?\bخدمات?\s*مشاوره(?:‌ای)?\b

#         ### ۰.B پیمانکاری (توقف فوری)
#         اگر هرکدام از موارد زیر بود ⇒ بلافاصله «پیمانکاری»:
#         - «طراحی و اجرا» یا EPC/DB/Turnkey
#         - «انتخاب پیمانکار» یا «شناسایی پیمانکار» یا «انعقاد قرارداد با پیمانکار» یا «واگذاری به پیمانکار»
#         - «خدمات پایش/مانیتورینگ/Monitoring …» وقتی با «پیمانکار» یا در قالب خدمات عملیاتی آمده و **همراهِ واژه‌های تحلیلی** (تحلیل/ارزیابی/مطالعه/ممیزی/گزارش) نیست.
#         *تبصره:* اگر «پایش/مانیتورینگ» با واژگان تحلیلی مثل «تحلیل نتایج/مطالعات/ارزیابی/ممیزی/گزارش» همراه شد ⇒ مشاوره‌ای.

#         ## پس از قدم ۰ (اگر هنوز تصمیم نگرفته‌ای)
#         1) اگر فقط سیگنال‌های اجرایی قوی بود و نشانهٔ صریح مشاوره‌ای نبود ⇒ پیمانکاری.
#         2) اگر سیگنال‌های مشاوره‌ای (مطالعه/بررسی/تحلیل/امکان‌سنجی/نظارت/کنترل پروژه/طراحیِ بدون اجرا/ممیزی/ارزیابی/تهیه گزارش/راهبرد/آموزش/…) آمده و اجرای فیزیکی نیامده ⇒ مشاوره‌ای.
#         3) اگر فقط «خرید/تأمین/تدارک/اجاره/فروش…» و هیچ نشانهٔ مشاوره‌ای/اجرایی نبود ⇒ چاپ نکن.

#         # نکات حساس
#         - اگر «پشتیبانی/استقرار/راه‌اندازی/توسعه/بروزرسانی» **بعد از** «خدمات مشاوره» و با قید «جهت/برای/به‌منظور/در خصوص/در زمینه» آمدند، آن‌ها را اجرایی تلقی نکن؛ Override قدم ۰ برقرار است.
#         - ملاک اصلی «عنوان» است؛ «شرح آگهی» فقط برای رفع ابهام استفاده شود.

#         # چاپ خروجی
#         - ورودی می‌تواند آبجکت یا آرایه باشد.
#         - برای هر آیتمی که «مشاوره‌ای» شد و «شماره مناقصه در هزاره» معتبر دارد ⇒ همان شماره را (با ارقام انگلیسی) در یک سطر چاپ کن.
#         - هیچ چیز دیگری چاپ نکن. تکراری‌ها را دستکاری نکن.

#         # Regexهای کمکی (اختیاری)
#         - مشاوره‌ای:
#         - (?i)\bخدمات?\s*مشاوره(?:‌ای)?\b
#         - (?i)(انتخاب|شناسایی)\s*مشاور\b
#         - (?i)\bمهندس\s*مشاور\b
#         - (?i)انجام\s*خدمات?\s*مشاوره(?:‌ای)?\b
#         - (?i)\bRFP\s*مشاوره\b
#         - (?i)نظارت(\s*عالیه|\s*مقیم|\s*کارگاهی)?\s*بر\s*اجرای\b
#         - (?i)\bطراحی\s*(تفصیلی|پایه|مفهومی)\b(?!.*\b(طراحی\s*و\s*اجرا|EPC|DB|Turn\s*Key|Turnkey)\b)
#         - (?i)\b(?:دوره(?:\s*های)?)\s*(?:آ|ا)موزش(?:ی|ى)\b|\bکارگاه\s*(?:آ|ا)موزش(?:ی|ى)\b
#         - (?i)\b(ارائه|ارايه)\s*مشاوره\b
#         - (?i)\bمشاوره\s*(جهت|برای|به\s*منظور|در\s*خصوص|در\s*زمینه)\b
#         - (?i)\bمشاوره\s*(فنی|تخصصی|کارشناسی)\b
#         - (?i)(خرید|خریداری|استعلام|تأمین|تدارک|انعقاد\s*قرارداد|واگذاری|برگزاری\s*مناقصه).{0,80}?\bخدمات?\s*مشاوره(?:‌ای)?\b
#         - پیمانکاری:
#         - (?i)(EPC|DB|Turn\s*Key|Turnkey|طراحی\s*و\s*اجرا)\b
#         - (?i)(انتخاب|شناسایی)\s*پیمانکار\b|انعقاد\s*قرارداد\s*با\s*پیمانکار\b|واگذاری\s*به\s*پیمانکار\b
#         - (?i)\b(پایش|مانیتورینگ|Monitoring)\b(?!.*\b(تحلیل|ارزیابی|مطالعه|ممیزی|گزارش)\b)

#     """
#     def prepare_json_message(self, tenders_data: List[Dict[str, Any]]) -> str:
#         """
#         Prepare the JSON message for the language model.
        
#         Args:
#             tenders_data: List of dictionaries containing tender information
            
#         Returns:
#             JSON string message
#         """
#         message = "لطفاً JSON زیر را بررسی کنید و شماره مناقصات مشاوره‌ای را به من بدهید:\n\n"
        
#         # Convert to JSON string for the AI
#         json_data = []
#         for tender in tenders_data:
#             json_item = {
#                 "شماره مناقصه در هزاره": tender.get('شماره مناقصه در هزاره', ''),
#                 "عنوان": tender.get('عنوان', ''),
#                 "شرح آگهی": tender.get('شرح آگهی', '')
#             }
#             json_data.append(json_item)
        
#         message += json.dumps(json_data, ensure_ascii=False, indent=2)
        
#         return message
    
#     def filter_consulting_tenders(self, tenders_data: List[Dict[str, Any]]) -> List[str]:
#         """
#         Use the language model to filter consulting tenders.
        
#         Args:
#             tenders_data: List of dictionaries containing tender information
            
#         Returns:
#             List of tender IDs for consulting tenders
#         """
#         try:
#             logger.info(f"Filtering {len(tenders_data)} tenders")
            
#             # Prepare the messages
#             system_prompt = self.get_system_prompt()
#             user_message = self.prepare_json_message(tenders_data)
            
#             # Send the request to the language model
#             logger.info("Sending request to language model")
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_message}
#                 ],
#                 temperature=0.1
                
#             )
            
#             # Parse the response
#             logger.info("Parsing language model response")
#             response_text = response.choices[0].message.content.strip()
            
#             # Extract tender IDs (expected format is a simple list)
#             tender_ids = []
#             for line in response_text.split('\n'):
#                 line = line.strip()
#                 if line and line.isdigit():
#                     tender_ids.append(line)
#                 # Handle cases where the model might add other characters
#                 elif line and any(char.isdigit() for char in line):
#                     # Extract digits only
#                     digits = ''.join(char for char in line if char.isdigit())
#                     if digits:
#                         tender_ids.append(digits)
            
#             logger.info(f"Found {len(tender_ids)} consulting tenders")
#             return tender_ids
            
#         except Exception as e:
#             logger.error(f"Error filtering consulting tenders: {e}")
#             raise
    
#     def process_excel(self, input_path: str, output_path: Optional[str] = None, full_data_path: Optional[str] = None) -> str:
#         """
#         Process tender data in an Excel file and filter consulting tenders.
#         Now only extracts 3 columns and converts to JSON for AI processing.
        
#         Args:
#             input_path: Path to the input Excel file
#             output_path: Path to save the output Excel file
#             full_data_path: Path to the full tender data Excel file
            
#         Returns:
#             Path to the output Excel file
#         """
#         try:
#             # Read the input Excel file
#             logger.info(f"Reading Excel file: {input_path}")
#             df = pd.read_excel(input_path, engine='openpyxl')
            
#             # Check if the required columns exist (now only 3 columns)
#             required_columns = ["شماره مناقصه در هزاره", "عنوان", "شرح آگهی"]
#             for col in required_columns:
#                 if col not in df.columns:
#                     logger.error(f"Column '{col}' not found in the Excel file")
#                     raise ValueError(f"Column '{col}' not found in the Excel file")
            
#             # Extract only the required 3 columns
#             extracted_df = df[required_columns].copy()
            
#             # Convert DataFrame to list of dictionaries (JSON format)
#             tenders_data = extracted_df.to_dict('records')
#             logger.info(f"Extracted {len(tenders_data)} tenders for AI processing")
            
#             # Filter consulting tenders using JSON input
#             tender_ids = self.filter_consulting_tenders(tenders_data)
            
#             # Use full data if provided, otherwise use the input data
#             data_source_path = full_data_path if full_data_path and os.path.exists(full_data_path) else input_path
            
#             logger.info(f"Reading source data from: {data_source_path}")
#             source_df = pd.read_excel(data_source_path, engine='openpyxl')
            
#             # Filter the source data based on the tender IDs
#             filtered_df = source_df[source_df["شماره مناقصه در هزاره"].astype(str).isin(tender_ids)]
            
#             # Generate output path if not provided
#             if not output_path:
#                 dirname = os.path.dirname(input_path)
#                 basename = os.path.basename(input_path)
#                 output_path = os.path.join(dirname, f"filtered_{basename}")
            
#             # Create output directory if it doesn't exist
#             os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
#             # Save filtered tenders to Excel
#             logger.info(f"Saving filtered tenders to: {output_path}")
#             filtered_df.to_excel(output_path, index=False, engine='openpyxl')
            
#             # Also save the full filtered data with a standard name
#             if full_data_path and os.path.exists(full_data_path):
#                 full_output_path = os.path.join(
#                     os.path.dirname(output_path),
#                     f"full_filtered_{os.path.basename(full_data_path)}"
#                 )
                
#                 logger.info(f"Saving full filtered data to: {full_output_path}")
#                 filtered_df.to_excel(full_output_path, index=False, engine='openpyxl')
            
#             logger.info(f"Successfully processed {len(tenders_data)} tenders, filtered to {len(filtered_df)} consulting tenders")
#             return output_path
            
#         except Exception as e:
#             logger.error(f"Error processing Excel file: {e}")
#             raise
        # ------------------------------------------------------------------------------------

# """
# AI Processor module for filtering tender data using a language model with JSON input.
# """
# import os
# import pandas as pd
# import json
# from typing import List, Dict, Any, Optional
# import logging
# from openai import OpenAI

# logger = logging.getLogger(__name__)

# class TenderAIProcessor:
#     """
#     Processes tender data using a language model to filter consulting tenders.
#     Now works with JSON input instead of Excel.
#     """
    
#     def __init__(self, api_key: str, base_url: str = None):
#         """
#         Initialize the AI processor.
        
#         Args:
#             api_key: API key for the OpenAI API
#             base_url: Base URL for the OpenAI API (optional)
#         """
#         try:
#             # Initialize the OpenAI client
#             if base_url:
#                 self.client = OpenAI(api_key=api_key, base_url=base_url)
#             else:
#                 self.client = OpenAI(api_key=api_key)
            
#             self.model = "gpt-5-mini"
#             logger.info("AI processor initialized successfully")
#         except Exception as e:
#             logger.error(f"Error initializing AI processor: {e}")
#             raise
    
#     def get_system_prompt(self) -> str:
#         """
#         Return the system prompt for the language model.
#         Updated to work with JSON input.
#         """
#         return """
#         # هدف
#         از روی «عنوان» (و در صورت وجود «شرح آگهی») تشخیص بده هر آیتم «مشاوره‌ای» است یا نه؛ سپس فقط شمارهٔ «شماره مناقصه در هزاره» آیتم‌های مشاوره‌ای را چاپ کن.

#         # ورودی
#         JSON آبجکت یا آرایه‌ای از آبجکت‌ها با حداقل کلیدهای:
#         - «عنوان»
#         - «شماره مناقصه در هزاره»
#         - (اختیاری) «شرح آگهی»

#         # خروجی (سخت‌گیرانه)
#         فقط شماره‌ها؛ هر کدام در یک سطر مستقل.
#         هیچ متن/علامت/براکت/کاما/برچسب/فاصلهٔ اضافی چاپ نکن.
#         ترتیب ورودی را حفظ کن. آیتم‌های غیرمشاوره‌ای یا با شمارهٔ نامعتبر ⇒ چاپ نکن.

#         # نُرم‌سازی ذهنی (قبل از قضاوت)
#         - ی/ك عربی↔فارسی را یکسان کن؛ «ي→ی»، «ك→ک». «ۀ/ة→ه».
#         - نیم‌فاصله/ZWNJ/کشیده را بردار و فاصله‌ها را یکنواخت کن.
#         - چسبندگی «و» را جدا کن: «…وامنیت→… و امنیت»، «وخطوط→و خطوط».
#         - ارقام فارسی/عربی را برای چاپ به 0–9 تبدیل کن.
#         - شکل‌های جمع/اضافه (ها/های/ِ) را نادیده بگیر.
#         - «شماره مناقصه در هزاره» باید فقط عدد معتبر باشد (بعد از نُرم‌سازی). اگر خالی/نامعتبر بود ⇒ چاپ نکن.

#         # واژگان راهنما
#         ## مشاوره‌ای (سیگنال‌های قوی)
#         مشاوره، خدمات مشاوره، مهندس مشاور، خدمات مهندسی، خدمات طراحی و مهندسی، انتخاب/شناسایی «مشاور»، مطالعه/مطالعات/تحلیل، بررسی فنی/اقتصادی/فنی و اقتصادی، امکان‌سنجی، نظارت (عالیه/مقیم/کارگاهی/بر اجرا)، کنترل پروژه (PM/MC بدون اجرا)، طراحی مفهومی/پایه/تفصیلی (وقتی «طراحی و اجرا» نیامده)، تدوین، تهیه گزارش، هوشمندسازی، راهبرد/استراتژی، تهیه اسناد مناقصه/RFP، مدیریت طرح (بدون اجرا)، عامل سوم/چهارم، آموزش/دوره آموزشی/کارگاه آموزشی، ارزیابی، ممیزی/بازبینی، طرح جامع، نقشه‌برداری، ژئوتکنیک/آزمایشگاه خاک، Business Plan، BCP/طرح تداوم کسب‌وکار، کنترل کیفیت، qc، qa/qc، پایش، ارزیابی فنی، ارزیابی فنی بازرگانی، **پیش‌صلاحیت**، **تشخیص صلاحیت**، prequalification، pq، تهیه اسناد مناقصه، راهبرد/استراتژی، «ارائه مشاوره»، «مشاوره جهت/برای/به‌منظور/در خصوص/در زمینه»، «مشاوره فنی/تخصصی/کارشناسی.

#         ## پیمانکاری/اجرایی (سیگنال رد مشاوره‌ای)
#         ساخت/اجرا/احداث/نصب/راه‌اندازی/راه اندازی/توسعه/بهسازی/بازسازی/تامین/مرمت/آسفالت/روکش/جدول‌گذاری/لایروبی/حفاری/ابنیه/سیویل/برق‌رسانی/گازرسانی/روشنایی/محوطه‌سازی/فضای سبز (اجرایی)/رنگ‌آمیزی/تعمیرات و نگهداری (O&M)/بهره‌برداری/اپراتوری/EPC/PC/DB/Turnkey/پشتیبانی یا نگهداری عملیاتی سامانه/پایش یا مانیتورینگ عملیاتی.

#         # قواعد تصمیم‌گیری (ترتیب تقدم + «توقف فوری»)
#         ## قدم ۰ — Overrides قطعی
#         ### ۰.A مشاوره‌ای (توقف فوری؛ مگر استثناء)
#         اگر هرکدام از موارد زیر در «عنوان/شرح» بود ⇒ بلافاصله «مشاوره‌ای» و به قواعد بعدی نرو:
#         - «خدمات مشاوره/خدمت مشاوره/مشاوره‌ای»
#         - «انتخاب مشاور» یا «شناسایی مشاور»
#         - «مهندس مشاور»
#         - «انجام خدمات مشاوره»، «RFP مشاوره»
#         - «ارائه مشاوره»
#         - «خدمات مهندسی»
#         - «خدمات طراحی و مهندسی»
#         - «نظارت … بر اجرای …»
#         - «دوره(های) آموزشی» یا «کارگاه آموزشی»
#         - ««طراحی تفصیلی» یا «طراحی پایه» یا «طراحی مفهومی» **مشروط به نبودِ** «طراحی و اجرا
#         - الگوی «مشاوره (جهت|برای|به‌منظور|در خصوص|در زمینه) …»
#         - «مشاوره فنی/تخصصی/کارشناسی»
#         - الگوی ترکیبی با هر فاصله تا ۸۰ نویسه:
#         (خرید|خریداری|استعلام|تأمین|تدارک|انعقاد\s*قرارداد|واگذاری|برگزاری\s*مناقصه).{0,80}?\bخدمات?\s*مشاوره(?:‌ای)?\b

#         ### ۰.B پیمانکاری (توقف فوری)
#         اگر هرکدام از موارد زیر بود ⇒ بلافاصله «پیمانکاری»:
#         - «طراحی و اجرا» یا EPC/DB/Turnkey
#         - «انتخاب پیمانکار» یا «شناسایی پیمانکار» یا «انعقاد قرارداد با پیمانکار» یا «واگذاری به پیمانکار»
#         - «خدمات پایش/مانیتورینگ/Monitoring …» وقتی با «پیمانکار» یا در قالب خدمات عملیاتی آمده و **همراهِ واژه‌های تحلیلی** (تحلیل/ارزیابی/مطالعه/ممیزی/گزارش) نیست.
#         *تبصره:* اگر «پایش/مانیتورینگ» با واژگان تحلیلی مثل «تحلیل نتایج/مطالعات/ارزیابی/ممیزی/گزارش» همراه شد ⇒ مشاوره‌ای.

#         ## پس از قدم ۰ (اگر هنوز تصمیم نگرفته‌ای)
#         1) اگر فقط سیگنال‌های اجرایی قوی بود و نشانهٔ صریح مشاوره‌ای نبود ⇒ پیمانکاری.
#         2) اگر سیگنال‌های مشاوره‌ای (مطالعه/بررسی/تحلیل/امکان‌سنجی/نظارت/کنترل پروژه/طراحیِ بدون اجرا/ممیزی/ارزیابی/تهیه گزارش/راهبرد/آموزش/…) آمده و اجرای فیزیکی نیامده ⇒ مشاوره‌ای.
#         3) اگر فقط «خرید/تأمین/تدارک/نصب/راه اندازی/اجاره/فروش…» و هیچ نشانهٔ مشاوره‌ای نبود ⇒ چاپ نکن.

#         # نکات حساس
#         - اگر «پشتیبانی/استقرار/راه‌اندازی/توسعه/بروزرسانی» **بعد از** «خدمات مشاوره» و با قید «جهت/برای/به‌منظور/در خصوص/در زمینه» آمدند، آن‌ها را اجرایی تلقی نکن؛ Override قدم ۰ برقرار است.
#         - ملاک اصلی «عنوان» است؛ «شرح آگهی» فقط برای رفع ابهام استفاده شود.

#         # چاپ خروجی
#         - ورودی می‌تواند آبجکت یا آرایه باشد.
#         - برای هر آیتمی که «مشاوره‌ای» شد و «شماره مناقصه در هزاره» معتبر دارد ⇒ همان شماره را (با ارقام انگلیسی) در یک سطر چاپ کن.
#         - هیچ چیز دیگری چاپ نکن. تکراری‌ها را دستکاری نکن.

#         # Regexهای کمکی (اختیاری)
#         - مشاوره‌ای:
#         - (?i)\bخدمات?\s*مشاوره(?:‌ای)?\b
#         - (?i)(انتخاب|شناسایی)\s*مشاور\b
#         - (?i)\bمهندس\s*مشاور\b
#         - (?i)انجام\s*خدمات?\s*مشاوره(?:‌ای)?\b
#         - (?i)\bRFP\s*مشاوره\b
#         - (?i)نظارت(\s*عالیه|\s*مقیم|\s*کارگاهی)?\s*بر\s*اجرای\b
#         - (?i)\bطراحی\s*(تفصیلی|پایه|مفهومی)\b(?!.*\b(طراحی\s*و\s*اجرا|EPC|DB|Turn\s*Key|Turnkey)\b)
#         - (?i)\b(?:دوره(?:\s*های)?)\s*(?:آ|ا)موزش(?:ی|ى)\b|\bکارگاه\s*(?:آ|ا)موزش(?:ی|ى)\b
#         - (?i)\b(ارائه|ارايه)\s*مشاوره\b
#         - (?i)\bمشاوره\s*(جهت|برای|به\s*منظور|در\s*خصوص|در\s*زمینه)\b
#         - (?i)\bمشاوره\s*(فنی|تخصصی|کارشناسی)\b
#         - (?i)(خرید|خریداری|استعلام|تأمین|تدارک|انعقاد\s*قرارداد|واگذاری|برگزاری\s*مناقصه).{0,80}?\bخدمات?\s*مشاوره(?:‌ای)?\b
#         - پیمانکاری:
#         - (?i)(EPC|DB|Turn\s*Key|Turnkey|طراحی\s*و\s*اجرا)\b
#         - (?i)(انتخاب|شناسایی)\s*پیمانکار\b|انعقاد\s*قرارداد\s*با\s*پیمانکار\b|واگذاری\s*به\s*پیمانکار\b
#         - (?i)\b(پایش|مانیتورینگ|Monitoring)\b(?!.*\b(تحلیل|ارزیابی|مطالعه|ممیزی|گزارش)\b)

#     """
    
#     def prepare_json_message(self, tenders_data: List[Dict[str, Any]]) -> str:
#         """
#         Prepare the JSON message for the language model.
        
#         Args:
#             tenders_data: List of dictionaries containing tender information
            
#         Returns:
#             JSON string message
#         """
#         message = "لطفاً JSON زیر را بررسی کنید و شماره مناقصات مشاوره‌ای را به من بدهید:\n\n"
        
#         # Convert to JSON string for the AI
#         json_data = []
#         for tender in tenders_data:
#             json_item = {
#                 "شماره مناقصه در هزاره": tender.get('شماره مناقصه در هزاره', ''),
#                 "عنوان": tender.get('عنوان', ''),
#                 "شرح آگهی": tender.get('شرح آگهی', '')
#             }
#             json_data.append(json_item)
        
#         message += json.dumps(json_data, ensure_ascii=False, indent=2)
        
#         return message
    
#     def filter_consulting_tenders(self, tenders_data: List[Dict[str, Any]]) -> List[str]:
#         """
#         Use the language model to filter consulting tenders.
        
#         Args:
#             tenders_data: List of dictionaries containing tender information
            
#         Returns:
#             List of tender IDs for consulting tenders
#         """
#         try:
#             logger.info(f"Filtering {len(tenders_data)} tenders")
            
#             # For large datasets, process in batches
#             if len(tenders_data) > 100:
#                 logger.info(f"Large dataset detected ({len(tenders_data)} items). Processing in batches...")
#                 return self._process_large_dataset(tenders_data)
            
#             return self._process_single_batch(tenders_data)
            
#         except Exception as e:
#             logger.error(f"Error filtering consulting tenders: {e}")
#             # Return empty list instead of raising to prevent pipeline failure
#             logger.warning("Returning empty result due to error")
#             return []
    
#     def _process_large_dataset(self, tenders_data: List[Dict[str, Any]]) -> List[str]:
#         """Process large dataset in batches."""
#         batch_size = 50  # Process 50 tenders at a time
#         all_results = []
        
#         total_batches = (len(tenders_data) + batch_size - 1) // batch_size
#         logger.info(f"Processing {len(tenders_data)} tenders in {total_batches} batches of {batch_size}")
        
#         for i in range(0, len(tenders_data), batch_size):
#             batch = tenders_data[i:i + batch_size]
#             batch_num = (i // batch_size) + 1
            
#             logger.info(f"📦 Processing batch {batch_num}/{total_batches} ({len(batch)} items)")
            
#             try:
#                 batch_results = self._process_single_batch(batch)
#                 all_results.extend(batch_results)
                
#                 logger.info(f"✅ Batch {batch_num} completed: {len(batch_results)} consulting tenders found")
                
#                 # Add delay between batches to avoid rate limiting
#                 if i + batch_size < len(tenders_data):
#                     import time
#                     time.sleep(2)  # 2 second delay between batches
                    
#             except Exception as e:
#                 logger.error(f"❌ Batch {batch_num} failed: {e}")
#                 # Continue with next batch instead of failing completely
#                 continue
        
#         logger.info(f"🎉 Batch processing completed. Found {len(all_results)} total consulting tenders")
#         return all_results
    
#     def _process_single_batch(self, tenders_data: List[Dict[str, Any]]) -> List[str]:
#         """Process a single batch of tenders."""
#         # Prepare the messages
#         system_prompt = self.get_system_prompt()
#         user_message = self.prepare_json_message(tenders_data)
        
#         # Send the request to the language model with timeout and retry logic
#         logger.info("Sending request to language model")
        
#         max_retries = 3
#         timeout_seconds = 120  # 2 minutes timeout
        
#         for attempt in range(max_retries):
#             try:
#                 logger.info(f"Attempt {attempt + 1}/{max_retries}")
                
#                 response = self.client.chat.completions.create(
#                     model=self.model,
#                     messages=[
#                         {"role": "system", "content": system_prompt},
#                         {"role": "user", "content": user_message}
#                     ],
#                     temperature=0.1,
#                     timeout=timeout_seconds  # Add timeout
#                 )
                
#                 logger.info("✅ Received response from language model")
#                 break
                
#             except Exception as e:
#                 logger.error(f"❌ Attempt {attempt + 1} failed: {str(e)}")
#                 if attempt < max_retries - 1:
#                     import time
#                     wait_time = (attempt + 1) * 10  # Wait 10, 20, 30 seconds
#                     logger.info(f"⏳ Waiting {wait_time} seconds before retry...")
#                     time.sleep(wait_time)
#                 else:
#                     logger.error("All retry attempts failed")
#                     raise
        
#         # Parse the response
#         logger.info("Parsing language model response")
#         response_text = response.choices[0].message.content.strip()
        
#         # Extract tender IDs (expected format is a simple list)
#         tender_ids = []
#         for line in response_text.split('\n'):
#             line = line.strip()
#             if line and line.isdigit():
#                 tender_ids.append(line)
#             # Handle cases where the model might add other characters
#             elif line and any(char.isdigit() for char in line):
#                 # Extract digits only
#                 digits = ''.join(char for char in line if char.isdigit())
#                 if digits:
#                     tender_ids.append(digits)
        
#         logger.info(f"Found {len(tender_ids)} consulting tenders in this batch")
#         return tender_ids
    
#     def process_excel(self, input_path: str, output_path: Optional[str] = None, full_data_path: Optional[str] = None) -> str:
#         """
#         Process tender data in an Excel file and filter consulting tenders.
#         Now only extracts 3 columns and converts to JSON for AI processing.
        
#         Args:
#             input_path: Path to the input Excel file
#             output_path: Path to save the output Excel file
#             full_data_path: Path to the full tender data Excel file
            
#         Returns:
#             Path to the output Excel file
#         """
#         try:
#             # Read the input Excel file
#             logger.info(f"Reading Excel file: {input_path}")
#             df = pd.read_excel(input_path, engine='openpyxl')
            
#             # Check if the required columns exist (now only 3 columns)
#             required_columns = ["شماره مناقصه در هزاره", "عنوان", "شرح آگهی"]
#             for col in required_columns:
#                 if col not in df.columns:
#                     logger.error(f"Column '{col}' not found in the Excel file")
#                     raise ValueError(f"Column '{col}' not found in the Excel file")
            
#             # Extract only the required 3 columns
#             extracted_df = df[required_columns].copy()
            
#             # Convert DataFrame to list of dictionaries (JSON format)
#             tenders_data = extracted_df.to_dict('records')
#             logger.info(f"Extracted {len(tenders_data)} tenders for AI processing")
            
#             # Filter consulting tenders using JSON input
#             tender_ids = self.filter_consulting_tenders(tenders_data)
            
#             # Use full data if provided, otherwise use the input data
#             data_source_path = full_data_path if full_data_path and os.path.exists(full_data_path) else input_path
            
#             logger.info(f"Reading source data from: {data_source_path}")
#             source_df = pd.read_excel(data_source_path, engine='openpyxl')
            
#             # Filter the source data based on the tender IDs
#             filtered_df = source_df[source_df["شماره مناقصه در هزاره"].astype(str).isin(tender_ids)]
            
#             # Generate output path if not provided
#             if not output_path:
#                 dirname = os.path.dirname(input_path)
#                 basename = os.path.basename(input_path)
#                 output_path = os.path.join(dirname, f"filtered_{basename}")
            
#             # Create output directory if it doesn't exist
#             os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
#             # Save filtered tenders to Excel
#             logger.info(f"Saving filtered tenders to: {output_path}")
#             filtered_df.to_excel(output_path, index=False, engine='openpyxl')
            
#             # Also save the full filtered data with a standard name
#             if full_data_path and os.path.exists(full_data_path):
#                 full_output_path = os.path.join(
#                     os.path.dirname(output_path),
#                     f"full_filtered_{os.path.basename(full_data_path)}"
#                 )
                
#                 logger.info(f"Saving full filtered data to: {full_output_path}")
#                 filtered_df.to_excel(full_output_path, index=False, engine='openpyxl')
            
#             logger.info(f"Successfully processed {len(tenders_data)} tenders, filtered to {len(filtered_df)} consulting tenders")
#             return output_path
            
#         except Exception as e:
#             logger.error(f"Error processing Excel file: {e}")
#             raise     

# -----------------------------------------------------------------------------------------------------------------------------



"""
AI Processor module for filtering tender data using a language model with JSON input.
"""
import os
import pandas as pd
import json
from typing import List, Dict, Any, Optional
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class TenderAIProcessor:
    """
    Processes tender data using a language model to filter consulting tenders.
    Now works with JSON input instead of Excel.
    """
    
    def __init__(self, api_key: str, base_url: str = None):
        """
        Initialize the AI processor.
        
        Args:
            api_key: API key for the OpenAI API
            base_url: Base URL for the OpenAI API (optional)
        """
        try:
            # Initialize the OpenAI client
            if base_url:
                self.client = OpenAI(api_key=api_key, base_url=base_url)
            else:
                self.client = OpenAI(api_key=api_key)
            
            self.model = "gpt-5-mini"
            logger.info("AI processor initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AI processor: {e}")
            raise
    
    def get_system_prompt(self) -> str:
        """
        Return the system prompt for the language model.
        Updated to work with JSON input.
        """
        return """
        # هدف
        از روی «عنوان» (و در صورت وجود «شرح آگهی») تشخیص بده هر آیتم «مشاوره‌ای» است یا نه؛ سپس فقط شمارهٔ «شماره مناقصه در هزاره» آیتم‌های مشاوره‌ای را چاپ کن.

        # ورودی
        JSON آبجکت یا آرایه‌ای از آبجکت‌ها با حداقل کلیدهای:
        - «عنوان»
        - «شماره مناقصه در هزاره»
        - (اختیاری) «شرح آگهی»

        # خروجی (سخت‌گیرانه)
        فقط شماره‌ها؛ هر کدام در یک سطر مستقل.
        هیچ متن/علامت/براکت/کاما/برچسب/فاصلهٔ اضافی چاپ نکن.
        ترتیب ورودی را حفظ کن. آیتم‌های غیرمشاوره‌ای یا با شمارهٔ نامعتبر ⇒ چاپ نکن.

        # نُرم‌سازی ذهنی (قبل از قضاوت)
        - ی/ك عربی↔فارسی را یکسان کن؛ «ي→ی»، «ك→ک». «ۀ/ة→ه».
        - نیم‌فاصله/ZWNJ/کشیده را بردار و فاصله‌ها را یکنواخت کن.
        - چسبندگی «و» را جدا کن: «…وامنیت→… و امنیت»، «وخطوط→و خطوط».
        - ارقام فارسی/عربی را برای چاپ به 0–9 تبدیل کن.
        - شکل‌های جمع/اضافه (ها/های/ِ) را نادیده بگیر.
        - «شماره مناقصه در هزاره» باید فقط عدد معتبر باشد (بعد از نُرم‌سازی). اگر خالی/نامعتبر بود ⇒ چاپ نکن.

        # واژگان راهنما
        ## مشاوره‌ای (سیگنال‌های قوی)
        مشاوره، خدمات مشاوره، مهندس مشاور، خدمات مهندسی، خدمات طراحی و مهندسی، انتخاب/شناسایی «مشاور»، مطالعه/مطالعات/تحلیل، بررسی فنی/اقتصادی/فنی و اقتصادی، امکان‌سنجی، اندازه گیری، نظارت (عالیه/مقیم/کارگاهی/بر اجرا)، کنترل پروژه (PM/MC بدون اجرا)، طراحی مفهومی/پایه/تفصیلی (وقتی «طراحی و اجرا» نیامده)، تدوین، تهیه گزارش، هوشمندسازی، راهبرد/استراتژی، تهیه اسناد مناقصه/RFP، مدیریت طرح (بدون اجرا)، عامل سوم/چهارم، آموزش/دوره آموزشی/کارگاه آموزشی، ارزیابی، ممیزی/بازبینی، طرح جامع، نقشه‌برداری، ژئوتکنیک/آزمایشگاه خاک، Business Plan، BCP/طرح تداوم کسب‌وکار، کنترل کیفیت، qc، qa/qc، پایش، ارزیابی فنی، ارزیابی فنی بازرگانی، **پیش‌صلاحیت**، **تشخیص صلاحیت**، prequalification، pq، تهیه اسناد مناقصه، راهبرد/استراتژی، «ارائه مشاوره»، «مشاوره جهت/برای/به‌منظور/در خصوص/در زمینه»، «مشاوره فنی/تخصصی/کارشناسی.

        ## پیمانکاری/اجرایی (سیگنال رد مشاوره‌ای)
        ساخت/اجرا/احداث/نصب/راه‌اندازی/راه اندازی/پیاده سازی/توسعه/بهسازی/تأمین/تأمین اعتبار/بازسازی/تامین/مرمت/آسفالت/روکش/جدول‌گذاری/لایروبی/حفاری/ابنیه/سیویل/برق‌رسانی/گازرسانی/روشنایی/محوطه‌سازی/فضای سبز (اجرایی)/رنگ‌آمیزی/تعمیرات و نگهداری (O&M)/بهره‌برداری/اپراتوری/EPC/PC/DB/Turnkey/پشتیبانی یا نگهداری عملیاتی سامانه/پایش یا مانیتورینگ عملیاتی.

        # قواعد تصمیم‌گیری (ترتیب تقدم + «توقف فوری»)
        ## قدم ۰ — Overrides قطعی
        ### ۰.A مشاوره‌ای (توقف فوری؛ مگر استثناء)
        اگر هرکدام از موارد زیر در «عنوان/شرح» بود ⇒ بلافاصله «مشاوره‌ای» و به قواعد بعدی نرو:
        - «خدمات مشاوره/خدمت مشاوره/مشاوره‌ای»
        - «انتخاب مشاور» یا «شناسایی مشاور»
        - «مهندس مشاور»
        - «انجام خدمات مشاوره»، «RFP مشاوره»
        - «ارائه مشاوره»
        - «خدمات مهندسی»
        - «خدمات طراحی و مهندسی»
        - «نظارت … بر اجرای …»
        - «دوره(های) آموزشی» یا «کارگاه آموزشی»
        - ««طراحی تفصیلی» یا «طراحی پایه» یا «طراحی مفهومی» **مشروط به نبودِ** «طراحی و اجرا
        - الگوی «مشاوره (جهت|برای|به‌منظور|در خصوص|در زمینه) …»
        - «مشاوره فنی/تخصصی/کارشناسی»
        - الگوی ترکیبی با هر فاصله تا ۸۰ نویسه:
        (خرید|خریداری|استعلام|تأمین|تدارک|انعقاد\s*قرارداد|واگذاری|برگزاری\s*مناقصه).{0,80}?\bخدمات?\s*مشاوره(?:‌ای)?\b

        ### ۰.B پیمانکاری (توقف فوری)
        اگر هرکدام از موارد زیر بود ⇒ بلافاصله «پیمانکاری»:
        - «طراحی و اجرا» یا EPC/DB/Turnkey
        - «انتخاب پیمانکار» یا «شناسایی پیمانکار» یا «انعقاد قرارداد با پیمانکار» یا «واگذاری به پیمانکار»
        - «خدمات پایش/مانیتورینگ/Monitoring …» وقتی با «پیمانکار» یا در قالب خدمات عملیاتی آمده و **همراهِ واژه‌های تحلیلی** (تحلیل/ارزیابی/مطالعه/ممیزی/گزارش) نیست.
        *تبصره:* اگر «پایش/مانیتورینگ» با واژگان تحلیلی مثل «تحلیل نتایج/مطالعات/ارزیابی/ممیزی/گزارش» همراه شد ⇒ مشاوره‌ای.
        *تبصره:* اگر واژهٔ «ارزیابی» و «بررسی» به‌تنهایی آمدند ولی به خدمات عمومی/اجرایی (مانند ایاب و ذهاب، حمل‌ونقل، تغذیه، نظافت، نگهداری، تأمین کالا یا تجهیزات) مربوط بود ⇒ مشاوره‌ای نیست.
        *تبصره:* واژهٔ «ارزیابی» و «بررسی» فقط اگر با واژگانی مانند "فنی"، "اقتصادی"، "بازرگانی" و واژگانی که به خدمات مشاوره‌ای مربوط هستند و به خدمات اجرایی ربطی ندارند ⇒ مشاوره‌ای است.

        ## پس از قدم ۰ (اگر هنوز تصمیم نگرفته‌ای)
        1) اگر فقط سیگنال‌های اجرایی قوی بود و نشانهٔ صریح مشاوره‌ای نبود ⇒ پیمانکاری.
        2) اگر سیگنال‌های مشاوره‌ای (مطالعه/بررسی/تحلیل/امکان‌سنجی/نظارت/کنترل پروژه/طراحیِ بدون اجرا/ممیزی/تهیه گزارش/راهبرد/آموزش/…) آمده و اجرای فیزیکی نیامده ⇒ مشاوره‌ای.
        3) اگر فقط «خرید/تأمین/تدارک/نصب/راه اندازی/پیاده سازی/اجاره/فروش…» و هیچ نشانهٔ مشاوره‌ای نبود ⇒ چاپ نکن.

        # نکات حساس
        - اگر «پشتیبانی/استقرار/راه‌اندازی/توسعه/بروزرسانی» **بعد از** «خدمات مشاوره» و با قید «جهت/برای/به‌منظور/در خصوص/در زمینه» آمدند، آن‌ها را اجرایی تلقی نکن؛ Override قدم ۰ برقرار است.
        - ملاک اصلی «عنوان» است؛ «شرح آگهی» فقط برای رفع ابهام استفاده شود.

        # چاپ خروجی
        - ورودی می‌تواند آبجکت یا آرایه باشد.
        - برای هر آیتمی که «مشاوره‌ای» شد و «شماره مناقصه در هزاره» معتبر دارد ⇒ همان شماره را (با ارقام انگلیسی) در یک سطر چاپ کن.
        - هیچ چیز دیگری چاپ نکن. تکراری‌ها را دستکاری نکن.

        # بازبینی نهایی (self-check)
        بعد از اینکه برای هر آیتم تصمیم گرفتی (مشاوره‌ای یا نه):
        1. دوباره متن عنوان/شرح را مرور کن.
        2. مطابقت تصمیم خود را با همهٔ قواعد بالا بررسی کن.
        3. اگر تصمیم نهایی با هیچ‌یک از قواعد مشاوره‌ای یا پیمانکاری نمی‌خواند ⇒ از دانش خودت استفاده کن و در صورت مشاوره‌ای بودن آن را چاپ کن.


        # Regexهای کمکی (اختیاری)
        - مشاوره‌ای:
        - (?i)\bخدمات?\s*مشاوره(?:‌ای)?\b
        - (?i)(انتخاب|شناسایی)\s*مشاور\b
        - (?i)\bمهندس\s*مشاور\b
        - (?i)انجام\s*خدمات?\s*مشاوره(?:‌ای)?\b
        - (?i)\bRFP\s*مشاوره\b
        - (?i)نظارت(\s*عالیه|\s*مقیم|\s*کارگاهی)?\s*بر\s*اجرای\b
        - (?i)\bطراحی\s*(تفصیلی|پایه|مفهومی)\b(?!.*\b(طراحی\s*و\s*اجرا|EPC|DB|Turn\s*Key|Turnkey)\b)
        - (?i)\b(?:دوره(?:\s*های)?)\s*(?:آ|ا)موزش(?:ی|ى)\b|\bکارگاه\s*(?:آ|ا)موزش(?:ی|ى)\b
        - (?i)\b(ارائه|ارايه)\s*مشاوره\b
        - (?i)\bمشاوره\s*(جهت|برای|به\s*منظور|در\s*خصوص|در\s*زمینه)\b
        - (?i)\bمشاوره\s*(فنی|تخصصی|کارشناسی)\b
        - (?i)(خرید|خریداری|استعلام|تأمین|تدارک|انعقاد\s*قرارداد|واگذاری|برگزاری\s*مناقصه).{0,80}?\bخدمات?\s*مشاوره(?:‌ای)?\b
        - پیمانکاری:
        - (?i)(EPC|DB|Turn\s*Key|Turnkey|طراحی\s*و\s*اجرا)\b
        - (?i)(انتخاب|شناسایی)\s*پیمانکار\b|انعقاد\s*قرارداد\s*با\s*پیمانکار\b|واگذاری\s*به\s*پیمانکار\b
        - (?i)\b(پایش|مانیتورینگ|Monitoring)\b(?!.*\b(تحلیل|مطالعه|ممیزی|گزارش)\b)

    """
    
    def prepare_json_message(self, tenders_data: List[Dict[str, Any]]) -> str:
        """
        Prepare the JSON message for the language model.
        
        Args:
            tenders_data: List of dictionaries containing tender information
            
        Returns:
            JSON string message
        """
        message = "لطفاً JSON زیر را بررسی کنید و شماره مناقصات مشاوره‌ای را به من بدهید:\n\n"
        
        # Convert to JSON string for the AI
        json_data = []
        for tender in tenders_data:
            json_item = {
                "شماره مناقصه در هزاره": tender.get('شماره مناقصه در هزاره', ''),
                "عنوان": tender.get('عنوان', ''),
                "شرح آگهی": tender.get('شرح آگهی', '')
            }
            json_data.append(json_item)
        
        message += json.dumps(json_data, ensure_ascii=False, indent=2)
        
        return message
    
    def filter_consulting_tenders(self, tenders_data: List[Dict[str, Any]], progress_callback=None) -> List[str]:
        """
        Use the language model to filter consulting tenders.
        
        Args:
            tenders_data: List of dictionaries containing tender information
            
        Returns:
            List of tender IDs for consulting tenders
        """
        try:
            logger.info(f"Extracted {len(tenders_data)} tenders for AI processing")
            
            # For large datasets, process in batches
            if len(tenders_data) > 100:
                logger.info(f"Large dataset detected ({len(tenders_data)} items). Processing in batches...")
                return self._process_large_dataset(tenders_data, progress_callback)
            
            return self._process_single_batch(tenders_data)
            
        except Exception as e:
            logger.error(f"Error filtering consulting tenders: {e}")
            # Return empty list instead of raising to prevent pipeline failure
            logger.warning("Returning empty result due to error")
            return []
    
    def _process_large_dataset(self, tenders_data: List[Dict[str, Any]], progress_callback=None) -> List[str]:
        """Process large dataset in batches."""
        batch_size = 50  # Process 50 tenders at a time
        all_results = []
        
        total_batches = (len(tenders_data) + batch_size - 1) // batch_size
        logger.info(f"Processing {len(tenders_data)} tenders in {total_batches} batches of {batch_size}")
        
        for i in range(0, len(tenders_data), batch_size):
            batch = tenders_data[i:i + batch_size]
            batch_num = (i // batch_size) + 1
            
            batch_info = f"در حال پردازش دسته {batch_num}/{total_batches} ({len(batch)} آیتم)"
            logger.info(f"📦 Processing batch {batch_num}/{total_batches} ({len(batch)} items)")

            # Update progress callback if provided
            if progress_callback:
                progress_percent = (batch_num - 1) / total_batches * 100
                progress_callback(batch_info, progress_percent)

            try:
                batch_results = self._process_single_batch(batch)
                all_results.extend(batch_results)
                
                logger.info(f"✅ Batch {batch_num} completed: {len(batch_results)} consulting tenders found")
                
                # Add delay between batches to avoid rate limiting
                if i + batch_size < len(tenders_data):
                    import time
                    time.sleep(2)  # 2 second delay between batches
                    
            except Exception as e:
                logger.error(f"❌ Batch {batch_num} failed: {e}")
                # Continue with next batch instead of failing completely
                continue
                
        logger.info(f"🎉 Batch processing completed. Found {len(all_results)} total consulting tenders")
        # Final update to show completion
        if progress_callback:
            progress_callback("تکمیل پردازش تمام دسته‌ها", 100)
        return all_results
    
    def _process_single_batch(self, tenders_data: List[Dict[str, Any]]) -> List[str]:
        """Process a single batch of tenders."""
        # Prepare the messages
        system_prompt = self.get_system_prompt()
        user_message = self.prepare_json_message(tenders_data)
        
        # Send the request to the language model with timeout and retry logic
        logger.info("Sending request to language model")
        
        max_retries = 3
        timeout_seconds = 120  # 2 minutes timeout
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1}/{max_retries}")
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.2,
                    timeout=timeout_seconds  # Add timeout
                )
                
                logger.info("Received response from language model")
                break
                
            except Exception as e:
                logger.error(f"❌ Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    import time
                    wait_time = (attempt + 1) * 10  # Wait 10, 20, 30 seconds
                    logger.info(f"⏳ Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    logger.error("All retry attempts failed")
                    raise
        
        # Parse the response
        logger.info("Parsing language model response")
        response_text = response.choices[0].message.content.strip()
        
        # Extract tender IDs (expected format is a simple list)
        tender_ids = []
        for line in response_text.split('\n'):
            line = line.strip()
            if line and line.isdigit():
                tender_ids.append(line)
            # Handle cases where the model might add other characters
            elif line and any(char.isdigit() for char in line):
                # Extract digits only
                digits = ''.join(char for char in line if char.isdigit())
                if digits:
                    tender_ids.append(digits)
        
        logger.info(f"Found {len(tender_ids)} consulting tenders in this batch")
        return tender_ids
    
    def process_excel(self, input_path: str, output_path: Optional[str] = None, full_data_path: Optional[str] = None, progress_callback=None) -> str:
        """
        Process tender data in an Excel file and filter consulting tenders.
        Now only extracts 3 columns and converts to JSON for AI processing.
        
        Args:
            input_path: Path to the input Excel file
            output_path: Path to save the output Excel file
            full_data_path: Path to the full tender data Excel file
            
        Returns:
            Path to the output Excel file
        """
        try:
            # Read the input Excel file
            logger.info(f"Reading Excel file: {input_path}")
            df = pd.read_excel(input_path, engine='openpyxl')
            
            # Check if the required columns exist (now only 3 columns)
            required_columns = ["شماره مناقصه در هزاره", "عنوان", "شرح آگهی"]
            for col in required_columns:
                if col not in df.columns:
                    logger.error(f"Column '{col}' not found in the Excel file")
                    raise ValueError(f"Column '{col}' not found in the Excel file")
            
            # Extract only the required 3 columns
            extracted_df = df[required_columns].copy()
            
            # Convert DataFrame to list of dictionaries (JSON format)
            tenders_data = extracted_df.to_dict('records')
            logger.info(f"Extracted {len(tenders_data)} tenders for AI processing")
            
            # Filter consulting tenders using JSON input
            tender_ids = self.filter_consulting_tenders(tenders_data, progress_callback)
            
            # Use full data if provided, otherwise use the input data
            data_source_path = full_data_path if full_data_path and os.path.exists(full_data_path) else input_path
            
            logger.info(f"Reading source data from: {data_source_path}")
            source_df = pd.read_excel(data_source_path, engine='openpyxl')
            
            # Filter the source data based on the tender IDs
            filtered_df = source_df[source_df["شماره مناقصه در هزاره"].astype(str).isin(tender_ids)]
            
            # Generate output path if not provided
            if not output_path:
                dirname = os.path.dirname(input_path)
                basename = os.path.basename(input_path)
                output_path = os.path.join(dirname, f"filtered_{basename}")
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save filtered tenders to Excel
            logger.info(f"Saving filtered tenders to: {output_path}")
            filtered_df.to_excel(output_path, index=False, engine='openpyxl')
            
            # Also save the full filtered data with a standard name
            if full_data_path and os.path.exists(full_data_path):
                full_output_path = os.path.join(
                    os.path.dirname(output_path),
                    f"full_filtered_{os.path.basename(full_data_path)}"
                )
                
                logger.info(f"Saving full filtered data to: {full_output_path}")
                filtered_df.to_excel(full_output_path, index=False, engine='openpyxl')
            
            logger.info(f"Successfully processed {len(tenders_data)} tenders, filtered to {len(filtered_df)} consulting tenders")
            return output_path
            
        except Exception as e:
            logger.error(f"Error processing Excel file: {e}")
            raise     