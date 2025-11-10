# A2A Architecture with Google Genkit + ADK SDK

**Created:** 2025-10-29
**Framework:** Google Genkit (Firebase Genkit)
**Platform:** Google Cloud Ecosystem
**Agent Framework:** ADK (Agent Development Kit)

---

## Why Genkit + Google Ecosystem?

### Perfect Fit for DiagnosticPro

✅ **Already on Google Cloud:**
- Vertex AI Gemini 2.5 Flash (current AI)
- Cloud Run (backend hosting)
- Firestore (database)
- Cloud Storage (reports)
- Cloud Functions (webhooks)

✅ **Genkit Advantages:**
- Native Vertex AI integration
- Built-in observability (Firebase)
- TypeScript/JavaScript (matches current Node.js backend)
- Flow-based agent orchestration
- Native Firestore state management
- Firebase Functions deployment

✅ **ADK SDK Benefits:**
- Agent-to-agent communication primitives
- Built-in message passing
- State management across agents
- Error handling and retries
- Monitoring and tracing

---

## Genkit Architecture Overview

```typescript
// DiagnosticPro A2A with Genkit
import { genkit, z } from 'genkit';
import { vertexAI } from '@genkit-ai/vertexai';
import { firebaseAuth } from '@genkit-ai/firebase/auth';
import { onFlow, noAuth } from '@genkit-ai/firebase/functions';

// Initialize Genkit with Vertex AI
const ai = genkit({
  plugins: [
    vertexAI({
      projectId: 'diagnostic-pro-prod',
      location: 'us-central1',
    }),
  ],
  model: 'vertexai/gemini-2.5-flash',
});

// Define diagnostic workflow
export const diagnosticWorkflow = onFlow(
  ai,
  {
    name: 'diagnosticWorkflow',
    inputSchema: z.object({
      submissionId: z.string(),
      make: z.string(),
      model: z.string(),
      year: z.string(),
      symptoms: z.string(),
      errorCodes: z.array(z.string()),
    }),
    outputSchema: z.object({
      reportUrl: z.string(),
      analysisComplete: z.boolean(),
    }),
  },
  async (input) => {
    // Orchestrated A2A workflow
    const agentResults = await Promise.all([
      diagnosticAgent(input),
      financialAgent(input),
      communicationAgent(input),
      technicalAgent(input),
      researchAgent(input),
    ]);

    const criticResult = await criticAgent(agentResults);
    const synthesisResult = await synthesisAgent(criticResult);
    const pdfResult = await pdfAgent(synthesisResult);
    const deliveryResult = await deliveryAgent(pdfResult);

    return deliveryResult;
  }
);
```

---

## Agent Architecture with Genkit

### 1. Orchestrator Flow (Main Workflow)

```typescript
import { genkit } from 'genkit';
import { vertexAI } from '@genkit-ai/vertexai';
import { onFlow } from '@genkit-ai/firebase/functions';
import { Firestore } from '@google-cloud/firestore';

const ai = genkit({
  plugins: [vertexAI({ projectId: 'diagnostic-pro-prod' })],
});

const firestore = new Firestore();

// Main orchestrator flow
export const diagnosticOrchestrator = onFlow(
  ai,
  {
    name: 'diagnosticOrchestrator',
    inputSchema: DiagnosticSubmissionSchema,
    outputSchema: DiagnosticReportSchema,
  },
  async (submission) => {
    // 1. Store initial state in Firestore
    const sessionRef = firestore.collection('agentSessions').doc(submission.id);
    await sessionRef.set({
      status: 'processing',
      startedAt: new Date().toISOString(),
      submission,
    });

    try {
      // 2. Parallel agent execution
      console.log('🚀 Starting parallel agent execution...');
      const [diagnostic, financial, communication, technical, research] =
        await Promise.all([
          diagnosticAgent.run(submission),
          financialAgent.run(submission),
          communicationAgent.run(submission),
          technicalAgent.run(submission),
          researchAgent.run(submission),
        ]);

      // 3. Store agent results
      await sessionRef.update({
        agentResults: {
          diagnostic,
          financial,
          communication,
          technical,
          research,
        },
        agentPhaseComplete: true,
      });

      // 4. Critic validation
      console.log('🔍 Running critic validation...');
      const criticReview = await criticAgent.run({
        diagnostic,
        financial,
        communication,
        technical,
        research,
      });

      // 5. Handle critic feedback (retry if needed)
      if (!criticReview.approved) {
        console.log('⚠️ Critic requested revisions:', criticReview.issues);
        // Implement retry logic here
        throw new Error('Critic validation failed');
      }

      // 6. Synthesis
      console.log('📝 Synthesizing final report...');
      const synthesis = await synthesisAgent.run({
        agentResults: { diagnostic, financial, communication, technical, research },
        criticReview,
      });

      // 7. PDF Generation
      console.log('📄 Generating PDF...');
      const pdf = await pdfAgent.run({
        submission,
        analysis: synthesis,
      });

      // 8. Delivery
      console.log('📧 Delivering report...');
      const delivery = await deliveryAgent.run({
        submissionId: submission.id,
        pdfBuffer: pdf.buffer,
        email: submission.email,
      });

      // 9. Final state update
      await sessionRef.update({
        status: 'completed',
        completedAt: new Date().toISOString(),
        reportUrl: delivery.reportUrl,
      });

      return {
        reportUrl: delivery.reportUrl,
        analysisComplete: true,
      };

    } catch (error) {
      await sessionRef.update({
        status: 'failed',
        error: error.message,
        failedAt: new Date().toISOString(),
      });
      throw error;
    }
  }
);
```

---

### 2. Diagnostic Agent (Genkit Flow)

```typescript
import { defineFlow } from 'genkit';
import { vertexAI } from '@genkit-ai/vertexai';

// Define diagnostic agent as a Genkit flow
export const diagnosticAgent = defineFlow(
  {
    name: 'diagnosticAgent',
    inputSchema: DiagnosticSubmissionSchema,
    outputSchema: DiagnosticAnalysisSchema,
  },
  async (submission) => {
    // Use Vertex AI Gemini with specialized diagnostic prompt
    const result = await ai.generate({
      model: 'vertexai/gemini-2.5-flash',
      prompt: {
        text: generateDiagnosticPrompt(submission),
      },
      config: {
        temperature: 0.3, // More deterministic for diagnostic work
        topP: 0.8,
        maxOutputTokens: 4096,
      },
    });

    // Parse structured output
    const analysis = parseDiagnosticAnalysis(result.text);

    // Validate analysis
    if (!analysis.primaryDiagnosis || !analysis.differentialDiagnosis) {
      throw new Error('Incomplete diagnostic analysis');
    }

    return {
      primaryDiagnosis: analysis.primaryDiagnosis,
      differentialDiagnosis: analysis.differentialDiagnosis,
      diagnosticVerification: analysis.diagnosticVerification,
      likelyCausesRanked: analysis.likelyCausesRanked,
      confidence: analysis.confidence,
      agentId: 'diagnostic-v1',
      timestamp: new Date().toISOString(),
    };
  }
);

function generateDiagnosticPrompt(submission) {
  return `You are a master diagnostic technician with 30 years of experience across all equipment types.

CUSTOMER SUBMISSION:
- Equipment: ${submission.year} ${submission.make} ${submission.model}
- Type: ${submission.equipmentType}
- Mileage/Hours: ${submission.mileageHours}
- Error Codes: ${submission.errorCodes.join(', ')}
- Symptoms: ${submission.symptoms}
- Problem Description: ${submission.problemDescription}

YOUR TASK: Provide expert diagnostic analysis in these sections:

1. PRIMARY DIAGNOSIS
   - Most likely root cause
   - Confidence percentage (0-100%)
   - Technical reasoning

2. DIFFERENTIAL DIAGNOSIS
   - Alternative causes (ranked by likelihood)
   - Each with probability percentage
   - Why each could cause these symptoms

3. DIAGNOSTIC VERIFICATION
   - Exact tests to confirm diagnosis
   - Tools required
   - Expected test results (numerical values)

4. LIKELY CAUSES (RANKED)
   - All possible causes with percentages
   - Must sum to 100%

FORMAT: Use clear headings and bullet points. Be technical but explain clearly.`;
}
```

---

### 3. Financial Agent (Genkit Flow)

```typescript
export const financialAgent = defineFlow(
  {
    name: 'financialAgent',
    inputSchema: z.object({
      submission: DiagnosticSubmissionSchema,
      diagnosticResult: DiagnosticAnalysisSchema, // Can access other agent results
    }),
    outputSchema: FinancialAnalysisSchema,
  },
  async ({ submission, diagnosticResult }) => {
    // Build context-aware prompt using diagnostic findings
    const prompt = `You are an automotive cost analyst and consumer protection expert.

DIAGNOSIS: ${diagnosticResult.primaryDiagnosis}

SHOP QUOTE: ${submission.shopQuoteAmount || 'Not provided'}
SHOP RECOMMENDATION: ${submission.shopRecommendation || 'Not provided'}

YOUR TASK: Provide financial protection analysis:

1. COST BREAKDOWN
   - Fair parts cost (OEM and aftermarket)
   - Fair labor cost (regional shop rates)
   - Reasonable markup
   - Total fair price range

2. RIPOFF DETECTION
   - Red flags in shop quote
   - Common scams for this repair
   - Overcharge analysis
   - Unnecessary repairs identified

3. AUTHORIZATION GUIDE
   - Approve, reject, or get second opinion
   - Specific recommendations
   - Negotiation leverage points

Be specific with dollar amounts and percentages.`;

    const result = await ai.generate({
      model: 'vertexai/gemini-2.5-flash',
      prompt: { text: prompt },
      config: {
        temperature: 0.2, // Very deterministic for financial analysis
        maxOutputTokens: 3072,
      },
    });

    return parseFinancialAnalysis(result.text);
  }
);
```

---

### 4. Communication Agent (Genkit Flow)

```typescript
export const communicationAgent = defineFlow(
  {
    name: 'communicationAgent',
    inputSchema: CommunicationInputSchema,
    outputSchema: CommunicationOutputSchema,
  },
  async ({ submission, diagnosticResult }) => {
    const prompt = `You are a customer empowerment coach and negotiation expert.

DIAGNOSIS: ${diagnosticResult.primaryDiagnosis}
CUSTOMER SITUATION: ${submission.problemDescription}

YOUR TASK: Empower the customer with communication tools:

1. SHOP INTERROGATION (5 questions)
   - Technical questions to test mechanic competence
   - Questions they should answer correctly
   - Red flags in wrong answers

2. CONVERSATION SCRIPTING
   - Word-for-word dialogue for phone/in-person
   - Professional but firm tone
   - How to ask for explanations

3. NEGOTIATION TACTICS
   - Specific negotiation strategies
   - Price reduction approaches
   - When to walk away
   - Leverage points

Make it actionable and specific. Give exact phrases to use.`;

    const result = await ai.generate({
      model: 'vertexai/gemini-2.5-flash',
      prompt: { text: prompt },
      config: {
        temperature: 0.4, // Slightly creative for conversation scripts
        maxOutputTokens: 3072,
      },
    });

    return parseCommunicationAnalysis(result.text);
  }
);
```

---

### 5. Technical Agent (Genkit Flow)

```typescript
export const technicalAgent = defineFlow(
  {
    name: 'technicalAgent',
    inputSchema: TechnicalInputSchema,
    outputSchema: TechnicalOutputSchema,
  },
  async ({ submission, diagnosticResult }) => {
    const prompt = `You are a technical educator and OEM parts specialist.

EQUIPMENT: ${submission.year} ${submission.make} ${submission.model}
DIAGNOSIS: ${diagnosticResult.primaryDiagnosis}

YOUR TASK: Provide technical education and parts strategy:

1. TECHNICAL EDUCATION
   - How this system works
   - Why it failed
   - Failure mechanism explained simply
   - Future prevention

2. OEM PARTS STRATEGY
   - Specific OEM part numbers
   - Cross-references and alternatives
   - Where to buy authentic parts
   - How to verify authenticity

3. ROOT CAUSE ANALYSIS
   - Deep technical dive
   - Engineering perspective
   - System interactions
   - Contributing factors

Be technical but clear. Include specific part numbers.`;

    const result = await ai.generate({
      model: 'vertexai/gemini-2.5-flash',
      prompt: { text: prompt },
      config: {
        temperature: 0.3,
        maxOutputTokens: 4096,
      },
    });

    return parseTechnicalAnalysis(result.text);
  }
);
```

---

### 6. Research Agent (Genkit Flow with Tools)

```typescript
import { defineTool } from 'genkit';

// Define research tools
const tsbSearchTool = defineTool(
  {
    name: 'tsbSearch',
    description: 'Search NHTSA database for Technical Service Bulletins',
    inputSchema: z.object({
      make: z.string(),
      model: z.string(),
      year: z.string(),
    }),
    outputSchema: z.object({
      tsbs: z.array(z.object({
        number: z.string(),
        title: z.string(),
        summary: z.string(),
      })),
    }),
  },
  async ({ make, model, year }) => {
    // Call NHTSA API
    const response = await fetch(
      `https://api.nhtsa.gov/products/vehicle/tsbs?make=${make}&model=${model}&modelYear=${year}`
    );
    return await response.json();
  }
);

const recallSearchTool = defineTool(
  {
    name: 'recallSearch',
    description: 'Search for safety recalls',
    inputSchema: z.object({
      make: z.string(),
      model: z.string(),
      year: z.string(),
    }),
    outputSchema: z.object({
      recalls: z.array(z.object({
        campaignNumber: z.string(),
        component: z.string(),
        summary: z.string(),
      })),
    }),
  },
  async ({ make, model, year }) => {
    // Call NHTSA recalls API
    const response = await fetch(
      `https://api.nhtsa.gov/products/vehicle/recalls?make=${make}&model=${model}&modelYear=${year}`
    );
    return await response.json();
  }
);

// Research agent with tools
export const researchAgent = defineFlow(
  {
    name: 'researchAgent',
    inputSchema: ResearchInputSchema,
    outputSchema: ResearchOutputSchema,
    tools: [tsbSearchTool, recallSearchTool],
  },
  async ({ submission, diagnosticResult }) => {
    // Agent can use tools automatically
    const result = await ai.generate({
      model: 'vertexai/gemini-2.5-flash',
      prompt: {
        text: `Find authoritative sources for this diagnosis:

EQUIPMENT: ${submission.year} ${submission.make} ${submission.model}
DIAGNOSIS: ${diagnosticResult.primaryDiagnosis}

YOUR TASK:
1. Search for relevant TSBs
2. Check for safety recalls
3. Find manufacturer documentation
4. Provide authoritative sources

Use the tsbSearch and recallSearch tools.`,
      },
      tools: [tsbSearchTool, recallSearchTool],
      config: {
        temperature: 0.2,
      },
    });

    return parseResearchAnalysis(result.text, result.toolCalls);
  }
);
```

---

### 7. Critic Agent (Validation Flow)

```typescript
export const criticAgent = defineFlow(
  {
    name: 'criticAgent',
    inputSchema: z.object({
      diagnostic: DiagnosticAnalysisSchema,
      financial: FinancialAnalysisSchema,
      communication: CommunicationOutputSchema,
      technical: TechnicalOutputSchema,
      research: ResearchOutputSchema,
    }),
    outputSchema: z.object({
      approved: z.boolean(),
      issues: z.array(z.string()),
      score: z.number(),
      recommendations: z.array(z.string()),
    }),
  },
  async (agentResults) => {
    const prompt = `You are a quality control expert reviewing multi-agent diagnostic analysis.

AGENT OUTPUTS:
Diagnostic: ${JSON.stringify(agentResults.diagnostic, null, 2)}
Financial: ${JSON.stringify(agentResults.financial, null, 2)}
Communication: ${JSON.stringify(agentResults.communication, null, 2)}
Technical: ${JSON.stringify(agentResults.technical, null, 2)}
Research: ${JSON.stringify(agentResults.research, null, 2)}

YOUR TASK: Validate for:
1. Internal consistency (do agents agree?)
2. Technical accuracy (any errors?)
3. Completeness (all sections present?)
4. Logic (does reasoning make sense?)
5. Safety (appropriate urgency level?)

RESPOND WITH:
- approved: true/false
- issues: array of problems found
- score: 0-100
- recommendations: how to improve

Be strict. Flag ANY inconsistencies or technical errors.`;

    const result = await ai.generate({
      model: 'vertexai/gemini-2.5-flash',
      prompt: { text: prompt },
      config: {
        temperature: 0.1, // Very deterministic for criticism
        maxOutputTokens: 2048,
      },
    });

    return parseCriticReview(result.text);
  }
);
```

---

### 8. Synthesis Agent (Combination Flow)

```typescript
export const synthesisAgent = defineFlow(
  {
    name: 'synthesisAgent',
    inputSchema: SynthesisInputSchema,
    outputSchema: FinalAnalysisSchema,
  },
  async ({ agentResults, criticReview }) => {
    const prompt = `You are a master writer combining specialist reports into one coherent diagnostic report.

AGENT OUTPUTS:
${JSON.stringify(agentResults, null, 2)}

CRITIC FEEDBACK:
${JSON.stringify(criticReview, null, 2)}

YOUR TASK: Create a unified, professional 15-section report:
1. PRIMARY DIAGNOSIS
2. DIFFERENTIAL DIAGNOSIS
3. DIAGNOSTIC VERIFICATION
4. SHOP INTERROGATION
5. CONVERSATION SCRIPTING
6. COST BREAKDOWN
7. RIPOFF DETECTION
8. AUTHORIZATION GUIDE
9. TECHNICAL EDUCATION
10. OEM PARTS STRATEGY
11. NEGOTIATION TACTICS
12. LIKELY CAUSES (RANKED)
13. RECOMMENDATIONS
14. SOURCE VERIFICATION
15. ROOT CAUSE ANALYSIS

Ensure:
- Seamless narrative flow
- No contradictions
- Consistent tone
- Remove redundancy
- Add smooth transitions
- Maintain technical accuracy

FORMAT: Each section as markdown with clear headings.`;

    const result = await ai.generate({
      model: 'vertexai/gemini-2.5-flash',
      prompt: { text: prompt },
      config: {
        temperature: 0.4, // Balanced for creative synthesis
        maxOutputTokens: 8192, // Larger for full report
      },
    });

    return parseSynthesizedReport(result.text);
  }
);
```

---

### 9. PDF Agent (Already Built!)

```typescript
import { generateDiagnosticProPDF } from './reportPdfProduction.js';

export const pdfAgent = defineFlow(
  {
    name: 'pdfAgent',
    inputSchema: PdfInputSchema,
    outputSchema: z.object({
      buffer: z.instanceof(Buffer),
      pageCount: z.number(),
      valid: z.boolean(),
    }),
  },
  async ({ submission, analysis }) => {
    const tempPath = `/tmp/report_${submission.id}.pdf`;

    // Use existing production PDF generator
    const stream = await generateDiagnosticProPDF(submission, analysis, tempPath);

    return new Promise((resolve, reject) => {
      stream.on('finish', () => {
        const fs = require('fs');
        const buffer = fs.readFileSync(tempPath);
        const pageCount = Math.floor(buffer.length / 4096); // Rough estimate
        fs.unlinkSync(tempPath);

        resolve({
          buffer,
          pageCount,
          valid: pageCount > 5 && pageCount < 30,
        });
      });

      stream.on('error', reject);
    });
  }
);
```

---

### 10. Delivery Agent (Upload & Email)

```typescript
import { Storage } from '@google-cloud/storage';
import { sendEmail } from './emailService';

const storage = new Storage();
const bucket = storage.bucket('diagnostic-pro-prod-reports');

export const deliveryAgent = defineFlow(
  {
    name: 'deliveryAgent',
    inputSchema: DeliveryInputSchema,
    outputSchema: z.object({
      reportUrl: z.string(),
      emailSent: z.boolean(),
      uploadedAt: z.string(),
    }),
  },
  async ({ submissionId, pdfBuffer, email }) => {
    // 1. Upload to Cloud Storage
    const fileName = `reports/${submissionId}.pdf`;
    const file = bucket.file(fileName);

    await file.save(pdfBuffer, {
      metadata: {
        contentType: 'application/pdf',
        metadata: { submissionId },
      },
    });

    // 2. Generate signed URL (24 hour expiry)
    const [signedUrl] = await file.getSignedUrl({
      action: 'read',
      expires: Date.now() + 24 * 60 * 60 * 1000,
    });

    // 3. Update Firestore
    const firestore = new Firestore();
    await firestore.collection('diagnosticSubmissions').doc(submissionId).update({
      status: 'ready',
      reportUrl: signedUrl,
      completedAt: new Date().toISOString(),
    });

    // 4. Send email
    const emailSent = await sendEmail({
      to: email,
      subject: 'Your DiagnosticPro Report is Ready',
      body: `Your diagnostic report is ready! Download: ${signedUrl}`,
      attachments: [
        {
          filename: `DiagnosticPro-${submissionId}.pdf`,
          content: pdfBuffer,
        },
      ],
    });

    return {
      reportUrl: signedUrl,
      emailSent,
      uploadedAt: new Date().toISOString(),
    };
  }
);
```

---

## Deployment Architecture

### Cloud Run Services (Genkit Functions)

```yaml
# Deploy each agent as a Cloud Run service
services:
  - orchestrator:
      memory: 1Gi
      cpu: 2
      timeout: 300s

  - diagnostic-agent:
      memory: 512Mi
      cpu: 1
      timeout: 60s

  - financial-agent:
      memory: 512Mi
      cpu: 1
      timeout: 60s

  - communication-agent:
      memory: 512Mi
      cpu: 1
      timeout: 60s

  - technical-agent:
      memory: 512Mi
      cpu: 1
      timeout: 60s

  - research-agent:
      memory: 512Mi
      cpu: 1
      timeout: 90s  # Needs extra time for API calls

  - critic-agent:
      memory: 512Mi
      cpu: 1
      timeout: 60s

  - synthesis-agent:
      memory: 1Gi
      cpu: 1
      timeout: 120s  # Larger output

  - pdf-agent:
      memory: 512Mi
      cpu: 1
      timeout: 30s

  - delivery-agent:
      memory: 512Mi
      cpu: 1
      timeout: 60s
```

---

## Deployment Commands

### 1. Initialize Genkit Project

```bash
cd /home/jeremy/000-projects/diagnostic-platform/DiagnosticPro/02-src/backend

# Initialize Genkit
npm install -D genkit-cli
npx genkit init

# Install Genkit plugins
npm install @genkit-ai/vertexai
npm install @genkit-ai/firebase
npm install @genkit-ai/googleai
npm install genkit
```

### 2. Project Structure

```
services/
├── backend-genkit/           # New Genkit A2A system
│   ├── src/
│   │   ├── agents/
│   │   │   ├── orchestrator.ts
│   │   │   ├── diagnostic.ts
│   │   │   ├── financial.ts
│   │   │   ├── communication.ts
│   │   │   ├── technical.ts
│   │   │   ├── research.ts
│   │   │   ├── critic.ts
│   │   │   ├── synthesis.ts
│   │   │   ├── pdf.ts
│   │   │   └── delivery.ts
│   │   ├── flows/
│   │   │   └── diagnostic-workflow.ts
│   │   ├── tools/
│   │   │   ├── tsb-search.ts
│   │   │   └── recall-search.ts
│   │   ├── schemas/
│   │   │   └── types.ts
│   │   └── index.ts
│   ├── genkit.config.ts
│   ├── package.json
│   └── tsconfig.json
└── backend/                  # Current system (keep as fallback)
```

### 3. Deploy to Cloud Run

```bash
# Deploy orchestrator
gcloud run deploy diagnosticpro-orchestrator \
  --source ./services/backend-genkit \
  --region us-central1 \
  --project diagnostic-pro-prod \
  --memory 1Gi \
  --cpu 2 \
  --timeout 300s

# Deploy each agent (can parallelize)
for agent in diagnostic financial communication technical research critic synthesis pdf delivery; do
  gcloud run deploy diagnosticpro-agent-${agent} \
    --source ./services/backend-genkit \
    --region us-central1 \
    --project diagnostic-pro-prod \
    --memory 512Mi \
    --cpu 1 \
    --timeout 60s \
    --set-env-vars AGENT_TYPE=${agent}
done
```

---

## Monitoring with Firebase/Genkit

### Built-in Observability

```typescript
// Genkit automatically tracks:
// - Flow execution time
// - Agent performance
// - Token usage per agent
// - Error rates
// - Retry attempts

// View in Firebase Console
// https://console.firebase.google.com/project/diagnostic-pro-prod/genkit
```

### Custom Metrics

```typescript
import { trace } from '@genkit-ai/core/tracing';

export const diagnosticAgent = defineFlow(
  /* ... */,
  async (submission) => {
    return trace(
      {
        name: 'diagnostic-agent-execution',
        metadata: {
          submissionId: submission.id,
          equipmentType: submission.equipmentType,
        },
      },
      async () => {
        const start = Date.now();
        const result = await ai.generate(/* ... */);
        const duration = Date.now() - start;

        // Custom metrics
        console.log(JSON.stringify({
          agent: 'diagnostic',
          duration,
          tokenCount: result.usage.totalTokens,
          submissionId: submission.id,
        }));

        return result;
      }
    );
  }
);
```

---

## Cost Comparison

### Current System
- 1 Vertex AI call: ~$0.02
- Total: **$0.02/diagnostic**

### Genkit A2A System
- 5 parallel agents: ~$0.08
- 1 critic: ~$0.02
- 1 synthesis: ~$0.03
- Total: **~$0.13/diagnostic**

### At Scale
- 1000 diagnostics/month
- Current: $20/month
- Genkit A2A: $130/month
- **Increase: +$110/month**

**Solution:** Increase price from $4.99 to $6.99 ($2 increase = $2000/month revenue increase, covers AI costs + profit)

---

## Migration Timeline

### Week 1-2: Setup & Core Agents
- [ ] Initialize Genkit project
- [ ] Build orchestrator flow
- [ ] Implement diagnostic agent
- [ ] Implement financial agent
- [ ] Implement communication agent

### Week 3-4: Complete Agent Suite
- [ ] Implement technical agent
- [ ] Implement research agent with tools
- [ ] Implement critic agent
- [ ] Implement synthesis agent
- [ ] Integrate existing PDF agent

### Week 5-6: Testing & Deployment
- [ ] Integration testing (10 test diagnostics)
- [ ] Deploy to Cloud Run
- [ ] A/B test (10% traffic)
- [ ] Monitor quality metrics

### Week 7-8: Full Rollout
- [ ] Increase to 50% traffic
- [ ] Compare quality scores
- [ ] Full cutover to A2A
- [ ] Deprecate monolithic system

**Total: 8 weeks**

---

## Next Steps

1. ✅ Approve Genkit + ADK approach
2. 🔄 Initialize Genkit project structure
3. 🔄 Build proof-of-concept with 3 agents
4. 🔄 Test quality vs current system
5. 🔄 Deploy to staging environment
6. 🔄 Production rollout

---

**Recommendation: PROCEED with Genkit + Google ecosystem**

- Perfect fit for existing infrastructure
- Native Vertex AI integration
- TypeScript matches current codebase
- Built-in observability
- Production-ready framework

Ready to start building? I can initialize the Genkit project structure right now.
