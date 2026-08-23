def register_enterprise(app):

    from backend.app.ahos_30_5.clinical_evidence_post_market_surveillance import router as ahos305
    from backend.app.ahos_30_6.cybersecurity_zero_trust_platform import router as ahos306
    from backend.app.ahos_30_7.global_commercial_launch_partner_ecosystem import router as ahos307
    from backend.app.ahos_31_0.autonomous_global_healthcare_enterprise_platform import router as ahos310

    app.include_router(ahos305)
    app.include_router(ahos306)
    app.include_router(ahos307)
    app.include_router(ahos310)
