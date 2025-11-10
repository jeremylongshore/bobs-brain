# Agent-to-Agent (A2A) Workflow Conversion - DiagnosticPro

**Created:** 2025-10-29
**Current Architecture:** Monolithic Vertex AI + PDF Generation
**Proposed Architecture:** Multi-Agent Collaborative System

---

## Current Workflow (Monolithic)

```
Customer Form → Firestore
     ↓
Stripe Payment → Webhook
     ↓
Single Backend Process:
  1. Call Vertex AI (one big prompt, 15 sections)
  2. Parse response
  3. Generate PDF
  4. Upload to Cloud Storage
  5. Update Firestore
  6. Send email
```

**Problems:**
- Single point of failure
- No parallelization
- Hard to improve individual sections
- Can't iterate on specific agent expertise
- No ability to verify/critique between steps
- Difficult to add specialized knowledge

---

## Proposed A2A Workflow

### Architecture Overview

```
Customer Form → Orchestrator Agent (Coordinator)
     ↓
Specialized Agents (Parallel Execution):
  ├── Diagnostic Agent (Primary diagnosis)
  ├── Technical Agent (Technical education, parts)
  ├── Financial Agent (Cost breakdown, ripoff detection)
  ├── Communication Agent (Shop interrogation, conversation scripts)
  └── Research Agent (Source verification, OEM data)
     ↓
Critic Agent (Validates outputs)
     ↓
Synthesis Agent (Combines into coherent report)
     ↓
PDF Agent (Generates formatted report)
     ↓
Delivery Agent (Upload, email, notifications)
```

---

## Agent Breakdown

### 1. **Orchestrator Agent** (Coordinator)
**Role:** Traffic control and workflow management

**Responsibilities:**
- Receive customer submission
- Parse and structure input data
- Assign tasks to specialized agents
- Monitor agent progress
- Handle failures and retries
- Coordinate timing and dependencies

**Tech Stack:**
- LangGraph for orchestration
- Firestore for state management
- Pub/Sub for agent communication

**Inputs:**
- Customer diagnostic submission
- Equipment details
- Symptoms and codes

**Outputs:**
- Task assignments to specialized agents
- Status updates to Firestore
- Error handling and escalation

---

### 2. **Diagnostic Agent** (Primary Analysis)
**Role:** Core technical diagnosis

**Responsibilities:**
- Analyze symptoms and error codes
- Determine primary diagnosis
- Create differential diagnosis
- Rank likely causes by probability
- Provide diagnostic verification steps

**Specialized Knowledge:**
- OBD-II code database
- J1939 heavy equipment protocols
- TSB (Technical Service Bulletins) database
- Failure mode patterns

**Prompts:**
- "You are a master diagnostic technician with 30 years of experience..."
- Access to RAG database of repair cases
- Context: Make, model, year, mileage, codes

**Outputs:**
- `primaryDiagnosis` (with confidence %)
- `differentialDiagnosis` (ranked alternatives)
- `diagnosticVerification` (test procedures)
- `likelyCausesRanked` (probability distribution)

---

### 3. **Technical Agent** (Education & Parts)
**Role:** Technical knowledge and OEM specifications

**Responsibilities:**
- Explain system operation
- Provide technical education
- Identify OEM part numbers
- Source authentic parts strategy
- Explain failure mechanisms

**Specialized Knowledge:**
- OEM service manuals
- Part number cross-references
- System diagrams and schematics
- Manufacturer technical bulletins

**Prompts:**
- "Explain this automotive system to a technically-minded owner..."
- "Provide OEM part numbers and sourcing strategy..."

**Outputs:**
- `technicalEducation`
- `oemPartsStrategy`
- `rootCauseAnalysis` (deep technical dive)

---

### 4. **Financial Agent** (Cost & Fraud Detection)
**Role:** Pricing analysis and ripoff protection

**Responsibilities:**
- Analyze shop quote fairness
- Detect overcharges and scams
- Provide fair price ranges
- Identify unnecessary repairs
- Authorization recommendations

**Specialized Knowledge:**
- Mitchell/AllData labor times
- Parts pricing databases
- Regional shop rate averages
- Common scam patterns

**Prompts:**
- "Analyze this shop quote for fairness and identify red flags..."
- "Calculate fair price range for this repair in this region..."

**Outputs:**
- `costBreakdown` (parts + labor + markup)
- `ripoffDetection` (scam identification)
- `authorizationGuide` (approve/reject/negotiate)

---

### 5. **Communication Agent** (Customer Coaching)
**Role:** Human interaction strategy

**Responsibilities:**
- Write shop interrogation questions
- Create conversation scripts
- Develop negotiation tactics
- Coach customer communication
- Provide empowerment strategies

**Specialized Knowledge:**
- Negotiation psychology
- Shop communication patterns
- Consumer protection laws
- Effective questioning techniques

**Prompts:**
- "Create 5 technical questions to test this mechanic's competence..."
- "Write a word-for-word negotiation script for this scenario..."

**Outputs:**
- `shopInterrogation` (5 technical questions)
- `conversationScripting` (verbatim dialogue)
- `negotiationTactics` (specific strategies)

---

### 6. **Research Agent** (Source Verification)
**Role:** Evidence and references

**Responsibilities:**
- Find authoritative sources
- Link to TSBs and recalls
- Verify technical claims
- Provide regulatory references
- Research specific failure modes

**Tools:**
- Web search API
- NHTSA database access
- Manufacturer TSB databases
- Technical forum scraping
- YouTube repair video database

**Outputs:**
- `sourceVerification` (links, TSBs, recalls)
- `recommendations` (next steps with citations)

---

### 7. **Critic Agent** (Quality Control)
**Role:** Validate and improve agent outputs

**Responsibilities:**
- Review all agent outputs
- Check for consistency
- Identify contradictions
- Verify technical accuracy
- Flag missing information
- Request revisions

**Prompts:**
- "Review this diagnosis and identify any technical errors..."
- "Check if the cost analysis matches the repair complexity..."
- "Ensure the conversation script aligns with the diagnosis..."

**Outputs:**
- Validation report
- Revision requests to agents
- Quality score per section
- Go/no-go decision

---

### 8. **Synthesis Agent** (Report Compiler)
**Role:** Combine agent outputs into coherent narrative

**Responsibilities:**
- Integrate 15 sections
- Ensure narrative flow
- Remove redundancy
- Add transitions
- Maintain consistent tone
- Create executive summary

**Outputs:**
- Unified analysis object
- 15 polished sections
- Executive summary
- Coherent 2000+ word report

---

### 9. **PDF Agent** (Document Generation)
**Role:** Format and render final report

**Responsibilities:**
- Apply production PDF generator
- Validate section completeness
- Handle typography and layout
- Generate cover page
- Add disclaimers
- Control pagination

**Existing Code:** `reportPdfProduction.js` (already built!)

**Outputs:**
- PDF buffer
- Page count validation
- Section completeness check

---

### 10. **Delivery Agent** (Distribution)
**Role:** Upload and notify customer

**Responsibilities:**
- Upload PDF to Cloud Storage
- Generate signed URLs
- Send email with report
- Update Firestore status
- Log delivery metrics
- Handle failures and retries

**Outputs:**
- Cloud Storage path
- Signed URL
- Email delivery confirmation
- Status updates

---

## Implementation Approaches

### Option 1: LangGraph (Recommended)
**Framework:** LangGraph (LangChain)

**Pros:**
- Built for agent orchestration
- State management included
- Visual workflow graphs
- Easy to debug and monitor
- Good documentation

**Architecture:**
```python
from langgraph.graph import StateGraph, END

# Define workflow graph
workflow = StateGraph(DiagnosticState)

# Add agent nodes
workflow.add_node("orchestrator", orchestrator_agent)
workflow.add_node("diagnostic", diagnostic_agent)
workflow.add_node("financial", financial_agent)
workflow.add_node("communication", communication_agent)
workflow.add_node("technical", technical_agent)
workflow.add_node("research", research_agent)
workflow.add_node("critic", critic_agent)
workflow.add_node("synthesis", synthesis_agent)
workflow.add_node("pdf", pdf_agent)
workflow.add_node("delivery", delivery_agent)

# Define edges (workflow paths)
workflow.add_edge("orchestrator", "diagnostic")
workflow.add_edge("orchestrator", "financial")
workflow.add_edge("orchestrator", "communication")
workflow.add_edge("orchestrator", "technical")
workflow.add_edge("orchestrator", "research")

# All agents → critic
workflow.add_edge("diagnostic", "critic")
workflow.add_edge("financial", "critic")
workflow.add_edge("communication", "critic")
workflow.add_edge("technical", "critic")
workflow.add_edge("research", "critic")

# Critic → synthesis → PDF → delivery
workflow.add_edge("critic", "synthesis")
workflow.add_edge("synthesis", "pdf")
workflow.add_edge("pdf", "delivery")
workflow.add_edge("delivery", END)

app = workflow.compile()
```

**Cost:** Same as current (uses Vertex AI per agent)

---

### Option 2: CrewAI
**Framework:** CrewAI (specialized for multi-agent tasks)

**Pros:**
- Designed for agent collaboration
- Role-based agents
- Built-in memory and context
- Easy agent definition

**Architecture:**
```python
from crewai import Agent, Task, Crew

# Define agents
diagnostic_agent = Agent(
    role='Master Diagnostic Technician',
    goal='Provide accurate primary and differential diagnosis',
    backstory='30 years automotive repair experience...',
    tools=[code_lookup, tsb_search],
    verbose=True
)

financial_agent = Agent(
    role='Automotive Cost Analyst',
    goal='Detect overcharges and provide fair pricing',
    backstory='Expert in labor rates and parts pricing...',
    tools=[pricing_db, labor_time_lookup],
    verbose=True
)

# Define tasks
diagnostic_task = Task(
    description='Analyze symptoms and codes...',
    agent=diagnostic_agent
)

financial_task = Task(
    description='Review shop quote for fairness...',
    agent=financial_agent
)

# Create crew
crew = Crew(
    agents=[diagnostic_agent, financial_agent, ...],
    tasks=[diagnostic_task, financial_task, ...],
    process='sequential'  # or 'hierarchical'
)

result = crew.kickoff()
```

---

### Option 3: Custom Orchestration (Maximum Control)
**Framework:** Custom Node.js/Python with Pub/Sub

**Pros:**
- Full control
- Minimal dependencies
- Easy to optimize
- Can use existing Cloud Run infrastructure

**Architecture:**
```javascript
// Agent orchestrator (Cloud Run service)
app.post('/webhook/stripe', async (req, res) => {
  const submissionId = req.body.submissionId;

  // 1. Kick off parallel agents via Pub/Sub
  await Promise.all([
    pubsub.topic('diagnostic-agent').publish({ submissionId }),
    pubsub.topic('financial-agent').publish({ submissionId }),
    pubsub.topic('communication-agent').publish({ submissionId }),
    pubsub.topic('technical-agent').publish({ submissionId }),
    pubsub.topic('research-agent').publish({ submissionId })
  ]);

  // 2. Each agent writes results to Firestore
  // 3. Critic agent monitors for completion
  // 4. Synthesis agent combines results
  // 5. PDF and delivery agents finalize
});

// Individual agent (separate Cloud Run service)
app.post('/agent/diagnostic', async (req, res) => {
  const { submissionId } = req.body;

  // Load submission from Firestore
  const submission = await firestore
    .collection('diagnosticSubmissions')
    .doc(submissionId)
    .get();

  // Call Vertex AI with specialized prompt
  const result = await vertexAI.generate({
    prompt: diagnosticPrompt(submission.data()),
    model: 'gemini-2.5-flash'
  });

  // Save to Firestore
  await firestore.collection('agentOutputs').doc(submissionId).set({
    diagnostic: result,
    timestamp: new Date(),
    agentId: 'diagnostic-v1'
  }, { merge: true });
});
```

---

## Infrastructure Changes

### New Services Required

1. **Agent Services (Cloud Run)** - 10 services
   - `orchestrator-agent`
   - `diagnostic-agent`
   - `financial-agent`
   - `communication-agent`
   - `technical-agent`
   - `research-agent`
   - `critic-agent`
   - `synthesis-agent`
   - `pdf-agent`
   - `delivery-agent`

2. **Pub/Sub Topics** - For agent communication
   - `diagnostic-tasks`
   - `agent-results`
   - `critic-reviews`
   - `synthesis-ready`

3. **Firestore Collections** - Enhanced state management
   - `agentTasks` - Task queue
   - `agentOutputs` - Individual agent results
   - `agentStatus` - Progress tracking
   - `criticReviews` - Quality control results

4. **Cloud Scheduler** - Timeout management
   - Monitor stuck agents
   - Trigger retries
   - Escalate failures

---

## Cost Analysis

### Current System
- **1 Vertex AI call** per diagnostic (~20K chars output)
- **Cost:** ~$0.02 per diagnostic
- **Latency:** 15-30 seconds

### A2A System
- **5-7 parallel Vertex AI calls** (smaller specialized prompts)
- **1 critic call** (validation)
- **1 synthesis call** (combination)
- **Total:** 7-9 Vertex AI calls
- **Cost:** ~$0.08-$0.12 per diagnostic (4-6x higher)
- **Latency:** 20-40 seconds (similar, thanks to parallelization)

**Cost Increase:** ~$0.08 per diagnostic
**Monthly at 1000 diagnostics:** +$80/month

---

## Benefits of A2A

### 1. **Specialization**
- Each agent becomes an expert in its domain
- Easier to improve individual sections
- Can swap models per agent (Gemini vs Claude vs GPT)

### 2. **Parallelization**
- 5 agents run simultaneously
- Faster than sequential processing
- Better resource utilization

### 3. **Quality Control**
- Critic agent catches errors before delivery
- Can request revisions from specific agents
- Higher quality output

### 4. **Flexibility**
- Add new agents without changing others
- A/B test different agent strategies
- Easy to upgrade individual components

### 5. **Debugging**
- See which agent failed
- Retry specific agents only
- Better error tracking

### 6. **Scalability**
- Each agent scales independently
- Can prioritize critical agents
- Horizontal scaling per agent type

---

## Migration Path

### Phase 1: Parallel Testing (No Customer Impact)
1. Keep existing monolithic system running
2. Build A2A system in parallel
3. Run both on same diagnostic inputs
4. Compare quality and cost
5. **Timeline:** 2-3 weeks

### Phase 2: Hybrid System (Gradual Rollout)
1. Route 10% traffic to A2A
2. Monitor quality metrics
3. Compare customer satisfaction
4. Gradually increase to 50%
5. **Timeline:** 2-4 weeks

### Phase 3: Full Cutover
1. Route 100% to A2A
2. Keep monolithic as fallback
3. Monitor for 2 weeks
4. Deprecate old system
5. **Timeline:** 1-2 weeks

**Total Migration:** 5-9 weeks

---

## Risks & Mitigations

### Risk 1: Higher Cost
**Impact:** 4-6x increase in AI API costs
**Mitigation:**
- Test with smaller models for some agents
- Cache common agent responses
- Batch multiple diagnostics
- Increase price to $5.99 or $6.99

### Risk 2: Increased Complexity
**Impact:** More moving parts, harder to debug
**Mitigation:**
- Comprehensive logging per agent
- Visual workflow monitoring (LangSmith)
- Automated health checks
- Clear rollback plan

### Risk 3: Latency
**Impact:** Could be slower than monolithic
**Mitigation:**
- Parallel execution (5 agents at once)
- Async processing with notifications
- Set aggressive timeouts
- Monitor P95 latency

### Risk 4: Consistency
**Impact:** Agents might contradict each other
**Mitigation:**
- Critic agent validates consistency
- Synthesis agent resolves conflicts
- Clear agent guidelines and prompts
- Shared context between agents

---

## Recommendation

### Immediate Action: **Option 1 (LangGraph)**

**Why:**
1. Best balance of control and ease
2. Visual workflow debugging
3. Production-ready framework
4. Easy to scale and modify
5. Good documentation and community

**Start With:**
1. Build orchestrator + 3 core agents (diagnostic, financial, communication)
2. Test quality vs current system
3. Add remaining agents iteratively
4. Deploy critic agent for quality control
5. Full A2A rollout

**Timeline:** 6-8 weeks to production
**Cost Impact:** +$80-120/month at current volume
**Quality Impact:** Likely +15-25% improvement

---

## Next Steps

1. **Approve A2A approach** (LangGraph recommended)
2. **Set up LangGraph development environment**
3. **Build proof-of-concept with 3 agents**
4. **Compare quality on 10 test diagnostics**
5. **Decide on full migration or abort**

---

**Document Status:** DRAFT - Awaiting Approval
**Author:** Claude Code
**Date:** 2025-10-29
