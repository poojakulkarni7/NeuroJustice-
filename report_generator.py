def build_report(user_input,category, pros, cons, risks, sections):

    report = f"""
================ NEUROJUSTICE REPORT ================

SITUATION:
{user_input}

------------------------------------------------------
PROS:
{chr(10).join("• " + p for p in pros)}

------------------------------------------------------
CONS:
{chr(10).join("• " + c for c in cons)}

------------------------------------------------------
LEGAL RISKS (FROM PDF):
{chr(10).join("• " + r for r in risks)}

------------------------------------------------------
SECTIONS (FROM IPC / BCI PDF):
{chr(10).join("• " + s for s in sections)}

======================================================
END
======================================================
"""
    return report