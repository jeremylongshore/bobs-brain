import os, requests
# ----- LLM -----
def llm_client():
    p = os.getenv("PROVIDER", "anthropic")
    m = os.getenv("MODEL", "claude-3-5-sonnet-20240620")

    if p == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        def call(prompt: str):
            msg = client.messages.create(model=m, max_tokens=2048,
                messages=[{"role":"user","content":prompt}])
            return "".join([b.text for b in msg.content if getattr(b, "type","")== "text"])
        return call

    if p == "google":
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel(m)
        return lambda prompt: model.generate_content(prompt).text

    if p == "openrouter":
        key = os.getenv("OPENROUTER_API_KEY")
        url = "https://openrouter.ai/api/v1/chat/completions"
        def call(prompt: str):
            r = requests.post(url, headers={"Authorization": f"Bearer {key}"},
                json={"model": m, "messages":[{"role":"user","content":prompt}]}, timeout=120).json()
            return r["choices"][0]["message"]["content"]
        return call

    if p == "ollama":
        base = os.getenv("OLLAMA_BASE_URL","http://localhost:11434").rstrip("/")
        model = os.getenv("OLLAMA_MODEL","llama3.1:8b")
        def call(prompt: str):
            r = requests.post(f"{base}/api/generate", json={"model":model,"prompt":prompt}, timeout=180).json()
            return r.get("response","")
        return call

    if p == "vertex":
        # stub hook for your Vertex wrapper if you use it
        raise NotImplementedError("Vertex wrapper not wired in this minimal repo.")
    raise ValueError(f"Unknown PROVIDER={p}")

# ----- State DB -----
def state_db():
    from sqlalchemy import create_engine
    return create_engine(os.getenv("DATABASE_URL","sqlite:///./bb.db"), future=True)

# ----- Vector store -----
def vector_store():
    vb = os.getenv("VECTOR_BACKEND","chroma")
    if vb == "chroma":
        from chromadb import PersistentClient
        return PersistentClient(path=os.getenv("CHROMA_DIR",".chroma"))
    if vb == "pgvector":
        raise NotImplementedError("PGVector wrapper out of scope for minimal repo.")
    if vb == "pinecone":
        raise NotImplementedError("Pinecone wrapper out of scope for minimal repo.")
    raise ValueError(f"Unknown VECTOR_BACKEND={vb}")

# ----- Graph -----
def graph_db():
    if os.getenv("GRAPH_BACKEND","none") != "neo4j":
        return None
    from neo4j import GraphDatabase
    return GraphDatabase.driver(os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD")))

# ----- Cache -----
def cache_client():
    if os.getenv("CACHE_BACKEND","none") != "redis":
        return None
    import redis
    return redis.from_url(os.getenv("REDIS_URL"))

# ----- Artifacts -----
def artifact_store():
    if os.getenv("ARTIFACT_BACKEND","local") == "local":
        os.makedirs(os.getenv("ARTIFACT_DIR","./artifacts"), exist_ok=True)
        return ("local", os.getenv("ARTIFACT_DIR","./artifacts"))
    import boto3
    s3 = boto3.client("s3",
        aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
        endpoint_url=os.getenv("S3_ENDPOINT"))
    return ("s3", s3, os.getenv("S3_BUCKET"))