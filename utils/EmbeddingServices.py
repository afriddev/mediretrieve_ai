from sentence_transformers import SentenceTransformer
import numpy as np
from typing import cast, Any
from sklearn.metrics.pairwise import cosine_similarity
import fitz


class EmbeddingServices:
    model: Any = {}
    temp: dict[str, dict[str, Any]] = {}

    def __init__(self):
        self.model = cast(
            Any, SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")
        )
        self.temp = {"data": {}, "vectors": {}, "other": {}}

    def convertTextsToVector(self, texts: list[str]) -> list[float]:
        vectors = self.model.encode(
            texts, convert_to_numpy=True, normalize_embeddings=True
        ).astype(np.float32)
        return vectors.tolist()

    def convertObjectToVectors(
        self,
        data: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:

        try:
            if len(data.items()) == 0:
                self.temp["other"]["noData"] = None
                return self.temp

            tempKeys = [key for key, _ in data.items()]
            tempValues = [data[key] for key in tempKeys]
            vectors = self.convertTextsToVector(texts=tempValues)

            for index, _ in enumerate(tempValues):
                self.temp["data"][tempKeys[index]] = data[tempKeys[index]]
                self.temp["vectors"][tempKeys[index] + "_embedding"] = vectors[index]

        except Exception as e:
            print(e)
            self.temp["other"]["noData"] = None

        finally:

            return self.temp

    def convertArrayOfObjectsToVectors(self, data: list[dict[str, Any]]):
        temp = [value for obj in data for value in obj.values()]
        return self.convertTextsToVector(texts=temp)

    def extarctTextFromPdfFile(self) -> str:
        # import base64
        # from io import BytesIO
        # pdf_bytes = base64.b64decode(base64_string)
        # doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        extarctedText: Any = ""
        doc = fitz.open("a.pdf")
        for page in doc:
            p = cast(Any, page)
            extarctedText = extarctedText + p.get_text()
        return extarctedText

    @staticmethod
    def compareVectors(
        vector1: list[float], vector2: list[float], similarity: float
    ) -> bool:
        return (
            True
            if round(
                cosine_similarity(
                    cast(Any, np.array(vector1).reshape(1, -1)),
                    cast(Any, np.array(vector2).reshape(1, -1)),
                )[0][0],
                2,
            )
            >= similarity
            else False
        )

    @staticmethod
    def compareVectorOnListOfObjects(
        vector: list[float],
        arrayOfObjects: list[dict[str, list[float] | str | float]],
        similartiy: float,
    ) -> list[dict[str, str | float | list[float]]]:
        temp: list[dict[str, str | list[float] | float]] = []
        for obj in arrayOfObjects:
            for _, value in obj.items():
                if isinstance(value, list) and all(isinstance(v, float) for v in value):
                    if EmbeddingServices.compareVectors(vector, value, similartiy):
                        temp.append(obj)

        return temp
