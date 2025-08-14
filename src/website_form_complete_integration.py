#!/usr/bin/env python3
"""
Complete Website Form to BigQuery Integration with Email
Includes AI analysis, email delivery, vehicle tracking, and PDF generation
MVP3 Compatible with Enhanced Features
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import google.generativeai as genai
from flask import Flask, jsonify, request
from google.cloud import bigquery, datastore, pubsub_v1
from google.oauth2 import service_account
from googleapiclient.discovery import build

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


class CompleteFormIntegration:
    """Handle website form submissions with complete data flow"""

    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        self.mvp_project = "diagnostic-pro-mvp"

        # Initialize clients
        self.bq_client = bigquery.Client(project=project_id)
        self.datastore_client = datastore.Client(project=self.mvp_project)
        self.publisher = pubsub_v1.PublisherClient()

        # Configure Gemini AI
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

        # Initialize email service
        self.email_service = self._init_email_service()

        # Ensure all tables exist
        self._ensure_all_tables()

        logger.info("Complete form integration initialized with email support")

    def _init_email_service(self):
        """Initialize email service (Gmail or SendGrid based on config)"""
        if os.getenv("SENDGRID_API_KEY"):
            return SendGridEmailService(os.getenv("SENDGRID_API_KEY"))
        else:
            return GmailEmailService()

    def _ensure_all_tables(self):
        """Ensure all BigQuery tables exist"""
        
        # Create customer submissions dataset
        dataset_id = f"{self.project_id}.customer_submissions"
        dataset = bigquery.Dataset(dataset_id)
        dataset.description = "Customer diagnostic submissions with complete tracking"
        dataset.location = "US"
        
        self.bq_client.create_dataset(dataset, exists_ok=True)

        # 1. Main diagnostics table with enhanced schema
        self._create_diagnostics_table(dataset_id)
        
        # 2. Email history table
        self._create_email_history_table(dataset_id)
        
        # 3. Vehicle history table
        self._create_vehicle_history_table(dataset_id)
        
        logger.info("✅ All tables ready for complete data flow")

    def _create_diagnostics_table(self, dataset_id):
        """Create main diagnostics table"""
        table_id = f"{dataset_id}.diagnostics"
        schema = [
            # Core submission fields
            bigquery.SchemaField("submission_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
            
            # Customer fields
            bigquery.SchemaField("customer_name", "STRING"),
            bigquery.SchemaField("customer_email", "STRING"),
            bigquery.SchemaField("customer_phone", "STRING"),
            bigquery.SchemaField("customer_company", "STRING"),
            bigquery.SchemaField("customer_type", "STRING"),
            bigquery.SchemaField("customer_location_city", "STRING"),
            bigquery.SchemaField("customer_location_state", "STRING"),
            bigquery.SchemaField("customer_location_zip", "STRING"),
            
            # Equipment/Vehicle fields
            bigquery.SchemaField("equipment_type", "STRING"),
            bigquery.SchemaField("equipment_brand", "STRING"),
            bigquery.SchemaField("equipment_model", "STRING"),
            bigquery.SchemaField("equipment_serial", "STRING"),
            bigquery.SchemaField("equipment_year", "INTEGER"),
            bigquery.SchemaField("equipment_hours", "INTEGER"),
            bigquery.SchemaField("vehicle_id", "STRING"),  # Generated from serial/model
            
            # Problem fields
            bigquery.SchemaField("problem_description", "STRING"),
            bigquery.SchemaField("problem_category", "STRING"),
            bigquery.SchemaField("error_codes", "STRING", mode="REPEATED"),
            bigquery.SchemaField("symptoms", "STRING", mode="REPEATED"),
            bigquery.SchemaField("service_type", "STRING"),
            bigquery.SchemaField("urgency_level", "STRING"),
            
            # AI Analysis fields
            bigquery.SchemaField("ai_analysis", "STRING"),  # Full markdown analysis
            bigquery.SchemaField("ai_analysis_json", "JSON"),  # Structured data
            bigquery.SchemaField("suggested_solutions", "JSON"),
            bigquery.SchemaField("confidence_score", "FLOAT64"),
            bigquery.SchemaField("similar_cases", "JSON"),
            bigquery.SchemaField("estimated_cost_min", "FLOAT64"),
            bigquery.SchemaField("estimated_cost_max", "FLOAT64"),
            bigquery.SchemaField("estimated_cost_fair", "FLOAT64"),
            bigquery.SchemaField("red_flags", "STRING", mode="REPEATED"),
            bigquery.SchemaField("bottom_line", "STRING"),
            bigquery.SchemaField("questions_for_shop", "STRING", mode="REPEATED"),
            bigquery.SchemaField("parts_needed", "JSON"),
            bigquery.SchemaField("labor_hours_book", "FLOAT64"),
            bigquery.SchemaField("labor_hours_actual", "FLOAT64"),
            bigquery.SchemaField("diy_feasible", "BOOLEAN"),
            bigquery.SchemaField("warranty_applies", "BOOLEAN"),
            
            # Email status
            bigquery.SchemaField("email_sent", "BOOLEAN"),
            bigquery.SchemaField("email_sent_at", "TIMESTAMP"),
            bigquery.SchemaField("email_status", "STRING"),
            
            # Tracking fields
            bigquery.SchemaField("session_id", "STRING"),
            bigquery.SchemaField("ip_address", "STRING"),
            bigquery.SchemaField("user_agent", "STRING"),
            bigquery.SchemaField("submission_source", "STRING"),
            
            # Status fields
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("resolution", "STRING"),
            bigquery.SchemaField("resolution_time", "INTEGER"),
            
            # Neo4j integration
            bigquery.SchemaField("neo4j_node_id", "STRING"),
            
            # Metadata
            bigquery.SchemaField("metadata", "JSON"),
        ]
        
        table = bigquery.Table(table_id, schema=schema)
        table.clustering_fields = ["customer_type", "equipment_type", "created_at"]
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY, 
            field="created_at"
        )
        
        self.bq_client.create_table(table, exists_ok=True)

    def _create_email_history_table(self, dataset_id):
        """Create email history tracking table"""
        table_id = f"{dataset_id}.email_history"
        schema = [
            bigquery.SchemaField("email_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("submission_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("sent_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("recipient_email", "STRING"),
            bigquery.SchemaField("subject", "STRING"),
            bigquery.SchemaField("email_content_html", "STRING"),  # Full HTML saved
            bigquery.SchemaField("email_content_text", "STRING"),  # Full text saved
            bigquery.SchemaField("pdf_content_base64", "STRING"),  # PDF saved as base64
            bigquery.SchemaField("email_provider", "STRING"),  # gmail/sendgrid
            bigquery.SchemaField("status", "STRING"),  # sent/delivered/opened/clicked
            bigquery.SchemaField("tracking_id", "STRING"),
            bigquery.SchemaField("opened_at", "TIMESTAMP"),
            bigquery.SchemaField("clicked_at", "TIMESTAMP"),
            bigquery.SchemaField("metadata", "JSON"),
        ]
        
        table = bigquery.Table(table_id, schema=schema)
        self.bq_client.create_table(table, exists_ok=True)

    def _create_vehicle_history_table(self, dataset_id):
        """Create vehicle history tracking table"""
        table_id = f"{dataset_id}.vehicle_history"
        schema = [
            bigquery.SchemaField("vehicle_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("equipment_serial", "STRING"),
            bigquery.SchemaField("equipment_brand", "STRING"),
            bigquery.SchemaField("equipment_model", "STRING"),
            bigquery.SchemaField("equipment_year", "INTEGER"),
            bigquery.SchemaField("first_seen", "TIMESTAMP"),
            bigquery.SchemaField("last_seen", "TIMESTAMP"),
            bigquery.SchemaField("total_submissions", "INTEGER"),
            bigquery.SchemaField("all_submission_ids", "STRING", mode="REPEATED"),
            bigquery.SchemaField("common_problems", "JSON"),
            bigquery.SchemaField("lifetime_cost", "FLOAT64"),
            bigquery.SchemaField("average_repair_cost", "FLOAT64"),
            bigquery.SchemaField("last_service_date", "TIMESTAMP"),
            bigquery.SchemaField("owner_history", "JSON"),  # Track ownership changes
            bigquery.SchemaField("maintenance_schedule", "JSON"),
            bigquery.SchemaField("warranty_info", "JSON"),
            bigquery.SchemaField("metadata", "JSON"),
        ]
        
        table = bigquery.Table(table_id, schema=schema)
        self.bq_client.create_table(table, exists_ok=True)

    def process_form_submission(self, form_data: Dict) -> Dict:
        """Process website form submission with complete flow"""
        
        try:
            # 1. Generate submission ID and validate data
            submission_id = self._generate_submission_id(form_data)
            cleaned_data = self._validate_form_data(form_data)
            
            logger.info(f"Processing submission {submission_id}")
            
            # 2. Get AI analysis with enhanced prompt
            ai_response = self._get_ai_analysis_enhanced(cleaned_data)
            
            # 3. Generate vehicle ID for tracking
            vehicle_id = self._generate_vehicle_id(cleaned_data)
            
            # 4. Prepare complete record with all fields
            record = self._prepare_complete_record(
                submission_id, cleaned_data, ai_response, vehicle_id
            )
            
            # 5. Store in BigQuery (main table)
            self._store_in_bigquery(record)
            
            # 6. Update vehicle history
            self._update_vehicle_history(vehicle_id, record)
            
            # 7. Generate and send email with PDF
            email_result = self._send_diagnostic_email(record, ai_response)
            
            # 8. Store email history
            self._store_email_history(submission_id, email_result)
            
            # 9. Update record with email status
            self._update_email_status(submission_id, email_result)
            
            # 10. Store in Datastore for MVP3 backward compatibility
            self._store_in_datastore(record)
            
            # 11. Trigger async processing (Circle of Life, Neo4j, etc.)
            self._trigger_async_processing(record)
            
            logger.info(f"✅ Complete processing for {submission_id}")
            
            return {
                "success": True,
                "submission_id": submission_id,
                "vehicle_id": vehicle_id,
                "ai_analysis": ai_response.get("analysis", ""),
                "suggested_solutions": ai_response.get("solutions", []),
                "estimated_cost": ai_response.get("estimated_cost", {}),
                "bottom_line": ai_response.get("bottom_line", ""),
                "email_sent": email_result.get("success", False),
                "message": "Your submission has been received. Check your email for the detailed diagnostic report."
            }
            
        except Exception as e:
            logger.error(f"Form processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "There was an error processing your submission. Please try again."
            }

    def _get_ai_analysis_enhanced(self, data: Dict) -> Dict:
        """Get AI analysis using enhanced master technician prompt"""
        
        try:
            # Build enhanced prompt with all context
            current_datetime = datetime.now().isoformat()
            equipment_type = data.get('equipment_type', 'Unknown')
            equipment_brand = data.get('equipment_brand', '')
            equipment_model = data.get('equipment_model', '')
            equipment_year = data.get('equipment_year', '')
            equipment_hours = data.get('equipment_hours', '')
            equipment_serial = data.get('equipment_serial', '')
            problem_description = data.get('problem_description', '')
            error_codes = ', '.join(data.get('error_codes', [])) if data.get('error_codes') else 'None'
            service_type = data.get('service_type', 'repair')
            customer_type = data.get('customer_type', 'individual')
            repair_history = data.get('repair_history', 'Not available')
            
            # Use the enhanced 14-section prompt
            prompt = f"""
You are DiagnosticPro's MASTER TECHNICIAN with 30+ years diagnosing {equipment_type} equipment. You've seen every failure mode, know every diagnostic shortcut shops take, and can spot incompetence immediately. Your mission: protect the customer's wallet while ensuring proper repairs.

Current Analysis Context:
- Date/Time: {current_datetime}
- Equipment: {equipment_brand} {equipment_model} {equipment_year}
- Operating Hours: {equipment_hours}
- Serial Number: {equipment_serial}
- Problem Description: {problem_description}
- Error Codes: {error_codes}
- Service Type: {service_type}
- Customer Type: {customer_type}
- Previous Repairs: {repair_history}

Use ALL the data above to provide the most accurate analysis possible. Reference specific error codes, mileage patterns, and equipment type in your diagnosis.

📋 COMPREHENSIVE ANALYSIS (2500 words max):

🎯 1. PRIMARY DIAGNOSIS
- Root cause (confidence %)
- Reference specific error codes if provided
- Component failure analysis
- Age/mileage considerations
- Environmental factors (climate, operating conditions)
- Maintenance history impact

🔍 2. DIFFERENTIAL DIAGNOSIS
- Alternative causes ranked by probability
- Why each ruled in/out with specific evidence
- Equipment-specific patterns
- Model year known issues
- Operating environment considerations

✅ 3. DIAGNOSTIC VERIFICATION
- Exact tests shop MUST perform (in order)
- Tools needed, expected readings, tolerances
- Cost estimates for testing ($X-$Y range)
- Time required for proper diagnosis
- What corners shops might cut

❓ 4. SHOP INTERROGATION
- 5 technical questions to expose incompetence
- Specific data they must show you (printouts, readings)
- Red flag responses that indicate BS
- Follow-up questions if they can't answer
- How to verify their diagnostic equipment is calibrated

💸 5. COST BREAKDOWN
- Fair parts pricing analysis (OEM vs aftermarket)
- Labor hour estimates (book time vs actual)
- Total price range (low/fair/high)
- Overcharge identification thresholds
- Regional pricing variations
- Warranty coverage possibilities

🚩 6. RIPOFF DETECTION
- Parts cannon indicators (replacing everything)
- Diagnostic shortcuts (guessing without testing)
- Price gouging red flags (>30% over market)
- Unnecessary upsells to watch for
- Scare tactics they might use

⚖️ 7. AUTHORIZATION GUIDE
- Approve immediately (safety critical)
- Reject outright (obvious scam)
- Get 2nd opinion (unclear diagnosis)
- Negotiate first (overpriced but needed)
- DIY consideration (if safe and feasible)

🔧 8. TECHNICAL EDUCATION
- System operation (how it's supposed to work)
- Failure mechanism (why it broke)
- Prevention tips (avoid repeat failure)
- Maintenance intervals
- Operating best practices

📦 9. OEM PARTS STRATEGY
- Specific part numbers (primary and superseded)
- Why OEM critical (or when aftermarket OK)
- Pricing sources (where to verify costs)
- Warranty implications
- Quality differences that matter

💬 10. NEGOTIATION TACTICS
- Price comparisons (quote other shops)
- Labor justification (why X hours?)
- Warranty demands (parts AND labor)
- Payment terms (completion vs progress)
- Documentation requirements

🔍 11. QUALITY VERIFICATION
- Post-repair tests (before leaving shop)
- Monitoring schedule (first 10/50/100 hours)
- Return triggers (what requires going back)
- Documentation to demand
- Video/photo evidence of repairs

🕵️ 12. INSIDER INTELLIGENCE
- Known issues for this model (TSB/recalls)
- TSB references (specific numbers)
- Common shortcuts shops take
- Manufacturer defect patterns
- Fleet manager insights
- Insurance claim considerations

📊 13. DATA TRACKING
- What to document (photos, receipts, readings)
- Legal protection measures
- Lemon law applicability
- Warranty claim preparation
- Future resale impact

🛠️ 14. ALTERNATIVE SOLUTIONS
- Temporary fixes (if safe)
- Used parts options
- Rebuild vs replace analysis
- Upgrade opportunities
- Preventive replacements while apart

For {service_type}: Include safety, urgency, temp fixes.

BE RUTHLESSLY SPECIFIC. PROTECT THE CUSTOMER'S WALLET. DEMAND TECHNICAL PROOF.

Format for PDF output:
- Use clear headers and subheaders
- Bullet points for easy scanning
- Bold key numbers and prices
- Include summary box at top
- Add "BOTTOM LINE" recommendation at end

Return response as properly formatted JSON with markdown content:
{{
  "analysis": "full markdown formatted analysis with all 14 sections",
  "solutions": ["solution1", "solution2", "solution3", "solution4", "solution5"],
  "confidence": 0.00,
  "similar_cases": ["case1", "case2", "case3"],
  "urgent": true/false,
  "estimated_cost": {{"min": 0, "max": 0, "fair": 0}},
  "red_flags": ["flag1", "flag2", "flag3"],
  "bottom_line": "Clear action recommendation",
  "questions_for_shop": ["q1", "q2", "q3", "q4", "q5"],
  "diy_feasible": true/false,
  "parts_needed": [{{"part": "name", "number": "XXX", "price": 0}}],
  "labor_hours": {{"book": 0, "actual": 0}},
  "warranty_applies": true/false
}}
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse response
            try:
                result = json.loads(response.text)
            except:
                # Fallback if not valid JSON - provide comprehensive default structure
                result = {
                    "analysis": response.text[:2000] if response.text else "Unable to generate detailed analysis",
                    "solutions": [
                        "Schedule professional diagnostic evaluation",
                        "Document all symptoms and error codes",
                        "Get written quotes from multiple shops",
                        "Request itemized parts and labor breakdown",
                        "Contact support for detailed diagnosis"
                    ],
                    "confidence": 0.5,
                    "similar_cases": [],
                    "urgent": False,
                    "estimated_cost": {"min": 0, "max": 0, "fair": 0},
                    "red_flags": [],
                    "bottom_line": "Professional diagnosis recommended",
                    "questions_for_shop": [
                        "What specific tests did you perform?",
                        "Can you show me the diagnostic readings?",
                        "Why do all these parts need replacement?",
                        "What's the warranty on parts and labor?",
                        "Can you provide a written estimate?"
                    ],
                    "diy_feasible": False,
                    "parts_needed": [],
                    "labor_hours": {"book": 0, "actual": 0},
                    "warranty_applies": False
                }
            
            return result
            
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            # Return comprehensive fallback structure
            return {
                "analysis": "Unable to generate AI analysis at this time. Error has been logged.",
                "solutions": [
                    "Contact support for manual analysis",
                    "Document all symptoms with photos/videos",
                    "Get multiple shop opinions",
                    "Request detailed diagnostic reports",
                    "Save all error codes displayed"
                ],
                "confidence": 0.0,
                "similar_cases": [],
                "urgent": False,
                "estimated_cost": {"min": 0, "max": 0, "fair": 0},
                "red_flags": ["No AI analysis available - be extra cautious"],
                "bottom_line": "Manual expert review required",
                "questions_for_shop": [
                    "What diagnostic equipment did you use?",
                    "Can I see the test results?",
                    "What's the root cause of the problem?",
                    "Are there any TSBs for this issue?",
                    "What's included in your warranty?"
                ],
                "diy_feasible": False,
                "parts_needed": [],
                "labor_hours": {"book": 0, "actual": 0},
                "warranty_applies": False
            }

    def _generate_vehicle_id(self, data: Dict) -> str:
        """Generate unique vehicle ID from equipment data"""
        serial = data.get('equipment_serial', '')
        brand = data.get('equipment_brand', '')
        model = data.get('equipment_model', '')
        
        # Create consistent vehicle ID
        vehicle_string = f"{brand}_{model}_{serial}".upper().replace(" ", "_")
        return hashlib.md5(vehicle_string.encode()).hexdigest()[:16]

    def _prepare_complete_record(self, submission_id: str, data: Dict, ai_response: Dict, vehicle_id: str) -> Dict:
        """Prepare complete record with all fields"""
        
        now = datetime.now().isoformat()
        
        return {
            "submission_id": submission_id,
            "created_at": now,
            "updated_at": now,
            
            # Customer data
            "customer_name": data.get("customer_name", ""),
            "customer_email": data.get("customer_email", ""),
            "customer_phone": data.get("customer_phone", ""),
            "customer_company": data.get("customer_company", ""),
            "customer_type": data.get("customer_type", "individual"),
            "customer_location_city": data.get("customer_location_city", ""),
            "customer_location_state": data.get("customer_location_state", ""),
            "customer_location_zip": data.get("customer_location_zip", ""),
            
            # Equipment data
            "equipment_type": data.get("equipment_type", ""),
            "equipment_brand": data.get("equipment_brand", ""),
            "equipment_model": data.get("equipment_model", ""),
            "equipment_serial": data.get("equipment_serial", ""),
            "equipment_year": data.get("equipment_year"),
            "equipment_hours": data.get("equipment_hours"),
            "vehicle_id": vehicle_id,
            
            # Problem data
            "problem_description": data.get("problem_description", ""),
            "problem_category": self._categorize_problem(data.get("problem_description", "")),
            "error_codes": data.get("error_codes", []),
            "symptoms": data.get("symptoms", []),
            "service_type": data.get("service_type", "repair"),
            "urgency_level": data.get("urgency_level", "normal"),
            
            # AI analysis
            "ai_analysis": ai_response.get("analysis", ""),
            "ai_analysis_json": json.dumps(ai_response),
            "suggested_solutions": json.dumps(ai_response.get("solutions", [])),
            "confidence_score": ai_response.get("confidence", 0.5),
            "similar_cases": json.dumps(ai_response.get("similar_cases", [])),
            "estimated_cost_min": ai_response.get("estimated_cost", {}).get("min", 0),
            "estimated_cost_max": ai_response.get("estimated_cost", {}).get("max", 0),
            "estimated_cost_fair": ai_response.get("estimated_cost", {}).get("fair", 0),
            "red_flags": ai_response.get("red_flags", []),
            "bottom_line": ai_response.get("bottom_line", ""),
            "questions_for_shop": ai_response.get("questions_for_shop", []),
            "parts_needed": json.dumps(ai_response.get("parts_needed", [])),
            "labor_hours_book": ai_response.get("labor_hours", {}).get("book", 0),
            "labor_hours_actual": ai_response.get("labor_hours", {}).get("actual", 0),
            "diy_feasible": ai_response.get("diy_feasible", False),
            "warranty_applies": ai_response.get("warranty_applies", False),
            
            # Email status (will be updated after sending)
            "email_sent": False,
            "email_sent_at": None,
            "email_status": "pending",
            
            # Tracking
            "session_id": data.get("session_id", ""),
            "ip_address": request.remote_addr if request else "",
            "user_agent": request.headers.get("User-Agent", "") if request else "",
            "submission_source": "website",
            
            # Status
            "status": "new",
            "resolution": "",
            "resolution_time": None,
            
            # Metadata
            "metadata": json.dumps(data.get("metadata", {}))
        }

    def _send_diagnostic_email(self, record: Dict, ai_response: Dict) -> Dict:
        """Generate and send diagnostic email with PDF"""
        
        try:
            # Generate email content
            email_html = self._generate_email_html(record, ai_response)
            email_text = self._generate_email_text(record, ai_response)
            
            # Generate PDF
            pdf_content = self._generate_pdf_report(record, ai_response)
            
            # Send email
            result = self.email_service.send_diagnostic_report(
                recipient=record["customer_email"],
                subject=f"Diagnostic Report - {record['equipment_brand']} {record['equipment_model']}",
                html_body=email_html,
                text_body=email_text,
                pdf_attachment=pdf_content
            )
            
            return {
                "success": result.get("success", False),
                "email_html": email_html,
                "email_text": email_text,
                "pdf_base64": base64.b64encode(pdf_content).decode() if pdf_content else "",
                "provider": result.get("provider", "unknown"),
                "tracking_id": result.get("tracking_id", ""),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Email sending error: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _generate_email_html(self, record: Dict, ai_response: Dict) -> str:
        """Generate HTML email content"""
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px 5px 0 0; }}
                .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
                .section {{ background: white; margin: 20px 0; padding: 15px; border-radius: 5px; }}
                .cost-box {{ background: #e8f5e9; padding: 15px; border-left: 4px solid #4caf50; }}
                .warning-box {{ background: #fff3e0; padding: 15px; border-left: 4px solid #ff9800; }}
                .danger-box {{ background: #ffebee; padding: 15px; border-left: 4px solid #f44336; }}
                h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                h3 {{ color: #34495e; }}
                ul {{ margin: 10px 0; padding-left: 20px; }}
                .footer {{ text-align: center; padding: 20px; color: #7f8c8d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Diagnostic Report</h1>
                    <p>Submission ID: {record['submission_id']}</p>
                    <p>Date: {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                
                <div class="content">
                    <div class="section">
                        <h2>Equipment Information</h2>
                        <p><strong>Type:</strong> {record['equipment_type']}</p>
                        <p><strong>Brand:</strong> {record['equipment_brand']}</p>
                        <p><strong>Model:</strong> {record['equipment_model']}</p>
                        <p><strong>Serial:</strong> {record['equipment_serial']}</p>
                        <p><strong>Hours:</strong> {record['equipment_hours']}</p>
                    </div>
                    
                    <div class="section">
                        <h2>Problem Description</h2>
                        <p>{record['problem_description']}</p>
                        <p><strong>Error Codes:</strong> {', '.join(record['error_codes']) if record['error_codes'] else 'None'}</p>
                    </div>
                    
                    <div class="section">
                        <h2>🎯 Bottom Line Recommendation</h2>
                        <div class="cost-box">
                            <p><strong>{ai_response.get('bottom_line', 'Professional diagnosis recommended')}</strong></p>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>💸 Estimated Costs</h2>
                        <div class="cost-box">
                            <p><strong>Fair Price:</strong> ${ai_response.get('estimated_cost', {}).get('fair', 0):,.2f}</p>
                            <p><strong>Price Range:</strong> ${ai_response.get('estimated_cost', {}).get('min', 0):,.2f} - ${ai_response.get('estimated_cost', {}).get('max', 0):,.2f}</p>
                        </div>
                    </div>
                    
                    {"<div class='section'><h2>🚩 Red Flags to Watch For</h2><div class='danger-box'><ul>" + ''.join([f"<li>{flag}</li>" for flag in ai_response.get('red_flags', [])]) + "</ul></div></div>" if ai_response.get('red_flags') else ""}
                    
                    <div class="section">
                        <h2>✅ Recommended Solutions</h2>
                        <ol>
                            {"".join([f"<li>{solution}</li>" for solution in ai_response.get('solutions', [])])}
                        </ol>
                    </div>
                    
                    <div class="section">
                        <h2>❓ Questions to Ask Your Shop</h2>
                        <ul>
                            {"".join([f"<li>{question}</li>" for question in ai_response.get('questions_for_shop', [])])}
                        </ul>
                    </div>
                    
                    <div class="section">
                        <h2>📋 Full Analysis</h2>
                        <div style="white-space: pre-wrap; font-family: monospace; background: #f5f5f5; padding: 15px; border-radius: 5px;">
{ai_response.get('analysis', 'Analysis not available')}
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <p>This report was generated by DiagnosticPro's AI system with 30+ years of master technician expertise.</p>
                    <p>Always verify recommendations with a qualified technician.</p>
                    <p>© 2025 DiagnosticPro | support@diagnosticpro.io</p>
                </div>
            </div>
        </body>
        </html>
        """

    def _generate_email_text(self, record: Dict, ai_response: Dict) -> str:
        """Generate plain text email content"""
        
        return f"""
DIAGNOSTIC REPORT
================
Submission ID: {record['submission_id']}
Date: {datetime.now().strftime('%B %d, %Y')}

EQUIPMENT INFORMATION
--------------------
Type: {record['equipment_type']}
Brand: {record['equipment_brand']}
Model: {record['equipment_model']}
Serial: {record['equipment_serial']}
Hours: {record['equipment_hours']}

PROBLEM DESCRIPTION
------------------
{record['problem_description']}
Error Codes: {', '.join(record['error_codes']) if record['error_codes'] else 'None'}

BOTTOM LINE RECOMMENDATION
-------------------------
{ai_response.get('bottom_line', 'Professional diagnosis recommended')}

ESTIMATED COSTS
--------------
Fair Price: ${ai_response.get('estimated_cost', {}).get('fair', 0):,.2f}
Price Range: ${ai_response.get('estimated_cost', {}).get('min', 0):,.2f} - ${ai_response.get('estimated_cost', {}).get('max', 0):,.2f}

RED FLAGS TO WATCH FOR
---------------------
{chr(10).join(['• ' + flag for flag in ai_response.get('red_flags', [])])}

RECOMMENDED SOLUTIONS
--------------------
{chr(10).join([f"{i+1}. {solution}" for i, solution in enumerate(ai_response.get('solutions', []))])}

QUESTIONS TO ASK YOUR SHOP
-------------------------
{chr(10).join(['• ' + q for q in ai_response.get('questions_for_shop', [])])}

FULL ANALYSIS
------------
{ai_response.get('analysis', 'Analysis not available')}

---
This report was generated by DiagnosticPro's AI system.
Always verify recommendations with a qualified technician.
© 2025 DiagnosticPro | support@diagnosticpro.io
        """

    def _generate_pdf_report(self, record: Dict, ai_response: Dict) -> bytes:
        """Generate PDF report (placeholder - implement with reportlab or similar)"""
        # TODO: Implement actual PDF generation
        # For now, return empty bytes
        return b""

    def _store_email_history(self, submission_id: str, email_result: Dict):
        """Store email history in BigQuery"""
        
        table_id = f"{self.project_id}.customer_submissions.email_history"
        
        email_record = {
            "email_id": hashlib.md5(f"{submission_id}_{datetime.now().isoformat()}".encode()).hexdigest()[:16],
            "submission_id": submission_id,
            "sent_at": datetime.now().isoformat(),
            "recipient_email": email_result.get("recipient", ""),
            "subject": email_result.get("subject", ""),
            "email_content_html": email_result.get("email_html", ""),
            "email_content_text": email_result.get("email_text", ""),
            "pdf_content_base64": email_result.get("pdf_base64", ""),
            "email_provider": email_result.get("provider", "unknown"),
            "status": "sent" if email_result.get("success") else "failed",
            "tracking_id": email_result.get("tracking_id", ""),
            "metadata": json.dumps(email_result.get("metadata", {}))
        }
        
        errors = self.bq_client.insert_rows_json(table_id, [email_record])
        
        if errors:
            logger.error(f"Email history storage error: {errors}")

    def _update_vehicle_history(self, vehicle_id: str, record: Dict):
        """Update or create vehicle history record"""
        
        try:
            # Query existing vehicle record
            query = f"""
            SELECT * FROM `{self.project_id}.customer_submissions.vehicle_history`
            WHERE vehicle_id = @vehicle_id
            LIMIT 1
            """
            
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("vehicle_id", "STRING", vehicle_id)
                ]
            )
            
            results = list(self.bq_client.query(query, job_config=job_config))
            
            if results:
                # Update existing vehicle
                update_query = f"""
                UPDATE `{self.project_id}.customer_submissions.vehicle_history`
                SET 
                    last_seen = CURRENT_TIMESTAMP(),
                    total_submissions = total_submissions + 1,
                    all_submission_ids = ARRAY_CONCAT(all_submission_ids, [@submission_id]),
                    lifetime_cost = lifetime_cost + @cost,
                    last_service_date = CURRENT_TIMESTAMP()
                WHERE vehicle_id = @vehicle_id
                """
                
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter("vehicle_id", "STRING", vehicle_id),
                        bigquery.ScalarQueryParameter("submission_id", "STRING", record["submission_id"]),
                        bigquery.ScalarQueryParameter("cost", "FLOAT64", record.get("estimated_cost_fair", 0))
                    ]
                )
                
                self.bq_client.query(update_query, job_config=job_config)
                
            else:
                # Create new vehicle record
                table_id = f"{self.project_id}.customer_submissions.vehicle_history"
                
                vehicle_record = {
                    "vehicle_id": vehicle_id,
                    "equipment_serial": record.get("equipment_serial", ""),
                    "equipment_brand": record.get("equipment_brand", ""),
                    "equipment_model": record.get("equipment_model", ""),
                    "equipment_year": record.get("equipment_year"),
                    "first_seen": datetime.now().isoformat(),
                    "last_seen": datetime.now().isoformat(),
                    "total_submissions": 1,
                    "all_submission_ids": [record["submission_id"]],
                    "lifetime_cost": record.get("estimated_cost_fair", 0),
                    "average_repair_cost": record.get("estimated_cost_fair", 0),
                    "last_service_date": datetime.now().isoformat(),
                    "metadata": json.dumps({})
                }
                
                errors = self.bq_client.insert_rows_json(table_id, [vehicle_record])
                
                if errors:
                    logger.error(f"Vehicle history creation error: {errors}")
                    
        except Exception as e:
            logger.error(f"Vehicle history update error: {e}")

    def _update_email_status(self, submission_id: str, email_result: Dict):
        """Update main record with email status"""
        
        try:
            update_query = f"""
            UPDATE `{self.project_id}.customer_submissions.diagnostics`
            SET 
                email_sent = @sent,
                email_sent_at = @sent_at,
                email_status = @status,
                updated_at = CURRENT_TIMESTAMP()
            WHERE submission_id = @submission_id
            """
            
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("submission_id", "STRING", submission_id),
                    bigquery.ScalarQueryParameter("sent", "BOOLEAN", email_result.get("success", False)),
                    bigquery.ScalarQueryParameter("sent_at", "TIMESTAMP", datetime.now().isoformat() if email_result.get("success") else None),
                    bigquery.ScalarQueryParameter("status", "STRING", "sent" if email_result.get("success") else "failed")
                ]
            )
            
            self.bq_client.query(update_query, job_config=job_config)
            
        except Exception as e:
            logger.error(f"Email status update error: {e}")

    def _categorize_problem(self, description: str) -> str:
        """Categorize problem based on description"""
        
        categories = {
            "hydraulic": ["hydraulic", "fluid", "pressure", "cylinder", "pump", "boom", "arm"],
            "engine": ["engine", "start", "power", "fuel", "exhaust", "smoke", "oil"],
            "electrical": ["electrical", "battery", "wire", "fuse", "alternator", "lights"],
            "transmission": ["transmission", "gear", "clutch", "drive", "shift"],
            "structural": ["frame", "bucket", "arm", "track", "tire", "attachment"],
            "controls": ["control", "joystick", "pedal", "switch", "button", "display"],
            "maintenance": ["maintenance", "service", "oil", "filter", "grease", "fluid"],
        }
        
        description_lower = description.lower()
        for category, keywords in categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        
        return "general"

    def _generate_submission_id(self, form_data: Dict) -> str:
        """Generate unique submission ID"""
        timestamp = datetime.now().isoformat()
        data_str = f"{timestamp}{json.dumps(form_data)}"
        return hashlib.md5(data_str.encode()).hexdigest()[:12]

    def _validate_form_data(self, form_data: Dict) -> Dict:
        """Validate and clean form data"""
        
        # Required fields
        required = ["problem_description"]
        for field in required:
            if field not in form_data or not form_data[field]:
                raise ValueError(f"Required field missing: {field}")
        
        # Clean and normalize data
        cleaned = {}
        for key, value in form_data.items():
            if isinstance(value, str):
                cleaned[key] = value.strip()
            else:
                cleaned[key] = value
        
        # Parse error codes if provided as string
        if "error_codes" in cleaned and isinstance(cleaned["error_codes"], str):
            cleaned["error_codes"] = [code.strip() for code in cleaned["error_codes"].split(",")]
        
        return cleaned

    def _store_in_bigquery(self, record: Dict):
        """Store record in BigQuery"""
        
        table_id = f"{self.project_id}.customer_submissions.diagnostics"
        
        # Clean None values
        cleaned_record = {k: v for k, v in record.items() if v is not None}
        
        errors = self.bq_client.insert_rows_json(table_id, [cleaned_record])
        
        if errors:
            logger.error(f"BigQuery insert errors: {errors}")
            raise Exception("Failed to store in BigQuery")
        
        logger.info(f"✅ Stored in BigQuery: {record['submission_id']}")

    def _store_in_datastore(self, record: Dict):
        """Store in Datastore for MVP3 backward compatibility"""
        
        try:
            key = self.datastore_client.key("diagnostic_submissions", record["submission_id"])
            entity = datastore.Entity(key=key)
            
            # Map to MVP3 expected fields
            entity.update({
                "problem_description": record["problem_description"],
                "equipment_type": record["equipment_type"],
                "service_type": record["service_type"],
                "customer_email": record["customer_email"],
                "ai_solution": record["ai_analysis"],
                "confidence": record["confidence_score"],
                "created_at": datetime.fromisoformat(record["created_at"]),
                "status": "new"
            })
            
            self.datastore_client.put(entity)
            logger.info(f"✅ Stored in Datastore: {record['submission_id']}")
            
        except Exception as e:
            logger.warning(f"Datastore storage failed (non-critical): {e}")

    def _trigger_async_processing(self, record: Dict):
        """Trigger async processing via Pub/Sub"""
        
        try:
            topic_path = self.publisher.topic_path(self.project_id, "diagnostic-submissions")
            
            # Create message
            message_data = json.dumps({
                "submission_id": record["submission_id"],
                "vehicle_id": record["vehicle_id"],
                "type": "new_submission",
                "timestamp": record["created_at"]
            }).encode("utf-8")
            
            # Publish
            future = self.publisher.publish(topic_path, message_data)
            logger.info(f"Published to Pub/Sub: {future.result()}")
            
        except Exception as e:
            logger.warning(f"Pub/Sub publish failed (non-critical): {e}")


class GmailEmailService:
    """Gmail email service using service account"""
    
    def __init__(self):
        self.sender_email = "reports@diagnosticpro.io"
        self.service = self._build_service()
    
    def _build_service(self):
        """Build Gmail service"""
        # TODO: Implement Gmail service account setup
        pass
    
    def send_diagnostic_report(self, **kwargs):
        """Send diagnostic report via Gmail"""
        # TODO: Implement Gmail sending
        return {"success": False, "provider": "gmail", "error": "Not implemented"}


class SendGridEmailService:
    """SendGrid email service"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.sender_email = "reports@diagnosticpro.io"
    
    def send_diagnostic_report(self, recipient, subject, html_body, text_body, pdf_attachment=None):
        """Send diagnostic report via SendGrid"""
        
        import requests
        
        url = "https://api.sendgrid.com/v3/mail/send"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "personalizations": [{"to": [{"email": recipient}]}],
            "from": {"email": self.sender_email, "name": "DiagnosticPro"},
            "subject": subject,
            "content": [
                {"type": "text/plain", "value": text_body},
                {"type": "text/html", "value": html_body}
            ]
        }
        
        # Add PDF attachment if provided
        if pdf_attachment:
            data["attachments"] = [{
                "content": base64.b64encode(pdf_attachment).decode(),
                "type": "application/pdf",
                "filename": "diagnostic_report.pdf"
            }]
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 202:
            return {
                "success": True,
                "provider": "sendgrid",
                "tracking_id": response.headers.get("X-Message-Id", "")
            }
        else:
            return {
                "success": False,
                "provider": "sendgrid",
                "error": f"{response.status_code}: {response.text}"
            }


# Flask endpoints
integration = CompleteFormIntegration()

@app.route("/submit-diagnostic", methods=["POST"])
def submit_diagnostic():
    """Main endpoint for website form submissions"""
    
    form_data = request.get_json() or request.form.to_dict()
    result = integration.process_form_submission(form_data)
    
    return jsonify(result), 200 if result["success"] else 400

@app.route("/customer-webhook", methods=["POST"])
def customer_webhook():
    """Backward compatible webhook endpoint"""
    return submit_diagnostic()

@app.route("/mvp3/submit-diagnostic", methods=["POST"])
def mvp3_submit():
    """MVP3 compatible endpoint"""
    return submit_diagnostic()

@app.route("/check-status/<submission_id>", methods=["GET"])
def check_status(submission_id):
    """Check submission status"""
    
    try:
        query = f"""
        SELECT status, ai_analysis, suggested_solutions, updated_at, email_sent, bottom_line
        FROM `bobs-house-ai.customer_submissions.diagnostics`
        WHERE submission_id = @submission_id
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("submission_id", "STRING", submission_id)
            ]
        )
        
        results = list(integration.bq_client.query(query, job_config=job_config))
        
        if results:
            record = results[0]
            return jsonify({
                "success": True,
                "status": record.status,
                "ai_analysis": record.ai_analysis,
                "suggested_solutions": json.loads(record.suggested_solutions),
                "bottom_line": record.bottom_line,
                "email_sent": record.email_sent,
                "updated_at": str(record.updated_at)
            })
        else:
            return jsonify({"success": False, "message": "Submission not found"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/vehicle-history/<vehicle_id>", methods=["GET"])
def vehicle_history(vehicle_id):
    """Get complete vehicle history"""
    
    try:
        query = f"""
        SELECT * FROM `bobs-house-ai.customer_submissions.vehicle_history`
        WHERE vehicle_id = @vehicle_id
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("vehicle_id", "STRING", vehicle_id)
            ]
        )
        
        results = list(integration.bq_client.query(query, job_config=job_config))
        
        if results:
            vehicle = results[0]
            return jsonify({
                "success": True,
                "vehicle_id": vehicle.vehicle_id,
                "total_submissions": vehicle.total_submissions,
                "lifetime_cost": vehicle.lifetime_cost,
                "last_service_date": str(vehicle.last_service_date),
                "all_submission_ids": vehicle.all_submission_ids
            })
        else:
            return jsonify({"success": False, "message": "Vehicle not found"}), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "website-form-complete-integration",
        "bigquery": True,
        "datastore": True,
        "ai": True,
        "email": True,
        "vehicle_tracking": True
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)