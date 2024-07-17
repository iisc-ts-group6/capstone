from src.data_loader import DatasetLoader

dl = DatasetLoader()

random_questions = dl.get_random_questions(datafile="master_sheet_use.csv", num=5)

print(random_questions)

