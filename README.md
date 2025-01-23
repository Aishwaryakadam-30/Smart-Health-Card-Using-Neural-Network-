# 🏥 Smart Health Card

Smart Health Card is an AI-powered health monitoring system that utilizes machine learning models to predict health outcomes based on user-provided data. This project includes a web interface and backend for processing health-related metrics.

---

## 📂 Project Structure
Smart Health Card ├── CNN_TESTING.py # CNN model for health predictions ├── dataset.csv # Dataset used for ML models ├── dm.py # Data management for the project ├── Health_Doctor_excercise_diet.csv # Health metrics and cardio data ├── ML_ALGORITHMS.py # Various ML algorithms ├── NN.h5 # Trained Neural Network model ├── Training.csv # Training dataset ├── Testing.csv # Testing dataset ├── TRAINING.py # ML model training script ├── manage.py # Django project manager ├── settings.py # Project settings ├── urls.py # URL routing for the web app ├── views.py # Handles requests and responses ├── models.py # Database models ├── admin.py # Django admin configuration ├── forms.py # User input forms ├── db.sqlite3 # SQLite database ├── requirements.txt # Dependencies list ├── README.md # Project documentation



---

## 🛠 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository

## Set up the virtual environment:
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

## Install dependencies:
pip install -r requirements.txt

## Apply database migrations:
python manage.py migrate

## Run the application:
python manage.py runserver

## Access the application:
Open your browser and visit http://127.0.0.1:8000/.


## 🧠 Models
CNN Model: Implements a convolutional neural network (CNN_TESTING.py) for health classification.
Neural Network: A pre-trained model (NN.h5) used for accurate predictions.
ML Algorithms: Custom algorithms implemented in ML_ALGORITHMS.py.

## 📊 Datasets
Health_Doctor_excercise_diet.csv – Health and cardio data.
dataset.csv – General health-related dataset.
Training.csv & Testing.csv – Used for model training and evaluation.

## 🚀 Usage
Train the model:
python TRAINING.py

## Test the model:
python CNN_TESTING.py

## Access web interface:
After running the server, use the web application to upload data and visualize health insights.

## 📷 Visualization
The project generates accuracy and loss graphs during training:
Model Accuracy: model_accuracy.png
Model Loss: model_loss.png

## 📧 Contact
For any inquiries or contributions, feel free to reach out:

Email: your-kadamaishu1999@gmail.com

⭐ If you found this project useful, consider giving it a star!



