"""
backend/logger.py
Centralized logging for FitAI — logs to console + fitai_debug.log file.
"""

import logging
import os
from datetime import datetime

LOG_FILE = "fitai_debug.log"

# ── Setup ──────────────────────────────────────────────────────────────────────
logger = logging.getLogger("fitai")
logger.setLevel(logging.DEBUG)

# Avoid adding duplicate handlers on Streamlit reruns
if not logger.handlers:
    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)


def log_tryon_request(category, person_size, item_size, description, denoise_steps, seed):
    logger.info("=" * 60)
    logger.info(f"TRY-ON REQUEST")
    logger.info(f"  Category      : {category}")
    logger.info(f"  Person image  : {person_size[0]}x{person_size[1]} px")
    logger.info(f"  Item image    : {item_size[0]}x{item_size[1]} px")
    logger.info(f"  Description   : {description}")
    logger.info(f"  Denoise steps : {denoise_steps}")
    logger.info(f"  Seed          : {seed}")
    logger.info("=" * 60)


def log_model_selected(category, model_name, space):
    logger.info(f"MODEL SELECTED  : {model_name} ({space}) for category='{category}'")


def log_space_attempt(space, attempt_num):
    logger.info(f"SPACE ATTEMPT #{attempt_num} : {space}")


def log_space_success(space):
    logger.info(f"SPACE SUCCESS   : {space}")


def log_space_failure(space, error):
    logger.warning(f"SPACE FAILED    : {space} → {error}")


def log_result(result_size):
    logger.info(f"RESULT IMAGE    : {result_size[0]}x{result_size[1]} px")
    logger.info("TRY-ON COMPLETE")


def log_groq_analysis(category, raw_response, parsed):
    logger.info(f"GROQ ANALYSIS   : category='{category}'")
    logger.debug(f"  Raw response  : {raw_response[:300]}")
    logger.info(f"  Parsed cat    : {parsed.get('category')}")
    logger.info(f"  Color         : {parsed.get('color')}")
    logger.info(f"  Fit           : {parsed.get('fit')}")
    logger.info(f"  Fabric        : {parsed.get('fabric')}")
    logger.info(f"  Prompt        : {parsed.get('prompt')}")


def log_error(stage, error):
    logger.error(f"ERROR at [{stage}] : {error}", exc_info=True)