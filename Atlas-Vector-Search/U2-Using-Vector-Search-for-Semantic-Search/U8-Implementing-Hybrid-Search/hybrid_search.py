from pymongo import MongoClient
import os
import embeddings
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
dbName = "sample_mflix"
collectionName = "embedded_movies"
collection = client[dbName][collectionName]

### CONFIGURATION PARAMETERS

vector_priority = 1
text_priority = 1
limit = 10
overrequest_factor = 10
num_candidates = limit * overrequest_factor
query = "A movie that is about people who are trying to escape from a maximum security facility."
embedding = embeddings.get_embeddings(query)

vector_search = {
    "$vectorSearch": {
        "index":          "vectorPlotIndex",
        "path":           "plot_embedding",
        "queryVector":    embedding,
        "numCandidates":  num_candidates,
        "limit":          limit
    }
}

make_array = {
    "$group": { "_id": None, "docs": {"$push": "$$ROOT"} }
}

add_rank = {
    "$unwind": { "path": "$docs", "includeArrayIndex": "rank" }
}

def make_compute_score_doc(priority, score_field_name):
    return {
        "$addFields": {
            score_field_name: {
                "$divide": [
                    1.0,
                    { "$add": ["$rank", priority, 1] }
                ]
            }
        }
    }

def make_projection_doc(score_field_name):
    return  {
        "$project": {
            score_field_name:  1,
            "_id":             "$docs._id",
            "title":           "$docs.title",
            "plot":            "$docs.plot",
            "year":            "$docs.year",
        }
    }


text_search = {
    "$search": {
        "index":  "plotIndex",
        "text":   { "query": query, "path": "plot" },
    }
}

limit_results = {
    "$limit" : limit
}

combine_search_results = {
    "$group": {
        "_id":        "$_id",
        "vs_score":   {"$max":    "$vs_score"},
        "ts_score":   {"$max":    "$ts_score"},
        "title":      {"$first":  "$title"},
        "plot":       {"$first":  "$plot"},
        "year":       {"$first":  "$year"}
    }
}

project_combined_results = {
    "$project": {
        "_id":        1,
        "title":      1,
        "plot":       1,
        "year":       1,
        "score": {
            "$let": {
                "vars": {
                    "vs_score":  { "$ifNull":  ["$vs_score", 0] },
                    "ts_score":  { "$ifNull":  ["$ts_score", 0] }
                },
                "in": { "$add": ["$$vs_score", "$$ts_score"] }
            }
        }
    }
}

sort_results = {
    "$sort": { "score": -1}
}

pipeline = [
    vector_search,
    make_array,
    add_rank,
    make_compute_score_doc(vector_priority, "vs_score"),
    make_projection_doc("vs_score"),
    {
        "$unionWith": { "coll": "movies",
            "pipeline": [
                text_search,
                limit_results,
                make_array,
                add_rank,
                make_compute_score_doc(text_priority, "ts_score"),
                make_projection_doc("ts_score")
            ]
        }
    },
    combine_search_results,
    project_combined_results,
    sort_results,
    limit_results
]

x = collection.aggregate(pipeline)
for doc in x:
    print(doc)
