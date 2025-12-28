import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# --- CONTEXT ---
# This script prototypes an "Autonomous Agent" workflow.
# In the full production version, this logic is handled by an LLM (e.g., GPT-4)
# via LangChain. For this prototype, we simulate the "Function Calling" 
# and "Process Mining" logic using Pandas to demonstrate the concept without API keys.

class TestBenchAgent:
    def __init__(self, data_path="test_bench_log.csv"):
        self.data_path = data_path
        self.df = None
        self.report = []

    def load_data(self):
        """Simulates the Agent reading a CSV file."""
        print(f"🤖 Agent: Loading data from {self.data_path}...")
        
        # GENERATE DUMMY DATA (Simulating a real log file)
        # Scenario: Engine RPM goes up, Oil Pressure drops (Process Deviation/Failure)
        timestamps = pd.date_range(start="2025-01-01 08:00", periods=600, freq="S")
        rpm = np.linspace(1000, 6000, 600) + np.random.normal(0, 50, 600)
        
        # Create a fault: Oil pressure drops when RPM > 5000 (Process Deviation)
        oil_pressure = 5.0 - (rpm / 2000)  # Normal physics
        # Add the anomaly
        oil_pressure[-100:] = oil_pressure[-100:] - 1.5 # Sudden drop
        
        self.df = pd.DataFrame({
            "Timestamp": timestamps,
            "RPM": rpm,
            "Oil_Pressure_bar": oil_pressure
        })
        self.df.to_csv(self.data_path, index=False)
        print("✅ Data Loaded and cached.")

    def analyze_process_stability(self):
        """
        Agent 'Tool': Checks for process deviations using statistical rules.
        (In production, the LLM decides to call this function).
        """
        print("🤖 Agent: Analyzing process stability (Process Mining)...")
        
        # Logic: Check if Oil Pressure drops below threshold while RPM is high
        critical_indices = self.df[
            (self.df["RPM"] > 5000) & (self.df["Oil_Pressure_bar"] < 1.0)
        ]
        
        if not critical_indices.empty:
            msg = f"⚠️ ALERT: Process Deviation detected! Oil Pressure dropped below 1.0 bar during High-RPM test."
            self.report.append(msg)
            print(msg)
        else:
            self.report.append("✅ Process is stable.")

    def generate_visualization(self):
        """Agent 'Tool': Creates a visualization of the anomaly."""
        print("🤖 Agent: Generating visualization chart...")
        
        plt.figure(figsize=(10, 6))
        
        # Plot RPM
        plt.subplot(2, 1, 1)
        plt.plot(self.df["Timestamp"], self.df["RPM"], color='blue', label='Engine RPM')
        plt.ylabel("RPM")
        plt.title("Test Run Analysis: RPM vs Oil Pressure")
        plt.grid(True)
        plt.legend()
        
        # Plot Oil Pressure
        plt.subplot(2, 1, 2)
        plt.plot(self.df["Timestamp"], self.df["Oil_Pressure_bar"], color='green', label='Oil Pressure (bar)')
        
        # Highlight the anomaly (last 100 points)
        plt.axvspan(self.df["Timestamp"].iloc[-100], self.df["Timestamp"].iloc[-1], color='red', alpha=0.3, label='Detected Deviation')
        
        plt.ylabel("Pressure (bar)")
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig("analysis_chart.png")
        print("✅ Chart saved as 'analysis_chart.png'.")

    def export_report(self):
        """Simulates the LLM writing a final summary."""
        with open("agent_report.md", "w") as f:
            f.write("# 🤖 Test Bench Analysis Report\n")
            f.write(f"**Date:** {pd.Timestamp.now()}\n\n")
            f.write("## 1. Process Analytics Findings\n")
            for line in self.report:
                f.write(f"- {line}\n")
            f.write("\n## 2. Visual Evidence\n")
            f.write("![Chart](analysis_chart.png)\n")
        print("✅ Report generated: 'agent_report.md'")

if __name__ == "__main__":
    # --- SIMULATION START ---
    agent = TestBenchAgent()
    agent.load_data()
    agent.analyze_process_stability() # Agent "decides" to check stability
    agent.generate_visualization()    # Agent "decides" to plot data
    agent.export_report()             # Agent summarizes results