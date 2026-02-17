# 🤖 Descrierea Problemei Rezolvate cu Ajutorul Inteligenței Artificiale  

---

## 🩺 I. Descriere Plastică

În chirurgia endoscopică nazală (FESS – *Functional Endoscopic Sinus Surgery*), medicul operează în apropierea unor structuri foarte delicate din zona sinusurilor.  
Una dintre cele mai importante este **artera etmoidală anterioară (AEA)** — un vas subțire, dar vital.  
Dacă este lezată, pot apărea complicații grave precum:  
- 🩸 **hemoragii severe**,  
- 👁️ **hematom orbitar** sau chiar **pierderea vederii**,  
- ⏱️ prelungirea intervenției chirurgicale și creșterea riscului operator.

### 💡 De ce este important
Pentru a evita aceste situații, chirurgul are nevoie să știe **cu exactitate** unde se află AEA înaintea și în timpul operației.  
Aici intervine **inteligența artificială**, care poate analiza imaginile obținute prin **CBCT (Cone-Beam Computed Tomography)** și **identifica automat** această arteră.  

Astfel, AI-ul funcționează ca un **asistent digital** ce:
- învață din imagini etichetate de specialiști,  
- recunoaște artera în imagini noi,  
- o marchează vizual, oferind medicului o „hartă” clară și precisă a regiunii sensibile.  

Rezultatul? O intervenție **mai sigură, mai rapidă și mai predictibilă** pentru pacient.

---

### 👥 Cine sunt utilizatorii
- **Chirurgii ORL**, care efectuează operațiile FESS și folosesc segmentarea pentru orientare preoperatorie și intraoperatorie.  
- **Radiologii**, care interpretează imaginile CBCT și pot verifica automat rezultatele segmentării.  
- **Sistemele de navigație chirurgicală**, care pot integra datele de segmentare AI pentru ghidaj 3D în timp real.

---

### 📥 Date de intrare și 📤 Date de ieșire
- **Date de intrare:** imagini medicale CBCT ce surprind structurile sinusurilor.  
- **Date de ieșire:** imaginea originală cu **artera etmoidală anterioară evidențiată vizual** (prin culoare sau contur).  

🔍 Pe scurt: AI-ul „vede” ce ochiul uman ar putea rata și ajută medicul să se orienteze mai sigur în timpul intervenției.

---

## 🧪 II. Descriere Formală

### **A. Ce se rezolvă**
Se dezvoltă un sistem bazat pe **inteligență artificială** capabil de **segmentare automată** a **arterei etmoidale anterioare (AEA)** pe imagini medicale **CBCT (Cone-Beam Computed Tomography)**.  
Scopul este obținerea unei **măști binare** care să delimiteze cu precizie AEA, pentru a sprijini analiza și planificarea chirurgicală.

---

### **B. Datele de intrare și ieșire**

**Date de intrare:**
- Imagini CBCT în format **DICOM**, care conțin structurile anatomice ale sinusurilor paranasale și vasculatura aferentă.  
- Opțional, **măști de segmentare manuale (Ground Truth)** realizate de experți, utilizate în etapa de antrenare a modelului.

**Fluxul de procesare:**
1. **Preprocesare:** corectarea intensităților, alinierea volumelor, filtrarea zgomotului.  
2. **Segmentare AI:** aplicarea unui model de *deep learning* (ex: U-Net, SegNet) pentru detectarea automată a arterei.  
3. **Postprocesare:** rafinarea marginilor, extragerea volumelor și generarea măștii finale.

**Date de ieșire:**
- 🩸 **Masca binară** a arterei etmoidale anterioare (valori 0/1).
    - Format posibil: **DICOM-RTStruct** – pentru integrarea directă în software medical sau navigație chirurgicală.
   
- 📊 **Metrici de performanță** – Dice, IoU, Hausdorff Distance, Mean Surface Distance.
  

---

### **C. Cum se măsoară performanța**

Performanța modelului AI este evaluată comparând segmentarea automată cu **segmentarea de referință (Ground Truth)** realizată de specialiști.

**Metrici de suprapunere (Overlap Metrics):**
- **Dice Similarity Coefficient (DSC):** gradul de suprapunere între segmentările AI și Ground Truth (valoare ideală: 1).  
- **Jaccard Index (IoU – Intersection over Union):** proporția de voxeli (unități volumetrice 3D) comuni între cele două segmentări.

**Metrici de distanță (Distance Metrics):**
- **Hausdorff Distance (HD):** măsoară cea mai mare distanță între marginile segmentărilor.  
- **Mean Surface Distance (MSD):** distanța medie între suprafețele segmentate.

---

### **D. Concluzie**

Prin aplicarea inteligenței artificiale la analiza imaginilor CBCT:
- se **automatizează** procesul de identificare a unei structuri critice (AEA),  
- se **reduce riscul intraoperator** și timpul de analiză,  
- iar chirurgul beneficiază de o **hartă tridimensională precisă**, care poate fi utilizată împreună cu sistemul de navigație, adaptată fiecărui pacient.
