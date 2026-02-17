## nnU-Net
 https://github.com/MIC-DKFZ/nnUNet

**Ce este:**

* Este o bibliotecă complet automată pentru segmentarea imagisticii medicale. Este o implementare automată și complet configurabilă a U-Net, creată de Fabian Isensee și echipa sa.

**Ce face special:**

* Nu trebuie să setezi manual arhitectura, preprocessing-ul sau hiperparametrii.
* Analizează datele tale și adaptează automat U-Net la ele.
* Include pipeline complet: augmentare, training, inference și post-processing.

**Avantaje:**

* A fost foarte performant în competițiile de segmentare medicală.
* Funcționează „out-of-the-box” pentru orice volum medical 3D sau 2D.

## 3D U-Net (pytorch-3dunet)
https://arxiv.org/abs/1606.06650 

https://github.com/wolny/pytorch-3dunet

**Ce este:**

* Este mai mult o implementare a arhitecturii 3D U-Net în PyTorch.O arhitectură de rețea pentru segmentarea volumetrică 3D, extensie a U-Net original.

**Cum funcționează:**

* Folosește straturi de convoluție și pooling 3D pentru a procesa datele, învățând caracteristici spațiale în toate cele trei dimensiuni.

**Proces manual:**

* Necesită definirea manuală a arhitecturii, preprocessing-ului (resampling, normalizare etc.) și a parametrilor de antrenament.

**Scop:**

* Oferă o arhitectură flexibilă și complexă care poate fi adaptată la probleme diferite.

## Tabel comparativ

| Aspect                         | nnU-Net                                                                                                   | 3D U-Net (pytorch-3dunet)                                                                                              |
| ------------------------------ | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Ce este                        | O implementare automată și complet configurabilă a U-Net, creată de Fabian Isensee și echipa sa.          | O arhitectură de rețea pentru segmentarea volumetrică 3D, extensie a U-Net original.                                   |
| Necesită configurare manuală?  | Nu. Analizează automat datele și setează arhitectura, preprocessing-ul și hiperparametrii.                | Da. Trebuie să alegi manual arhitectura, preprocessing-ul (resampling, normalizare etc.) și parametrii de antrenament. |
| Pipeline inclus                | Da. Include: augmentare, training, inference, post-processing. Funcționează „out-of-the-box”.             | Nu. Trebuie să construiești și să rulezi tu întregul pipeline.                                                         |
| Flexibilitate                  | Mai puțin flexibil în customizare profundă, dar adaptează automat rețeaua pentru datele tale.             | Foarte flexibil: poți modifica arhitectura, loss-ul, augmentările, dimensiunile rețelei etc.                           |
| Complexitate pentru utilizator | Mică. Poți începe direct cu datele tale.                                                                  | Mare. Necesită experiență pentru a alege corect toate setările.                                                        |
| Performanță                    | Foarte bună în competiții de segmentare medicală, recunoscut ca state-of-the-art „out-of-the-box”.        | Depinde de experiența și tuning-ul utilizatorului; poate fi foarte performant, dar necesită muncă.                     |
| Scop ideal                     | Segmentare rapidă și precisă pentru orice volum medical 3D sau 2D fără să te stresezi cu detalii tehnice. | Cercetare sau proiecte unde vrei să controlezi fiecare aspect al rețelei și pipeline-ului.                             |



---
---

# Reţele neuronale convoluţionale, Big Data şi Deep Learning în analiza automată de imagini


Aceasta lucrare este relevanta pentru proiectul nostru deoarece principiile CNN si transfer learning prezentate pot fi aplicate la segmentarea automata a arterei etmoidale anterioare in volume CBCT, ghidand alegerea arhitecturilor si metodologiei.


- **Date utilizate:** Lucrarea discuta aplicarea CNN in analiza automata a imaginilor, fara a se concentra pe un set specific de date.
- **Algoritm AI:** 
    - Prezentarea arhitecturilor CNN clasice, cum ar fi AlexNet si VGGNet, esentiale pentru invatarea caracteristicilor imaginii. 
    - Abordeaza principiile segmentarii automate, inclusiv folosirea Big Data pentru antrenarea retelelor. 

- **Performanta:** Nu sunt prezentate metrici specifice, dar lucrarea evidentiaza eficienta CNN in recunoasterea si clasificarea imaginilor.
- **Tehnologii:** Discuta despre utilizarea Big Data in antrenarea CNN, esentiala pentru segmentarea precisa a AEA.
- **Link:** https://journals.indexcopernicus.com/api/file/viewByFileId/1084300

---

### Comparatie arhitecturi CNN folosite in lucrare

| Caracteristica | AlexNet | VGGNet |
|----------------|---------|--------|
| An | 2012 | 2014 |
| Context | Una dintre primele arhitecturi CNN care a demonstrat performante remarcabile in recunoasterea imaginilor (ImageNet) | Dezvoltata de echipa Visual Geometry Group (Oxford), arhitectura mai adanca si mai regulata decat AlexNet |
| Structura | Mai multe straturi convolutionale, straturi de pooling si straturi complet conectate, cu functii de activare ReLU | Blocuri repetate de straturi convolutionale 3×3 si pooling, structura mai adanca |
| Caracteristici invatate | Contururi, texturi si forme, utile pentru detectia si clasificarea structurilor anatomice | Caracteristici mai detaliate ale imaginii, recunoastere detalii fine pentru segmentare medicala |
| Utilizare in imagistica medicala | Fundal pentru multe arhitecturi de segmentare medicala, invatare 2D | Transfer learning, adaptata pentru segmentarea medicala 3D, inclusiv CBCT, recunoastere detalii fine |
| Observatie | Este 2D si mai simpla decat modelele moderne | Mai adanca, ofera precizie mai buna in recunoasterea detaliilor fine |
| Link referinta | [AlexNet - Wikipedia](https://en.wikipedia.org/wiki/AlexNet) | [VGGNet - Wikipedia](https://en.wikipedia.org/wiki/VGGNet) |



---
---

# Beyond benchmarks: Towards robust artificial intelligence bone segmentation in socio-technical systems

Aceasta lucrare este relevanta pentru proiectul nostru deoarece prezinta una dintre cele mai extinse evaluari multicentrice ale performantei retelelor neuronale convolutionale 3D utilizate in segmentarea structurilor osoase pe imagini CT si CBCT, exact tipul de imagistica pe care il folosim pentru segmentarea arterei etmoidale anterioare (AEA).
Metodologia de analiza a robustetii modelelor si recomandarile privind calitatea imaginilor (voxel size, orientare, artefacte) pot fi aplicate direct in dezvoltarea si antrenarea unui sistem AI pentru detectia si segmentarea AEA.

- **Date utilizate:**
    - 1.000 de volume clinice CT si CBCT (de la 100 de pacienti) pentru a testa 3.7 milioane de combinatii de parametri de achizitie.
    - 19.218 segmentari evaluate, cu ground truth realizat manual de experti in chirurgie maxilo-faciala.
- **Algoritmi AI:**
    - Au fost analizate 20 de modele AI comerciale si academice pentru segmentarea mandibulei.
    - Arhitecturi utilizate: 3D-U-Net, nnU-Net, Swin-UNETR, DynUNet, 3D-VNet, U-Mamba etc.
    - Modelele au fost evaluate pe baza mai multor factori clinici si tehnici (voxel size, artefacte, rotatie, patologie).
- **Performanta:**
    - Media generala: Dice Similarity Coefficient (DSC) ≈ 81.7%.
    - Cele mai performante modele (bazate pe 3D-U-Net) au atins >90% DSC pe subseturi curate.
    - Performanta a scazut cu pana la 25% in conditii nefavorabile (artefacte, rotatii, osteosinteza, patologie).
    - Modelele antrenate exclusiv pe CBCT au avut o precizie medie cu 5% mai mare decat cele pe CT.
- **Tehnologii si librarii:**
    - Python 3.11, frameworkuri de tip MONAI, PyTorch, nnU-Net, metrici DeepMind (DSC, NSD, HD95, MASD).
    - Segmentarile de referinta realizate cu 3D Slicer si Mimics.
    - Codul de analiza este disponibil open-source: https://github.com/OMFSdigital/AI_Mandible_Benchmarking 
- **Link:** https://www.sciencedirect.com/science/article/pii/S0957417425036474 


---
---

# Segmentarea Structurilor Asemanatoare pe CBCT

Această lucrare demonstrează fezabilitatea utilizării nnU-Net direct pe date CBCT pentru segmentarea unei structuri tubulare din zona de interes, oferind o bază de încredere pentru proiect.

**Titlu Complet:** **Automatic Segmentation of the Nasolacrimal Canal: Application of the nnU-Net v2 Model in CBCT Imaging**

**Link:** https://www.mdpi.com/2077-0383/14/3/778

* **Problema Rezolvată:** Segmentarea automată a **Canalului Nasolacrimal (NLC)** pe imagini **CBCT**.
* **Relevanță Directă:**
  * Folosește **CBCT** (modalitatea de imagistică a proiectului tău).
  * Utilizează **nnU-Net** (framework-ul ideal de implementare).
  * Abordează o **structură tubulară** din vecinătatea sinusurilor etmoidale.
* **Date Folosite:** Volume CBCT.
* **Algoritmi AI:** **nnU-Net v2** (o variantă automată și optimizată a rețelei **3D U-Net**).
* **Obiectiv:** Obținerea unui instrument fiabil pentru clinicieni, similar scopului proiectului tău (îmbunătățirea planificării preoperatorii).
* **Performanțe Cheie:** Se raportează rezultate excelente de segmentare, confirmând că nnU-Net este robust și precis chiar și pe imaginile CBCT.
* **Tehnologii:** nnU-Net, Deep Learning (3D CNN).

---

# MONAI (Medical Open Network for AI)

Link GitHub: https://github.com/Project-MONAI/MONAI

* **Ce este:**
  * Un ecosistem software open-source bazat pe **PyTorch**, dedicat cercetării și dezvoltării Deep Learning exclusiv în domeniul imagisticii medicale 3D.

* **Ce face special:**
  * Oferă **flexibilitate și modularitate** superioară, fiind o alternativă la nnU-Net, ideală pentru experimentare academică.
  * Suportă implementări optimizate de **3D U-Net**, **V-Net** și arhitecturi moderne (ex. **Swin-UNETR** bazate pe Transformer).

* **Avantaje:**
  * Include utilitare puternice pentru gestionarea fișierelor **DICOM (.dcm)** și **NIFTI**.
  * Facilitează implementarea **transformărilor și augmentărilor 3D** specifice (rotiri, scalări), esențiale pentru a crește robustețea modelului pe volumele CBCT.
  * Permite controlul detaliat asupra funcțiilor de pierdere și optimizatorilor.
---