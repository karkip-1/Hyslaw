Hy's Law Interactive Dashboard
This Streamlit application provides an interactive tool for analyzing clinical trial data to identify subjects meeting Hy's Law criteria based on laboratory test results.

Overview:
Hy's Law is a rule of thumb for predicting drug-induced liver injury. This dashboard:

Identifies subjects where:
ALT or AST > 3× Upper Limit of Normal (ULN)
Total Bilirubin > 2× ULN
Provides visualizations of key lab parameters across visits.
Allows users to explore and download individual subject data.

Features 
Upload SDTM.LB Dataset: Upload a CSV file containing laboratory data for analysis.
Custom Reference Ranges: Input ULN values for ALT, AST, and Total Bilirubin via the sidebar.
Interactive Visualizations: Generate dynamic plots of lab parameters for subjects meeting Hy's Law criteria.
Key Metrics: View the maximum values for ALT, AST, and Total Bilirubin.
Data Export: Download subject-specific data for further investigation.
