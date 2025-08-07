#!/usr/bin/env python3
"""
Mock Alice - Shared Context Listener for Testing Bob's Task Delegation
Simulates Alice processing tasks until the real Alice is functional
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from google.cloud import firestore
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MockAlice:
    """Mock Alice that processes tasks from /shared_context collection"""

    def __init__(self, firestore_project: str = "diagnostic-pro-mvp"):
        self.firestore_client = firestore.Client(project=firestore_project, database="bob-brain")
        self.agent_id = "mock_alice"
        self.running = True

        # Mock Alice capabilities
        self.capabilities = {
            'gcp_monitoring': self._mock_gcp_monitoring,
            'cloud_deployment': self._mock_cloud_deployment,
            'resource_analysis': self._mock_resource_analysis,
            'cost_optimization': self._mock_cost_optimization,
            'backup_management': self._mock_backup_management,
            'security_audit': self._mock_security_audit,
            'default': self._mock_default_task
        }

        # Performance simulation
        self.success_rate = 0.85  # 85% task success rate
        self.processing_time_range = (2, 8)  # 2-8 seconds processing time

        logger.info(f"🤖 Mock Alice initialized with {len(self.capabilities)} capabilities")

    def start_listening(self, poll_interval: int = 5):
        """Start listening for tasks from Bob"""
        logger.info(f"👂 Mock Alice listening for tasks (polling every {poll_interval}s)...")

        while self.running:
            try:
                # Get pending tasks for Alice
                pending_tasks = self._get_pending_tasks()

                if pending_tasks:
                    logger.info(f"📝 Found {len(pending_tasks)} pending task(s)")

                    for task in pending_tasks:
                        self._process_task(task)

                else:
                    logger.debug("😴 No pending tasks, continuing to listen...")

                time.sleep(poll_interval)

            except KeyboardInterrupt:
                logger.info("🛑 Mock Alice shutting down...")
                self.running = False
                break
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}")
                time.sleep(poll_interval)

    def _get_pending_tasks(self, limit: int = 5) -> List[Dict]:
        """Get pending tasks from Firestore"""
        try:
            docs = (self.firestore_client.collection('shared_context')
                   .where('agent_to', '==', 'alice')
                   .where('status', '==', 'pending')
                   .order_by('created_at')
                   .limit(limit)
                   .stream())

            tasks = []
            for doc in docs:
                task_data = doc.to_dict()
                task_data['task_id'] = doc.id
                tasks.append(task_data)

            return tasks

        except Exception as e:
            logger.error(f"❌ Failed to get pending tasks: {e}")
            return []

    def _process_task(self, task: Dict):
        """Process a single task from Bob"""
        task_id = task['task_id']
        task_type = task.get('task_type', 'default')
        description = task.get('description', 'No description')

        logger.info(f"🔄 Processing task {task_id}: {description}")

        try:
            # Claim the task
            if not self._claim_task(task_id):
                logger.warning(f"⚠️  Failed to claim task {task_id}")
                return

            # Simulate processing time
            processing_time = random.uniform(*self.processing_time_range)
            time.sleep(processing_time)

            # Execute task based on type
            handler = self.capabilities.get(task_type, self.capabilities['default'])
            result = handler(task)

            # Determine success based on success rate
            success = random.random() < self.success_rate

            if not success:
                # Simulate failure
                result = {
                    'status': 'failed',
                    'error': 'Mock failure for testing',
                    'retry_suggested': True
                }

            # Complete the task
            self._complete_task(task_id, result, success)

            status_emoji = "✅" if success else "❌"
            logger.info(f"{status_emoji} Task {task_id} {'completed' if success else 'failed'} in {processing_time:.1f}s")

        except Exception as e:
            logger.error(f"❌ Error processing task {task_id}: {e}")
            self._complete_task(task_id, {'error': str(e)}, False)

    def _claim_task(self, task_id: str) -> bool:
        """Claim a pending task"""
        try:
            doc_ref = self.firestore_client.collection('shared_context').document(task_id)
            doc_ref.update({
                'status': 'in_progress',
                'claimed_by': self.agent_id,
                'claimed_at': firestore.SERVER_TIMESTAMP,
                'attempts': firestore.Increment(1)
            })
            return True
        except Exception as e:
            logger.error(f"❌ Failed to claim task {task_id}: {e}")
            return False

    def _complete_task(self, task_id: str, result: Dict, success: bool):
        """Mark task as completed with results"""
        try:
            doc_ref = self.firestore_client.collection('shared_context').document(task_id)

            update_data = {
                'status': 'completed' if success else 'failed',
                'completed_at': firestore.SERVER_TIMESTAMP,
                'completed_by': self.agent_id,
                'result': result,
                'processing_time_seconds': result.get('processing_time', 0),
                'updated_at': firestore.SERVER_TIMESTAMP
            }

            doc_ref.update(update_data)

        except Exception as e:
            logger.error(f"❌ Failed to complete task {task_id}: {e}")

    # Mock task handlers
    def _mock_gcp_monitoring(self, task: Dict) -> Dict:
        """Mock GCP monitoring task"""
        metadata = task.get('metadata', {})
        service = metadata.get('service', 'unknown')
        region = metadata.get('region', 'us-central1')

        # Simulate checking service health
        services_health = {
            'bob-extended-brain': {'status': 'healthy', 'uptime': '99.9%', 'memory': '45%'},
            'alice-cloud-bestie': {'status': 'healthy', 'uptime': '99.8%', 'memory': '62%'},
            'diagnosticpro-mvp': {'status': 'healthy', 'uptime': '99.7%', 'memory': '38%'}
        }

        health = services_health.get(service, {
            'status': 'unknown',
            'uptime': '0%',
            'memory': 'unknown'
        })

        return {
            'task_type': 'gcp_monitoring',
            'service': service,
            'region': region,
            'health_status': health['status'],
            'uptime': health['uptime'],
            'memory_usage': health['memory'],
            'last_checked': datetime.now().isoformat(),
            'recommendations': self._generate_monitoring_recommendations(health)
        }

    def _mock_cloud_deployment(self, task: Dict) -> Dict:
        """Mock cloud deployment task"""
        metadata = task.get('metadata', {})

        return {
            'task_type': 'cloud_deployment',
            'deployment_status': 'success',
            'service_url': f"https://{metadata.get('service', 'mock-service')}-12345.us-central1.run.app",
            'build_time': f"{random.randint(30, 180)}s",
            'resource_allocation': {
                'memory': metadata.get('memory', '512Mi'),
                'cpu': metadata.get('cpu', '1'),
                'max_instances': metadata.get('max_instances', 10)
            },
            'estimated_monthly_cost': f"${random.uniform(5, 25):.2f}"
        }

    def _mock_resource_analysis(self, task: Dict) -> Dict:
        """Mock resource analysis task"""
        return {
            'task_type': 'resource_analysis',
            'analysis_type': task.get('metadata', {}).get('analysis_type', 'general'),
            'resources_analyzed': random.randint(15, 45),
            'cost_breakdown': {
                'compute': f"${random.uniform(50, 200):.2f}",
                'storage': f"${random.uniform(5, 20):.2f}",
                'networking': f"${random.uniform(2, 8):.2f}"
            },
            'optimization_opportunities': [
                'Resize underutilized VMs',
                'Delete unused storage buckets',
                'Optimize Cloud Run memory allocation'
            ],
            'potential_savings': f"${random.uniform(20, 80):.2f}/month"
        }

    def _mock_cost_optimization(self, task: Dict) -> Dict:
        """Mock cost optimization task"""
        return {
            'task_type': 'cost_optimization',
            'actions_taken': [
                'Deleted 3 unused storage buckets',
                'Resized overprovisioned VM instances',
                'Optimized Cloud Run concurrency settings'
            ],
            'monthly_savings': f"${random.uniform(15, 60):.2f}",
            'annual_projected_savings': f"${random.uniform(180, 720):.2f}",
            'optimization_score': f"{random.uniform(75, 95):.1f}%"
        }

    def _mock_backup_management(self, task: Dict) -> Dict:
        """Mock backup management task"""
        return {
            'task_type': 'backup_management',
            'backup_status': 'completed',
            'backup_location': 'gs://bobs-house-ai-backups',
            'backup_size': f"{random.uniform(0.1, 5.0):.2f}GB",
            'backup_time': f"{random.randint(30, 180)}s",
            'retention_policy': '30 days',
            'next_backup': (datetime.now() + timedelta(days=1)).isoformat()
        }

    def _mock_security_audit(self, task: Dict) -> Dict:
        """Mock security audit task"""
        return {
            'task_type': 'security_audit',
            'audit_scope': task.get('metadata', {}).get('scope', 'full'),
            'security_score': f"{random.uniform(80, 98):.1f}%",
            'vulnerabilities_found': random.randint(0, 3),
            'recommendations': [
                'Enable 2FA for all service accounts',
                'Rotate API keys older than 90 days',
                'Review IAM permissions for unused roles'
            ],
            'compliance_status': 'compliant',
            'next_audit_date': (datetime.now() + timedelta(days=30)).isoformat()
        }

    def _mock_default_task(self, task: Dict) -> Dict:
        """Mock default task handler for unknown task types"""
        return {
            'task_type': task.get('task_type', 'unknown'),
            'status': 'processed',
            'message': f"Mock Alice processed task: {task.get('description', 'No description')}",
            'capabilities_available': list(self.capabilities.keys()),
            'suggestion': 'Use a specific task_type for better results'
        }

    def _generate_monitoring_recommendations(self, health: Dict) -> List[str]:
        """Generate monitoring recommendations based on health status"""
        recommendations = []

        if health['status'] != 'healthy':
            recommendations.append("Investigate service health issues")

        memory_usage = float(health.get('memory', '0%').replace('%', ''))
        if memory_usage > 80:
            recommendations.append("Consider increasing memory allocation")
        elif memory_usage < 20:
            recommendations.append("Consider reducing memory allocation to save costs")

        uptime = float(health.get('uptime', '0%').replace('%', ''))
        if uptime < 99:
            recommendations.append("Monitor service stability and error rates")

        return recommendations or ["Service appears to be running optimally"]

    def create_test_tasks(self, count: int = 3):
        """Create test tasks for Bob to delegate"""
        logger.info(f"🧪 Creating {count} test tasks for Bob to delegate...")

        test_tasks = [
            {
                'agent_from': 'bob',
                'agent_to': 'alice',
                'task_type': 'gcp_monitoring',
                'description': 'Check health of bob-extended-brain service',
                'priority': 'medium',
                'metadata': {
                    'service': 'bob-extended-brain',
                    'region': 'us-central1'
                }
            },
            {
                'agent_from': 'bob',
                'agent_to': 'alice',
                'task_type': 'resource_analysis',
                'description': 'Analyze current GCP resource usage and costs',
                'priority': 'low',
                'metadata': {
                    'analysis_type': 'cost_optimization',
                    'time_period': '30_days'
                }
            },
            {
                'agent_from': 'bob',
                'agent_to': 'alice',
                'task_type': 'backup_management',
                'description': 'Create backup of Firestore database',
                'priority': 'high',
                'metadata': {
                    'backup_type': 'full',
                    'retention_days': 30
                }
            }
        ]

        created_tasks = []
        for i, task_data in enumerate(test_tasks[:count]):
            task_data.update({
                'status': 'pending',
                'created_at': firestore.SERVER_TIMESTAMP,
                'attempts': 0,
                'max_attempts': 3
            })

            doc_ref = self.firestore_client.collection('shared_context').add(task_data)[1]
            created_tasks.append(doc_ref.id)
            logger.info(f"✅ Created test task {i+1}: {doc_ref.id}")

        return created_tasks


def main():
    """Main function to run Mock Alice"""
    print("🤖 Starting Mock Alice - Bob's Task Processing Assistant")
    print("=" * 60)

    mock_alice = MockAlice()

    # Optionally create test tasks
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--create-test-tasks':
        mock_alice.create_test_tasks(3)
        print("✅ Test tasks created. Run without --create-test-tasks to start listening.")
        return

    try:
        mock_alice.start_listening(poll_interval=5)
    except KeyboardInterrupt:
        print("\n👋 Mock Alice shutting down gracefully...")


if __name__ == "__main__":
    main()


"""
USAGE INSTRUCTIONS:

1. Setup:
   pip install google-cloud-firestore

2. Run Mock Alice:
   python3 mock_alice_listener.py

3. Create test tasks:
   python3 mock_alice_listener.py --create-test-tasks

4. Test Bob's task delegation:
   - Bob creates tasks in /shared_context collection
   - Mock Alice processes them automatically
   - Check Firestore console to see results

5. Mock Alice Capabilities:
   - gcp_monitoring: Service health checks
   - cloud_deployment: Deployment simulation
   - resource_analysis: Cost and usage analysis
   - cost_optimization: Savings recommendations
   - backup_management: Backup operations
   - security_audit: Security assessments
"""
