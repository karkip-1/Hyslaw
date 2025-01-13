#---------------------------------------------------------------------------
#Program Name   : hy_law_final.py
#Programmer     : Prafulla Karki
#Date           : 2025-01-12
#Purpose        : To create a Streamlit dashboard for visualizing and analyzing
#                 Hy's Law i.e Subject who meet Hy's law criteria
#---------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Title and Description
st.title("Hy's Law Interactive Dashboard")
st.markdown("""
Analyze clinical trial data to identify subjects meeting **Hy's Law criteria**:
- ALT or AST > 3× Upper Limit of Normal (ULN)
- Total Bilirubin > 2× ULN
""")

# GitHub CSV URL
github_csv_url = "https://raw.githubusercontent.com/karkip-1/demo/main/sdtm_lb_data.csv"  # Update with your actual raw GitHub URL

# Read Dataset from GitHub URL
try:
    df = pd.read_csv(github_csv_url)
    st.sidebar.markdown("### Dataset Summary")
    st.sidebar.write(df.describe())
except Exception as e:
    st.error(f"Error loading the dataset: {e}")
    st.stop()

# Sidebar: ULN Reference Ranges
st.sidebar.markdown("### Reference Ranges")
alt_uln = st.sidebar.number_input("ALT ULN (U/L)", value=40)
ast_uln = st.sidebar.number_input("AST ULN (U/L)", value=40)
bili_uln = st.sidebar.number_input("Total Bilirubin ULN (mg/dL)", value=1.2)

# Filter Lab Parameters
alt_df = df[df['LBTESTCD'] == 'ALT'].copy()
ast_df = df[df['LBTESTCD'] == 'AST'].copy()
tb_df = df[df['LBTESTCD'] == 'BILI'].copy()

# Identify Subjects Meeting Hy's Law Criteria
def identify_hys_law_subjects(alt_df, ast_df, tb_df, alt_uln, ast_uln, bili_uln):
    subjects_meeting_criteria = set()
    for subject in df['USUBJID'].unique():
        max_alt = alt_df[alt_df['USUBJID'] == subject]['LBSTRESN'].max()
        max_ast = ast_df[ast_df['USUBJID'] == subject]['LBSTRESN'].max()
        max_tb = tb_df[tb_df['USUBJID'] == subject]['LBSTRESN'].max()
        if (max_alt > 3 * alt_uln or max_ast > 3 * ast_uln) and max_tb > 2 * bili_uln:
            subjects_meeting_criteria.add(subject)
    return sorted(list(subjects_meeting_criteria))

# Generate Hy's Law Visualization
def plot_hys_law_subject(subject, alt_df, ast_df, tb_df, alt_uln, ast_uln, bili_uln):
    visits = sorted(df['VISITNUM'].unique())
    alt_values = alt_df[alt_df['USUBJID'] == subject].set_index('VISITNUM')['LBSTRESN']
    ast_values = ast_df[ast_df['USUBJID'] == subject].set_index('VISITNUM')['LBSTRESN']
    tb_values = tb_df[tb_df['USUBJID'] == subject].set_index('VISITNUM')['LBSTRESN']

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=visits, y=alt_values, mode='lines+markers', name='ALT',
        line=dict(color='blue'), hovertemplate='%{x}<br>ALT: %{y:.1f} U/L<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=visits, y=ast_values, mode='lines+markers', name='AST',
        line=dict(color='red'), hovertemplate='%{x}<br>AST: %{y:.1f} U/L<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=visits, y=tb_values, mode='lines+markers', name='Total Bilirubin',
        line=dict(color='green'), hovertemplate='%{x}<br>Bilirubin: %{y:.1f} mg/dL<extra></extra>'
    ))

    fig.add_hline(y=3*alt_uln, line_dash="dash", line_color="blue", annotation_text="3× ALT ULN")
    fig.add_hline(y=3*ast_uln, line_dash="dash", line_color="red", annotation_text="3× AST ULN")
    fig.add_hline(y=2*bili_uln, line_dash="dash", line_color="green", annotation_text="2× TB ULN")

    fig.update_layout(
        title=f"Hy's Law Analysis - Subject {subject}",
        xaxis_title="Visit Number",
        yaxis_title="Lab Values (ALT/AST in U/L, Total Bilirubin in mg/dL)",
        hovermode="x unified",
        height=600
    )

    return fig

# Process and Display Results
subjects_meeting_criteria = identify_hys_law_subjects(alt_df, ast_df, tb_df, alt_uln, ast_uln, bili_uln)

if not subjects_meeting_criteria:
    st.warning("No subjects meet Hy's Law criteria in this dataset.")
else:
    st.success(f"{len(subjects_meeting_criteria)} subjects meet Hy's Law criteria.")
    selected_subject = st.selectbox("Select Subject", subjects_meeting_criteria)
    plot = plot_hys_law_subject(selected_subject, alt_df, ast_df, tb_df, alt_uln, ast_uln, bili_uln)
    st.plotly_chart(plot, use_container_width=True)

    # Display Key Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        max_alt = alt_df['LBSTRESN'].max()
        st.metric("Max ALT", f"{max_alt:.1f} U/L", f"{(max_alt / alt_uln):.1f}×ULN")
    with col2:
        max_ast = ast_df['LBSTRESN'].max()
        st.metric("Max AST", f"{max_ast:.1f} U/L", f"{(max_ast / ast_uln):.1f}×ULN")
    with col3:
        max_tb = tb_df['LBSTRESN'].max()
        st.metric("Max Total Bilirubin", f"{max_tb:.1f} mg/dL", f"{(max_tb / bili_uln):.1f}×ULN")

    # Export Subject Data
    if st.button("Download Subject Data"):
        subject_data = df[df['USUBJID'] == selected_subject]
        csv = subject_data.to_csv(index=False)
        st.download_button("Download as CSV", data=csv, file_name=f"subject_{selected_subject}_data.csv")

