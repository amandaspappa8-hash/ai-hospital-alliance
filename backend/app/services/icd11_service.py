import json
import logging
import os
import time
import uuid
from pathlib import Path
from typing import Optional

import httpx
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..models import ICD11Code, ICD11Mapping

logger = logging.getLogger(__name__)

WHO_AUTH_URL = "https://icdaccessmanagement.who.int/connect/token"
WHO_CLIENT_ID = os.getenv("WHO_ICD11_CLIENT_ID", "")
WHO_CLIENT_SECRET = os.getenv("WHO_ICD11_CLIENT_SECRET", "")
BUNDLED_ICD11_PATH = Path(__file__).parent.parent.parent / "data" / "icd11_simplified.json"


class ICD11Service:
    def __init__(self, db: Session):
        self.db = db
        self._token: Optional[str] = None
        self._token_expiry: float = 0
        self._online: Optional[bool] = None

    def search(self, query: str, lang: str = "en", limit: int = 10, chapter_filter: Optional[str] = None) -> list[dict]:
        local_results = self._search_local(query, lang, limit, chapter_filter)
        if local_results:
            return local_results
        if self._is_online():
            try:
                return self._search_who_api(query, limit)
            except Exception as e:
                logger.warning(f"WHO API failed: {e}")
        return []

    def _search_local(self, query: str, lang: str, limit: int, chapter_filter: Optional[str]) -> list[dict]:
        try:
            like_query = f"%{query}%"
            q = self.db.query(ICD11Code).filter(
                (ICD11Code.title.ilike(like_query)) |
                (ICD11Code.title_ar.ilike(like_query)) |
                (ICD11Code.code.ilike(like_query))
            ).filter(ICD11Code.is_leaf == True)
            if chapter_filter:
                q = q.filter(ICD11Code.chapter == chapter_filter)
            codes = q.limit(limit).all()
            return [self._code_to_dict(c, lang) for c in codes]
        except Exception as e:
            logger.error(f"Local search error: {e}")
            return []

    def _search_who_api(self, query: str, limit: int = 10) -> list[dict]:
        token = self._get_who_token()
        headers = {"Accept": "application/json", "API-Version": "v2", "Accept-Language": "en"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(
                "https://id.who.int/icd/entity/search",
                params={"q": query, "flatResults": True, "highlightingEnabled": False, "medicalCodingMode": True},
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
        results = []
        for item in data.get("destinationEntities", [])[:limit]:
            results.append({
                "code": item.get("theCode", ""),
                "title": item.get("title", ""),
                "title_en": item.get("title", ""),
                "title_ar": None,
                "chapter": item.get("chapter", ""),
                "definition": None,
                "is_leaf": True,
                "source": "who_api",
            })
        return results

    def get_by_code(self, code: str, lang: str = "en") -> Optional[dict]:
        code = code.upper().strip()
        local = self.db.query(ICD11Code).filter(ICD11Code.code == code).first()
        if local:
            return self._code_to_dict(local, lang)
        if self._is_online():
            try:
                results = self._search_who_api(code, limit=1)
                if results:
                    return results[0]
            except Exception:
                pass
        return None

    def map_from_icd10(self, icd10_code: str) -> list[dict]:
        mappings = self.db.query(ICD11Mapping).filter(ICD11Mapping.icd10_code == icd10_code.upper()).all()
        results = []
        for m in mappings:
            code = self.get_by_code(m.icd11_code)
            if code:
                code["mapping_type"] = m.mapping_type
                results.append(code)
        return results

    def is_seeded(self) -> bool:
        return self.db.query(ICD11Code).count() > 0

    def seed_from_bundled_json(self) -> int:
        if not BUNDLED_ICD11_PATH.exists():
            logger.error(f"Bundled file not found: {BUNDLED_ICD11_PATH}")
            return 0
        with open(BUNDLED_ICD11_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        count = 0
        batch = []
        for entry in data:
            existing = self.db.query(ICD11Code).filter(ICD11Code.code == entry["code"]).first()
            if existing:
                continue
            code = ICD11Code(
                id=uuid.uuid4(),
                code=entry["code"],
                title=entry["title"],
                title_ar=entry.get("title_ar"),
                definition=entry.get("definition"),
                parent_code=entry.get("parent_code"),
                chapter=entry.get("chapter"),
                block=entry.get("block"),
                is_leaf=entry.get("is_leaf", True),
            )
            batch.append(code)
            count += 1
            if len(batch) >= 500:
                self.db.bulk_save_objects(batch)
                self.db.commit()
                batch = []
        if batch:
            self.db.bulk_save_objects(batch)
            self.db.commit()
        logger.info(f"✅ Seeded {count} ICD-11 codes")
        return count

    def _get_who_token(self) -> str:
        if not WHO_CLIENT_ID:
            return ""
        if self._token and time.time() < self._token_expiry - 60:
            return self._token
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(
                WHO_AUTH_URL,
                data={"client_id": WHO_CLIENT_ID, "client_secret": WHO_CLIENT_SECRET, "scope": "icdapi_access", "grant_type": "client_credentials"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            resp.raise_for_status()
            token_data = resp.json()
        self._token = token_data["access_token"]
        self._token_expiry = time.time() + token_data.get("expires_in", 3600)
        return self._token

    def _is_online(self) -> bool:
        if self._online is not None:
            return self._online
        try:
            with httpx.Client(timeout=3.0) as client:
                resp = client.get("https://id.who.int/icd", follow_redirects=True)
                self._online = resp.status_code < 500
        except Exception:
            self._online = False
        return self._online

    def _code_to_dict(self, code: ICD11Code, lang: str = "en") -> dict:
        title = code.title_ar if (lang == "ar" and code.title_ar) else code.title
        return {
            "code": code.code,
            "title": title,
            "title_en": code.title,
            "title_ar": code.title_ar,
            "chapter": code.chapter,
            "block": code.block,
            "definition": code.definition,
            "is_leaf": code.is_leaf,
            "source": "local_cache",
        }


from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..tenant_isolation import get_db, get_tenant_context, TenantContext

icd11_router = APIRouter(prefix="/icd11", tags=["ICD-11"])


@icd11_router.get("/search")
def search_icd11(
    q: str = Query(..., min_length=2),
    lang: str = Query("en"),
    limit: int = Query(10, le=50),
    chapter: Optional[str] = Query(None),
    ctx: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    if not ctx.tenant.icd11_enabled:
        raise HTTPException(status_code=403, detail="ICD-11 not enabled for this tenant")
    service = ICD11Service(db)
    results = service.search(q, lang=lang, limit=limit, chapter_filter=chapter)
    return {"query": q, "results": results, "count": len(results)}


@icd11_router.get("/code/{code}")
def get_icd11_code(
    code: str,
    lang: str = Query("en"),
    ctx: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = ICD11Service(db)
    result = service.get_by_code(code, lang=lang)
    if not result:
        raise HTTPException(status_code=404, detail=f"ICD-11 code '{code}' not found")
    return result


@icd11_router.get("/map/icd10/{icd10_code}")
def map_icd10_to_icd11(
    icd10_code: str,
    ctx: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = ICD11Service(db)
    results = service.map_from_icd10(icd10_code)
    return {"icd10_code": icd10_code.upper(), "icd11_equivalents": results, "count": len(results)}


@icd11_router.get("/status")
def icd11_status(
    ctx: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    service = ICD11Service(db)
    count = db.query(ICD11Code).count()
    online = service._is_online()
    return {
        "local_cache_count": count,
        "local_cache_ready": count > 0,
        "who_api_reachable": online,
        "mode": "online" if online else "offline",
        "icd11_enabled": ctx.tenant.icd11_enabled,
    }
