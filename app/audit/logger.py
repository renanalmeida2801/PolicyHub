import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | AUDIT | %(message)s"
)

audit_logger = logging.getLogger("audit")