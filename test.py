import pandas as pd
from transformers import pipeline


try:
    classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    print("Emotion analysis model loaded successfully.")
except Exception as e:
    print(f"Error loading emotion analysis model: {e}")
    classifier = None


def predict_top_3_emotions(text):
    """Predicts the top 3 most likely emotions for a given text."""
    if classifier is None:
        return ["Error: Model not loaded"] 

    print(f"Predicting emotions for: '{text}'")
    model_output = classifier(text)[0]
    
    if isinstance(model_output, list) and len(model_output) > 0:
        sorted_emotions = sorted(model_output, key=lambda x: x['score'], reverse=True)
        top_3 = [emotion["label"] for emotion in sorted_emotions[:3]]
        return top_3
    else:
        return ["Error: No results from model"]



def evaluate_top_3_accuracy(csv_filepath):
    """Evaluates top-3 emotion detection accuracy using the provided method."""
    try:
        df = pd.read_csv(csv_filepath)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_filepath}' not found.")
        return

    correct_predictions = 0
    total_tweets = len(df)

    for index, row in df.iterrows():
        true_emotion = row["sentiment"]
        tweet = row["tweet"]

        predicted_emotions = predict_top_3_emotions(tweet)

        if true_emotion in predicted_emotions:
            correct_predictions += 1

    accuracy = correct_predictions / total_tweets if total_tweets > 0 else 0

    print("\n--- Top-3 Evaluation Results ---")
    print(f"Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    csv_filepath = "filtered_tweets.csv"
    evaluate_top_3_accuracy(csv_filepath)
