from sentence_transformers import SentenceTransformer
import numpy as np
from typing import cast, Any


class EmbeddingServices:

    model = cast(Any, SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1"))

    @staticmethod
    def convertTextToVector( text: str) -> list[float]:
        vecotr = np.array(EmbeddingServices.model.encode(text)).reshape(1, -1)
        return vecotr[0].astype(float).tolist()

    @staticmethod
    def convertObjectToVectors(
         data: dict[str, Any]
    ) -> dict[str, None | str | list[float]]:
        vector_map: dict[str, list[float] | None | str] = {}
        for key, value in data.items():
            if isinstance(value, str):
                vector_map[key] = value
                vector_map[key + "_vector"] = EmbeddingServices.convertTextToVector(value)
            else:
                vector_map[key] = None
        return vector_map
