import streamlit as st
import pandas as pd
import numpy as np
import io

# Page configuration for a clean, professional corporate dashboard layout
st.set_page_config(page_title="SMETA 7.0 Social Compliance Digital Portal", layout="wide")

# Custom CSS styling to mirror the professional corporate theme
st.markdown("""
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1F4E79; margin-bottom: 5px; }
    .sub-header { font-size: 14px; font-style: italic; color: #595959; margin-bottom: 25px; }
    .kpi-card { background-color: #F2F4F8; padding: 20px; border-radius: 8px; border-left: 5px solid #1F4E79; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .kpi-val { font-size: 24px; font-weight: bold; color: #1F4E79; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">SMETA 7.0 Social Compliance Audit Digital Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Internal Operational Readiness & Labor Standards Audit Framework (Excluding Health & Safety)</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR: METADATA PROFILE INPUTS
# -----------------------------------------------------------------------------
st.sidebar.header("Audit Profile & Scope")
audited_entity = st.sidebar.text_input("Audited Entity", value="[Input Facility Name]")
audit_date = st.sidebar.date_input("Audit Execution Date")
lead_auditor = st.sidebar.text_input("Lead Auditor / HRBP", value="[Input Name]")
scope_profile = st.sidebar.text_area("Scope Parameters", value="Excluding HSE / Focused strictly on Governance, Policies, Employment Act 1955, and Supplier Reporting Awareness.")

# -----------------------------------------------------------------------------
# INITIAL DATA STRUCTURES
# -----------------------------------------------------------------------------
@st.cache_data
def get_initial_data():
    gov = [
        {"Ref ID": "GOV-01", "Sub-Category": "Legal Compliance", "Criteria Details": "Verify company possesses a valid Business Licence issued by the local municipal authority (e.g., DBKL, MBPJ, MBSA) reflecting current business activities.", "Objective Evidence / Records to Review": "Valid original local council business licence, renewal receipts, corresponding premises activity check."},
        {"Ref ID": "GOV-02", "Sub-Category": "Legal Compliance", "Criteria Details": "Review corporate registration records from Suruhanjaya Syarikat Malaysia (SSM) to validate business structure, directors, and legal status.", "Objective Evidence / Records to Review": "SSM Corporate Profile e-Info printout, Company Form 9, Form 24, Form 49."},
        {"Ref ID": "GOV-03", "Sub-Category": "Legal Compliance", "Criteria Details": "Ensure presence and validity of all sector-specific operating permits, manufacturing licenses, or transport/logistics certifications.", "Objective Evidence / Records to Review": "MITI/MIDA manufacturing licenses, KPDN approvals, specialized departmental operational green-lights."},
        {"Ref ID": "GOV-04", "Sub-Category": "Management Systems", "Criteria Details": "Evaluate presence of a formalized Management Systems Assessment (MSA) Social Compliance Policy signed by top management as required under SMETA 7.0.", "Objective Evidence / Records to Review": "Signed Ethical Trade / Social Compliance Policy statement posted on company boards and localized into native languages."},
        {"Ref ID": "GOV-05", "Sub-Category": "Management Systems", "Criteria Details": "Verify formal appointment of a trained, competent internal representative accountable for implementation of social and labor compliance standards.", "Objective Evidence / Records to Review": "Organizational chart, job description documents defining social compliance KPIs, training records/certificates for the designated manager."},
        {"Ref ID": "GOV-06", "Sub-Category": "Management Systems", "Criteria Details": "Check for established systems of internal monitoring, root-cause analysis, and systematic self-assessments to proactively capture labor non-compliances.", "Objective Evidence / Records to Review": "Internal audit schedules, past non-compliance tracking registers, preventive action records, annual management review minutes."},
        {"Ref ID": "GOV-07", "Sub-Category": "Business Ethics", "Criteria Details": "Assess presence of an Anti-Bribery and Corruption (ABC) Policy explicitly meeting Section 17A of the Malaysian Anti-Corruption Commission (MACC) Act.", "Objective Evidence / Records to Review": "Written ABC Policy documentation, signed employee anti-corruption codes, anti-bribery training attendance sheets across all ranks."},
        {"Ref ID": "GOV-08", "Sub-Category": "Business Ethics", "Criteria Details": "Verify functionality, security, and anonymity of workplace whistleblowing and grievance systems allowing workers to report ethical issues safely.", "Objective Evidence / Records to Review": "Whistleblowing tracking logs, dedicated anonymous dropboxes, external reporting hotlines, clear non-retaliation clause text."}
    ]

    lab = [
        {"Ref ID": "LAB-01", "Sub-Category": "Forced Labour", "Criteria Details": "Ensure absolute zero withholding of worker identity documentation, passports, or bank cards. Workers must retain unhindered custody of personal papers.", "Objective Evidence / Records to Review": "Passport and ID retention policy, worker interviews, physical verification of individualized secure lockers provided to foreign personnel."},
        {"Ref ID": "LAB-02", "Sub-Category": "Forced Labour", "Criteria Details": "Verify that workers have full freedom of movement and are not restricted from leaving workplace or accommodation parameters during non-work hours.", "Objective Evidence / Records to Review": "Security logs, worker interview transcripts, employee handbook clauses regarding resignation notice and gate access."},
        {"Ref ID": "LAB-03", "Sub-Category": "Recruitment", "Criteria Details": "Audit recruitment streams to ensure the 'Employer Pays Principle' is followed: zero fees or costs charged to workers for recruitment, visas, or onboarding.", "Objective Evidence / Records to Review": "Foreign worker agency agreements, itemized recruitment invoice trails, financial ledgers, direct worker interviews confirming zero fee payments."},
        {"Ref ID": "LAB-04", "Sub-Category": "Employment Contracts", "Criteria Details": "Confirm all workers hold valid written contracts of service clearly breaking down working conditions, compiled in a language they fully understand.", "Objective Evidence / Records to Review": "Sample contract templates for all source nationalities, signed employee duplicates, native language translated contracts on file."},
        {"Ref ID": "LAB-05", "Sub-Category": "Company Policy Framework", "Criteria Details": "Audit the standalone Company Grievance Policy to ensure clear, multi-tiered escalation pathways, protection against retaliation, and defined resolution timelines.", "Objective Evidence / Records to Review": "Formal written Grievance Policy document, evidence of distribution via employee handbook, signature sign-off records."},
        {"Ref ID": "LAB-06", "Sub-Category": "Company Policy Framework", "Criteria Details": "Verify the institutionalization of a comprehensive Sexual Harassment Prevention Policy that explicitly details reporting procedures, investigation frameworks, and a designated inquiry panel as mandated under Section 81B of the Employment Act 1955.", "Objective Evidence / Records to Review": "Standalone Sexual Harassment Policy document, committee appointment letters, training records for investigation panel members."},
        {"Ref ID": "LAB-07", "Sub-Category": "Company Policy Framework", "Criteria Details": "Review the formal Disciplinary Policy and Code of Conduct to ensure it contains objective progressive disciplinary steps, clearly outlines what constitutes minor/major misconduct, and formally details the Domestic Inquiry (DI) process while strictly banning financial penalties or physical punishments.", "Objective Evidence / Records to Review": "Written Disciplinary Policy, Domestic Inquiry guidelines/templates, employee handbook acknowledge sheets, past warning letter files."},
        {"Ref ID": "LAB-08", "Sub-Category": "Working Hours", "Criteria Details": "Verify normal working hours do not exceed 45 hours per week, matching the statutory ceiling mandated by the Employment Act 1955.", "Objective Evidence / Records to Review": "Electronic attendance swipe logs, daily roster allocations, payroll hours calculation files."},
        {"Ref ID": "LAB-09", "Sub-Category": "Working Hours", "Criteria Details": "Verify monthly overtime tracking ensures no employee exceeds the statutory cap of 104 overtime hours per month.", "Objective Evidence / Records to Review": "Monthly payroll records, overtime summary logs, exception reports flag-marking high-hour workers."},
        {"Ref ID": "LAB-10", "Sub-Category": "Working Hours", "Criteria Details": "Ensure standard cumulative working hours (normal + OT hours) do not consistently exceed the SMETA standard limit of 60 hours per week.", "Objective Evidence / Records to Review": "Weekly aggregate timecard summaries, peak-season overtime voluntary consent sign-off sheets."},
        {"Ref ID": "LAB-11", "Sub-Category": "Working Hours", "Criteria Details": "Check that all employees receive at least one full 24-hour statutory rest day for every 7 days of operation (Section 59 EA 1955).", "Objective Evidence / Records to Review": "Roster patterns, punch card audit trails showing consecutive days worked without gap gaps."},
        {"Ref ID": "LAB-12", "Sub-Category": "Wages & Benefits", "Criteria Details": "Verify that the basic base wage paid to all employees meets or exceeds the current Gazetted National Minimum Wage Order.", "Objective Evidence / Records to Review": "Payroll registers, individual electronic bank transfer vouchers (EPF/SOCSO portal receipts), basic rate checking."},
        {"Ref ID": "LAB-13", "Sub-Category": "Wages & Benefits", "Criteria Details": "Audit overtime calculations on standard working days to ensure payment is executed at a minimum of 1.5 times the hourly rate of pay (Section 60A(3)(a)).", "Objective Evidence / Records to Review": "Payroll calculation formulas, sample individual payslips checking basic rate to OT rate conversion."},
        {"Ref ID": "LAB-14", "Sub-Category": "Wages & Benefits", "Criteria Details": "Audit overtime compensation for work executed on assigned rest days to ensure statutory rates are applied correctly (2.0x basic hourly rate).", "Objective Evidence / Records to Review": "Rest day attendance rosters cross-checked with payroll itemized overtime disbursements."},
        {"Ref ID": "LAB-15", "Sub-Category": "Wages & Benefits", "Criteria Details": "Audit compensation for work executed on gazetted Public Holidays to ensure statutory rates are applied correctly (3.0x basic hourly rate).", "Objective Evidence / Records to Review": "Public holiday shift logs cross-referenced with payroll itemized payouts."},
        {"Ref ID": "LAB-16", "Sub-Category": "Wages & Benefits", "Criteria Details": "Verify regular and timely execution of monthly wage disbursements, arriving no later than the 7th day after the wage period ends (Section 19 EA 1955).", "Objective Evidence / Records to Review": "Corporate bank transmission receipts, monthly bank clearance dates, worker interview consensus."},
        {"Ref ID": "LAB-17", "Sub-Category": "Wages & Benefits", "Criteria Details": "Confirm provision of itemized, detailed payslips (digital or hardcopy) containing explicit transparency of hours, rates, allowances, and deductions.", "Objective Evidence / Records to Review": "Sample payslips across various operational segments, verification of itemized hours matching punch cards."},
        {"Ref ID": "LAB-18", "Sub-Category": "Wages & Benefits", "Criteria Details": "Ensure all payroll deductions are legally compliant, validly authorized, and strictly limited to statutory mandates or Section 24 EA 1955 allowances.", "Objective Evidence / Records to Review": "EPF/SOCSO/EIS monthly submission statements, PCB tax payment logs, formal JTK (Labor Dept) deduction approval letters if applying housing cuts."},
        {"Ref ID": "LAB-19", "Sub-Category": "Child Labour", "Criteria Details": "Enforce rigorous age-verification processes during the recruitment pipeline to guarantee zero deployment of child labor (under 15 years old).", "Objective Evidence / Records to Review": "Onboarding documentation checks, certified true copies of NRIC/Passports, age calculation verification protocols."},
        {"Ref ID": "LAB-20", "Sub-Category": "Young Workers", "Criteria Details": "If employing young persons (ages 15-18), verify absolute compliance with restrictions on hazardous tasks, machinery, and night shift limits.", "Objective Evidence / Records to Review": "Shift rosters, specific job placement matrix mapping, Children and Young Persons (Employment) Act 1966 documentation compliance."},
        {"Ref ID": "LAB-21", "Sub-Category": "Discrimination", "Criteria Details": "Verify active execution of a robust equal opportunity policy covering hiring, training, promotion, and remuneration parameters.", "Objective Evidence / Records to Review": "Hiring criteria files, performance review matrix tracking, demographic wage distribution data analysis."},
        {"Ref ID": "LAB-22", "Sub-Category": "Discrimination", "Criteria Details": "Evaluate SMETA 7.0 requirement for gender data tracking: verify HR actively gathers gender-differentiated data on wages and promotions to avoid equity gaps.", "Objective Evidence / Records to Review": "Gender-segregated corporate compensation structures, promotion rate reporting metrics by gender."},
        {"Ref ID": "LAB-23", "Sub-Category": "Freedom of Assoc.", "Criteria Details": "Verify workers are free to join trade unions, form independent committees, or establish dialogue forums without management interference.", "Objective Evidence / Records to Review": "Worker-Management Committee meeting minutes, forum charter outlines, worker interview testimony."},
        {"Ref ID": "LAB-24", "Sub-Category": "Grievance Communications", "Criteria Details": "Ensure presence of a highly accessible, multi-lingual, multi-channel grievance submission infrastructure for internal staff.", "Objective Evidence / Records to Review": "Grievance registry logs, tracking system files showing response times and resolutions, verbal/digital process guidelines."},
        {"Ref ID": "LAB-25", "Sub-Category": "Leave Entitlements", "Criteria Details": "Verify tracking and full allocation of statutory paid annual leave days and public holiday allocations matching Section 60D & 60F EA 1955.", "Objective Evidence / Records to Review": "Annual leave utilization trackers, public holiday schedule declarations, individual employee leave balances."},
        {"Ref ID": "LAB-26", "Sub-Category": "Leave Entitlements", "Criteria Details": "Check operational alignment with amended paid parental leave: minimum 98 days for maternity leave and 7 consecutive days for paternity leave.", "Objective Evidence / Records to Review": "HR maternity and paternity leave trackers, medical certificates files, payroll distribution files during parental leave windows."}
    ]

    sup = [
        {"Ref ID": "SUP-01", "Sub-Category": "Supply Chain Due Diligence", "Criteria Details": "Verify implementation of a formalized Supplier Code of Conduct embedding SMETA and ETI Base Code standards across all tier-1 suppliers.", "Objective Evidence / Records to Review": "Signed copy of Supplier Code of Conduct from active tier-1 vendors, procurement vendor onboarding checklists."},
        {"Ref ID": "SUP-02", "Sub-Category": "Supplier Reporting Awareness", "Criteria Details": "Audit the mechanisms deployed to ensure supplier worker grievance awareness. Verify that tier-1 suppliers explicitly educate their own workforce regarding the principal company's whistleblower channels, anonymous hotlines, or their own internal escalation pathways.", "Objective Evidence / Records to Review": "Supplier training toolkits, multi-lingual posters displayed on supplier premises, signed supplier acknowledgment forms, records of grievance reporting awareness campaigns targeting vendor personnel."},
        {"Ref ID": "SUP-03", "Sub-Category": "Supply Chain Due Diligence", "Criteria Details": "Assess presence of an active social compliance risk-mapping process to categorize and evaluate critical suppliers.", "Objective Evidence / Records to Review": "Supplier risk-matrix profiles, completed vendor Self-Assessment Questionnaires (SAQs), risk tiering summary spreadsheets."},
        {"Ref ID": "SUP-04", "Sub-Category": "Contractor Management", "Criteria Details": "Verify legal standing and social compliance binding of third-party labor service providers (e.g., security, cleaning, outsourced logistics).", "Objective Evidence / Records to Review": "Service level agreements (SLAs), valid business licenses of service agencies, signed ethical compliance addendums."},
        {"Ref ID": "SUP-05", "Sub-Category": "Contractor Management", "Criteria Details": "Conduct down-stream spot-checks on payroll and statutory contribution logs for third-party contractor personnel deployed on-site.", "Objective Evidence / Records to Review": "Anonymized sample payslips for on-site security guards/cleaners, EPF Borang A receipts from the contractor agency."},
        {"Ref ID": "SUP-06", "Sub-Category": "Sub-Contracting Controls", "Criteria Details": "Verify operational policies strictly manage and prevent unauthorized subcontracting or reliance on unmapped home-based workflows.", "Objective Evidence / Records to Review": "Standard purchasing terms, factory capacity evaluation trackers, subcontractor declaration forms."},
        {"Ref ID": "SUP-07", "Sub-Category": "Sub-Contracting Controls", "Criteria Details": "Check for an active tracker managing supplier non-compliances, corrective action progress tracking, and verification of closure.", "Objective Evidence / Records to Review": "Supplier Corrective Action Plan (CAPA) tracking logs, email communication trails, desktop verification audit notes."}
    ]
    
    # Initialize baseline response placeholders
    for item in gov + lab + sup:
        item["Compliance Status"] = "Compliant"
        item["Auditor Findings & Observed Evidence"] = ""
        item["Root Cause & CAPA Plan"] = ""
        
    return pd.DataFrame(gov), pd.DataFrame(lab), pd.DataFrame(sup)

# Initialize session state dataframes so user edits persist across tab changes
if 'df_gov' not in st.session_state:
    st.session_state.df_gov, st.session_state.df_lab, st.session_state.df_sup = get_initial_data()

# -----------------------------------------------------------------------------
# DYNAMIC CALCULATION ENGINE & REPORT PREP
# -----------------------------------------------------------------------------
df_all = pd.concat([st.session_state.df_gov, st.session_state.df_lab, st.session_state.df_sup], ignore_index=True)
total_criteria = len(df_all)
compliant_count = len(df_all[df_all["Compliance Status"] == "Compliant"])
nc_df = df_all[df_all["Compliance Status"].isin(["Minor NC", "Major NC", "Critical NC", "CAR"])]
nc_count = len(nc_df)
compliance_rate = (compliant_count / total_criteria) * 100 if total_criteria > 0 else 100.0

breakdown_data = {
    "Audit Domain Section": ["1. Governance & Management Systems", "2. Labour Practices & EA 1955", "3. Supply Chain Governance"],
    "Total Scope Items": [len(st.session_state.df_gov), len(st.session_state.df_lab), len(st.session_state.df_sup)],
    "Compliant Items": [
        len(st.session_state.df_gov[st.session_state.df_gov["Compliance Status"] == "Compliant"]),
        len(st.session_state.df_lab[st.session_state.df_lab["Compliance Status"] == "Compliant"]),
        len(st.session_state.df_sup[st.session_state.df_sup["Compliance Status"] == "Compliant"])
    ]
}
df_breakdown = pd.DataFrame(breakdown_data)
df_breakdown["Domain Score (%)"] = (df_breakdown["Compliant Items"] / df_breakdown["Total Scope Items"]) * 100

# -----------------------------------------------------------------------------
# PORTAL WORKSPACE INTERFACE TABS
# -----------------------------------------------------------------------------
tab_dash, tab_gov, tab_lab, tab_sup = st.tabs([
    "📊 Summary Dashboard", 
    "⚖️ 1. Governance & Management", 
    "🏃‍♂️ 2. Labour Practices & EA 1955", 
    "🤝 3. Supply Chain Due Diligence"
])

status_config = st.column_config.SelectboxColumn(
    "Compliance Status",
    help="Select localized workplace standard threshold match",
    options=["Compliant", "Minor NC", "Major NC", "Critical NC", "CAR", "N/A"],
    required=True
)

# --- TAB 1: SUMMARY DASHBOARD ---
with tab_dash:
    st.subheader("Real-Time Facility Compliance Analytics")
    
    # Render KPI Block cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card">Total Audit Scope Items<br><span class="kpi-val">{total_criteria}</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card">Compliant Checkpoints<br><span class="kpi-val" style="color:#2E7D32;">{compliant_count}</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card">Active Non-Compliances / CARs<br><span class="kpi-val" style="color:#C62828;">{nc_count}</span></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card">Overall Compliance Rating<br><span class="kpi-val">{compliance_rate:.1f}%</span></div>', unsafe_allow_html=True)
        
    # --- INTERACTIVE NON-COMPLIANCE VIEWER ---
    if nc_count > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander(f"🚨 Click to view details for the {nc_count} Active Non-Compliances", expanded=False):
            st.dataframe(
                nc_df[["Ref ID", "Sub-Category", "Criteria Details", "Compliance Status", "Auditor Findings & Observed Evidence"]], 
                use_container_width=True, 
                hide_index=True
            )
            
    st.markdown("---")
    st.markdown("### Profile Snapshot Details")
    st.write(f"**Target Company / Location:** {audited_entity} | **Audit Team Head:** {lead_auditor} | **Date Listed:** {audit_date}")
    
    st.markdown("### Sector Performance Metrics")
    st.dataframe(df_breakdown.style.format({"Domain Score (%)": "{:.1f}%"}), use_container_width=True)

# --- TAB 2: GOVERNANCE & MANAGEMENT ---
with tab_gov:
    st.markdown("### Pillar 1: Business Governance & Management Systems Assessment")
    st.session_state.df_gov = st.data_editor(
        st.session_state.df_gov,
        column_config={"Compliance Status": status_config},
        disabled=["Ref ID", "Sub-Category", "Criteria Details", "Objective Evidence / Records to Review"],
        use_container_width=True,
        key="editor_gov"
    )

# --- TAB 3: LABOUR PRACTICES & EA 1955 ---
with tab_lab:
    st.markdown("### Pillar 2: Labour Standards & Malaysian Employment Act 1955 Compliance")
    st.session_state.df_lab = st.data_editor(
        st.session_state.df_lab,
        column_config={"Compliance Status": status_config},
        disabled=["Ref ID", "Sub-Category", "Criteria Details", "Objective Evidence / Records to Review"],
        use_container_width=True,
        key="editor_lab"
    )

# --- TAB 4: SUPPLY CHAIN DUE DILIGENCE ---
with tab_sup:
    st.markdown("### Pillar 3: Supply Chain Governance & Contractor Due Diligence")
    st.session_state.df_sup = st.data_editor(
        st.session_state.df_sup,
        column_config={"Compliance Status": status_config},
        disabled=["Ref ID", "Sub-Category", "Criteria Details", "Objective Evidence / Records to Review"],
        use_container_width=True,
        key="editor_sup"
    )

# -----------------------------------------------------------------------------
# REPORT EXPORT GENERATION UTILITY (FULL EXCEL WORKBOOK)
# -----------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Export Audit Artifacts")

# Build the Excel file directly in memory
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a specific sheet
    df_breakdown.to_excel(writer, sheet_name='Summary_Dashboard', index=False)
    st.session_state.df_gov.to_excel(writer, sheet_name='1_Governance', index=False)
    st.session_state.df_lab.to_excel(writer, sheet_name='2_Labor_Practices', index=False)
    st.session_state.df_sup.to_excel(writer, sheet_name='3_Supply_Chain', index=False)

st.sidebar.download_button(
    label="⬇️ Download Full Audit Report (Excel)",
    data=buffer.getvalue(),
    file_name=f"SMETA_7.0_Full_Audit_{audited_entity.replace(' ', '_')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
