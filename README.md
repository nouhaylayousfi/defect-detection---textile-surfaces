# Automated Fabric Defect Detection System

This project implements an end-to-end automated fabric defect detection system for the textile industry using unsupervised anomaly detection.

## Overview

The system detects various fabric defects (tears, holes, stains, weaving irregularities) from single images captured in real-time. It relies solely on defect-free samples during training, eliminating the need for large labeled datasets of defective examples.

Key components:
- Deep learning-based anomaly detection with PatchCore
- Real-time visual feedback via Arduino-controlled LEDs (green for defect-free, red for defective)
- Remote monitoring through a ThingsBoard cloud dashboard
- CPU-based deployment for practical industrial use

## Dataset

The model was trained and evaluated on the TILDA Textile Texture Database. The dataset was split as follows:
- Training: 770 defect-free images 
- Validation: 132 defective images 
- Test: 130 mixed images 

## Requirements

- Python 3.11
- Anomalib library
- PyTorch
- OpenCV
- PySerial (for Arduino communication)
- Paho-MQTT (for ThingsBoard integration)
- Arduino IDE (for uploading the sketch)
