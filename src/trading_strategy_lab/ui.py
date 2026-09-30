"""Local desktop interface for authorized-history analysis; no broker connection."""
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from . import APP_NAME, AUTHOR
from .history import import_csv, summarize
from .market import import_ohlc_csv, ground_trade_entries
from .analysis import candidate_report
from .execution import ExecutionMode

class TradeTraceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} — By {AUTHOR}")
        self.geometry("900x650")
        self.trade_path = tk.StringVar(); self.ohlc_path = tk.StringVar()
        self.mode = tk.StringVar(value=ExecutionMode.ANALYSIS.value)
        self._build()

    def _file_row(self, parent, label, variable, command):
        ttk.Label(parent, text=label).pack(anchor="w", pady=(8, 0))
        row=ttk.Frame(parent); row.pack(fill="x")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Choose CSV", command=command).pack(side="left", padx=(8, 0))

    def _build(self):
        frame=ttk.Frame(self, padding=18); frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=APP_NAME, font=("Segoe UI", 24, "bold")).pack(anchor="w")
        ttk.Label(frame, text=f"By {AUTHOR}").pack(anchor="w")
        ttk.Label(frame, text="Analyze only history you are authorized to use. No broker or live order connection is enabled.").pack(anchor="w", pady=(8,0))
        self._file_row(frame, "MT4 / MT5 trade-history CSV", self.trade_path, lambda:self.trade_path.set(filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])) )
        self._file_row(frame, "Optional OHLC candle CSV", self.ohlc_path, lambda:self.ohlc_path.set(filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])) )
        modes=ttk.LabelFrame(frame,text="Execution mode",padding=8);modes.pack(fill="x",pady=12)
        for value in ExecutionMode: ttk.Radiobutton(modes,text=value.value.title(),value=value.value,variable=self.mode,command=self._mode_changed).pack(side="left",padx=8)
        self.mode_note=ttk.Label(modes,text="Analysis mode: no orders can be submitted.");self.mode_note.pack(side="left",padx=12)
        ttk.Button(frame,text="Analyze history",command=self.analyze).pack(anchor="w")
        self.output=tk.Text(frame,wrap="word",height=23,state="disabled",font=("Consolas",10));self.output.pack(fill="both",expand=True,pady=(12,0))

    def _mode_changed(self):
        mode=self.mode.get()
        self.mode_note.config(text="LIVE LOCKED: broker authorization, risk limits, and a separate MT5 adapter are required." if mode=="live" else f"{mode.title()} mode: no live orders are available in this version.")

    def analyze(self):
        if not self.trade_path.get(): messagebox.showerror(APP_NAME,"Choose a trade-history CSV first."); return
        try:
            trades=import_csv(self.trade_path.get()); result={"application":APP_NAME,"author":AUTHOR,"mode":self.mode.get(),"history":summarize(trades)}
            if self.ohlc_path.get():
                grounded=ground_trade_entries(trades,import_ohlc_csv(self.ohlc_path.get())); result["candidate_report"]=candidate_report(trades,grounded)
            self.output.config(state="normal");self.output.delete("1.0","end");self.output.insert("1.0",json.dumps(result,indent=2,default=str));self.output.config(state="disabled")
        except Exception as exc: messagebox.showerror("Import failed",str(exc))

def main(): TradeTraceApp().mainloop()
if __name__=="__main__": main()
