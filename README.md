# Real-Time Emotion Detection Web Application

This project demonstrates a full-stack web application for real-time emotion detection in text. It leverages the power of pre-trained transformer models from Hugging Face to analyze user-provided text and instantly display the probabilities of various emotions. The application provides a user-friendly interface, user authentication, a history of past analyses, and a responsive UI.

## Features

*   **Real-time Emotion Analysis:** Analyze text input and instantly see the predicted emotion probabilities.
*   **Interactive UI:**  Visualize emotion scores using dynamic progress bars for a clear and intuitive understanding.
*   **User Authentication:** Secure user accounts with registration and login functionality.
*   **Analysis History:**  Store and retrieve past analyses for logged-in users.
*   **Responsive Design:**  Adapts to different screen sizes for optimal viewing on various devices.
*   **Easy Deployment:**  Built with Flask, making it easy to deploy to various platforms.


## Technologies Used

*   **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Transformers (Hugging Face)
*   **Frontend:** HTML, CSS, JavaScript, Bootstrap
*   **Database:** SQLite (can be easily adapted to other databases like PostgreSQL)
*   **Model:** `SamLowe/roberta-base-go_emotions` (pre-trained emotion classification model)


## Installation and Setup

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/PriyanujBoruah/Emotion-Detector-from-Text.git
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    (Make sure you have a `requirements.txt` file with the necessary packages, or create one using `pip freeze > requirements.txt`)

4.  **Set up the Database:**

    ```bash
    flask db init        # Initializes the database
    flask db migrate     # Creates migration scripts
    flask db upgrade     # Applies the migrations
    ```

5.  **Run the App:**

    ```bash
    python app.py
    ```

6.  **Access the App:** Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1.  **Register/Login:** Create an account or log in if you already have one.
2.  **Enter Text:** Type or paste the text you want to analyze into the text area on the dashboard.
3.  **Analyze:** Click the "Analyze" button.
4.  **View Results:** The predicted emotion probabilities will be displayed instantly with progress bars.
5.  **View History:**  Logged-in users can access their analysis history on the dashboard.


## Project Structure

```
Emotion-Detector-from-Text/
├── app.py             # Main Flask application file
├── templates/
│   ├── layout.html     # Base template
│   ├── index.html      # Home page / dashboard
│   ├── login.html      # Login page
│   └── register.html   # Registration page
└── static/ style.css   # Static files (CSS)
```
