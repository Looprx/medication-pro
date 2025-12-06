import streamlit as st
import requests
import pandas as pd
import pubchempy as pcp

# --- 1. APP CONFIGURATION (Professional Look) ---
st.set_page_config(
    page_title="MedSafe Pro",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to hide technical clutter and make it look like a medical app
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stAlert {
        padding: 10px;
        border-radius: 10px;
    }
    h1 {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATASETS (Common Meds for Dropdown) ---
# A list of common Indian/Global medications to make selection easy
COMMON_MEDS = [
    "Paracetamol", "Metformin", "Atorvastatin", "Amlodipine", 
    "Omeprazole", "Losartan", "Aspirin", "Ibuprofen", 
    "Azithromycin", "Amoxicillin", "Ciprofloxacin", "Pantoprazole",
    "Telmisartan", "Warfarin", "Clopidogrel", "Thyroxine", 
    "Montelukast", "Cetirizine", "Alprazolam", "Clonazepam"
]

# --- 3. INTELLIGENT FUNCTIONS ---

def get_drug_info(drug_name):
    """Fetches Usage (OpenFDA) and Formula (PubChem)"""
    info = {"usage": "Information not available in standard database.", "formula": "N/A", "cid": None}
    
    # A. Get Formula
    try:
        compounds = pcp.get_compounds(drug_name, 'name')
        if compounds:
            info["formula"] = compounds[0].molecular_formula
            info["cid"] = compounds[0].cid
    except:
        pass

    # B. Get Usage
    try:
        url = f'https://api.fda.gov/drug/label.json?search=openfda.brand_name:"{drug_name}"&limit=1'
        res = requests.get(url).json()
        if "results" in res:
            usage = res['results'][0].get('indications_and_usage', [''])[0]
            # Clean up text to make it readable
            info["usage"] = usage[:400] + "..." if usage else "No specific usage details found."
    except:
        pass
        
    return info

def predict_disease_context(drug_list):
    """
    AI Logic: Heuristic inference based on drug classes.
    Predicts what the patient might be suffering from.
    """
    predictions = []
    
    # Simple Knowledge Graph for Demo
    knowledge_base = {
        "metformin": "Type 2 Diabetes",
        "insulin": "Diabetes",
        "atorvastatin": "High Cholesterol / Heart Disease",
        "amlodipine": "High Blood Pressure (Hypertension)",
        "losartan": "High Blood Pressure",
        "omeprazole": "GERD / Acid Reflux",
        "pantoprazole": "Gastritis / Acid Reflux",
        "aspirin": "Pain or Heart Attack Prevention",
        "warfarin": "Blood Clotting Disorder (Thrombosis)",
        "alprazolam": "Anxiety / Panic Disorder",
        "montelukast": "Asthma / Allergies",
        "cetirizine": "Allergies",
        "thyroxine": "Hypothyroidism"
    }
    
    for drug in drug_list:
        clean_name = drug.lower()
        if clean_name in knowledge_base:
            predictions.append(f"**{drug}** suggests treatment for: *{knowledge_base[clean_name]}*")
    
    if not predictions:
        return ["Condition could not be predicted from this specific list."]
    return predictions

def check_real_interactions(drug_list):
    """
    Checks interactions using NIH RxNav API and returns a Matrix.
    """
    warnings = []
    rxcuis = {}
    
    # 1. Get IDs
    for name in drug_list:
        try:
            r = requests.get(f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={name}").json()
            if "idGroup" in r and "rxnormId" in r["idGroup"]:
                rxcuis[name] = r["idGroup"]["rxnormId"][0]
        except:
            continue

    # 2. Check Logic
    if len(rxcuis) < 2:
        return []

    ids = "+".join(rxcuis.values())
    url = f"https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis={ids}"
    
    try:
        r = requests.get(url).json()
        if "fullInteractionTypeGroup" in r:
            for group in r["fullInteractionTypeGroup"]:
                for chem in group["fullInteractionType"]:
                    for pair in chem["interactionPair"]:
                        # Capture the specific drug names involved in this clash
                        drug1 = chem["minConcept"][0]["name"]
                        drug2 = pair["interactionConcept"][0]["name"]
                        severity = pair["severity"]
                        desc = pair["description"]
                        warnings.append({"Drug A": drug1, "Drug B": drug2, "Severity": severity, "Effect": desc})
    except:
        pass
        
    return warnings

# --- 4. THE PROFESSIONAL UI ---

# Sidebar for Inputs
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3004/3004458.png", width=100) # Placeholder medical icon
    st.title("Patient Setup")
    
    # Feature 2: Dropdown list (Easier for user)
    selected_drugs = st.multiselect(
        "Select Medications from Database:",
        options=COMMON_MEDS,
        help="Start typing to search for a medicine"
    )
    
    # Option to add custom drug not in list
    custom_drug = st.text_input("Or add a medicine not in the list:")
    if custom_drug:
        selected_drugs.append(custom_drug)
        
    analyze = st.button("Run Safety Analysis", type="primary")

# Main Page Area
st.title("⚕️ MedSafe Pro")
st.caption("AI-Powered Drug Interaction & Disease Prediction System")

if analyze and selected_drugs:
    # Create Tabs for Organized View (Feature 7: Simple UI)
    tab1, tab2, tab3 = st.tabs(["⚠️ Safety Matrix", "🔍 Disease Prediction", "💊 Drug Details"])
    
    # --- TAB 1: INTERACTION CHECKER (Feature 6) ---
    with tab1:
        st.header("Interaction Analysis")
        
        interactions = check_real_interactions(selected_drugs)
        
        if interactions:
            st.error(f"⚠️ Warning: {len(interactions)} Potential Interactions Detected")
            
            # Create a Dataframe for the "Column Checking Thing"
            df = pd.DataFrame(interactions)
            
            # Display as a clean table
            st.dataframe(
                df, 
                column_config={
                    "Drug A": "Medicine 1",
                    "Drug B": "Medicine 2",
                    "Severity": st.column_config.TextColumn("Risk Level", help="N/A means data not specified"),
                    "Effect": "Clinical Consequence"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ No critical interactions found in the standard database.")
            st.info("Note: Always consult a doctor. This tool checks known chemical interactions only.")

    # --- TAB 2: AI DISEASE PREDICTION (Feature 3) ---
    with tab2:
        st.header("Patient Condition Analysis")
        st.markdown("Based on the medication list, the system predicts the user might be managing:")
        
        predictions = predict_disease_context(selected_drugs)
        
        for pred in predictions:
            st.markdown(f"- {pred}")
            
        st.warning("**Disclaimer:** This is an algorithmic prediction based on drug classes. It is not a clinical diagnosis.")

    # --- TAB 3: DETAILS & FORMULAS (Feature 1, 4, 5) ---
    with tab3:
        st.header("Pharmacological Details")
        
        for drug in selected_drugs:
            with st.expander(f"📄 Details for: {drug}"):
                details = get_drug_info(drug)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("**Chemical Formula:**")
                    # Render formula beautifully using LaTeX
                    if details['formula'] != "N/A":
                        st.latex(details['formula'])
                    else:
                        st.write("N/A")
                        
                    if details['cid']:
                        st.image(f"https://pubchem.ncbi.nlm.nih.gov/image/imagefly.cgi?cid={details['cid']}&width=300&height=300", caption="2D Structure")

                with col2:
                    st.markdown("**Clinical Use:**")
                    st.write(details['usage'])

elif analyze and not selected_drugs:
    st.warning("Please select at least one medication from the sidebar.")

else:
    # Welcome Screen
    st.markdown("""
    ### Welcome to MedSafe Pro
    This tool helps patients and caregivers avoid dangerous drug combinations.
    
    **How to use:**
    1. Select your medicines in the sidebar.
    2. Click **Run Safety Analysis**.
    3. View the **Safety Matrix** to see if drugs conflict.
    """)
