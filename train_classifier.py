import math
from sklearn import neighbors
import pickle

with open("Face Encodings/encodings_main_32_class.pkl", "rb") as f:
    encodings_array = pickle.load(f)

with open("Face Encodings/class_names_main_32_class.pkl", "rb") as f:
    class_names = pickle.load(f)

# Create and train the KNN classifier
n_neighbors = int(round(math.sqrt(len(encodings_array))))
knn_classifier = neighbors.KNeighborsClassifier()
knn_classifier.fit(encodings_array, class_names)

print(f'[INFO] Saving Classifier model')
with open("Classifier/classifier_mine_knn_32_class_main.clf", 'wb') as f:
    pickle.dump(knn_classifier, f)
