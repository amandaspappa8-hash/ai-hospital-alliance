import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from "react";
import { getUser } from "@/lib/auth-storage";
const CATALOG = [
    {
        name: "Complete Blood Count (CBC)",
        icon: "🩸", color: "#ef4444",
        tests: [
            { name: "CBC with Differential", code: "CBC-DIFF", turnaround: "2h" },
            { name: "Hemoglobin & Hematocrit", code: "HGB-HCT", turnaround: "1h" },
            { name: "WBC Count", code: "WBC", turnaround: "1h" },
            { name: "Platelet Count", code: "PLT", turnaround: "1h" },
            { name: "RBC Count", code: "RBC", turnaround: "1h" },
            { name: "Reticulocyte Count", code: "RETIC", turnaround: "3h" },
            { name: "Peripheral Blood Smear", code: "PBS", turnaround: "4h" },
            { name: "ESR (Erythrocyte Sedimentation Rate)", code: "ESR", turnaround: "2h" },
        ]
    },
    {
        name: "Metabolic & Chemistry Panel",
        icon: "⚗️", color: "#f59e0b",
        tests: [
            { name: "Basic Metabolic Panel (BMP)", code: "BMP", turnaround: "2h" },
            { name: "Comprehensive Metabolic Panel (CMP)", code: "CMP", turnaround: "3h" },
            { name: "Fasting Blood Glucose", code: "FBG", turnaround: "1h" },
            { name: "Random Blood Glucose", code: "RBG", turnaround: "30min" },
            { name: "HbA1c (Glycated Hemoglobin)", code: "HBA1C", turnaround: "4h" },
            { name: "Urea / BUN", code: "UREA", turnaround: "2h" },
            { name: "Creatinine + eGFR", code: "CREAT", turnaround: "2h" },
            { name: "Uric Acid", code: "UA", turnaround: "2h" },
            { name: "Electrolytes (Na, K, Cl, CO2)", code: "ELEC", turnaround: "1h" },
            { name: "Calcium (Total & Ionized)", code: "CA", turnaround: "2h" },
            { name: "Magnesium", code: "MG", turnaround: "2h" },
            { name: "Phosphorus", code: "PHOS", turnaround: "2h" },
            { name: "Total Protein & Albumin", code: "TP-ALB", turnaround: "2h" },
            { name: "C-Reactive Protein (CRP)", code: "CRP", turnaround: "2h" },
            { name: "Procalcitonin (PCT)", code: "PCT", turnaround: "3h" },
        ]
    },
    {
        name: "Liver Function Tests (LFT)",
        icon: "🫀", color: "#f97316",
        tests: [
            { name: "ALT (Alanine Aminotransferase)", code: "ALT", turnaround: "2h" },
            { name: "AST (Aspartate Aminotransferase)", code: "AST", turnaround: "2h" },
            { name: "ALP (Alkaline Phosphatase)", code: "ALP", turnaround: "2h" },
            { name: "GGT (Gamma-Glutamyl Transferase)", code: "GGT", turnaround: "2h" },
            { name: "Total & Direct Bilirubin", code: "BILI", turnaround: "2h" },
            { name: "Albumin", code: "ALB", turnaround: "2h" },
            { name: "Total Protein", code: "TP", turnaround: "2h" },
            { name: "LDH (Lactate Dehydrogenase)", code: "LDH", turnaround: "2h" },
            { name: "Ammonia", code: "NH3", turnaround: "1h", note: "STAT only" },
            { name: "Protein Electrophoresis (SPEP)", code: "SPEP", turnaround: "24h" },
        ]
    },
    {
        name: "Cardiac Markers",
        icon: "❤️", color: "#dc2626",
        tests: [
            { name: "Troponin I / Troponin T (hsTnT)", code: "TROP", turnaround: "1h", note: "High sensitivity" },
            { name: "CK (Creatine Kinase)", code: "CK", turnaround: "2h" },
            { name: "CK-MB", code: "CKMB", turnaround: "2h" },
            { name: "BNP (B-type Natriuretic Peptide)", code: "BNP", turnaround: "1h" },
            { name: "NT-proBNP", code: "NTBNP", turnaround: "2h" },
            { name: "Myoglobin", code: "MYO", turnaround: "1h" },
            { name: "D-Dimer", code: "DDIM", turnaround: "1h" },
            { name: "Fibrinogen", code: "FIB", turnaround: "3h" },
            { name: "Homocysteine", code: "HCY", turnaround: "6h" },
        ]
    },
    {
        name: "Lipid Profile",
        icon: "🫧", color: "#a855f7",
        tests: [
            { name: "Total Cholesterol", code: "CHOL", turnaround: "2h" },
            { name: "HDL Cholesterol", code: "HDL", turnaround: "2h" },
            { name: "LDL Cholesterol (direct)", code: "LDL", turnaround: "2h" },
            { name: "Triglycerides", code: "TRIG", turnaround: "2h" },
            { name: "VLDL Cholesterol", code: "VLDL", turnaround: "2h" },
            { name: "Non-HDL Cholesterol", code: "NHDL", turnaround: "2h" },
            { name: "Apolipoprotein A1 & B", code: "APO", turnaround: "6h" },
            { name: "Lipoprotein(a) [Lp(a)]", code: "LPA", turnaround: "8h" },
        ]
    },
    {
        name: "Coagulation & Thrombosis",
        icon: "🩹", color: "#e11d48",
        tests: [
            { name: "PT / INR", code: "PT-INR", turnaround: "1h" },
            { name: "aPTT", code: "APTT", turnaround: "1h" },
            { name: "Thrombin Time", code: "TT", turnaround: "2h" },
            { name: "Anti-Xa Level (Heparin monitoring)", code: "ANTIXA", turnaround: "4h" },
            { name: "Protein C Activity", code: "PROTC", turnaround: "8h" },
            { name: "Protein S Activity", code: "PROTS", turnaround: "8h" },
            { name: "Antithrombin III", code: "AT3", turnaround: "8h" },
            { name: "Factor V Leiden Mutation", code: "FVL", turnaround: "5 days" },
            { name: "Prothrombin Gene Mutation (G20210A)", code: "PGM", turnaround: "5 days" },
            { name: "Lupus Anticoagulant", code: "LA", turnaround: "5 days" },
            { name: "Antiphospholipid Antibodies", code: "APLA", turnaround: "5 days" },
            { name: "MTHFR Mutation", code: "MTHFR", turnaround: "5 days" },
        ]
    },
    {
        name: "Thyroid & Endocrine",
        icon: "🦋", color: "#06b6d4",
        tests: [
            { name: "TSH (Thyroid Stimulating Hormone)", code: "TSH", turnaround: "4h" },
            { name: "Free T3 (Triiodothyronine)", code: "FT3", turnaround: "4h" },
            { name: "Free T4 (Thyroxine)", code: "FT4", turnaround: "4h" },
            { name: "Anti-TPO Antibodies", code: "ANTITPO", turnaround: "6h" },
            { name: "Anti-Thyroglobulin", code: "ANTITG", turnaround: "6h" },
            { name: "Cortisol (AM/PM)", code: "CORT", turnaround: "4h" },
            { name: "ACTH", code: "ACTH", turnaround: "6h" },
            { name: "Prolactin", code: "PRL", turnaround: "4h" },
            { name: "Growth Hormone", code: "GH", turnaround: "6h" },
            { name: "IGF-1 (Somatomedin C)", code: "IGF1", turnaround: "8h" },
            { name: "PTH (Parathyroid Hormone)", code: "PTH", turnaround: "4h" },
            { name: "Vitamin D (25-OH)", code: "VITD", turnaround: "6h" },
            { name: "Aldosterone", code: "ALDO", turnaround: "6h" },
            { name: "Renin Activity", code: "RENIN", turnaround: "8h" },
            { name: "Insulin + C-Peptide", code: "INS-CP", turnaround: "6h" },
        ]
    },
    {
        name: "Reproductive & Sex Hormones",
        icon: "🧬", color: "#ec4899",
        tests: [
            { name: "FSH (Follicle Stimulating Hormone)", code: "FSH", turnaround: "4h" },
            { name: "LH (Luteinizing Hormone)", code: "LH", turnaround: "4h" },
            { name: "Estradiol (E2)", code: "E2", turnaround: "4h" },
            { name: "Progesterone", code: "PROG", turnaround: "4h" },
            { name: "Total & Free Testosterone", code: "TEST", turnaround: "6h" },
            { name: "DHEA-Sulfate", code: "DHEAS", turnaround: "6h" },
            { name: "Beta-hCG (Pregnancy)", code: "BHCG", turnaround: "1h" },
            { name: "AMH (Anti-Müllerian Hormone)", code: "AMH", turnaround: "8h" },
            { name: "SHBG (Sex Hormone Binding Globulin)", code: "SHBG", turnaround: "6h" },
            { name: "Androstenedione", code: "ANDRO", turnaround: "8h" },
        ]
    },
    {
        name: "Immunology & Autoimmune Diseases",
        icon: "🛡️", color: "#8b5cf6",
        tests: [
            { name: "ANA (Antinuclear Antibodies)", code: "ANA", turnaround: "24h", note: "SLE screening" },
            { name: "Anti-dsDNA Antibodies", code: "DSDNA", turnaround: "24h", note: "SLE specific" },
            { name: "Anti-Sm Antibodies", code: "ANTISM", turnaround: "3 days" },
            { name: "Anti-SSA (Ro) / Anti-SSB (La)", code: "ROLA", turnaround: "3 days", note: "Sjögren's" },
            { name: "Anti-Scl-70 (Topoisomerase I)", code: "SCL70", turnaround: "3 days", note: "Scleroderma" },
            { name: "Anti-Jo-1", code: "JO1", turnaround: "3 days", note: "Myositis" },
            { name: "Rheumatoid Factor (RF)", code: "RF", turnaround: "4h" },
            { name: "Anti-CCP Antibodies", code: "ANTICCP", turnaround: "24h", note: "RA specific" },
            { name: "ANCA (c-ANCA / p-ANCA)", code: "ANCA", turnaround: "24h", note: "Vasculitis" },
            { name: "Anti-GBM (Goodpasture)", code: "ANTIGBM", turnaround: "3 days" },
            { name: "Complement C3 & C4", code: "C3C4", turnaround: "8h" },
            { name: "CH50 (Total Complement)", code: "CH50", turnaround: "8h" },
            { name: "IgG, IgA, IgM (Immunoglobulins)", code: "IGS", turnaround: "8h" },
            { name: "IgE (Total & Specific Allergen)", code: "IGE", turnaround: "24h" },
            { name: "Anti-Mitochondrial Ab (AMA)", code: "AMA", turnaround: "3 days", note: "PBC" },
            { name: "Anti-Smooth Muscle Ab (ASMA)", code: "ASMA", turnaround: "3 days", note: "Autoimmune hepatitis" },
            { name: "Anti-LKM1", code: "LKM1", turnaround: "5 days" },
            { name: "Cryoglobulins", code: "CRYO", turnaround: "5 days" },
            { name: "Beta-2 Microglobulin", code: "B2M", turnaround: "6h" },
            { name: "HLA Typing (A, B, C, DR, DQ)", code: "HLA", turnaround: "5 days", note: "Transplant" },
        ]
    },
    {
        name: "Tumor Markers & Oncology",
        icon: "🔬", color: "#dc2626",
        tests: [
            { name: "PSA (Prostate Specific Antigen)", code: "PSA", turnaround: "4h" },
            { name: "Free PSA / PSA Ratio", code: "FPSA", turnaround: "4h" },
            { name: "AFP (Alpha-Fetoprotein)", code: "AFP", turnaround: "4h", note: "HCC / Testicular" },
            { name: "CEA (Carcinoembryonic Antigen)", code: "CEA", turnaround: "4h", note: "Colorectal" },
            { name: "CA 19-9", code: "CA199", turnaround: "6h", note: "Pancreatic" },
            { name: "CA 125", code: "CA125", turnaround: "6h", note: "Ovarian" },
            { name: "CA 15-3", code: "CA153", turnaround: "6h", note: "Breast" },
            { name: "CA 72-4", code: "CA724", turnaround: "6h", note: "Gastric" },
            { name: "HE4 (Human Epididymis Protein 4)", code: "HE4", turnaround: "8h", note: "Ovarian" },
            { name: "Beta-hCG (Tumor marker)", code: "BHCG-T", turnaround: "4h" },
            { name: "LDH (Lymphoma marker)", code: "LDH-T", turnaround: "2h" },
            { name: "Calcitonin", code: "CALCI", turnaround: "6h", note: "Thyroid cancer" },
            { name: "Thyroglobulin", code: "TG", turnaround: "6h", note: "Post-thyroidectomy" },
            { name: "NSE (Neuron-Specific Enolase)", code: "NSE", turnaround: "8h", note: "Small cell lung" },
            { name: "Cyfra 21-1", code: "CYFRA", turnaround: "8h", note: "NSCLC" },
            { name: "SCC Antigen", code: "SCC", turnaround: "8h", note: "Squamous cell" },
            { name: "Chromogranin A", code: "CGA", turnaround: "24h", note: "Neuroendocrine" },
            { name: "S100 Protein", code: "S100", turnaround: "24h", note: "Melanoma" },
        ]
    },
    {
        name: "Nucleic Acid & PCR (DNA/RNA)",
        icon: "🧫", color: "#10b981",
        tests: [
            { name: "COVID-19 RT-PCR", code: "COVID-PCR", turnaround: "4h" },
            { name: "Influenza A/B PCR", code: "FLU-PCR", turnaround: "2h" },
            { name: "RSV PCR", code: "RSV-PCR", turnaround: "2h" },
            { name: "HBV DNA Quantitative", code: "HBV-DNA", turnaround: "24h" },
            { name: "HCV RNA Quantitative", code: "HCV-RNA", turnaround: "24h" },
            { name: "HIV-1 Viral Load", code: "HIV-VL", turnaround: "24h" },
            { name: "CMV PCR (Quantitative)", code: "CMV-PCR", turnaround: "24h" },
            { name: "EBV PCR (Quantitative)", code: "EBV-PCR", turnaround: "24h" },
            { name: "HSV 1/2 PCR", code: "HSV-PCR", turnaround: "8h" },
            { name: "VZV PCR", code: "VZV-PCR", turnaround: "8h" },
            { name: "BK Virus PCR", code: "BKV-PCR", turnaround: "24h", note: "Transplant" },
            { name: "Tuberculosis PCR (GeneXpert)", code: "TB-PCR", turnaround: "2h" },
            { name: "Chlamydia / Gonorrhea PCR", code: "CT-GC", turnaround: "8h" },
            { name: "HPV DNA Test (Genotyping)", code: "HPV-DNA", turnaround: "24h" },
            { name: "Sepsis PCR Panel (SeptiFast)", code: "SEPSIS", turnaround: "6h" },
            { name: "Meningitis/Encephalitis PCR Panel", code: "MEPAN", turnaround: "4h" },
            { name: "Respiratory Pathogen Panel (FilmArray)", code: "RESP-PAN", turnaround: "2h" },
            { name: "GI Pathogen PCR Panel", code: "GI-PAN", turnaround: "4h" },
            { name: "Digital PCR (ddPCR)", code: "DDPCR", turnaround: "48h" },
            { name: "mRNA Expression Analysis", code: "MRNA", turnaround: "5 days" },
        ]
    },
    {
        name: "Genetics & DNA Analysis",
        icon: "🔭", color: "#6366f1",
        tests: [
            { name: "Whole Exome Sequencing (WES)", code: "WES", turnaround: "21 days", note: "Rare diseases" },
            { name: "Whole Genome Sequencing (WGS)", code: "WGS", turnaround: "30 days" },
            { name: "Chromosomal Microarray (CMA)", code: "CMA", turnaround: "14 days" },
            { name: "Karyotyping", code: "KARYO", turnaround: "14 days" },
            { name: "FISH (Fluorescence In Situ Hybridization)", code: "FISH", turnaround: "7 days" },
            { name: "BRCA1 / BRCA2 Analysis", code: "BRCA", turnaround: "14 days", note: "Hereditary breast/ovarian" },
            { name: "TP53 Mutation Analysis", code: "TP53", turnaround: "14 days", note: "Li-Fraumeni" },
            { name: "EGFR Mutation (Lung)", code: "EGFR", turnaround: "10 days" },
            { name: "KRAS / NRAS / BRAF", code: "RAS-RAF", turnaround: "10 days", note: "Colorectal/Melanoma" },
            { name: "ALK / ROS1 Gene Fusion", code: "ALK-ROS", turnaround: "10 days", note: "Lung cancer" },
            { name: "JAK2 V617F Mutation", code: "JAK2", turnaround: "7 days", note: "Myeloproliferative" },
            { name: "BCR-ABL Quantitative (MRD)", code: "BCRABL", turnaround: "7 days", note: "CML monitoring" },
            { name: "FLT3 / NPM1 (AML)", code: "AML-PAN", turnaround: "7 days" },
            { name: "Factor V Leiden (DNA)", code: "FVL-DNA", turnaround: "7 days" },
            { name: "HLA Typing (Next Gen)", code: "HLA-NGS", turnaround: "10 days" },
            { name: "Pharmacogenomics Panel", code: "PGX", turnaround: "14 days", note: "Drug metabolism" },
            { name: "Carrier Screening Panel", code: "CARRIER", turnaround: "14 days" },
            { name: "Prenatal Genetic Screening (NIPT)", code: "NIPT", turnaround: "10 days" },
            { name: "Copy Number Variation (CNV)", code: "CNV", turnaround: "14 days" },
            { name: "Methylation Analysis", code: "METHYL", turnaround: "21 days" },
            { name: "Oncology Somatic Mutation Panel", code: "ONCO-PAN", turnaround: "14 days" },
            { name: "Hereditary Cancer Panel (50 genes)", code: "HCP50", turnaround: "21 days" },
            { name: "Mitochondrial DNA Analysis", code: "MTDNA", turnaround: "21 days" },
        ]
    },
    {
        name: "Microbiology & Infectious Disease",
        icon: "🦠", color: "#84cc16",
        tests: [
            { name: "Blood Culture (Aerobic + Anaerobic)", code: "BC", turnaround: "5 days" },
            { name: "Urine Culture & Sensitivity", code: "UC", turnaround: "48h" },
            { name: "Sputum Culture", code: "SC", turnaround: "48h" },
            { name: "Wound Swab Culture", code: "WC", turnaround: "48h" },
            { name: "Stool Culture & Ova/Parasites", code: "STOOL", turnaround: "48h" },
            { name: "CSF Culture (Meningitis)", code: "CSF", turnaround: "72h", note: "STAT" },
            { name: "AFB Culture (TB)", code: "AFB", turnaround: "6 weeks" },
            { name: "Fungal Culture", code: "FUNGAL", turnaround: "4 weeks" },
            { name: "HIV 1/2 Antibody + Ag", code: "HIV-AG", turnaround: "2h" },
            { name: "HBsAg / Anti-HBs / HBeAg", code: "HBV-SER", turnaround: "4h" },
            { name: "Anti-HCV", code: "HCV-AB", turnaround: "4h" },
            { name: "RPR / VDRL (Syphilis)", code: "SYPH", turnaround: "4h" },
            { name: "TPPA (Syphilis confirmatory)", code: "TPPA", turnaround: "8h" },
            { name: "Malaria RDT & Smear", code: "MAL", turnaround: "1h" },
            { name: "Brucella Serology", code: "BRUC", turnaround: "24h" },
            { name: "Widal Test", code: "WIDAL", turnaround: "6h" },
            { name: "Antifungal Sensitivity (MIC)", code: "AF-MIC", turnaround: "72h" },
        ]
    },
    {
        name: "Urinalysis & Renal",
        icon: "🧪", color: "#0ea5e9",
        tests: [
            { name: "Urinalysis (Complete)", code: "UA-COMP", turnaround: "1h" },
            { name: "Urine Microscopy", code: "UA-MICRO", turnaround: "1h" },
            { name: "Urine Protein / Creatinine Ratio", code: "PCR-U", turnaround: "2h" },
            { name: "24h Urine Protein", code: "24H-PROT", turnaround: "4h" },
            { name: "Urine Albumin/Creatinine (ACR)", code: "ACR", turnaround: "2h", note: "Diabetic nephropathy" },
            { name: "Urine Electrolytes (Na, K, Cl)", code: "UE", turnaround: "2h" },
            { name: "Urine Osmolality", code: "U-OSM", turnaround: "2h" },
            { name: "Cystatin C", code: "CYS-C", turnaround: "4h", note: "Better GFR marker" },
            { name: "Beta-2 Microglobulin (Urine)", code: "B2M-U", turnaround: "8h" },
        ]
    },
    {
        name: "Historical Disease & Prior Exposure",
        icon: "📋", color: "#94a3b8",
        tests: [
            { name: "Anti-HAV IgG (Hepatitis A immunity)", code: "HAV-IGG", turnaround: "6h" },
            { name: "Anti-HBc IgG (past HBV infection)", code: "HBCAB", turnaround: "4h" },
            { name: "Anti-HCV (past HCV exposure)", code: "HCV-PAST", turnaround: "4h" },
            { name: "Rubella IgG (immunity)", code: "RUB-IGG", turnaround: "6h" },
            { name: "CMV IgG (prior infection)", code: "CMV-IGG", turnaround: "6h" },
            { name: "EBV VCA IgG (prior EBV)", code: "EBV-IGG", turnaround: "6h" },
            { name: "Toxoplasma IgG", code: "TOXO-IGG", turnaround: "6h" },
            { name: "HSV 1/2 IgG", code: "HSV-IGG", turnaround: "6h" },
            { name: "Varicella-Zoster IgG", code: "VZV-IGG", turnaround: "6h" },
            { name: "Measles IgG (immunity)", code: "MEAS-IGG", turnaround: "6h" },
            { name: "Mumps IgG", code: "MUMP-IGG", turnaround: "6h" },
            { name: "IGRA (TB — QuantiFERON)", code: "IGRA", turnaround: "24h", note: "Latent TB" },
            { name: "Brucella IgG/IgM (past brucellosis)", code: "BRUC-IGG", turnaround: "24h" },
            { name: "Rheumatic Fever (ASO Titre)", code: "ASO", turnaround: "4h" },
            { name: "Lyme Disease IgG (past exposure)", code: "LYME-IGG", turnaround: "24h" },
            { name: "HIV-1 Western Blot (confirmatory)", code: "HIV-WB", turnaround: "48h" },
        ]
    },
    {
        name: "Drug Monitoring & Toxicology",
        icon: "💊", color: "#f43f5e",
        tests: [
            { name: "Digoxin Level", code: "DIG", turnaround: "4h" },
            { name: "Vancomycin Trough/Peak", code: "VANC", turnaround: "2h" },
            { name: "Aminoglycoside Levels", code: "AMINO", turnaround: "2h" },
            { name: "Lithium Level", code: "LITHI", turnaround: "2h" },
            { name: "Phenytoin Level", code: "PHENY", turnaround: "2h" },
            { name: "Valproate Level", code: "VALP", turnaround: "2h" },
            { name: "Carbamazepine Level", code: "CARBA", turnaround: "4h" },
            { name: "Cyclosporine (Tacrolimus)", code: "CNI", turnaround: "4h", note: "Transplant" },
            { name: "Methotrexate Level", code: "MTX", turnaround: "4h" },
            { name: "Paracetamol Level (OD)", code: "PARA-OD", turnaround: "1h", note: "Overdose" },
            { name: "Salicylate Level", code: "SAL", turnaround: "1h" },
            { name: "Toxicology Screen (Urine)", code: "TOX-U", turnaround: "2h" },
            { name: "Heavy Metal Screen (Pb, As, Hg)", code: "HEAVY", turnaround: "5 days" },
            { name: "Alcohol (Ethanol) Level", code: "ETOH", turnaround: "1h" },
        ]
    },
    {
        name: "Vitamins & Nutritional Status",
        icon: "🌿", color: "#22c55e",
        tests: [
            { name: "Vitamin D (25-OH D3)", code: "VITD3", turnaround: "6h" },
            { name: "Vitamin B12 (Cobalamin)", code: "B12", turnaround: "6h" },
            { name: "Folate (Folic Acid)", code: "FOLATE", turnaround: "6h" },
            { name: "Vitamin B1 (Thiamine)", code: "B1", turnaround: "24h" },
            { name: "Vitamin B6 (Pyridoxine)", code: "B6", turnaround: "24h" },
            { name: "Vitamin A (Retinol)", code: "VITA", turnaround: "24h" },
            { name: "Vitamin E (Tocopherol)", code: "VITE", turnaround: "24h" },
            { name: "Zinc", code: "ZINC", turnaround: "24h" },
            { name: "Copper", code: "COPPER", turnaround: "24h" },
            { name: "Selenium", code: "SELEN", turnaround: "5 days" },
            { name: "Iron Studies (Fe, Ferritin, TIBC, Transferrin)", code: "IRON", turnaround: "4h" },
            { name: "Pre-albumin (Prealbumin)", code: "PREAL", turnaround: "6h", note: "Nutritional marker" },
        ]
    },
];
export default function LabCatalogPage() {
    const [search, setSearch] = useState("");
    const [selectedCat, setSelectedCat] = useState(null);
    const [selectedTest, setSelectedTest] = useState(null);
    const user = getUser();
    const filtered = CATALOG.map(cat => ({
        ...cat,
        tests: cat.tests.filter(t => t.name.toLowerCase().includes(search.toLowerCase()) ||
            t.code?.toLowerCase().includes(search.toLowerCase()))
    })).filter(cat => (selectedCat ? cat.name === selectedCat : true) &&
        cat.tests.length > 0);
    const totalTests = CATALOG.reduce((a, c) => a + c.tests.length, 0);
    return (_jsxs("div", { style: {
            padding: "28px 32px", fontFamily: "Inter, Arial, sans-serif", color: "white",
        }, children: [_jsx("div", { style: {
                    position: "fixed", inset: 0, zIndex: 0, pointerEvents: "none",
                    backgroundImage: "linear-gradient(rgba(16,185,129,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(16,185,129,0.03) 1px,transparent 1px)",
                    backgroundSize: "60px 60px",
                } }), _jsxs("div", { style: { position: "relative", zIndex: 1, maxWidth: 1400, margin: "0 auto" }, children: [_jsxs("div", { style: { marginBottom: 24 }, children: [_jsx("div", { style: { fontSize: 12, color: "#10b981", fontWeight: 700, letterSpacing: 2, textTransform: "uppercase", marginBottom: 6 }, children: "\u25C8 AI HOSPITAL ALLIANCE \u2014 LAB CATALOG" }), _jsx("h1", { style: {
                                    margin: 0, fontSize: 28, fontWeight: 900,
                                    background: "linear-gradient(135deg,#fff,#94a3b8)",
                                    WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
                                }, children: "\uD83E\uDDEA Complete Laboratory Test Catalog" }), _jsxs("p", { style: { color: "#475569", fontSize: 13, marginTop: 6 }, children: [totalTests, " tests \u00B7 ", CATALOG.length, " categories \u00B7 WHO \u00B7 AACC \u00B7 CAP standards \u00B7 ", user?.name] })] }), _jsx("div", { style: { display: "grid", gridTemplateColumns: "repeat(5,1fr)", gap: 12, marginBottom: 22 }, children: [
                            { label: "Total Tests", value: totalTests, color: "#10b981" },
                            { label: "Categories", value: CATALOG.length, color: "#3b82f6" },
                            { label: "Genetics/DNA", value: "23+", color: "#6366f1" },
                            { label: "Immunology", value: "20+", color: "#8b5cf6" },
                            { label: "Tumor Markers", value: "18+", color: "#dc2626" },
                        ].map(({ label, value, color }) => (_jsxs("div", { style: { padding: "12px 16px", borderRadius: 14, background: `${color}08`, border: `1px solid ${color}22` }, children: [_jsx("div", { style: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }, children: label }), _jsx("div", { style: { fontSize: 22, fontWeight: 900, color, marginTop: 4 }, children: value })] }, label))) }), _jsxs("div", { style: { display: "flex", gap: 10, marginBottom: 20, flexWrap: "wrap" }, children: [_jsx("input", { value: search, onChange: e => setSearch(e.target.value), placeholder: "\uD83D\uDD0D Search any test by name or code...", style: {
                                    flex: 1, minWidth: 280, padding: "12px 16px", borderRadius: 12, fontSize: 14,
                                    background: "rgba(255,255,255,0.05)", border: "1px solid rgba(16,185,129,0.3)",
                                    color: "white", outline: "none",
                                } }), _jsx("button", { onClick: () => { setSearch(""); setSelectedCat(null); }, style: {
                                    padding: "12px 18px", borderRadius: 12, fontSize: 13, fontWeight: 700,
                                    background: "rgba(255,255,255,0.05)", border: "1px solid rgba(255,255,255,0.1)",
                                    color: "#94a3b8", cursor: "pointer",
                                }, children: "Clear" })] }), _jsxs("div", { style: { display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 24 }, children: [_jsx("button", { onClick: () => setSelectedCat(null), style: {
                                    padding: "6px 14px", borderRadius: 20, fontSize: 12, fontWeight: 700,
                                    background: !selectedCat ? "rgba(16,185,129,0.2)" : "rgba(255,255,255,0.04)",
                                    color: !selectedCat ? "#4ade80" : "#64748b",
                                    border: `1px solid ${!selectedCat ? "rgba(16,185,129,0.4)" : "rgba(255,255,255,0.08)"}`,
                                    cursor: "pointer",
                                }, children: "All Categories" }), CATALOG.map(cat => (_jsxs("button", { onClick: () => setSelectedCat(cat.name === selectedCat ? null : cat.name), style: {
                                    padding: "6px 14px", borderRadius: 20, fontSize: 12, fontWeight: 700,
                                    background: selectedCat === cat.name ? `${cat.color}22` : "rgba(255,255,255,0.04)",
                                    color: selectedCat === cat.name ? cat.color : "#64748b",
                                    border: `1px solid ${selectedCat === cat.name ? cat.color + "55" : "rgba(255,255,255,0.08)"}`,
                                    cursor: "pointer",
                                }, children: [cat.icon, " ", cat.name.split("(")[0].trim()] }, cat.name)))] }), _jsx("div", { style: { display: "flex", flexDirection: "column", gap: 16 }, children: filtered.map(cat => (_jsxs("div", { style: {
                                background: "linear-gradient(135deg,#0f172a,#1a2540)",
                                border: `1px solid ${cat.color}22`, borderRadius: 20, overflow: "hidden",
                            }, children: [_jsxs("div", { style: {
                                        padding: "16px 22px", display: "flex", alignItems: "center", gap: 12,
                                        background: `${cat.color}08`, borderBottom: `1px solid ${cat.color}22`,
                                    }, children: [_jsx("span", { style: { fontSize: 22 }, children: cat.icon }), _jsxs("div", { children: [_jsx("div", { style: { fontWeight: 800, color: "white", fontSize: 15 }, children: cat.name }), _jsxs("div", { style: { color: "#64748b", fontSize: 12 }, children: [cat.tests.length, " tests"] })] })] }), _jsx("div", { style: { padding: 16, display: "grid", gridTemplateColumns: "repeat(auto-fill,minmax(280px,1fr))", gap: 8 }, children: cat.tests.map((test, i) => (_jsxs("div", { onClick: () => setSelectedTest(selectedTest?.name === test.name ? null : test), style: {
                                            padding: "10px 14px", borderRadius: 10, cursor: "pointer",
                                            background: selectedTest?.name === test.name ? `${cat.color}18` : "rgba(255,255,255,0.03)",
                                            border: `1px solid ${selectedTest?.name === test.name ? cat.color + "55" : "rgba(255,255,255,0.06)"}`,
                                            transition: "all 0.2s",
                                        }, onMouseEnter: e => { if (selectedTest?.name !== test.name)
                                            e.currentTarget.style.background = `${cat.color}10`; }, onMouseLeave: e => { if (selectedTest?.name !== test.name)
                                            e.currentTarget.style.background = "rgba(255,255,255,0.03)"; }, children: [_jsxs("div", { style: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 8 }, children: [_jsx("div", { style: { fontWeight: 600, color: "white", fontSize: 13, lineHeight: 1.4 }, children: test.name }), test.code && (_jsx("span", { style: {
                                                            padding: "2px 8px", borderRadius: 6, fontSize: 10, fontWeight: 800,
                                                            background: `${cat.color}22`, color: cat.color, whiteSpace: "nowrap", flexShrink: 0,
                                                        }, children: test.code }))] }), _jsxs("div", { style: { display: "flex", gap: 8, marginTop: 6, flexWrap: "wrap" }, children: [test.turnaround && (_jsxs("span", { style: { fontSize: 10, color: "#64748b" }, children: ["\u23F1 ", test.turnaround] })), test.note && (_jsxs("span", { style: { fontSize: 10, color: cat.color, fontWeight: 600 }, children: ["\u2022 ", test.note] }))] })] }, i))) })] }, cat.name))) }), filtered.length === 0 && (_jsxs("div", { style: { textAlign: "center", padding: 60, color: "#64748b" }, children: [_jsx("div", { style: { fontSize: 40, marginBottom: 12 }, children: "\uD83D\uDD0D" }), _jsxs("div", { style: { fontSize: 16, fontWeight: 700 }, children: ["No tests found for \"", search, "\""] })] }))] })] }));
}
