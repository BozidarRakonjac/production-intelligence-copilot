# Hybrid search - combines semantic (pgvector) and keyword (PostgreSQL) search

import json
from sqlalchemy import create_engine, text
from core.config import DATABASE_URL, VECTOR_SEARCH_TOP_K, KEYWORD_SEARCH_TOP_K, FINAL_TOP_K
from services.embedding import embed_query


def get_engine():
    return create_engine(DATABASE_URL)


def semantic_search(query: str, filters: dict) -> list[dict]:
    """Search pgvector for semantically similar content."""
    engine = get_engine()
    query_embedding = embed_query(query)
    embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

    # Build metadata filters
    where_clauses = ["1=1"]
    if filters.get("filter_machine_type"):
        where_clauses.append(f"metadata::jsonb->>'machine_type' = '{filters['filter_machine_type']}'")
    if filters.get("filter_source_table"):
        where_clauses.append(f"metadata::jsonb->>'source_table' = '{filters['filter_source_table']}'")
    if filters.get("filter_date_from"):
        where_clauses.append(f"metadata::jsonb->>'event_date' >= '{filters['filter_date_from']}'")
    if filters.get("filter_date_to"):
        where_clauses.append(f"metadata::jsonb->>'event_date' <= '{filters['filter_date_to']}'")

    where_str = " AND ".join(where_clauses)

    sql = text(f"""
        SELECT 
            id,
            content,
            metadata,
            1 - (embedding <=> '{embedding_str}'::vector) as score
        FROM gold.ai_ready_events
        WHERE {where_str}
        ORDER BY embedding <=> '{embedding_str}'::vector
        LIMIT :top_k
    """)

    with engine.connect() as conn:
        results = conn.execute(sql, {"top_k": VECTOR_SEARCH_TOP_K})
        rows = results.fetchall()

    return [
        {
            "id": row[0],
            "content": row[1],
            "metadata": json.loads(row[2]),
            "score": float(row[3]),
            "search_type": "semantic"
        }
        for row in rows
    ]


def keyword_search(query: str, filters: dict) -> list[dict]:
    """Full text search PostgreSQL for keyword matches."""
    engine = get_engine()

    where_clauses = ["to_tsvector('english', content) @@ plainto_tsquery('english', :query)"]
    if filters.get("filter_machine_type"):
        where_clauses.append(f"metadata::jsonb->>'machine_type' = '{filters['filter_machine_type']}'")
    if filters.get("filter_source_table"):
        where_clauses.append(f"metadata::jsonb->>'source_table' = '{filters['filter_source_table']}'")
    if filters.get("filter_date_from"):
        where_clauses.append(f"metadata::jsonb->>'event_date' >= '{filters['filter_date_from']}'")
    if filters.get("filter_date_to"):
        where_clauses.append(f"metadata::jsonb->>'event_date' <= '{filters['filter_date_to']}'")

    where_str = " AND ".join(where_clauses)

    sql = text(f"""
        SELECT
            id,
            content,
            metadata,
            ts_rank(to_tsvector('english', content), 
                    plainto_tsquery('english', :query)) as score
        FROM gold.ai_ready_events
        WHERE {where_str}
        ORDER BY score DESC
        LIMIT :top_k
    """)

    with engine.connect() as conn:
        results = conn.execute(sql, {"query": query, "top_k": KEYWORD_SEARCH_TOP_K})
        rows = results.fetchall()

    return [
        {
            "id": row[0],
            "content": row[1],
            "metadata": json.loads(row[2]),
            "score": float(row[3]),
            "search_type": "keyword"
        }
        for row in rows
    ]


def hybrid_search(query: str, filters: dict) -> list[dict]:
    """Combine semantic and keyword search results."""

    semantic_results = semantic_search(query, filters)
    keyword_results = keyword_search(query, filters)

    # Merge results - deduplicate by id
    seen_ids = set()
    combined = []

    # Semantic results first (higher priority)
    for result in semantic_results:
        if result["id"] not in seen_ids:
            seen_ids.add(result["id"])
            combined.append(result)

    # Add keyword results not already in semantic
    for result in keyword_results:
        if result["id"] not in seen_ids:
            seen_ids.add(result["id"])
            combined.append(result)

    # Sort by score and take top k
    combined.sort(key=lambda x: x["score"], reverse=True)
    return combined[:FINAL_TOP_K]