from sentence_transformers import SentenceTransformer

def predict(self, question, answer):
    if not self.model:
        raise ValueError("Model has not been loaded. Please load the model first.")
    self.model = SentenceTransformer(self.output_model_path)
    embeddings = self.model.encode([question, answer])
    similarity_score = self.cosine_similarity(embeddings[0], embeddings[1])

    # Save prediction results
    self.save_evaluation_metrics("prediction", similarity_score)

    return similarity_score
