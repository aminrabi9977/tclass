
"""
AI Processor module for filtering tender data using a language model.
"""
import os
import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class TenderAIProcessor:
    """
    Processes tender data using a language model to filter consulting tenders.
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
            
            self.model = "gpt-4o"
            logger.info("AI processor initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing AI processor: {e}")
            raise
    
    def get_system_prompt(self) -> str:
        """
        Return the system prompt for the language model.
        """
        return """
            > **هدف:** از فایل اکسل ورودی، فقط «شماره مناقصه در هزاره» (ستون A) مناقصات *مشاوره‌ای* را استخراج و به‌صورت یک لیست متنیِ تک‌ستونی (بدون علائم اضافی) برگردان.

            ---

            ## ۱) آماده‌سازی و نرمال‌سازی
            1) متن ستون‌های «عنوان» و «شرح آگهی» را:
            - به lower-case تبدیل کن (هم فارسی هم انگلیسی).
            - حروف عربی/فارسی را یکسان کن: ك→ک ، ي→ی.
            - نیم‌فاصله/تب/نقطه‌گذاری و پرانتزها را با یک فاصله جایگزین کن؛ فاصله‌های پیاپی را به یکی کاهش بده.
            - اعداد فارسی/عربی را به لاتین تبدیل کن.
            - به هیچ عنوان به ستون «دسته‌بندی» توجه نکن.
            - هر ستون یا عبارتی که صرفاً ماهیت تدارکات/فرآیند را بیان می‌کند را کاملاً نادیده بگیر: «استعلام بها»، «فراخوان»، «مناقصه/مزایده»، «برگزاری»، «عمومی/دو مرحله‌ای»، «قرارداد»، «پیوست»، «شماره نیاز/ارجاع»، «شماره تماس»، تاریخ‌ها و کدها. اینها هیچ نقشی در تشخیص مشاوره/پیمانکاری ندارند.
            2) تطبیق‌ها باید **کلمه/عبارت کامل** باشند (نه زیررشته‌ی تصادفی داخل کلمات).

            ---

            ## ۲) فرهنگ واژگان

            ### ۲.۱) نشانگرهای **مشاوره‌ایِ قوی** (K_s+)
            مشاوره، خدمات مشاوره، خدمات مهندسی، مهندس مشاور، مطالعات، مطالعه، امکان‌سنجی، نظارت، کنترل پروژه، طراحی مفهومی، بررسی، طراحی پایه، طراحی تفصیلی، تحلیل، تدوین، تهیه گزارش، مدیریت طرح، عامل سوم، عامل چهارم، دوره آموزشی، آموزش ، business plan، bcp، طرح تداوم کسب و کار، ارزیابی، ممیزی، بازبینی، راهبرد/استراتژی، تهیه اسناد مناقصه، طرح جامع

            **دامنه‌ی IT/امنیت (اضافه‌شده):**
            امنیت سایبری، امنیت اطلاعات، isms، soc، ot، ics، scada، ارزیابی امنیتی، تحلیل ریسک امنیتی، ارزیابی آسیب‌پذیری، تست نفوذ، vapt، penetration test، gap analysis، hardening، blue team، red team
            **دامنه مخابرات/شبکه:**
            شبکه بی‌سیم/وایرلس/رادیویی، مایکروویو، vhf/uhf، lte/5g، mpls، ip، dwdm/sdh، ftth، بیسیم دیجیتال، شبکه صنعتی/ot، شبکه it

            > - **قفل نگه‌دار (Hard Keep): هر عنوانی که شامل **خدمات مهندسی** و یکی از **طراحی مفهومی/پایه/تفصیلی/طراحی شبکه** باشد ⇒ مشاوره‌ای (مگر K_mix).**

            ### ۲.۲) نشانگرهای **اجرایی/پیمانکاری قوی** (K_c+)
            اجرای، اجرا، احداث، عملیات، ساخت، نصب، راه اندازی/راه‌اندازی، تجهیز، توسعه، بازسازی، تعمیر، نگهداری، دیوارکشی، راهسازی، epc، pc، بارگیری، حمل، خرید، تعویض، لایروبی، حفاری، اکتشاف

            > **ابهام “آزمایش/تست”**  
            > - اگر همراه مواد/کارهای فیزیکی باشد (بتن، جوش، رادیوگرافی، خاک، آسفالت، لوله، کابل، چاه، مخزن، سازه) ⇒ پیمانکاری.  
            > - اگر همراه امنیت/آی‌تی باشد (نفوذ، سایبری، vapt، isms، soc، سرور، شبکه) ⇒ **مشاوره‌ای**.
            > - واژه‌های تدارکاتی نظیر «استعلام بها»، «خرید» وقتی با «خدمات مشاوره/مهندسی/طراحی/مطالعات/نظارت» می‌آیند ⇒ خنثی و به نفع K_c+ محسوب نشوند.
            ### ۲.۳) ترکیب‌های حذفِ قطعی (K_mix)
            «طراحی و اجرا»، «طراحی، ساخت»، «طراحی، نصب»، «طراحی و تأمین»، «طراحی و راه‌اندازی»، epc، pc، «خدمات نگهداری»، «خدمات تعمیر و نگهداری»، «خدمات عملیاتی»، «خدمات اکتشاف»، «خدمات آزمایش» (وقتی آزمایش از نوع فیزیکی است: بتن/جوش/…).

            ### ۲.۴) استثناهای صریح (Overrides)
            - «نظارت بر اجرای/ساخت/نصب/راه‌اندازی/عملیات …» ⇒ **مشاوره‌ای** (حتی اگر واژه‌ی اجرایی آمده باشد).
            - «خرید خدمات مشاوره‌ای» و «انجام خدمات مشاوره‌ای» ⇒ **مشاوره‌ای** (واژه‌ی «خرید» را در این ساختار نادیده بگیر).
            - عبارات IT/امنیت بالا هرجا با «مشاوره/مطالعه/ارزیابی/ممیزی/تحلیل/آموزش/طرح/راهبرد» بیایند ⇒ **مشاوره‌ای**.

            ### ۲.۵) واژه‌های خنثی (N)
                N = «استعلام بها»، «فراخوان»، «مناقصه/مزایده»، «برگزاری»، «قرارداد»، «پیوست»، «شماره نیاز/ارجاع»، «شماره تماس»، «آگهی»، «عمومی/دو مرحله‌ای/یک مرحله‌ای»، «پیوست‌ها/شرایط خصوصی»
                - قانون: وجود N هیچ تغییری در تصمیم ایجاد نمی‌کند و در تعارض K_s+/K_c+ وزن صفر دارد.
            ---

            ## ۳) اولویت و منطق تصمیم‌گیری (ساده و مقاوم به نویز)
            برای هر ردیف، روی متنِ نرمال‌شده‌ی «عنوان» و اگر لازم بود «شرح آگهی»:

            1) اگر K_mix یافت شد ⇒ حذف.
            2) اگر قفل نگه‌دار برقرار بود ⇒ مشاوره‌ای.
            3) اگر K_s+ هست و K_c+ نیست ⇒ مشاوره‌ای.
            4) اگر هر دو K_s+ و K_c+ هستند:
                - اگر «نظارت» هست ⇒ مشاوره‌ای.
                - اگر حوزه IT/شبکه/امنیت همراه «طراحی/مطالعه/تحلیل/ارزیابی/مشاوره/آموزش» هست ⇒ مشاوره‌ای.
                - اگر الگوی «طراحی و اجرا/طراحی، ساخت/…» (K_mix) دیده شد ⇒ حذف.
                - در غیر این صورت برو به 5.
            5) اگر فقط K_c+ هست ⇒ حذف.
            6) اگر هنوز نامشخص بود ⇒ بازبینی معنایی:
            - هر چیزی که اجرای فیزیکی/عملیات میدانی/ساخت‌وساز را توصیف کند ⇒ **حذف**.
            - هر چیزی که به مطالعه/نظارت/تحلیل/آموزش/ارزیابی/مشاوره می‌پردازد ⇒ **مشاوره‌ای**.

            > **قاعده‌ی طلایی:** وجود صریح «مشاوره/مهندس مشاور/خدمات مشاوره» در عنوان، مگر در صورت K_mix یا «اجراییِ خالص» بدون استثنا، ⇒ **نگه‌دار**.

            ---

            ## ۴) خروجی
            پس از برچسب‌گذاری، **فقط** ستون «شماره مناقصه در هزاره» ردیف‌های *مشاوره‌ای* را، به ترتیب فایل، به‌صورت متن ساده برگردان. هر شماره در یک سطر، بدون هیچ علامت اضافی.

            ---

            ## ۵) کنترل کیفیت (پیشنهادی – فقط برای لاگ داخلی، نه خروجی)
            برای هر ردیف یک توضیح خیلی کوتاه (مثل «به‌دلیل وجود: مشاوره، امنیت سایبری») تولید کن و آن را در ذهن نگه‌دار یا در ستون کمکی ثبت کن؛ اما در خروجی نهایی **نمایش نده**. روی ۲۰ ردیف تصادفی دستی چک کن؛ اگر خطا > ۵٪ شد، لیست واژگان را گسترش بده (به‌خصوص هم‌معنی‌ها و املای جایگزین).


        """
    
    def prepare_user_message(self, tenders_data: List[Dict[str, Any]]) -> str:
        """
        Prepare the user message for the language model.
        
        Args:
            tenders_data: List of dictionaries containing tender information
            
        Returns:
            User message string
        """
        message = "لطفاً مناقصات زیر را بررسی کنید و شماره مناقصات مشاوره‌ای را به من بدهید:\n\n"
        
        for i, tender in enumerate(tenders_data, 1):
            message += f"مناقصه {i}:\n"
            message += f"شماره مناقصه در هزاره: {tender.get('شماره مناقصه در هزاره', '')}\n"
            message += f"عنوان: {tender.get('عنوان', '')}\n"
            message += f"شرح آگهی: {tender.get('شرح آگهی', '')}\n"
            message += f"دسته بندی: {tender.get('دسته بندی', '')}\n\n"
        
        return message
    
    def filter_consulting_tenders(self, tenders_data: List[Dict[str, Any]]) -> List[str]:
        """
        Use the language model to filter consulting tenders.
        
        Args:
            tenders_data: List of dictionaries containing tender information
            
        Returns:
            List of tender IDs for consulting tenders
        """
        try:
            logger.info(f"Filtering {len(tenders_data)} tenders")
            
            # Prepare the messages
            system_prompt = self.get_system_prompt()
            user_message = self.prepare_user_message(tenders_data)
            
            # Send the request to the language model
            logger.info("Sending request to language model")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1
                
            )
            
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
            
            logger.info(f"Found {len(tender_ids)} consulting tenders")
            return tender_ids
            
        except Exception as e:
            logger.error(f"Error filtering consulting tenders: {e}")
            raise
    
    def process_excel(self, input_path: str, output_path: Optional[str] = None, full_data_path: Optional[str] = None) -> str:
        """
        Process tender data in an Excel file and filter consulting tenders.
        
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
            
            # Check if the required columns exist
            required_columns = ["شماره مناقصه در هزاره", "عنوان", "شرح آگهی", "دسته بندی"]
            for col in required_columns:
                if col not in df.columns:
                    logger.error(f"Column '{col}' not found in the Excel file")
                    raise ValueError(f"Column '{col}' not found in the Excel file")
            
            # Convert DataFrame to list of dictionaries
            tenders_data = df.to_dict('records')
            
            # Filter consulting tenders
            tender_ids = self.filter_consulting_tenders(tenders_data)
            
            # Create a DataFrame with only the filtered tenders
            filtered_df = df[df["شماره مناقصه در هزاره"].astype(str).isin(tender_ids)]
            
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
            
            # If full data path is provided, read and filter the full data
            if full_data_path and os.path.exists(full_data_path):
                logger.info(f"Reading full data from: {full_data_path}")
                full_df = pd.read_excel(full_data_path, engine='openpyxl')
                
                # Filter the full data based on the tender IDs
                full_filtered_df = full_df[full_df["شماره مناقصه در هزاره"].astype(str).isin(tender_ids)]
                
                # Generate full output path
                full_output_path = os.path.join(
                    os.path.dirname(output_path),
                    f"full_filtered_{os.path.basename(input_path)}"
                )
                
                # Save full filtered data to Excel
                logger.info(f"Saving full filtered data to: {full_output_path}")
                full_filtered_df.to_excel(full_output_path, index=False, engine='openpyxl')
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error processing Excel file: {e}")
            raise