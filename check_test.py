import os
import fasttext
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel


app = FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class LanguageDetect:
    def __init__(self):
        pretrained_language_modal = f"{BASE_DIR}/trained_modals/lid.176.bin"
        self.modal = fasttext.load_model(pretrained_language_modal)

    def identify_language(self, query):
        language_predictions = self.modal.predict(query)
        print("LANGUAGE PREDICTIONS: ", language_predictions)
        predicted_language = language_predictions[0][0].split("__label__")[1]
        print("PREDICTED LANGUAGE: ", predicted_language)
        return predicted_language


class RequestPayload(BaseModel):
    query: str
    language: str


@app.get("/lang-detect/")
def detect_language(payload: RequestPayload):
    response_data = {
        "status": "Success",
        "message": "",
        "error": ""
    }
    try:
        passed_payload = payload.dict()
        user_query = passed_payload["query"]
        selected_language = passed_payload["language"]
        if user_query and selected_language:
            obj_detect_lang = LanguageDetect()
            detected_language = obj_detect_lang.identify_language(user_query)
            if detected_language == selected_language:
                response_data["message"] = "Operation was successful"
            else:
                response_data["message"] = "Operation was unsuccessful"
    except Exception as err_except:
        response_data["status"] = "Failed"
        response_data["error"] = str(err_except)
    return response_data
