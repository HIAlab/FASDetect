from flask import Flask, request, jsonify, json
from flask_cors import CORS
import glob
import dill
import numpy as np

def create_app():
  app = Flask(__name__)
  CORS(app)

  model_dir = 'models/'
  models = []
  files = []

  def load_models():
    global files
    files = glob.glob(model_dir+'*')
    for file in files:
      print ("Loading ", file)
      models.append(dill.load( open( file, "rb" )))
      print (file, "loaded")

  load_models()

  # @app.route('/')
  # def index():
  #   return 'Available endpoints: \nmodels : GET list of available trained models\npredict : predict instance'

  # @app.route('/summary')
  #def summary():
  #    data = make_summary()
  #    response = app.response_class(
  #        response=json.dumps(data),
  #        status=200,
  #        mimetype='application/json'
  #    )
  #    return response

  # Refresh model directory, load all models and return list of models
  @app.route('/models')
  def return_available_models():
    load_models()
    return dict(enumerate(files))

  @app.route('/model-details')
  def return_model_details():
    return 'Details for specific models   (sensitivity, specificity, description, ...)'

  @app.route('/', methods = ['GET', 'POST'])
  @app.route('/predict', methods = ['GET', 'POST'])
  def predict_instance():

  #   print('REQUEST HEADERS\m', request.headers)
  #   print('REQUEST DATA\m', request.data)
  #   print('REQUEST FORM\m', request.form)
  #   print('REQUEST JSON\m', request.json)

    req_data = request.get_json()
    req_features = np.array(req_data['features']).reshape(1, -1)

    # only 6 features are used for prediction, but 14 features have been used to create the model
    # in order to obtain good imputations, but only 6 features have been used by the classifier
    # we need to transform the input to the model to the required input format (i.e. 14 dimensions)

    nan = float("nan")
    feature_idx =  [0,3,6,8,10,12]
    features = [nan] * 14
    for idx, value in enumerate(req_features[0]):
      features[feature_idx[idx]] = value
    features = np.array(features).reshape(1, -1)

  # unpickle specified models and their corresponding feature scalers

  #   model = pickle.load( open( "models/LGBMClassifier_20201223-21h37m52s.p", "rb" ))
    model = models[0]

    clf = model["model"]

    return jsonify(
        desc = model["desc"],
        predict = clf.predict(features).tolist()[0],
        predict_proba = clf.predict_proba(features).tolist()[0][1],
        scores = model["scores"],
        feature_names = model["feature_names"],
        name = model["name"],
        misc = model["misc"],
  #       feature_importances = clf.feature_importances_.tolist()
    )

  return app
