import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import json
import os
from datetime import datetime
import tempfile
from pathlib import Path

# Import the main algorithm
from main import main as run_candidate_elimination


class CandidateEliminationGUI:
    """Main application class for the Candidate Elimination Algorithm GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Candidate Elimination Algorithm - Professional Tool")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Initialize variables
        self.current_data = None
        self.current_file_path = None
        self.positive_indicator = "Yes"
        self.negative_indicator = "No"
        self.results_history = []
        
        # Create results directory
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)
        
        # Load history
        self.load_history()
        
        # Setup styling
        self.setup_styles()
        
        # Create the main interface
        self.create_widgets()
    
    def setup_styles(self):
        """Configure professional styling for the application"""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('Info.TLabel', font=('Segoe UI', 10))
        style.configure('Success.TLabel', foreground='#2e7d32', font=('Segoe UI', 10, 'bold'))
        style.configure('Error.TLabel', foreground='#d32f2f', font=('Segoe UI', 10, 'bold'))
        
        # Configure button styles
        style.configure('Primary.TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Secondary.TButton', font=('Segoe UI', 9))
    
    def create_widgets(self):
        """Create the main interface widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Candidate Elimination Algorithm Tool", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_import_tab()
        self.create_results_tab()
        self.create_history_tab()
    
    def create_import_tab(self):
        """Create the file import and configuration tab"""
        self.import_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.import_frame, text="📁 File Import & Configuration")
        
        # Configure grid
        self.import_frame.columnconfigure(0, weight=1)
        self.import_frame.rowconfigure(3, weight=1)
        
        # File selection section
        file_section = ttk.LabelFrame(self.import_frame, text="File Selection", padding="10")
        file_section.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        file_section.columnconfigure(1, weight=1)
        
        ttk.Button(file_section, text="Browse CSV File", 
                  command=self.browse_file, style='Primary.TButton').grid(row=0, column=0, padx=(0, 10))
        
        self.file_label = ttk.Label(file_section, text="No file selected", style='Info.TLabel')
        self.file_label.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Drag and drop info
        drag_info = ttk.Label(file_section, 
                             text="💡 Tip: You can also drag and drop CSV files onto this window",
                             style='Info.TLabel')
        drag_info.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        # Configuration section
        config_section = ttk.LabelFrame(self.import_frame, text="Data Configuration", padding="10")
        config_section.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_section.columnconfigure(1, weight=1)
        
        # Positive indicator
        ttk.Label(config_section, text="Positive Class Indicator:", 
                 style='Info.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.positive_var = tk.StringVar(value="Yes")
        positive_entry = ttk.Entry(config_section, textvariable=self.positive_var, width=15)
        positive_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        # Negative indicator
        ttk.Label(config_section, text="Negative Class Indicator:", 
                 style='Info.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.negative_var = tk.StringVar(value="No")
        negative_entry = ttk.Entry(config_section, textvariable=self.negative_var, width=15)
        negative_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        # Help text
        help_text = ttk.Label(config_section, 
                             text="Specify what values in your target column represent positive and negative cases",
                             style='Info.TLabel')
        help_text.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        # Process button
        process_frame = ttk.Frame(self.import_frame)
        process_frame.grid(row=2, column=0, pady=10)
        
        self.process_btn = ttk.Button(process_frame, text="🚀 Process Data", 
                                     command=self.process_data, style='Primary.TButton',
                                     state='disabled')
        self.process_btn.pack()
        
        # Data preview section
        preview_section = ttk.LabelFrame(self.import_frame, text="Data Preview", padding="10")
        preview_section.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_section.columnconfigure(0, weight=1)
        preview_section.rowconfigure(1, weight=1)
        
        # Preview info
        self.preview_info = ttk.Label(preview_section, text="Load a CSV file to see preview", 
                                     style='Info.TLabel')
        self.preview_info.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        # Treeview for data preview
        self.create_preview_treeview(preview_section)
    
    def create_preview_treeview(self, parent):
        """Create treeview for data preview"""
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.preview_tree = ttk.Treeview(tree_frame)
        self.preview_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.preview_tree.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.preview_tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.preview_tree.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.preview_tree.configure(xscrollcommand=h_scrollbar.set)
    
    def create_results_tab(self):
        """Create the results display tab"""
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="📊 Results")
        
        # Configure grid
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(1, weight=1)
        
        # Results header
        header_frame = ttk.Frame(self.results_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(10, 20))
        header_frame.columnconfigure(1, weight=1)
        
        ttk.Label(header_frame, text="Algorithm Results", style='Title.TLabel').grid(row=0, column=0)
        
        self.save_results_btn = ttk.Button(header_frame, text="💾 Save Results", 
                                          command=self.save_results, style='Secondary.TButton',
                                          state='disabled')
        self.save_results_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Results content
        results_content = ttk.Frame(self.results_frame)
        results_content.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))
        results_content.columnconfigure(0, weight=1)
        results_content.rowconfigure(0, weight=1)
        
        # Text widget for results
        self.results_text = tk.Text(results_content, wrap=tk.WORD, font=('Consolas', 11))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for results
        results_scrollbar = ttk.Scrollbar(results_content, orient=tk.VERTICAL, 
                                         command=self.results_text.yview)
        results_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        # Configure text tags for formatting
        self.results_text.tag_configure("header", font=('Consolas', 14, 'bold'), foreground='#1976d2')
        self.results_text.tag_configure("subheader", font=('Consolas', 12, 'bold'), foreground='#388e3c')
        self.results_text.tag_configure("highlight", background='#e3f2fd')
    
    def create_history_tab(self):
        """Create the history tab"""
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📚 History")
        
        # Configure grid
        self.history_frame.columnconfigure(0, weight=1)
        self.history_frame.rowconfigure(1, weight=1)
        
        # History header
        header_frame = ttk.Frame(self.history_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(10, 20))
        header_frame.columnconfigure(1, weight=1)
        
        ttk.Label(header_frame, text="Processing History", style='Title.TLabel').grid(row=0, column=0)
        
        ttk.Button(header_frame, text="🗑️ Clear History", 
                  command=self.clear_history, style='Secondary.TButton').grid(row=0, column=2)
        
        # History listbox
        history_content = ttk.Frame(self.history_frame)
        history_content.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))
        history_content.columnconfigure(0, weight=1)
        history_content.rowconfigure(0, weight=1)
        
        self.history_listbox = tk.Listbox(history_content, font=('Segoe UI', 10))
        self.history_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.history_listbox.bind('<Double-1>', self.load_from_history)
        
        # History scrollbar
        history_scrollbar = ttk.Scrollbar(history_content, orient=tk.VERTICAL, 
                                         command=self.history_listbox.yview)
        history_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_listbox.configure(yscrollcommand=history_scrollbar.set)
        
        # History info
        ttk.Label(history_content, text="💡 Double-click an entry to view its results", 
                 style='Info.TLabel').grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        # Update history display
        self.update_history_display()
    
    def browse_file(self):
        """Open file dialog to select CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """Load and preview CSV file"""
        try:
            # Load data
            self.current_data = pd.read_csv(file_path)
            self.current_file_path = file_path
            
            # Update UI
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")
            self.process_btn.config(state='normal')
            
            # Update preview
            self.update_preview()
            
            # Show success message
            self.preview_info.config(text=f"✅ Loaded {len(self.current_data)} rows, {len(self.current_data.columns)} columns")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
            self.current_data = None
            self.current_file_path = None
            self.process_btn.config(state='disabled')
    
    def update_preview(self):
        """Update the data preview treeview"""
        # Clear existing data
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        if self.current_data is None:
            return
        
        # Configure columns
        columns = list(self.current_data.columns)
        self.preview_tree['columns'] = columns
        self.preview_tree['show'] = 'headings'
        
        # Configure column headers
        for col in columns:
            self.preview_tree.heading(col, text=col)
            self.preview_tree.column(col, width=100, anchor='center')
        
        # Add data (limit to first 100 rows for performance)
        for index, row in self.current_data.head(100).iterrows():
            values = [str(row[col]) for col in columns]
            self.preview_tree.insert('', 'end', values=values)
    
    def process_data(self):
        """Process the loaded data with the Candidate Elimination algorithm"""
        if self.current_data is None:
            messagebox.showerror("Error", "No data loaded")
            return
        
        try:
            # Get user-defined indicators
            positive_indicator = self.positive_var.get().strip()
            negative_indicator = self.negative_var.get().strip()
            
            if not positive_indicator or not negative_indicator:
                messagebox.showerror("Error", "Please specify both positive and negative indicators")
                return
            
            # Validate data
            target_column = self.current_data.columns[-1]
            unique_targets = self.current_data[target_column].unique()
            
            if positive_indicator not in unique_targets:
                messagebox.showerror("Error", f"Positive indicator '{positive_indicator}' not found in target column")
                return
            
            if negative_indicator not in unique_targets:
                messagebox.showerror("Error", f"Negative indicator '{negative_indicator}' not found in target column")
                return
            
            # Convert data to algorithm format
            processed_data = self.current_data.copy()
            processed_data[target_column] = processed_data[target_column].replace({
                positive_indicator: 'Yes',
                negative_indicator: 'No'
            })
            
            # Save processed data to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
                processed_data.to_csv(temp_file.name, index=False)
                temp_path = temp_file.name
            
            # Capture algorithm output
            import io
            from contextlib import redirect_stdout
            
            output_buffer = io.StringIO()
            
            # Run algorithm and capture output
            with redirect_stdout(output_buffer):
                run_candidate_elimination(temp_path)
            
            algorithm_output = output_buffer.getvalue()
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            # Display results
            self.display_results(algorithm_output, positive_indicator, negative_indicator)
            
            # Save to history
            self.save_to_history(algorithm_output, positive_indicator, negative_indicator)
            
            # Switch to results tab
            self.notebook.select(1)
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
    
    def display_results(self, algorithm_output, positive_indicator, negative_indicator):
        """Display the algorithm results in a formatted way"""
        self.results_text.delete(1.0, tk.END)
        
        # Header
        header_text = "CANDIDATE ELIMINATION ALGORITHM RESULTS\n"
        header_text += "=" * 50 + "\n\n"
        self.results_text.insert(tk.END, header_text, "header")
        
        # File info
        file_info = f"File: {os.path.basename(self.current_file_path)}\n"
        file_info += f"Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        file_info += f"Positive Indicator: '{positive_indicator}'\n"
        file_info += f"Negative Indicator: '{negative_indicator}'\n\n"
        self.results_text.insert(tk.END, file_info, "highlight")
        
        # Algorithm output
        self.results_text.insert(tk.END, "ALGORITHM OUTPUT:\n", "subheader")
        self.results_text.insert(tk.END, "-" * 20 + "\n")
        self.results_text.insert(tk.END, algorithm_output)
        
        # Enable save button
        self.save_results_btn.config(state='normal')
        
        # Store current results
        self.current_results = {
            'file_path': self.current_file_path,
            'positive_indicator': positive_indicator,
            'negative_indicator': negative_indicator,
            'output': algorithm_output,
            'timestamp': datetime.now().isoformat()
        }
    def save_results(self):
        """Save current results to file"""
        if not hasattr(self, 'current_results'):
            messagebox.showerror("Error", "No results to save")
            return
        
        try:
            # Generate filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"results_{timestamp}.txt"
            filepath = self.results_dir / filename
            
            # Save results
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("CANDIDATE ELIMINATION ALGORITHM RESULTS\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"File: {os.path.basename(self.current_results['file_path'])}\n")
                f.write(f"Processed: {self.current_results['timestamp']}\n")
                f.write(f"Positive Indicator: '{self.current_results['positive_indicator']}'\n")
                f.write(f"Negative Indicator: '{self.current_results['negative_indicator']}'\n\n")
                f.write("ALGORITHM OUTPUT:\n")
                f.write("-" * 20 + "\n")
                f.write(self.current_results['output'])
            
            messagebox.showinfo("Success", f"Results saved to: {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")
    
    def save_to_history(self, algorithm_output, positive_indicator, negative_indicator):
        """Save current processing to history"""
        history_entry = {
            'file_path': self.current_file_path,
            'file_name': os.path.basename(self.current_file_path),
            'positive_indicator': positive_indicator,
            'negative_indicator': negative_indicator,
            'output': algorithm_output,
            'timestamp': datetime.now().isoformat(),
            'display_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.results_history.append(history_entry)
        self.save_history()
        self.update_history_display()
    
    def load_history(self):
        """Load processing history from file"""
        history_file = self.results_dir / "history.json"
        try:
            if history_file.exists():
                with open(history_file, 'r', encoding='utf-8') as f:
                    self.results_history = json.load(f)
            else:
                self.results_history = []
        except Exception:
            self.results_history = []
    
    def save_history(self):
        """Save processing history to file"""
        history_file = self.results_dir / "history.json"
        try:
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(self.results_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save history: {e}")
    
    def update_history_display(self):
        """Update the history listbox"""
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.results_history):  # Show newest first
            display_text = f"{entry['display_timestamp']} - {entry['file_name']} ({entry['positive_indicator']}/{entry['negative_indicator']})"
            self.history_listbox.insert(tk.END, display_text)
    
    def load_from_history(self, event):
        """Load results from history when double-clicked"""
        selection = self.history_listbox.curselection()
        if not selection:
            return
        
        # Get the entry (remember we reversed the order)
        index = len(self.results_history) - 1 - selection[0]
        entry = self.results_history[index]
        
        # Display the historical results
        self.display_historical_results(entry)
        self.notebook.select(1)  # Switch to results tab
    
    def display_historical_results(self, entry):
        """Display historical results"""
        self.results_text.delete(1.0, tk.END)
        
        # Header
        header_text = "HISTORICAL RESULTS\n"
        header_text += "=" * 50 + "\n\n"
        self.results_text.insert(tk.END, header_text, "header")
        
        # Entry info
        info_text = f"File: {entry['file_name']}\n"
        info_text += f"Processed: {entry['display_timestamp']}\n"
        info_text += f"Positive Indicator: '{entry['positive_indicator']}'\n"
        info_text += f"Negative Indicator: '{entry['negative_indicator']}'\n\n"
        self.results_text.insert(tk.END, info_text, "highlight")
        
        # Algorithm output
        self.results_text.insert(tk.END, "ALGORITHM OUTPUT:\n", "subheader")
        self.results_text.insert(tk.END, "-" * 20 + "\n")
        self.results_text.insert(tk.END, entry['output'])
        
        # Disable save button for historical results
        self.save_results_btn.config(state='disabled')
    
    def clear_history(self):
        """Clear all processing history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            self.results_history = []
            self.save_history()
            self.update_history_display()
            messagebox.showinfo("Success", "History cleared successfully")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = CandidateEliminationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()