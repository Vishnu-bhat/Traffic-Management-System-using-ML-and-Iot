# 🚦 Intelligent Traffic Management System

A real-time, AI-powered traffic optimization platform developed in collaboration with the University of Gustave Eiffel, France, funded by CIFIPRA. The project leverages computer vision, machine learning, and IoT to minimize congestion at road intersections.

This project is a real-time, AI-driven traffic signal optimization system designed to minimize average vehicle delay across intersections using live video feeds, IoT infrastructure, and machine learning.

## 🌐 Overview

The system integrates live video processing, predictive modeling, and a responsive web dashboard to analyze and optimize traffic signal timing dynamically.

![Picture5](https://github.com/user-attachments/assets/cae2c66b-68f4-4809-bf2e-4a10d693b528)

## 📌 Project Highlights

- **Real-Time Vehicle Detection & Tracking**
  - YOLOv11 for custom object detection trained on Indian traffic scenarios.
  - DeepSORT for multi-object tracking and unique ID-based vehicle counting.

- **Edge Processing**
  - NVIDIA Jetson Nano used for on-device inference and video analytics.
  - Optimized using CUDA, cuDNN, and TensorRT.

- **Cloud Communication**
  - MQTT protocol used for lightweight real-time data transfer to AWS IoT Core.
  - Serverless backend using AWS Lambda, DynamoDB, and API Gateway.

- **Machine Learning**
  - XGBoost Regression model predicts optimal green signal durations.
  - Model trained on SUMO-simulated delay data for multiple signal configurations.

- **Visualization**
  - ReactJS frontend creates a digital twin of the intersection.
  - Displays live traffic status, vehicle counts, and signal timings.

## 🧠 Tech Stack

| Component          | Technology                |
|--------------------|---------------------------|
| Object Detection   | YOLOv11 (Custom-trained)  |
| Tracking           | DeepSORT                  |
| Edge Device        | NVIDIA Jetson Nano        |
| Cloud              | AWS IoT Core, Lambda, API Gateway, DynamoDB |
| ML Model           | XGBoost                   |
| Visualization      | ReactJS                   |
| Simulation         | SUMO                      |
| Data Pipeline      | MQTT                      |

## 🧪 Sample Workflow

1. Jetson Nano captures live traffic video → detects and tracks vehicles.
2. Count data is sent to AWS IoT Core via MQTT.
3. Data is stored in DynamoDB and processed via Lambda.
4. XGBoost model predicts optimal signal timings based on counts.
5. Frontend dashboard shows real-time signal state and vehicle flow.

## 📊 Model Performance

- **YOLOv11 + DeepSORT**
  - mAP@50: 0.913
  - mAP@50-95: 0.653
  - Tracking Accuracy: High under occlusions and dense traffic

- **XGBoost Model**
  - RMSE: 0.3679
  - R² Score: 0.80
  - Output: Green signal pair (e.g., 38s, 40s) with minimal average delay

## 🎓 Team

- Vishnu  
- Mohammed
- Niya  
- Govind  
- Isaac  
- Under guidance of Dr. Shihabudheen K. V. & Dr. Munavar Fairooz C.

