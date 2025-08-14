#!/usr/bin/env python3
"""
Website Form to BigQuery Integration
Maintains backward compatibility while enabling enhanced data collection
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, Optional

import google.generativeai as genai
from flask import Flask, jsonify, request
from google.cloud import bigquery, datastore, pubsub_v1

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


class WebsiteFormIntegration:
    """Handle website form submissions with BigQuery and AI integration"""

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

        # Ensure tables exist
        self._ensure_tables()

        logger.info("Website form integration initialized")

    def _ensure_tables(self):
        """Ensure BigQuery tables exist for form submissions"""

        # Create customer submissions dataset
        dataset_id = f"{self.project_id}.customer_submissions"
        dataset = bigquery.Dataset(dataset_id)
        dataset.description = "Customer diagnostic submissions from website"
        dataset.location = "US"

        self.bq_client.create_dataset(dataset, exists_ok=True)

        # Create main submissions table with enhanced schema
        table_id = f"{dataset_id}.diagnostics"
        schema = self._get_enhanced_schema()

        table = bigquery.Table(table_id, schema=schema)
        table.clustering_fields = ["customer_type", "equipment_type", "created_at"]
        table.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.DAY, field="created_at")

        self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"✅ Table ready: {table_id}")

    def _get_enhanced_schema(self):
        """Get the enhanced schema for customer submissions"""
        return [
            # Core submission fields
            bigquery.SchemaField("submission_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
            # Customer fields (from website form)
            bigquery.SchemaField("customer_name", "STRING"),
            bigquery.SchemaField("customer_email", "STRING"),
            bigquery.SchemaField("customer_phone", "STRING"),
            bigquery.SchemaField("customer_company", "STRING"),
            bigquery.SchemaField("customer_type", "STRING"),
            # Equipment fields (from form)
            bigquery.SchemaField("equipment_type", "STRING"),
            bigquery.SchemaField("equipment_brand", "STRING"),
            bigquery.SchemaField("equipment_model", "STRING"),
            bigquery.SchemaField("equipment_serial", "STRING"),
            # Problem fields (from form)
            bigquery.SchemaField("problem_description", "STRING"),
            bigquery.SchemaField("problem_category", "STRING"),
            bigquery.SchemaField("error_codes", "STRING", mode="REPEATED"),
            bigquery.SchemaField("service_type", "STRING"),
            bigquery.SchemaField("urgency_level", "STRING"),
            # AI processing fields
            bigquery.SchemaField("ai_analysis", "STRING"),
            bigquery.SchemaField("suggested_solutions", "JSON"),
            bigquery.SchemaField("confidence_score", "FLOAT64"),
            bigquery.SchemaField("similar_cases", "JSON"),
            # Tracking fields
            bigquery.SchemaField("session_id", "STRING"),
            bigquery.SchemaField("ip_address", "STRING"),
            bigquery.SchemaField("user_agent", "STRING"),
            bigquery.SchemaField("submission_source", "STRING"),
            # Status fields
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("assigned_to", "STRING"),
            bigquery.SchemaField("resolution", "STRING"),
            bigquery.SchemaField("resolution_time", "INTEGER"),
            # Neo4j integration
            bigquery.SchemaField("neo4j_node_id", "STRING"),
            # Metadata
            bigquery.SchemaField("metadata", "JSON"),
        ]

    def process_form_submission(self, form_data: Dict) -> Dict:
        """Process website form submission"""

        try:
            # 1. Generate submission ID
            submission_id = self._generate_submission_id(form_data)

            # 2. Validate and clean form data
            cleaned_data = self._validate_form_data(form_data)

            # 3. Get AI analysis
            ai_response = self._get_ai_analysis(cleaned_data)

            # 4. Prepare complete record
            record = {
                "submission_id": submission_id,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                # Customer data
                "customer_name": cleaned_data.get("customer_name", ""),
                "customer_email": cleaned_data.get("customer_email", ""),
                "customer_phone": cleaned_data.get("customer_phone", ""),
                "customer_company": cleaned_data.get("customer_company", ""),
                "customer_type": cleaned_data.get("customer_type", "individual"),
                # Equipment data
                "equipment_type": cleaned_data.get("equipment_type", ""),
                "equipment_brand": cleaned_data.get("equipment_brand", ""),
                "equipment_model": cleaned_data.get("equipment_model", ""),
                "equipment_serial": cleaned_data.get("equipment_serial", ""),
                # Problem data
                "problem_description": cleaned_data.get("problem_description", ""),
                "problem_category": self._categorize_problem(cleaned_data.get("problem_description", "")),
                "error_codes": cleaned_data.get("error_codes", []),
                "service_type": cleaned_data.get("service_type", "repair"),
                "urgency_level": cleaned_data.get("urgency_level", "normal"),
                # AI analysis
                "ai_analysis": ai_response.get("analysis", ""),
                "suggested_solutions": json.dumps(ai_response.get("solutions", [])),
                "confidence_score": ai_response.get("confidence", 0.5),
                "similar_cases": json.dumps(ai_response.get("similar_cases", [])),
                # Tracking
                "session_id": cleaned_data.get("session_id", ""),
                "ip_address": request.remote_addr if request else "",
                "user_agent": request.headers.get("User-Agent", "") if request else "",
                "submission_source": "website",
                # Status
                "status": "new",
                "assigned_to": "",
                "resolution": "",
                "resolution_time": None,
                # Metadata
                "metadata": json.dumps(cleaned_data.get("metadata", {})),
            }

            # 5. Store in BigQuery
            self._store_in_bigquery(record)

            # 6. Store in Datastore for backward compatibility
            self._store_in_datastore(record)

            # 7. Trigger async processing
            self._trigger_async_processing(record)

            # 8. Send to Neo4j
            self._send_to_neo4j(record)

            return {
                "success": True,
                "submission_id": submission_id,
                "ai_analysis": ai_response.get("analysis", ""),
                "suggested_solutions": ai_response.get("solutions", []),
                "message": "Your submission has been received and is being processed.",
            }

        except Exception as e:
            logger.error(f"Form processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "There was an error processing your submission. Please try again.",
            }

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

    def _categorize_problem(self, description: str) -> str:
        """Categorize problem based on description"""

        categories = {
            "hydraulic": ["hydraulic", "fluid", "pressure", "cylinder", "pump"],
            "engine": ["engine", "start", "power", "fuel", "exhaust"],
            "electrical": ["electrical", "battery", "wire", "fuse", "alternator"],
            "transmission": ["transmission", "gear", "clutch", "drive"],
            "structural": ["frame", "bucket", "arm", "track", "tire"],
            "controls": ["control", "joystick", "pedal", "switch", "button"],
            "maintenance": ["maintenance", "service", "oil", "filter", "grease"],
        }

        description_lower = description.lower()
        for category, keywords in categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category

        return "general"

    def _get_ai_analysis(self, data: Dict) -> Dict:
        """Get AI analysis using Gemini"""

        try:
            # Build enhanced prompt with all context
            current_datetime = datetime.now().isoformat()
            equipment_type = data.get("equipment_type", "Unknown")
            equipment_brand = data.get("equipment_brand", "")
            equipment_model = data.get("equipment_model", "")
            equipment_year = data.get("equipment_year", "")
            equipment_hours = data.get("equipment_hours", "")
            equipment_serial = data.get("equipment_serial", "")
            problem_description = data.get("problem_description", "")
            error_codes = ", ".join(data.get("error_codes", [])) if data.get("error_codes") else "None"
            service_type = data.get("service_type", "repair")
            customer_type = data.get("customer_type", "individual")
            repair_history = data.get("repair_history", "Not available")

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
  "analysis": "full markdown formatted analysis",
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
                        "Contact support for detailed diagnosis",
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
                        "Can you provide a written estimate?",
                    ],
                    "diy_feasible": False,
                    "parts_needed": [],
                    "labor_hours": {"book": 0, "actual": 0},
                    "warranty_applies": False,
                }

            return result

        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return {
                "analysis": "Unable to generate AI analysis at this time. Error has been logged.",
                "solutions": [
                    "Contact support for manual analysis",
                    "Document all symptoms with photos/videos",
                    "Get multiple shop opinions",
                    "Request detailed diagnostic reports",
                    "Save all error codes displayed",
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
                    "What's included in your warranty?",
                ],
                "diy_feasible": False,
                "parts_needed": [],
                "labor_hours": {"book": 0, "actual": 0},
                "warranty_applies": False,
            }

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
        """Store in Datastore for backward compatibility"""

        try:
            key = self.datastore_client.key("diagnostic_submissions", record["submission_id"])
            entity = datastore.Entity(key=key)

            # Map to MVP3 expected fields
            entity.update(
                {
                    "problem_description": record["problem_description"],
                    "equipment_type": record["equipment_type"],
                    "service_type": record["service_type"],
                    "customer_email": record["customer_email"],
                    "ai_solution": record["ai_analysis"],
                    "confidence": record["confidence_score"],
                    "created_at": datetime.fromisoformat(record["created_at"]),
                    "status": "new",
                }
            )

            self.datastore_client.put(entity)
            logger.info(f"✅ Stored in Datastore: {record['submission_id']}")

        except Exception as e:
            logger.warning(f"Datastore storage failed (non-critical): {e}")

    def _trigger_async_processing(self, record: Dict):
        """Trigger async processing via Pub/Sub"""

        try:
            topic_path = self.publisher.topic_path(self.project_id, "diagnostic-submissions")

            # Create message
            message_data = json.dumps(
                {"submission_id": record["submission_id"], "type": "new_submission", "timestamp": record["created_at"]}
            ).encode("utf-8")

            # Publish
            future = self.publisher.publish(topic_path, message_data)
            logger.info(f"Published to Pub/Sub: {future.result()}")

        except Exception as e:
            logger.warning(f"Pub/Sub publish failed (non-critical): {e}")

    def _send_to_neo4j(self, record: Dict):
        """Send to Neo4j for knowledge graph storage"""

        try:
            # This would connect to Neo4j Aura
            # For now, just log the intent
            logger.info(f"Would send to Neo4j: {record['submission_id']}")

        except Exception as e:
            logger.warning(f"Neo4j storage failed (non-critical): {e}")


# Flask endpoints for website integration
integration = WebsiteFormIntegration()


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
        SELECT status, ai_analysis, suggested_solutions, updated_at
        FROM `bobs-house-ai.customer_submissions.diagnostics`
        WHERE submission_id = @submission_id
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("submission_id", "STRING", submission_id)]
        )

        results = list(integration.bq_client.query(query, job_config=job_config))

        if results:
            record = results[0]
            return jsonify(
                {
                    "success": True,
                    "status": record.status,
                    "ai_analysis": record.ai_analysis,
                    "suggested_solutions": json.loads(record.suggested_solutions),
                    "updated_at": str(record.updated_at),
                }
            )
        else:
            return jsonify({"success": False, "message": "Submission not found"}), 404

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(
        {"status": "healthy", "service": "website-form-integration", "bigquery": True, "datastore": True, "ai": True}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
