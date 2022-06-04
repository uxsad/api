from typing import List

import pandas as pd
import tensorflow as tf
from fastapi import FastAPI
from pydantic import BaseModel

from data import CollectedData

# import mlpack


# model = tf.keras.models.load_model('model.h5')

emotions = ['anger', 'contempt', 'disgust', 'engagement', 'fear', 'joy',
            'sadness', 'surprise', 'valence']
models = {e: tf.keras.models.load_model(f'models/emotions.{e}.h5') for e in emotions}


# def aggregate(data: List[CollectedData]):
#     # We assume that the list already contains all the old_data that need to be
#     # aggregated: no need to check timestamps!
#     # Add additional features
#     pairs = zip([None, *data, None], [None, *data, None][1:])
#     new_data = starmap(compute_features, pairs)
#     new_data = list(new_data)
#     print("\n".join(str(s) for s in new_data))
#     new_data = [e for _, e in new_data if e is not None]
#     # Aggregate using additional features
#     aggregated = list(new_data)
#     return aggregated


class EmotionsData(BaseModel):
    anger: int
    contempt: int
    disgust: int
    engagement: int
    fear: int
    joy: int
    sadness: int
    surprise: int
    valence: int


app = FastAPI()


@app.get("/")
def status():
    return {"status": "ok", "version": "1.0.0"}


# def get_model(emotion: str):
#     with open("models.yaml", "r") as f:
#         models = yaml.safe_load(f)
#     model = pickle.loads(
#         codecs.decode(models[emotion]['model'].encode(), "base64"))
#     return model


@app.post("/classify", response_model=List[EmotionsData])
def classify(data: List[CollectedData]):
    # agg = aggregate(data)
    # print("\n".join(str(s) for s in agg))
    dfs = pd.concat(
        map(pd.json_normalize, map(lambda x: x.dict(), data))).astype(
        'float32')
    # emotions = ['anger', 'contempt', 'disgust', 'engagement', 'fear', 'joy',
    #             'sadness', 'surprise', 'valence']
    results = {e: models[e].predict(dfs).flatten() for e in emotions}
    return pd.DataFrame(results).to_dict(orient='records')
    # return {e: mlpack.linear_svm(input_model=get_model(e), test=data) for e in emotions}
