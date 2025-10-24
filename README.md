# Stroke Prediction Demo

A simple end-to-end demonstration of deploying a machine learning model as a REST API using **FastAPI**, **Docker**, and **GCP**.

The project trains a basic logistic regression model on the [Kaggle Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset), then serves it through a lightweight FastAPI backend with a minimal HTML frontend.

## Quick Start

1. **Download dataset**
Download the [Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset)
from Kaggle and place `healthcare-dataset-stroke-data.csv` in the `data/` directory:

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **(Optional) Install `requests` for local testing**
```bash
pip install requests
```

4. **Train model (in Jupyter)**
Run `notebooks/train.ipynb` to train and save the model to `models/log_reg_model.joblib`.

5. **Start API**
```bash
uvicorn app.main:app --reload
```

6. **Access frontend**
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to use the web form.

7. **Build Docker Container**
```bash
docker build -t stroke-predictor .
```

8. **Run Docker Container**
```bash
docker run --rm -p 5000:5000 -e PORT=5000 stroke-predictor
```