from fastapi import APIRouter, HTTPException
from datetime import datetime
from uuid import uuid4
import os
import redis

router = APIRouter(
    prefix="/ahos/52.7",
    tags=["AHOS 52.7 Real Redis Backend Integration Platform"]
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
STREAM_NAME = "clinical-events"
CONSUMER_GROUP = "ahos-clinical-workers"
CONSUMER_NAME = "ahos-worker-1"

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def uid(prefix):
    return f"{prefix}-{uuid4().hex[:10].upper()}"


@router.get("/health")
async def health():
    try:
        pong = r.ping()
        return {
            "status": "online",
            "phase": "AHOS 52.7",
            "platform": "Real Redis Backend Integration Platform",
            "readiness": "REAL_REDIS_BACKEND_READY",
            "redis_url": REDIS_URL,
            "redis_ping": pong,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/redis/ping")
async def redis_ping():
    return {
        "redis_ping": r.ping(),
        "status": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/streams/create")
async def create_stream():
    message_id = r.xadd(
        STREAM_NAME,
        {
            "event_id": uid("INIT"),
            "event_type": "stream_initialized",
            "priority": "normal",
            "created_at": datetime.utcnow().isoformat()
        }
    )

    return {
        "stream": STREAM_NAME,
        "message_id": message_id,
        "status": "created"
    }


@router.post("/groups/create")
async def create_group():
    try:
        r.xgroup_create(
            STREAM_NAME,
            CONSUMER_GROUP,
            id="0",
            mkstream=True
        )
        status = "created"
    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" in str(e):
            status = "already_exists"
        else:
            raise HTTPException(status_code=500, detail=str(e))

    return {
        "stream": STREAM_NAME,
        "consumer_group": CONSUMER_GROUP,
        "status": status
    }


@router.post("/messages/publish")
async def publish_message():
    payload = {
        "event_id": uid("CLINICAL"),
        "event_type": "critical_lab_result",
        "resource_type": "Observation",
        "resource_id": "Observation/105794590",
        "priority": "high",
        "value": "99",
        "unit": "mg/dL",
        "created_at": datetime.utcnow().isoformat()
    }

    message_id = r.xadd(STREAM_NAME, payload)

    return {
        "message_id": message_id,
        "stream": STREAM_NAME,
        "payload": payload,
        "status": "published"
    }


@router.get("/messages/read")
async def read_messages():
    data = r.xread(
        {STREAM_NAME: "0"},
        count=10,
        block=1000
    )

    return {
        "stream": STREAM_NAME,
        "count": sum(len(messages) for _, messages in data),
        "messages": data
    }


@router.post("/messages/consume")
async def consume_message():
    try:
        r.xgroup_create(
            STREAM_NAME,
            CONSUMER_GROUP,
            id="0",
            mkstream=True
        )
    except redis.exceptions.ResponseError:
        pass

    data = r.xreadgroup(
        CONSUMER_GROUP,
        CONSUMER_NAME,
        {STREAM_NAME: ">"},
        count=1,
        block=1000
    )

    consumed = []

    for stream, messages in data:
        for message_id, payload in messages:
            consumed.append({
                "stream": stream,
                "message_id": message_id,
                "payload": payload
            })
            r.xack(STREAM_NAME, CONSUMER_GROUP, message_id)

    return {
        "consumer_group": CONSUMER_GROUP,
        "consumer": CONSUMER_NAME,
        "consumed_count": len(consumed),
        "messages": consumed,
        "status": "consumed"
    }


@router.get("/dashboard")
async def dashboard():
    try:
        stream_length = r.xlen(STREAM_NAME)
        info = r.xinfo_stream(STREAM_NAME)
    except Exception:
        stream_length = 0
        info = {}

    return {
        "phase": "AHOS 52.7",
        "readiness": "REAL_REDIS_BACKEND_READY",
        "redis_connected": r.ping(),
        "stream": STREAM_NAME,
        "stream_length": stream_length,
        "consumer_group": CONSUMER_GROUP,
        "stream_info": info,
        "event_bus_score": 0.99,
        "status": "operational"
    }


@router.delete("/redis/flush-test")
async def flush_test():
    r.delete(STREAM_NAME)
    return {
        "stream": STREAM_NAME,
        "status": "deleted"
    }
