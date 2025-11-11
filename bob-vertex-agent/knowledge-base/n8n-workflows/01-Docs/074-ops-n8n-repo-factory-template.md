# N8N Workflow Template + Repo Factory + Sync

Use this operator prompt to build a reusable template repo and a repo factory + sync so you can drop many workflows into pre-made repos fast.

## OPERATOR PROMPT — n8n Workflow Template + Repo Factory + Sync

### Vars (set all)
```bash
ORG="<your-github-org>"
DEFAULT_BRANCH="main"
GH_SSH="git@github.com:$ORG"
TEMPLATE_REPO="n8n-workflow-template"        # will be created
WORKDIR="$HOME/n8n-repo-factory"
mkdir -p "$WORKDIR" && cd "$WORKDIR"
```

### 1) Create template repo locally
```bash
mkdir -p "$TEMPLATE_REPO"/{workflows,ops,.github/workflows,docs}
cat > "$TEMPLATE_REPO/README.md" <<'MD'
# n8n Workflow Repo
Minimal repo for a single n8n workflow or a small set.

## Quickstart
- Put JSON files in /workflows
- Import to n8n: `./ops/import-workflows.sh`
- Export from n8n: `./ops/export-workflows.sh`
MD

cat > "$TEMPLATE_REPO/.env.example" <<'ENV'
N8N_HOST=n8n.example.com
N8N_ENCRYPTION_KEY=REPLACE_WITH_LONG_RANDOM
ENV

cat > "$TEMPLATE_REPO/.github/workflows/ci.yml" <<'YML'
name: ci
on:
  pull_request:
    paths: ["workflows/**/*.json"]
  push:
    branches: ["main"]
    paths: ["workflows/**/*.json"]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint JSON
        run: |
          find workflows -name '*.json' -print0 | xargs -0 -I{} jq -e . {} >/dev/null
      - name: Shape check
        run: |
          for f in $(find workflows -name '*.json'); do
            jq -e '.nodes and .connections' "$f" >/dev/null || { echo "Bad workflow: $f"; exit 1; }
          done || true
YML

cat > "$TEMPLATE_REPO/ops/import-workflows.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
DIR="${1:-./workflows}"
CID=$(docker compose ps -q n8n 2>/dev/null || true)
[ -n "$CID" ] || { echo "Run near your n8n compose, or edit script to target remote."; exit 1; }
for f in "$DIR"/*.json; do [ -e "$f" ] || continue; echo "Import $f"; docker exec -i "$CID" n8n import:workflow --input=/proc/self/fd/0 < "$f"; done
SH
chmod +x "$TEMPLATE_REPO/ops/import-workflows.sh"

cat > "$TEMPLATE_REPO/ops/export-workflows.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-./workflows}"
CID=$(docker compose ps -q n8n 2>/dev/null || true)
[ -n "$CID" ] || { echo "Run near your n8n compose, or edit script to target remote."; exit 1; }
mkdir -p "$OUT"
docker exec "$CID" bash -lc "mkdir -p /home/node/.n8n/exported && n8n export:workflow --output=/home/node/.n8n/exported"
docker cp "$CID":/home/node/.n8n/exported/. "$OUT"
SH
chmod +x "$TEMPLATE_REPO/ops/export-workflows.sh"

git -C "$TEMPLATE_REPO" init
git -C "$TEMPLATE_REPO" add .
git -C "$TEMPLATE_REPO" commit -m "chore: template scaffold"
```

### 2) Create remote template repo on GitHub and push
```bash
gh repo create "$ORG/$TEMPLATE_REPO" --private --source "$TEMPLATE_REPO" --push --remote origin
gh api -X PATCH repos/$ORG/$TEMPLATE_REPO -f is_template=true
```

### 3) Repo Factory script (creates many repos from template)
```bash
cat > "$WORKDIR/repo-factory.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ORG="${ORG:?set ORG}"
TEMPLATE_REPO="${TEMPLATE_REPO:-n8n-workflow-template}"
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"
LIST_FILE="${1:-repos.txt}"   # one repo name per line

while read -r NAME; do
  [ -z "$NAME" ] && continue
  echo "Create $NAME from template..."
  gh repo create "$ORG/$NAME" --private --template "$ORG/$TEMPLATE_REPO" --confirm
  git clone "git@github.com:$ORG/$NAME.git"
  ( cd "$NAME" && git checkout -B "$DEFAULT_BRANCH" && git push -u origin "$DEFAULT_BRANCH" )
done < "$LIST_FILE"
SH
chmod +x "$WORKDIR/repo-factory.sh"
```

### 4) Sync script (push local workflows into matching repos)
```bash
# Convention: local folder structure: ./seed/<repo-name>/*.json
mkdir -p "$WORKDIR/seed"
cat > "$WORKDIR/sync-workflows.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
ORG="${ORG:?set ORG}"
ROOT="$(pwd)"
SEED_DIR="${1:-$ROOT/seed}"

for d in "$SEED_DIR"/*; do
  [ -d "$d" ] || continue
  REPO="$(basename "$d")"
  echo "Sync $REPO"
  if [ ! -d "$ROOT/$REPO/.git" ]; then
    git clone "git@github.com:$ORG/$REPO.git" "$ROOT/$REPO"
  fi
  rsync -a --delete "$d"/ "$ROOT/$REPO/workflows"/
  (
    cd "$ROOT/$REPO"
    git add workflows
    if ! git diff --cached --quiet; then
      git commit -m "chore(workflows): sync from seed"
      git push origin HEAD
    else
      echo "No changes for $REPO"
    fi
  )
done
SH
chmod +x "$WORKDIR/sync-workflows.sh"
```

### 5) Usage
```bash
# a) Prepare a list of repos to create
cat > "$WORKDIR/repos.txt" <<'TXT'
n8n-flow-leads-intake
n8n-flow-rss-to-slack
n8n-flow-gmail-to-sheets
TXT

# b) Create repos from template
export ORG="$ORG" TEMPLATE_REPO="$TEMPLATE_REPO" DEFAULT_BRANCH="$DEFAULT_BRANCH"
"$WORKDIR/repo-factory.sh" "$WORKDIR/repos.txt"

# c) Drop workflows into seed/<repo-name>/*.json and sync
# Example seed
mkdir -p "$WORKDIR/seed/n8n-flow-rss-to-slack"
echo '{}' > "$WORKDIR/seed/n8n-flow-rss-to-slack/example.json"   # replace with real
export ORG="$ORG"
"$WORKDIR/sync-workflows.sh" "$WORKDIR/seed"

echo "Done. Repos created from template and workflows synced."
```

## What you get:
- A template repo (n8n-workflow-template) set as "template" on GitHub.
- A factory to create many repos from it using a list.
- A sync that copies JSON workflows from seed/<repo>/ into each repo's /workflows and commits.

## Fast path:
- Put each workflow set under seed/<repo-name>/.
- Run sync-workflows.sh.
- Open PRs or push straight to main per your policy.

Want a variant that uses a single monorepo with folders per workflow and still deploys them separately to your VM?