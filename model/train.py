import joblib

class Model:
    def predict(self, X):
        return [len(X[0]) * 100]  # simple fake calorie logic

model = Model()

joblib.dump(model, "model/model.pkl")

print("Model saved!")