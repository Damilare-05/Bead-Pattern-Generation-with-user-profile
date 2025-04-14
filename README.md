# Bead-pattern-generation-web-app

## Overview

The Bead Pattern Generator is an intelligent, user-centric system designed to automate the creation of bead patterns using machine learning and rule-based symmetry algorithms. By extracting key color information from images and applying various symmetry rules, the system transforms user-uploaded images and fashion product imagery into creative bead designs. An integrated web interface facilitates real-time interaction, allowing users to preview, modify, and save patterns, along with an innovative cost-estimation feature to aid in budgeting for creative projects.

## Aim & Objectives

### Aim

To design and implement an intelligent system that automates bead pattern creation using machine learning (K-means Clustering) combined with rule-based symmetry algorithms. The goal is to empower users to generate creative bead designs effortlessly while assessing production costs at a glance.

### Objectives

1. **Data Acquisition and Preprocessing:**  
   - Utilize the “Fashion Product Images (Small)” dataset along with user-uploaded images to extract key color and style information for simple bead designs.
   
2. **Color Extraction:**  
   - Implement a basic color extraction process using k-means clustering to derive user-friendly color palettes from the dataset and uploaded images.
   
3. **Pattern Generation:**  
   - Apply a rule-based method to generate initial bead layouts based on extracted color palettes, ensuring that recommendations are intuitive and adaptable.
   
4. **User Interface Design:**  
   - Develop a web interface that allows users to preview, modify, and interact with the generated bead patterns, providing immediate visual feedback.
   
5. **Cost-Estimation Feature:**  
   - Incorporate a cost-estimation module that links bead types and quantities to approximate prices, thereby helping users evaluate the financial feasibility of their designs.
   
6. **User Testing and Evaluation:**  
   - Conduct user tests to gather feedback on design quality, usability, and cost accuracy, leading to iterative improvements.

## System Architecture

The application is structured into modular components to promote clarity and maintainability:

- **Pattern Generation Module:**  
  Implements core logic for extracting color palettes via k-means clustering and generating bead patterns using various symmetry algorithms (vertical, horizontal, radial, random, and multiple 1D patterns).

- **User Interface Module:**  
  Developed using Streamlit, this module manages user interactions such as image uploads, real-time pattern preview, and editing. It also displays visual elements (e.g., progress indicators, galleries) and integrates with back-end functionalities.

- **Data Persistence Module:**  
  Utilizes SQLite and SQLAlchemy for storing user profiles, contact messages, and saved patterns. This module ensures that user data and generated patterns are managed persistently and securely.

- **Multipage Navigation:**  
  Leveraging Streamlit’s multipage capabilities, the application is organized into distinct pages—for instance, a home page for user registration and a dedicated page for bead pattern generation—thus streamlining the user experience.

## Features

- **Image-Based Color Extraction:**  
  Extracts dominant colors from both fashion product images and user-uploaded images using a k-means clustering algorithm.
  
- **Dynamic Pattern Generation:**  
  Offers multiple rule-based symmetry algorithms (vertical, horizontal, radial, and more) to generate diverse bead patterns.
  
- **Interactive Web Interface:**  
  Provides an accessible and responsive platform where users can easily upload images, preview generated patterns, adjust settings, and save results.
  
- **Cost Estimation:**  
  Integrates a cost-estimation feature that calculates the approximate production cost based on the bead count and individual bead cost.
  
- **Persistent Storage:**  
  Utilizes a database for managing user profiles and storing historical pattern data, enabling seamless user experience and data tracking.

## Installation & Setup

To run the Bead Pattern Generator locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/bead-pattern-generator.git
   cd bead-pattern-generator
   ```

2. **Install Dependencies:**
   Ensure you have Python 3.7 or later installed and run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   Launch the Streamlit application by executing:
   ```bash
   streamlit run multipage.py
   ```

4. **Usage:**
   - Visit the default web page in your browser.
   - Create a user profile or sign in.
   - Upload an image to generate bead patterns.
   - Customize pattern settings, preview results, and save patterns.
   - Evaluate cost estimations and browse saved designs.

## Contributing

Contributions are welcome! If you wish to add features, fix bugs, or propose enhancements, please follow these guidelines:
- Fork the repository.
- Create a new branch for your feature or fix.
- Submit a pull request with a detailed explanation of your changes.
- Ensure that your code adheres to the project’s coding standards and includes comments/documentation where necessary.

## Contributors

- **Talabi Damilare – Pattern Generation Logic:**  
  This contributor focused on the core generation logic, implementing machine learning techniques (k-means clustering) and a variety of rule-based symmetry algorithms to produce creative bead patterns.

- **kinola-IQ – Interface, Database, and Pattern Saving:**  
  This contributor was responsible for developing the user interface using Streamlit, managing database interactions through SQLite and SQLAlchemy, and implementing functionalities for saving and previewing bead patterns.

