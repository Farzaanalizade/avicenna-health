#!/usr/bin/env python
"""
Worker Script - اجرای background jobs از صف
استفاده: python worker.py
یا در production: rq worker health_analysis
"""
import sys
import logging
from pathlib import Path

# اضافه کردن parent directory به path
sys.path.insert(0, str(Path(__file__).parent))

import structlog
from redis import Redis
from rq import Worker, Queue
from app.core.config import settings

# تنظیم logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


def run_worker():
    """
    اجرای RQ Worker
    این worker تمام jobs در صف را پردازش می‌کند
    """
    try:
        logger.info("🔄 Worker شروع می‌شود...", redis_url=settings.REDIS_URL)
        
        # اتصال به Redis
        redis_conn = Redis.from_url(settings.REDIS_URL)
        redis_conn.ping()
        logger.info("✓ Redis متصل شد")
        
        # ایجاد queue (نام باید مطابق با اسمی باشد که در job_queue.py استفاده می‌شود)
        queue = Queue("health_analysis", connection=redis_conn)
        
        # ایجاد worker
        worker = Worker(
            [queue],
            connection=redis_conn,
            name="health-analyzer-worker",
            result_ttl=3600,  # نتایج برای 1 ساعت نگهداری شوند
            failure_ttl=86400,  # خرابی‌ها برای 24 ساعت نگهداری شوند
            job_monitoring_interval=5,
            log_format='%(asctime)s %(message)s',
            date_format='%Y-%m-%d %H:%M:%S'
        )
        
        logger.info("✓ Worker آماده است")
        logger.info("👂 Jobs را شنیدن می‌کند...", queue_name="health_analysis")
        
        # اجرای worker
        worker.work(with_scheduler=False)
        
    except Exception as e:
        logger.error("❌ خطای Worker", error=str(e), exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run_worker()
