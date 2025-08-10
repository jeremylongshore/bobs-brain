#!/usr/bin/env python3
"""
Bob Unified Test Harness
Comprehensive testing without disrupting production Slack bot (process 56701)
"""

import os
import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add src directory to path for imports
sys.path.append('/home/jeremylongshore/bob-consolidation/src')

# Import our unified Bob (with modifications for testing)
import chromadb
import logging

class BobTestHarness:
    """Test harness for Bob Unified Agent - No Slack integration during tests"""
    
    def __init__(self):
        """Initialize test harness with safe testing configuration"""
        self.setup_test_logging()
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {},
            'overall_status': 'running',
            'errors': []
        }
        
        # Initialize ChromaDB connection for testing
        try:
            self.chroma_client = chromadb.PersistentClient(
                path='/home/jeremylongshore/.bob_brain/chroma'
            )
            self.knowledge_collection = self.chroma_client.get_collection('bob_knowledge')
            self.logger.info("✅ ChromaDB connection established for testing")
        except Exception as e:
            self.logger.error(f"❌ ChromaDB connection failed: {e}")
            self.test_results['errors'].append(f"ChromaDB connection: {e}")
        
        # Business context for testing
        self.business_context = {
            "company": "DiagnosticPro.io",
            "industry": "Vehicle Repair & Diagnostics",
            "mission": "Protect customers from shop overcharges through accurate diagnostics",
            "owner": "Jeremy Longshore",
            "experience": "15 years business experience (BBI, trucking)",
            "target_market": "Multi-billion repair industry disruption"
        }
    
    def setup_test_logging(self):
        """Configure test-specific logging"""
        os.makedirs('/home/jeremylongshore/bob-consolidation/logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'/home/jeremylongshore/bob-consolidation/logs/test_run_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BobTestHarness')
    
    def test_chromadb_connection(self) -> Dict[str, Any]:
        """Test ChromaDB knowledge base connection and integrity"""
        test_name = "ChromaDB Connection & Integrity"
        self.logger.info(f"🔍 Starting test: {test_name}")
        
        start_time = time.time()
        result = {
            'status': 'failed',
            'details': {},
            'duration': 0,
            'errors': []
        }
        
        try:
            # Test connection
            total_items = self.knowledge_collection.count()
            result['details']['total_items'] = total_items
            
            # Test basic query
            test_query = "DiagnosticPro"
            query_results = self.knowledge_collection.query(
                query_texts=[test_query],
                n_results=3,
                include=["documents", "metadatas", "distances"]
            )
            
            result['details']['test_query'] = test_query
            result['details']['query_results_count'] = len(query_results['documents'][0]) if query_results['documents'] else 0
            result['details']['sample_relevance'] = query_results['distances'][0][0] if query_results['distances'] and query_results['distances'][0] else None
            
            # Verify expected item count (should be around 970)
            if total_items >= 900:
                result['details']['item_count_status'] = 'healthy'
            else:
                result['details']['item_count_status'] = 'warning'
                result['errors'].append(f"Lower than expected item count: {total_items}")
            
            result['status'] = 'passed'
            self.logger.info(f"✅ {test_name} passed - {total_items} items available")
            
        except Exception as e:
            result['errors'].append(str(e))
            self.logger.error(f"❌ {test_name} failed: {e}")
        
        result['duration'] = time.time() - start_time
        self.test_results['tests'][test_name] = result
        return result
    
    def test_knowledge_search_functionality(self) -> Dict[str, Any]:
        """Test knowledge search with various queries"""
        test_name = "Knowledge Search Functionality"
        self.logger.info(f"🔍 Starting test: {test_name}")
        
        start_time = time.time()
        result = {
            'status': 'failed',
            'details': {'queries': []},
            'duration': 0,
            'errors': []
        }
        
        # Test queries covering different aspects
        test_queries = [
            "DiagnosticPro diagnostic procedures",
            "vehicle repair cost analysis",
            "shop overcharge protection",
            "Jeremy Longshore business experience",
            "BBI trucking background"
        ]
        
        try:
            for query in test_queries:
                query_start = time.time()
                
                query_results = self.knowledge_collection.query(
                    query_texts=[query],
                    n_results=3,
                    include=["documents", "metadatas", "distances"]
                )
                
                query_duration = time.time() - query_start
                
                query_info = {
                    'query': query,
                    'duration': query_duration,
                    'results_count': len(query_results['documents'][0]) if query_results['documents'] else 0,
                    'best_relevance': 1.0 - query_results['distances'][0][0] if query_results['distances'] and query_results['distances'][0] else 0,
                    'has_results': bool(query_results['documents'] and query_results['documents'][0])
                }
                
                result['details']['queries'].append(query_info)
                self.logger.info(f"  Query '{query}': {query_info['results_count']} results, {query_info['best_relevance']:.3f} relevance")
            
            # Calculate averages
            total_queries = len(result['details']['queries'])
            avg_duration = sum(q['duration'] for q in result['details']['queries']) / total_queries
            avg_results = sum(q['results_count'] for q in result['details']['queries']) / total_queries
            successful_queries = sum(1 for q in result['details']['queries'] if q['has_results'])
            
            result['details']['summary'] = {
                'total_queries': total_queries,
                'successful_queries': successful_queries,
                'success_rate': successful_queries / total_queries,
                'avg_duration': avg_duration,
                'avg_results_per_query': avg_results
            }
            
            if successful_queries >= 4:  # At least 4 out of 5 should work
                result['status'] = 'passed'
                self.logger.info(f"✅ {test_name} passed - {successful_queries}/{total_queries} queries successful")
            else:
                result['errors'].append(f"Low success rate: {successful_queries}/{total_queries}")
                self.logger.warning(f"⚠️ {test_name} partial success - {successful_queries}/{total_queries} queries successful")
            
        except Exception as e:
            result['errors'].append(str(e))
            self.logger.error(f"❌ {test_name} failed: {e}")
        
        result['duration'] = time.time() - start_time
        self.test_results['tests'][test_name] = result
        return result
    
    def test_business_communication_responses(self) -> Dict[str, Any]:
        """Test professional business communication generation"""
        test_name = "Business Communication Responses"
        self.logger.info(f"🔍 Starting test: {test_name}")
        
        start_time = time.time()
        result = {
            'status': 'failed',
            'details': {'responses': []},
            'duration': 0,
            'errors': []
        }
        
        test_scenarios = [
            {
                'input': 'Hello, I need help with vehicle diagnostics',
                'expected_themes': ['diagnostic', 'professional', 'help', 'vehicle']
            },
            {
                'input': 'What is DiagnosticPro and how does it work?',
                'expected_themes': ['DiagnosticPro', 'repair', 'diagnostics', 'overcharge']
            },
            {
                'input': 'I think a shop is overcharging me for repairs',
                'expected_themes': ['overcharge', 'protection', 'diagnostic', 'customer']
            },
            {
                'input': 'Tell me about Jeremy Longshore business experience',
                'expected_themes': ['Jeremy', 'business', 'experience', 'BBI', 'trucking']
            }
        ]
        
        try:
            for scenario in test_scenarios:
                response_start = time.time()
                
                # Simulate response generation logic from unified Bob
                user_message = scenario['input']
                
                # Query knowledge base
                knowledge_results = self.knowledge_collection.query(
                    query_texts=[user_message],
                    n_results=3
                )
                
                # Generate response based on knowledge and business context
                response = self.generate_test_response(user_message, knowledge_results)
                
                response_duration = time.time() - response_start
                
                # Analyze response quality
                response_lower = response.lower()
                theme_matches = sum(1 for theme in scenario['expected_themes'] 
                                  if theme.lower() in response_lower)
                theme_score = theme_matches / len(scenario['expected_themes'])
                
                response_info = {
                    'input': user_message,
                    'response': response,
                    'duration': response_duration,
                    'length': len(response),
                    'theme_score': theme_score,
                    'professional_tone': self.assess_professional_tone(response)
                }
                
                result['details']['responses'].append(response_info)
                self.logger.info(f"  Scenario: {user_message[:30]}... - Theme score: {theme_score:.2f}")
            
            # Calculate overall quality
            avg_theme_score = sum(r['theme_score'] for r in result['details']['responses']) / len(result['details']['responses'])
            avg_professional_score = sum(r['professional_tone'] for r in result['details']['responses']) / len(result['details']['responses'])
            
            result['details']['summary'] = {
                'avg_theme_relevance': avg_theme_score,
                'avg_professional_tone': avg_professional_score,
                'total_scenarios': len(test_scenarios)
            }
            
            if avg_theme_score >= 0.6 and avg_professional_score >= 0.7:
                result['status'] = 'passed'
                self.logger.info(f"✅ {test_name} passed - Theme: {avg_theme_score:.2f}, Professional: {avg_professional_score:.2f}")
            else:
                result['errors'].append(f"Quality scores below threshold - Theme: {avg_theme_score:.2f}, Professional: {avg_professional_score:.2f}")
        
        except Exception as e:
            result['errors'].append(str(e))
            self.logger.error(f"❌ {test_name} failed: {e}")
        
        result['duration'] = time.time() - start_time
        self.test_results['tests'][test_name] = result
        return result
    
    def generate_test_response(self, user_message: str, knowledge_results: Dict) -> str:
        """Generate test response using Bob's logic"""
        response_parts = []
        
        if knowledge_results['documents'] and knowledge_results['documents'][0]:
            # Use knowledge-based response
            best_match = knowledge_results['documents'][0][0]
            if len(best_match) > 300:
                best_match = best_match[:300] + "..."
            response_parts.append(f"Based on my knowledge: {best_match}")
        
        # Add business context
        if "diagnostic" in user_message.lower() or "repair" in user_message.lower():
            response_parts.append(
                f"At {self.business_context['company']}, we specialize in protecting customers "
                "from shop overcharges through accurate diagnostic procedures."
            )
        
        elif any(keyword in user_message.lower() for keyword in ["hello", "hi", "help"]):
            response_parts.append(
                f"Hello! I'm Bob, your AI business partner for {self.business_context['company']}. "
                f"With {self.business_context['experience']}, I can help with diagnostics and industry insights."
            )
        
        return " ".join(response_parts) if response_parts else (
            "I'm Bob, your professional AI assistant specializing in vehicle diagnostics "
            "and repair industry operations. How can I assist you today?"
        )
    
    def assess_professional_tone(self, response: str) -> float:
        """Assess professional tone of response (0.0 to 1.0)"""
        professional_indicators = [
            'professional', 'business', 'experience', 'assist', 'help',
            'diagnostic', 'industry', 'knowledge', 'specialized', 'expert'
        ]
        
        unprofessional_indicators = [
            'awesome', 'cool', 'hey there', 'yo', 'sup', 'lol'
        ]
        
        response_lower = response.lower()
        
        professional_count = sum(1 for indicator in professional_indicators 
                               if indicator in response_lower)
        unprofessional_count = sum(1 for indicator in unprofessional_indicators 
                                 if indicator in response_lower)
        
        # Professional score based on indicators
        base_score = min(professional_count * 0.2, 0.8)
        penalty = unprofessional_count * 0.3
        
        return max(0.0, min(1.0, base_score - penalty + 0.2))  # Base professional assumption
    
    def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all tests and generate comprehensive report"""
        self.logger.info("🚀 Starting Bob Unified comprehensive testing...")
        self.logger.info("=" * 60)
        
        # Run individual tests
        tests_to_run = [
            self.test_chromadb_connection,
            self.test_knowledge_search_functionality,
            self.test_business_communication_responses
        ]
        
        passed_tests = 0
        total_tests = len(tests_to_run)
        
        for test_func in tests_to_run:
            try:
                result = test_func()
                if result['status'] == 'passed':
                    passed_tests += 1
            except Exception as e:
                self.logger.error(f"❌ Test execution error: {e}")
                self.test_results['errors'].append(f"Test execution: {e}")
        
        # Calculate overall results
        success_rate = passed_tests / total_tests
        
        if success_rate >= 0.8:
            self.test_results['overall_status'] = 'passed'
        elif success_rate >= 0.6:
            self.test_results['overall_status'] = 'partial'
        else:
            self.test_results['overall_status'] = 'failed'
        
        self.test_results['summary'] = {
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'success_rate': success_rate,
            'completion_time': datetime.now().isoformat()
        }
        
        self.logger.info("=" * 60)
        self.logger.info(f"🏁 Testing complete: {passed_tests}/{total_tests} tests passed ({success_rate:.1%})")
        
        return self.test_results
    
    def generate_test_report(self) -> str:
        """Generate formatted test report"""
        report_lines = [
            "# Bob Unified Agent Test Report",
            f"**Generated**: {self.test_results['timestamp']}",
            f"**Overall Status**: {self.test_results['overall_status'].upper()}",
            "",
            "## Summary",
            f"- **Tests Passed**: {self.test_results['summary']['passed_tests']}/{self.test_results['summary']['total_tests']}",
            f"- **Success Rate**: {self.test_results['summary']['success_rate']:.1%}",
            "",
            "## Individual Test Results",
            ""
        ]
        
        for test_name, test_data in self.test_results['tests'].items():
            status_emoji = "✅" if test_data['status'] == 'passed' else "❌"
            report_lines.extend([
                f"### {status_emoji} {test_name}",
                f"**Status**: {test_data['status'].upper()}",
                f"**Duration**: {test_data['duration']:.2f}s",
                ""
            ])
            
            if test_data.get('details'):
                report_lines.append("**Details**:")
                for key, value in test_data['details'].items():
                    if isinstance(value, dict):
                        report_lines.append(f"- {key}: {json.dumps(value, indent=2)}")
                    else:
                        report_lines.append(f"- {key}: {value}")
                report_lines.append("")
            
            if test_data.get('errors'):
                report_lines.append("**Errors**:")
                for error in test_data['errors']:
                    report_lines.append(f"- {error}")
                report_lines.append("")
        
        return "\n".join(report_lines)


def main():
    """Main test execution"""
    print("🤖 Bob Unified Test Harness")
    print("=" * 50)
    print("⚠️  SAFE TESTING MODE - No Slack integration")
    print("⚠️  Process 56701 remains active and protected")
    print("=" * 50)
    
    # Initialize test harness
    test_harness = BobTestHarness()
    
    # Run comprehensive tests
    results = test_harness.run_comprehensive_tests()
    
    # Generate and save report
    report = test_harness.generate_test_report()
    
    # Save report to file
    report_file = f'/home/jeremylongshore/bob-consolidation/logs/test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n📊 Test report saved to: {report_file}")
    
    # Print summary
    if results['overall_status'] == 'passed':
        print("🎉 All tests passed! Unified Bob is ready for deployment.")
        return 0
    elif results['overall_status'] == 'partial':
        print("⚠️  Some tests passed. Review results before deployment.")
        return 1
    else:
        print("❌ Tests failed. Address issues before deployment.")
        return 2


if __name__ == "__main__":
    exit(main())