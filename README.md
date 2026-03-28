# GunDetection_synthetic-data
# Gun Detection using Synthetic Data Generation

Overview
This project implements an end-to-end gun detection system using a **synthetic dataset** generated through hand detection and image overlay techniques.
Due to the lack of publicly available gun datasets and to incorporate a cost efficient approach, a custom pipeline was built to generate synthetic data resembleing realistic training data.
---
# Problem Statement
- Limited availability of real-world gun datasets  
- Difficulty in collecting and labeling such data
- aim to reduce the cost of overall process
- Need for an automated data generation approach

# Dataset creation
# Positive Dataset
- Started with ~10,000 positive hand images
- Overlaid 4 different gun PNGs to simulate real-world scenarios
- Applied augmentation techniques:
  - Horizontal flipping
  - Noise addition
  - Brightness adjustment
  - Darkening
- Generated ~200,000 positive samples

# Negative Dataset
- Collected ~300,000 negative images
- Includes:
  - Hands without guns
  - Human activity scenes
  - Background environments

# Final Dataset Ratio
- Positive : Negative ≈ 1 : 1.5

# The dataset was intentionally balanced with a higher proportion of negative samples to improve model robustness and reduce false detections in real-world scenarios.

# Solution Approach
The project follows a multi-stage pipeline:
1. Hand Detection  
2. Frame Extraction  
3. Gun Overlay  
4. Automatic Annotation  
5. Data Augmentation  
6. Data Cleaning  
7. Model Training  
8. Inference  

# Note
Final model weights are not included due to confidentiality constraints.

---

# 🔹 Author
Prit Bhadja
