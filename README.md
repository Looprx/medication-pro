# 💊 MedSafe Pro: AI-Powered Drug Safety System

**MedSafe Pro** is a Python-based web application designed to prevent dangerous polypharmacy (drug mixing) errors. It uses real-time medical APIs to detect toxic drug interactions, displays chemical structures, and uses an algorithmic inference engine to predict patient conditions based on their medication list.

built with **Streamlit**, **Python**, and **OpenFDA**.

---

## 🚀 Features

### 1. ⚠️ Advanced Interaction Checker
- Detects toxic combinations between two or more drugs.
- Generates a **Safety Matrix Table** showing the severity and clinical consequences of mixing specific medicines.
- Uses the **NIH RxNav API** for accurate, clinical-grade data.

### 2. 🔍 AI Disease Context Prediction
- Implements a reverse-inference logic to analyze the user's medication list.
- Predicts likely medical conditions (e.g., "User is likely managing Type 2 Diabetes") based on drug classes.

### 3. 🧪 Chemical & Pharmacological Data
- Fetches real-time **Chemical Formulas** (e.g., $C_9H_8O_4$).
- Displays **2D Molecular Structures** dynamically.
- Provides simplified "Clinical Usage" summaries for non-medical users.

### 4. 📱 User-Friendly Interface
- **Dropdown Selection:** Choose from common medications easily without typing.
- **Visual Alerts:** Color-coded warnings (Red for Danger, Green for Safe).
- **Tabbed Layout:** Organizes complex data into "Safety," "Predictions," and "Details."

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) (Python web framework)
- **Data Processing:** Pandas
- **APIs Used:** - **NIH RxNav:** For interaction checking.
  - **OpenFDA:** For drug labeling and usage.
  - **PubChem:** For chemical properties and images.
- **Chemical Informatics:** PubChemPy

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/medsafe-pro.git](https://github.com/your-username/medsafe-pro.git)
cd medsafe-pro
2. Install DependenciesCreate a virtual environment (optional but recommended) and install the required libraries:Bashpip install streamlit pandas requests pubchempy
3. Run the ApplicationBashstreamlit run app.py
The application will automatically open in your browser at http://localhost:8501.📂 Project Structuremedsafe-pro/
│
├── app.py              # Main application logic
├── requirements.txt    # List of dependencies
├── README.md           # Project documentation
└── assets/             # Images and icons (optional)
📸 Screenshots(Add screenshots of your app here)Landing PageInteraction MatrixDashboard ViewSafety Alerts⚠️ Medical DisclaimerIMPORTANT: This software is for educational and informational purposes only.It is not a substitute for professional medical advice, diagnosis, or treatment.The interaction data is fetched from public government databases (NIH/FDA) but may not cover all biological nuances.Always consult a licensed physician or pharmacist before changing any medication.🤝 ContributingContributions are welcome!Fork the ProjectCreate your Feature Branch (git checkout -b feature/AmazingFeature)Commit your Changes (git commit -m 'Add some AmazingFeature')Push to the Branch (git push origin feature/AmazingFeature)Open a Pull Request📄 LicenseDistributed under the MIT License. See LICENSE for more information.
### One More Step: The `requirements.txt`
For a GitHub project to be complete, you also need a `requirements.txt` file so others know which libraries to install. Create a file named `requirements.txt` and paste this inside:

```text
streamlit
pandas
requests
pubchempy
