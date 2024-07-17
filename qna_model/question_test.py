from src.data_loader import DatasetLoader

dl = DatasetLoader()

random_questions = dl.get_random_questions(datafile="sample1.csv", num=6)

print(random_questions)

