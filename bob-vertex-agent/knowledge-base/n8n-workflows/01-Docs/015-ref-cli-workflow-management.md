# N8N CLI Workflow Management Guide

Yes, but with limits. n8n doesn't ship a full CLI editor for workflows, but you can manage them in a few ways:

## 1. REST API (official)
- Every workflow is just JSON.
- You can GET/POST/PUT to the API to list, create, update, or delete workflows.
- Example (with API key):

```bash
curl -H "Authorization: Bearer $N8N_API_KEY" \
     https://n8n.yourdomain.com/rest/workflows

curl -X PUT -H "Authorization: Bearer $N8N_API_KEY" \
     -H "Content-Type: application/json" \
     -d @workflow.json \
     https://n8n.yourdomain.com/rest/workflows/12
```

## 2. Export/Import CLI

Inside the container you can run:

```bash
# export all workflows
docker exec -ti n8n n8n export:workflow --output=/home/node/.n8n/exported

# import from JSON
docker exec -ti n8n n8n import:workflow --input=/home/node/.n8n/myworkflow.json
```

This is the easiest for version control. Workflows live as JSON files you can edit, then re-import.

## 3. Version control approach
- Export workflows as JSON to a Git repo.
- Edit them (JSON or via a VS Code extension for n8n).
- Commit, review, merge.
- On deploy: import the updated JSON back into your VM's n8n instance.
- You can automate this with a GitHub Action or a local make deploy script.

## 4. Limitations
- CLI/API editing = JSON only. There's no "node palette" outside the web UI.
- Large or complex workflows are easier to design in the browser, then export.
- Best pattern: design in UI → export to Git → review/edit → import via CLI/API.

---

**Pro tip**: set up a dev n8n (local Docker) and a prod n8n (VM). Export from dev, review in Git, then import into prod. It's cleaner than hand-editing production workflows live.

Want me to write you a ready-to-use bash script that pulls workflows from Git, imports them to your VM's n8n, and can be run as `./deploy-workflows.sh`?