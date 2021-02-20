from tensorflow.keras.models import Sequential, save_model, load_model

model = load_model('main.h5')
model.summary()
