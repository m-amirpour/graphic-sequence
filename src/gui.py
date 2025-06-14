import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from graph_algorithm import GraphSequenceAnalyzer
from test_graph import TestCases

class GraphSequenceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Sequence Analyzer")
        
        # Configure the root window
        self.root.minsize(800, 600)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Helvetica', 12, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 11))
        style.configure('Info.TLabel', font=('Helvetica', 10))
        style.configure('Success.TLabel', foreground='green', font=('Helvetica', 10, 'bold'))
        style.configure('Error.TLabel', foreground='red', font=('Helvetica', 10, 'bold'))
        
        # Initialize variables
        self.current_graph_index = 0
        self.graphs = []
        
        # Get screen dimensions and set window size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        
        self.analyzer = GraphSequenceAnalyzer()
        self.test_cases = {
            name: (sequence, description) 
            for name, (sequence, description, _) in TestCases.get_test_cases().items()
        }
        self.test_cases["Custom Input"] = ([], "Enter your own sequence of non-negative integers, separated by commas.")
        
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI components with improved layout"""
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=2)
        main_container.rowconfigure(0, weight=1)
        
        # Create left and right panels
        left_panel = self.create_left_panel(main_container)
        right_panel = self.create_right_panel(main_container)
        
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
    def create_left_panel(self, parent):
        """Create the left panel with controls"""
        left_panel = ttk.Frame(parent)
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(3, weight=1)  # Make theory frame expandable
        
        # Test case selection
        test_frame = ttk.LabelFrame(left_panel, text="Test Cases", padding=(10, 5))
        test_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        test_frame.columnconfigure(1, weight=1)
        
        ttk.Label(test_frame, text="Select Test Case:", style='Header.TLabel').grid(
            row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        
        self.test_case_var = tk.StringVar()
        self.test_case_combo = ttk.Combobox(
            test_frame, 
            textvariable=self.test_case_var,
            values=list(self.test_cases.keys()),
            state="readonly",
            width=40
        )
        self.test_case_combo.grid(row=0, column=1, sticky="ew", pady=5)
        self.test_case_combo.set("Select a test case")
        self.test_case_combo.bind('<<ComboboxSelected>>', self.on_test_case_selected)
        
        # Input section with method selection
        input_frame = ttk.LabelFrame(left_panel, text="Sequence Input", padding=(10, 5))
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Method selection
        method_frame = ttk.Frame(input_frame)
        method_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(5, 10))
        method_frame.columnconfigure(1, weight=1)
        
        ttk.Label(method_frame, text="Checking Method:", style='Header.TLabel').grid(
            row=0, column=0, sticky="w", padx=(0, 10))
            
        self.method_var = tk.StringVar(value="both")
        methods = [
            ("Both Methods", "both"),
            ("Havel-Hakimi", "havel-hakimi"),
            ("Erdős-Gallai", "erdos-gallai")
        ]
        
        method_select = ttk.Frame(method_frame)
        method_select.grid(row=0, column=1, sticky="w")
        
        for text, value in methods:
            ttk.Radiobutton(
                method_select,
                text=text,
                value=value,
                variable=self.method_var
            ).pack(side=tk.LEFT, padx=5)
        
        # Sequence input
        ttk.Label(input_frame, text="Enter sequence:", style='Header.TLabel').grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        
        self.sequence_entry = ttk.Entry(input_frame)
        self.sequence_entry.grid(row=1, column=1, sticky="ew", pady=5)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="e", pady=(5, 10))
        
        ttk.Button(btn_frame, text="Analyze", command=self.analyze_sequence,
                  padding=(20, 5)).grid(row=0, column=0)
        
        # Results section
        self.results_frame = ttk.LabelFrame(left_panel, text="Results", padding=(10, 5))
        self.results_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        self.results_frame.columnconfigure(0, weight=1)
        
        # Theory section with scrollbar
        theory_frame = ttk.LabelFrame(left_panel, text="Theoretical Information", padding=(10, 5))
        theory_frame.grid(row=3, column=0, sticky="nsew")
        theory_frame.columnconfigure(0, weight=1)
        theory_frame.rowconfigure(0, weight=1)
        
        # Add scrollbar to theory text
        theory_scroll = ttk.Scrollbar(theory_frame)
        theory_scroll.grid(row=0, column=1, sticky="ns")
        
        self.theory_text = tk.Text(
            theory_frame,
            wrap=tk.WORD,
            width=40,
            height=10,
            yscrollcommand=theory_scroll.set,
            font=('Helvetica', 10),
            padx=5,
            pady=5
        )
        self.theory_text.grid(row=0, column=0, sticky="nsew")
        theory_scroll.config(command=self.theory_text.yview)
        self.theory_text.config(state=tk.DISABLED)
        
        return left_panel
        
    def create_right_panel(self, parent):
        """Create the right panel with graph visualization"""
        right_panel = ttk.Frame(parent)
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        
        # Graph visualization
        self.graph_frame = ttk.LabelFrame(right_panel, text="Graph Visualization", padding=(10, 5))
        self.graph_frame.grid(row=0, column=0, sticky="nsew")
        self.graph_frame.columnconfigure(0, weight=1)
        self.graph_frame.rowconfigure(0, weight=1)
        
        # Navigation controls
        nav_frame = ttk.Frame(right_panel, padding=(0, 5))
        nav_frame.grid(row=1, column=0, sticky="ew")
        nav_frame.columnconfigure(1, weight=1)
        
        self.prev_button = ttk.Button(
            nav_frame,
            text="◀ Previous",
            command=self.show_previous_graph,
            state=tk.DISABLED,
            padding=(10, 2)
        )
        self.prev_button.grid(row=0, column=0, padx=5)
        
        self.graph_label = ttk.Label(
            nav_frame,
            text="",
            style='Info.TLabel',
            anchor="center"
        )
        self.graph_label.grid(row=0, column=1)
        
        self.next_button = ttk.Button(
            nav_frame,
            text="Next ▶",
            command=self.show_next_graph,
            state=tk.DISABLED,
            padding=(10, 2)
        )
        self.next_button.grid(row=0, column=2, padx=5)
        
        return right_panel
        
    def show_current_graph(self):
        """Display the current graph with improved layout"""
        if not self.graphs:
            return
            
        # Clear previous graph
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
            
        # Create new figure that fills the frame
        fig = Figure(figsize=(8, 8), dpi=100, tight_layout=True)
        ax = fig.add_subplot(111)
        
        G = self.graphs[self.current_graph_index]
        pos = nx.spring_layout(G, k=1.5, iterations=50)  # Increased k for better spacing
        
        # Draw graph with enhanced visual properties
        nx.draw(G, pos, ax=ax,
               with_labels=True,
               node_color='#ADD8E6',  # Light blue
               node_size=2000,
               font_size=16,
               font_weight='bold',
               font_color='#000000',
               width=2,
               edge_color='#404040',
               alpha=0.9,
               bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        # Create canvas with improved size handling
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        
        # Make canvas expandable
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Update navigation label with more information
        total_graphs = len(self.graphs)
        self.graph_label.config(
            text=f"Realization {self.current_graph_index + 1} of {total_graphs}"
        )
        
    def analyze_sequence(self):
        """Analyze the input sequence with improved feedback"""
        try:
            # Get and clean the input
            sequence_text = self.sequence_entry.get().strip()
            if not sequence_text:
                messagebox.showwarning("Input Error", "Please enter a sequence")
                return
                
            sequence = [int(x.strip()) for x in sequence_text.split(',')]
            
            # Get selected method
            method = self.method_var.get()
            
            # Clear previous results
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            # Create results container with proper spacing
            results_container = ttk.Frame(self.results_frame)
            results_container.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
            results_container.columnconfigure(0, weight=1)
            
            # Check if sequence is graphic using selected method
            is_graphic = self.analyzer.is_graphic(sequence, method=method)
            
            # Add method used to results
            method_names = {
                'both': 'Both Methods',
                'havel-hakimi': 'Havel-Hakimi Algorithm',
                'erdos-gallai': 'Erdős-Gallai Theorem'
            }
            ttk.Label(results_container,
                     text=f"Method used: {method_names[method]}",
                     style='Info.TLabel').grid(
                         row=0, column=0, sticky="w", pady=2)
            
            if is_graphic:
                self.graphs = self.analyzer.generate_all_graphs(sequence)
                
                # Show detailed results
                ttk.Label(results_container, 
                         text="✓ The sequence is graphic",
                         style='Success.TLabel').grid(
                             row=1, column=0, sticky="w", pady=2)
                             
                ttk.Label(results_container,
                         text=f"Found {len(self.graphs)} different realization" + 
                              ("s" if len(self.graphs) != 1 else ""),
                         style='Info.TLabel').grid(
                             row=2, column=0, sticky="w", pady=2)
                
                if sequence:
                    ttk.Label(results_container,
                             text=f"Sum of degrees: {sum(sequence)}",
                             style='Info.TLabel').grid(
                                 row=3, column=0, sticky="w", pady=2)
                
                self.current_graph_index = 0
                self.show_current_graph()
                self.update_navigation_buttons()
            else:
                ttk.Label(results_container,
                         text="✗ The sequence is not graphic",
                         style='Error.TLabel').grid(
                             row=1, column=0, sticky="w", pady=2)
                
                # Show reason why it's not graphic
                if sum(sequence) % 2 != 0:
                    reason = "Sum of degrees must be even"
                elif max(sequence) >= len(sequence):
                    reason = "Maximum degree exceeds possible connections"
                else:
                    reason = "Violates degree sequence constraints"
                    
                ttk.Label(results_container,
                         text=f"Reason: {reason}",
                         style='Info.TLabel').grid(
                             row=2, column=0, sticky="w", pady=2)
                
                self.graphs = []
                self.clear_graph_display()
                
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter valid integers separated by commas"
            )
            
    def on_test_case_selected(self, event):
        """Handle test case selection"""
        selected = self.test_case_var.get()
        sequence, description = self.test_cases[selected]
        
        if selected == "Custom Input":
            self.sequence_entry.delete(0, tk.END)
            self.update_theory_text("Enter your own sequence of non-negative integers, separated by commas.")
            self.clear_graph_display()
            return
            
        self.sequence_entry.delete(0, tk.END)
        self.sequence_entry.insert(0, ", ".join(map(str, sequence)))
        
        # Update theory text
        self.update_theory_text(description)
        
        # Automatically analyze the sequence
        self.analyze_sequence()
        
    def update_theory_text(self, description: str):
        """Update theoretical information with proper formatting"""
        self.theory_text.config(state=tk.NORMAL)
        self.theory_text.delete(1.0, tk.END)
        self.theory_text.insert(tk.END, description)
        self.theory_text.config(state=tk.DISABLED)
        
    def show_next_graph(self):
        """Show next graph in the sequence"""
        if self.graphs and self.current_graph_index < len(self.graphs) - 1:
            self.current_graph_index += 1
            self.show_current_graph()
            self.update_navigation_buttons()
            
    def show_previous_graph(self):
        """Show previous graph in the sequence"""
        if self.graphs and self.current_graph_index > 0:
            self.current_graph_index -= 1
            self.show_current_graph()
            self.update_navigation_buttons()
            
    def update_navigation_buttons(self):
        """Update the state of navigation buttons"""
        if not self.graphs:
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
            self.graph_label.config(text="")
            return
            
        self.prev_button.config(
            state=tk.NORMAL if self.current_graph_index > 0 else tk.DISABLED)
        self.next_button.config(
            state=tk.NORMAL if self.current_graph_index < len(self.graphs) - 1 
            else tk.DISABLED)
            
    def clear_graph_display(self):
        """Clear the graph display area"""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        self.graph_label.config(text="")
        self.update_navigation_buttons()