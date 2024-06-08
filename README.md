# capstone
Cohort 2 group 6 Capstone project


# Project Title:
## Automated Answer Validation for Science Question Answering
### Overview and Problem Statement:
In the domain of scientific question answering, validating answers and providing accurate
feedback is critical for effective learning. The goal of this capstone project is to develop an
automated answer validation system using techniques like Siamese text similarity model, etc.
The system will compare student responses with the correct answer and distractors to
determine the level of correctness and provide appropriate feedback. The automated answer
validation system for science question answering will benefit educators and students in
science-related subjects. It will streamline the assessment process, reduce manual effort, and
ensure consistent evaluations, leading to improved learning outcomes in the science domain.

### Challenges:
1. Implementing a robust Siamese text similarity model for answer validation in the science
domain.
2. Preprocessing and structuring the dataset from the provided SCIQ dataset to create
meaningful pairs of student responses and correct answers.
3. Handling varying lengths of text data during model training and inference.
4. Addressing potential semantic ambiguities and domain-specific challenges in science
questions and responses.

### Data Description:
The SciQ dataset contains 13,679 crowdsourced science exam questions about Physics,
Chemistry and Biology, among others. The questions are in multiple-choice format with 4
answer options each. For the majority of the questions, an additional paragraph with
supporting evidence for the correct answer is provided. (string).
● answer1: One of the candidate answers for the question (string).
● answer2: One of the candidate answers for the question (string).
● answer3: One of the candidate answers for the question (string).
● answer4: One of the candidate answers for the question (string).
● correct_answer: The correct answer for the question (string).
● support: The supporting text for the question (string).

### Methodology:
● Combine the question and supporting text to create meaningful context for answer
validation in the science domain. Structure the data to form pairs of student responses
and correct answers, along with corresponding labels (0 for incorrect and 1 for correct).
● Implement a Siamese neural network architecture using NLP libraries and deep learning
frameworks. Train the model on the pairs of student responses and correct answers to
learn the underlying text representations
● MLOps Implementation: Develop an interface for educators to input student responses
and query the similarity model for validation in the science domain.
● Monitoring & Maintenance: Fine-tune the model and update the answer validation
system based on the evaluation results.
References:
1. SCIQ (Science Question Answering) dataset from Kaggle:
https://www.kaggle.com/datasets/thedevastator/sciq-a-dataset-for-science-question-an
swering
2. Siamese network for image and text similarity:
https://medium.com/@prabhnoor0212/siamese-network-keras-31a3a8f37d04

--- 

## Additional  Reference


#### SciEntsBank dataset Kaggle link
https://huggingface.co/datasets/nkazi/SciEntsBank/tree/main/data?show_file_info=data%2Ftrain-00001.parquet

#### Common commands used
See [COMMANDS.md](COMMANDS.md)

---