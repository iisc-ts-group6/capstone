
    # Load the fine-tuned model
    model = SentenceTransformer(FINETUNE_MODEL_PATH)
    
    test_examples = st.create_examples(test_df)
    # Evaluate the model on the test set
    test_sentences1 = [example.texts[0] for example in test_examples]
    test_sentences2 = [example.texts[1] for example in test_examples]
    test_labels = [example.label for example in test_examples]
    
    # Compute embeddings for test set
    embeddings1 = model.encode(test_sentences1)
    embeddings2 = model.encode(test_sentences2)

    # Compute cosine similarities
    cosine_similarities = [np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
                       for emb1, emb2 in zip(embeddings1, embeddings2)]
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    print(type(cosine_scores))
    print(cosine_scores)    
    
    # Threshold for determining equivalence (you may need to adjust this)
    threshold = 0.5

    # Make predictions
    test_predictions = [1 if sim >= threshold else 0 for sim in cosine_similarities]

    # Calculate accuracy
    accuracy = np.mean(np.array(test_predictions) == np.array(test_labels))
    print(f'Test Accuracy: {accuracy * 100:.2f}%')
    
    # Create a DataFrame to view the results
    results_df = pd.DataFrame({
        'sentence_1': test_sentences1,
        'sentence_2': test_sentences2,
        'label': test_labels,
        'prediction': test_predictions,
        'cosine_similarity': cosine_similarities
    })
    
    results_df.to_excel('qa_results.xlsx', index=False)