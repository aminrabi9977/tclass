"""
Desktop GUI Alternative using tkinter for the Tender Processing System.
Lighter weight alternative to the web interface.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import shutil

class TenderProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tender Processing System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.selected_file = tk.StringVar()
        self.processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface."""
        
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: File Processing
        self.process_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.process_frame, text="Process File")
        self.setup_process_tab()
        
        # Tab 2: Results
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="View Results")
        self.setup_results_tab()
        
        # Tab 3: Settings
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        self.setup_settings_tab()
        
    def setup_process_tab(self):
        """Set up the file processing tab."""
        
        # Title
        title_label = ttk.Label(
            self.process_frame, 
            text="Tender Processing System", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # File selection section
        file_frame = ttk.LabelFrame(self.process_frame, text="File Selection", padding=10)
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(file_frame, text="Select HTML file:").pack(anchor=tk.W)
        
        file_selection_frame = ttk.Frame(file_frame)
        file_selection_frame.pack(fill=tk.X, pady=5)
        
        self.file_entry = ttk.Entry(
            file_selection_frame, 
            textvariable=self.selected_file,
            width=60
        )
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.browse_button = ttk.Button(
            file_selection_frame,
            text="Browse",
            command=self.browse_file
        )
        self.browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Processing section
        process_frame = ttk.LabelFrame(self.process_frame, text="Processing", padding=10)
        process_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            process_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to process")
        self.status_label = ttk.Label(process_frame, textvariable=self.status_var)
        self.status_label.pack(pady=5)
        
        # Process button
        self.process_button = ttk.Button(
            process_frame,
            text="Start Processing",
            command=self.start_processing,
            style='Accent.TButton'
        )
        self.process_button.pack(pady=10)
        
        # Log output
        log_frame = ttk.LabelFrame(process_frame, text="Processing Log", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=15,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_results_tab(self):
        """Set up the results viewing tab."""
        
        # Results info
        info_frame = ttk.LabelFrame(self.results_frame, text="Processing Results", padding=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.results_info = ttk.Label(
            info_frame,
            text="No processing results available",
            font=("Arial", 10)
        )
        self.results_info.pack()
        
        # Results table
        table_frame = ttk.LabelFrame(self.results_frame, text="Classified Tenders", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview for results
        columns = ('ID', 'Department', 'Title', 'Organizer', 'Region')
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=120)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Download buttons
        download_frame = ttk.Frame(self.results_frame)
        download_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.download_excel_button = ttk.Button(
            download_frame,
            text="Download Excel",
            command=self.download_excel,
            state=tk.DISABLED
        )
        self.download_excel_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_results_button = ttk.Button(
            download_frame,
            text="Refresh Results",
            command=self.refresh_results
        )
        self.refresh_results_button.pack(side=tk.LEFT, padx=5)
        
    def setup_settings_tab(self):
        """Set up the settings tab."""
        
        # API Settings
        api_frame = ttk.LabelFrame(self.settings_frame, text="API Configuration", padding=10)
        api_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(api_frame, text="OpenAI API Key:").pack(anchor=tk.W)
        self.api_key_entry = ttk.Entry(api_frame, show="*", width=50)
        self.api_key_entry.pack(fill=tk.X, pady=2)
        
        ttk.Label(api_frame, text="Base URL:").pack(anchor=tk.W, pady=(10, 0))
        self.base_url_entry = ttk.Entry(api_frame, width=50)
        self.base_url_entry.pack(fill=tk.X, pady=2)
        
        # Load current settings
        self.load_settings()
        
        save_button = ttk.Button(api_frame, text="Save Settings", command=self.save_settings)
        save_button.pack(pady=10)
        
        # System Info
        info_frame = ttk.LabelFrame(self.settings_frame, text="System Information", padding=10)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        info_text = f"""Python Version: {sys.version.split()[0]}
Working Directory: {os.getcwd()}
Data Directory: {os.path.join(os.getcwd(), 'data')}"""
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
        
    def browse_file(self):
        """Open file dialog to select HTML file."""
        filename = filedialog.askopenfilename(
            title="Select HTML file",
            filetypes=[("HTML files", "*.html *.htm"), ("All files", "*.*")]
        )
        if filename:
            self.selected_file.set(filename)
            
    def start_processing(self):
        """Start the processing pipeline in a separate thread."""
        if not self.selected_file.get():
            messagebox.showerror("Error", "Please select an HTML file first")
            return
            
        if not os.path.exists(self.selected_file.get()):
            messagebox.showerror("Error", "Selected file does not exist")
            return
            
        if self.processing:
            messagebox.showwarning("Warning", "Processing is already in progress")
            return
            
        # Start processing in separate thread
        self.processing = True
        self.process_button.config(state=tk.DISABLED)
        self.log_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.run_processing)
        thread.daemon = True
        thread.start()
        
    def run_processing(self):
        """Run the processing pipeline."""
        try:
            # Copy file to input directory
            input_dir = os.path.join(os.getcwd(), 'data', 'input')
            os.makedirs(input_dir, exist_ok=True)
            
            filename = os.path.basename(self.selected_file.get())
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_filename = f"{timestamp}_{filename}"
            dest_path = os.path.join(input_dir, dest_filename)
            
            self.update_status("Copying file to input directory...", 10)
            shutil.copy2(self.selected_file.get(), dest_path)
            
            # Run main.py
            self.update_status("Starting processing pipeline...", 20)
            
            main_py_path = os.path.join(os.getcwd(), "main.py")
            
            process = subprocess.Popen(
                [sys.executable, main_py_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                universal_newlines=True
            )
            
            # Read output in real-time
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.root.after(0, self.append_log, output.strip())
                    # Update progress based on log content
                    if "HTML extraction" in output:
                        self.root.after(0, self.update_status, "HTML extraction...", 30)
                    elif "AI filtering" in output:
                        self.root.after(0, self.update_status, "AI filtering...", 60)
                    elif "Department classification" in output:
                        self.root.after(0, self.update_status, "Department classification...", 80)
            
            # Get final result
            return_code = process.poll()
            
            if return_code == 0:
                self.root.after(0, self.update_status, "Processing completed successfully!", 100)
                self.root.after(0, self.refresh_results)
                self.root.after(0, messagebox.showinfo, "Success", "Processing completed successfully!")
            else:
                stderr = process.stderr.read()
                self.root.after(0, self.update_status, "Processing failed", 0)
                self.root.after(0, self.append_log, f"Error: {stderr}")
                self.root.after(0, messagebox.showerror, "Error", f"Processing failed: {stderr}")
                
        except Exception as e:
            self.root.after(0, self.update_status, f"Error: {str(e)}", 0)
            self.root.after(0, messagebox.showerror, "Error", f"Processing failed: {str(e)}")
        finally:
            self.processing = False
            self.root.after(0, lambda: self.process_button.config(state=tk.NORMAL))
            
    def update_status(self, message, progress):
        """Update status and progress."""
        self.status_var.set(message)
        self.progress_var.set(progress)
        
    def append_log(self, message):
        """Append message to log."""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        
    def refresh_results(self):
        """Refresh the results display."""
        try:
            # Clear existing data
            for item in self.results_tree.get_children():
                self.results_tree.delete(item)
            
            # Look for latest results
            dept_dir = os.path.join(os.getcwd(), 'data', 'output', 'dept_classified')
            
            if not os.path.exists(dept_dir):
                self.results_info.config(text="No results directory found")
                return
                
            excel_files = [f for f in os.listdir(dept_dir) if f.endswith('.xlsx')]
            
            if not excel_files:
                self.results_info.config(text="No result files found")
                return
                
            # Get latest file
            excel_files.sort(key=lambda x: os.path.getmtime(os.path.join(dept_dir, x)), reverse=True)
            latest_file = os.path.join(dept_dir, excel_files[0])
            
            # Read Excel file
            df = pd.read_excel(latest_file)
            
            # Update info
            self.results_info.config(text=f"Results: {len(df)} tenders processed")
            
            # Populate tree
            for index, row in df.head(100).iterrows():  # Show first 100 rows
                tender_id = row.get('شماره مناقصه در هزاره', '')
                department = row.get('معاونت مربوطه', '')
                title = row.get('عنوان', '')[:50] + "..." if len(str(row.get('عنوان', ''))) > 50 else row.get('عنوان', '')
                organizer = row.get('برگزارکننده', '')[:30] + "..." if len(str(row.get('برگزارکننده', ''))) > 30 else row.get('برگزارکننده', '')
                region = row.get('منطقه', '')
                
                self.results_tree.insert('', tk.END, values=(tender_id, department, title, organizer, region))
            
            # Enable download button
            self.download_excel_button.config(state=tk.NORMAL)
            self.latest_file = latest_file
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load results: {str(e)}")
            
    def download_excel(self):
        """Download the Excel file."""
        if not hasattr(self, 'latest_file') or not os.path.exists(self.latest_file):
            messagebox.showerror("Error", "No result file available")
            return
            
        # Ask user where to save
        save_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialname=f"tender_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
        
        if save_path:
            try:
                shutil.copy2(self.latest_file, save_path)
                messagebox.showinfo("Success", f"File saved to: {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                
    def load_settings(self):
        """Load settings from .env file."""
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('OPENAI_API_KEY', '')
            base_url = os.getenv('OPENAI_BASE_URL', '')
            
            if api_key:
                self.api_key_entry.insert(0, api_key)
            if base_url:
                self.base_url_entry.insert(0, base_url)
                
        except Exception as e:
            print(f"Error loading settings: {e}")
            
    def save_settings(self):
        """Save settings to .env file."""
        try:
            env_content = f"""# Environment Variables for Tender Processing System
OPENAI_API_KEY={self.api_key_entry.get()}
OPENAI_BASE_URL={self.base_url_entry.get()}
LOG_LEVEL=INFO
"""
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)
                
            messagebox.showinfo("Success", "Settings saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

def main():
    """Main function to run the desktop GUI."""
    root = tk.Tk()
    app = TenderProcessorGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()