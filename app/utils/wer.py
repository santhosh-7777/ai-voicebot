import jiwer
from app.utils.logger import get_logger

logger = get_logger("wer")

def calculate_wer(reference: str, hypothesis: str) -> dict:
    reference = reference.lower().strip()
    hypothesis = hypothesis.lower().strip()
    
    wer_score = jiwer.wer(reference, hypothesis)
    cer_score = jiwer.cer(reference, hypothesis)
    
    logger.info(f"WER: {wer_score:.2f} | CER: {cer_score:.2f}")
    return {
        "reference": reference,
        "hypothesis": hypothesis,
        "wer": round(wer_score, 4),
        "cer": round(cer_score, 4),
        "wer_percent": round(wer_score * 100, 2),
        "cer_percent": round(cer_score * 100, 2)
    }

def evaluate_asr(test_cases: list) -> dict:
    all_references = []
    all_hypotheses = []
    results = []

    for case in test_cases:
        ref = case["reference"].lower().strip()
        hyp = case["hypothesis"].lower().strip()
        all_references.append(ref)
        all_hypotheses.append(hyp)
        wer_score = jiwer.wer(ref, hyp)
        results.append({
            "reference": ref,
            "hypothesis": hyp,
            "wer": round(wer_score * 100, 2)
        })

    overall_wer = jiwer.wer(all_references, all_hypotheses)
    logger.info(f"Overall WER: {overall_wer:.4f}")

    return {
        "overall_wer_percent": round(overall_wer * 100, 2),
        "total_samples": len(test_cases),
        "individual_results": results
    }