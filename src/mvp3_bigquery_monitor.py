#!/usr/bin/env python3
"""
MVP3 BigQuery Monitor for Bob's Brain
Monitors new diagnostic submissions and notifies Bob via Slack
Phase 4: Integration with massive expansion-ready schema
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List

import requests
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MVP3BigQueryMonitor:
    """Monitor MVP3 diagnostic submissions in BigQuery"""

    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        self.dataset_id = "circle_of_life"
        self.table_id = "mvp3_diagnostic_submissions"

        # Bob's Slack webhook (if configured)
        self.slack_webhook = os.environ.get("SLACK_WEBHOOK_URL")

        # Track last check timestamp
        self.last_check = datetime.utcnow() - timedelta(minutes=5)

        logger.info("🚀 MVP3 BigQuery Monitor initialized")

    async def check_new_submissions(self) -> List[Dict]:
        """Check for new diagnostic submissions since last check"""
        try:
            query = f"""
            SELECT
                submission_id,
                full_name,
                email,
                equipment_type,
                problem_description,
                selected_service,
                payment_status,
                ai_analysis,
                created_at
            FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE created_at > @last_check
            ORDER BY created_at DESC
            LIMIT 10
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("last_check", "TIMESTAMP", self.last_check)]
            )

            query_job = self.bq_client.query(query, job_config=job_config)
            results = query_job.result()

            submissions = []
            for row in results:
                submissions.append(
                    {
                        "submission_id": row.submission_id,
                        "customer": row.full_name,
                        "email": row.email,
                        "equipment": row.equipment_type,
                        "problem": row.problem_description[:200] if row.problem_description else "No description",
                        "service": row.selected_service,
                        "payment": row.payment_status,
                        "analyzed": row.ai_analysis is not None,
                        "created": row.created_at.isoformat() if row.created_at else None,
                    }
                )

            if submissions:
                logger.info(f"📊 Found {len(submissions)} new submissions")

            # Update last check time
            self.last_check = datetime.utcnow()

            return submissions

        except Exception as e:
            logger.error(f"❌ Failed to check submissions: {e}")
            return []

    async def notify_bob(self, submissions: List[Dict]):
        """Notify Bob about new submissions via Slack or logging"""
        if not submissions:
            return

        for submission in submissions:
            message = self._format_notification(submission)

            # Try Slack first
            if self.slack_webhook:
                try:
                    response = requests.post(self.slack_webhook, json={"text": message}, timeout=10)
                    if response.status_code == 200:
                        logger.info(f"✅ Notified Bob via Slack about {submission['submission_id']}")
                    else:
                        logger.warning(f"⚠️ Slack notification failed: {response.status_code}")
                except Exception as e:
                    logger.error(f"❌ Slack error: {e}")

            # Always log the notification
            logger.info(f"📢 BOB NOTIFICATION: {message}")

    def _format_notification(self, submission: Dict) -> str:
        """Format submission notification for Bob"""
        payment_emoji = "✅" if submission["payment"] == "completed" else "⏳"
        analysis_emoji = "🤖" if submission["analyzed"] else "📝"

        message = (
            f"🔧 New Diagnostic Submission!\n"
            f"Customer: {submission['customer']} ({submission['email']})\n"
            f"Equipment: {submission['equipment']}\n"
            f"Service: {submission['service']}\n"
            f"Problem: {submission['problem']}\n"
            f"Payment: {payment_emoji} {submission['payment']}\n"
            f"Analysis: {analysis_emoji} {'Complete' if submission['analyzed'] else 'Pending'}\n"
            f"ID: {submission['submission_id']}"
        )

        return message

    async def get_daily_metrics(self) -> Dict:
        """Get daily metrics for dashboard"""
        try:
            query = f"""
            SELECT
                DATE(created_at) as date,
                COUNT(*) as total_submissions,
                COUNT(DISTINCT email) as unique_customers,
                SUM(payment_amount) as revenue,
                AVG(ai_confidence_score) as avg_confidence,
                COUNTIF(payment_status = 'completed') as paid_submissions,
                COUNTIF(email_sent) as emails_sent
            FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE DATE(created_at) = CURRENT_DATE()
            GROUP BY date
            """

            query_job = self.bq_client.query(query)
            results = list(query_job.result())

            if results:
                row = results[0]
                return {
                    "date": row.date.isoformat() if row.date else None,
                    "total_submissions": row.total_submissions,
                    "unique_customers": row.unique_customers,
                    "revenue": float(row.revenue) if row.revenue else 0,
                    "avg_confidence": float(row.avg_confidence) if row.avg_confidence else 0,
                    "paid_submissions": row.paid_submissions,
                    "emails_sent": row.emails_sent,
                }

            return {
                "date": datetime.utcnow().date().isoformat(),
                "total_submissions": 0,
                "unique_customers": 0,
                "revenue": 0,
                "avg_confidence": 0,
                "paid_submissions": 0,
                "emails_sent": 0,
            }

        except Exception as e:
            logger.error(f"❌ Failed to get daily metrics: {e}")
            return {}

    async def monitor_loop(self, interval_seconds=60):
        """Continuous monitoring loop"""
        logger.info("🔄 Starting MVP3 monitoring loop...")

        while True:
            try:
                # Check for new submissions
                submissions = await self.check_new_submissions()

                # Notify Bob about new submissions
                await self.notify_bob(submissions)

                # Get and log daily metrics
                metrics = await self.get_daily_metrics()
                if metrics.get("total_submissions", 0) > 0:
                    logger.info(f"📊 Today's metrics: {json.dumps(metrics, indent=2)}")

                # Wait before next check
                await asyncio.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"❌ Monitor loop error: {e}")
                await asyncio.sleep(interval_seconds)

    def integrate_with_bob(self):
        """Integration code for Bob's Brain"""
        return {
            "monitor": self,
            "check_submissions": self.check_new_submissions,
            "get_metrics": self.get_daily_metrics,
            "description": "MVP3 BigQuery Monitor - Tracks diagnostic submissions",
            "capabilities": [
                "Real-time submission monitoring",
                "Payment status tracking",
                "AI analysis status",
                "Daily metrics aggregation",
                "Slack notifications",
                "Customer tracking",
            ],
        }


async def main():
    """Run the monitor standalone"""
    monitor = MVP3BigQueryMonitor()

    # Check current status
    logger.info("🔍 Checking current MVP3 status...")

    # Get today's metrics
    metrics = await monitor.get_daily_metrics()
    logger.info(f"📊 Today's metrics: {json.dumps(metrics, indent=2)}")

    # Check recent submissions
    submissions = await monitor.check_new_submissions()
    if submissions:
        logger.info(f"📝 Recent submissions: {len(submissions)}")
        for sub in submissions:
            logger.info(f"  - {sub['submission_id']}: {sub['customer']} ({sub['service']})")
    else:
        logger.info("📭 No new submissions in the last 5 minutes")

    # Start monitoring loop
    logger.info("🚀 Starting continuous monitoring...")
    await monitor.monitor_loop(interval_seconds=30)


if __name__ == "__main__":
    asyncio.run(main())
