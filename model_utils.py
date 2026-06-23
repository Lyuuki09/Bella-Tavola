from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import joblib  # type: ignore
except Exception:  # pragma: no cover - optional dependency in this stage
    joblib = None


class LocalFallbackModel:
    """Fallback model with deterministic fraud scoring."""

    def predict_proba(self, features: Any) -> list[list[float]]:
        probabilities: list[list[float]] = []
        for row in features:
            valor, hora, distancia, tentativas, pais = row
            score = (
                0.003 * float(valor)
                + 0.02 * float(distancia)
                + 0.25 * float(tentativas)
                + 0.5 * float(pais)
                + (0.2 if int(hora) <= 5 else 0.0)
            )
            prob_fraude = max(0.0, min(0.999, score / 3.0))
            probabilities.append([1.0 - prob_fraude, prob_fraude])
        return probabilities

    def predict(self, features: Any) -> list[int]:
        return [1 if p[1] >= 0.5 else 0 for p in self.predict_proba(features)]


def _load_from_local_file(local_path: Path) -> Any:
    if joblib is None:
        return LocalFallbackModel()
    return joblib.load(local_path)


def load_model(
    repo_id: str,
    filename: str = "model.pkl",
    force_download: bool = False,
) -> Any:
    """
    Load model from local file or Hugging Face Hub.

    Strategy:
    1) use local file if available and no force download;
    2) attempt download from Hugging Face if repo_id is informed;
    3) fallback to local deterministic model.
    """
    local_path = Path(filename)
    if local_path.exists() and not force_download:
        return _load_from_local_file(local_path)

    if repo_id:
        try:
            from huggingface_hub import hf_hub_download  # type: ignore

            downloaded = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                force_download=force_download,
            )
            return _load_from_local_file(Path(downloaded))
        except Exception:
            if local_path.exists():
                return _load_from_local_file(local_path)

    return LocalFallbackModel()
