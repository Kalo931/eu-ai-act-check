def assess(**k):
    risk = "Grün"; reasons=[]; tasks=[]
    if not k.get("is_ai"):
        return {"risk":"Grün","reasons":["Kein KI-System i.S.d. EU AI Act"],"tasks":["Best Practices prüfen"]}

    if k.get("biometric_remote") or k.get("auto_scoring") or k.get("critical_infra"):
        risk="Rot"; reasons.append("hochkritischer Anwendungsfall")
        tasks += ["Risikobewertung/DPIA durchführen","Rechtsprüfung einholen","Techn.-org. Maßnahmen nachschärfen"]

    sensitive = set(k.get("sensitive", []))
    if (
        ("Gesundheit" in sensitive)
        or ("Kinder/Jugendliche" in sensitive)
        or ("Personenbezogen" in sensitive and not k.get("logging"))
    ):
        if risk!="Rot": risk="Gelb"
        reasons.append("sensible/personenbezogene Daten ohne ausreichende Kontrollen")
        tasks += ["Protokollierung aktivieren","Datenminimierung/DPIA prüfen"]

    if not k.get("transparency"):
        if risk!="Rot": risk="Gelb"
        reasons.append("fehlender Transparenzhinweis")
        tasks.append("Nutzer klar informieren: 'Dieses Feature nutzt KI.'")

    if not k.get("human_oversight"):
        if risk!="Rot": risk="Gelb"
        reasons.append("fehlende menschliche Aufsicht")
        tasks.append("Verantwortliche Rolle/Prozess definieren")

    if k.get("use_case") in ["Bildung","HR/Bewerbung"] and not k.get("genai_label"):
        if risk!="Rot": risk="Gelb"
        reasons.append("GenAI-Inhalte ohne Kennzeichnung")
        tasks.append("Kennzeichnung/Labeling einführen")

    if not tasks:
        tasks = ["Transparenzhinweis aktuell halten","Protokolle regelmäßig prüfen","Verantwortlichkeiten dokumentieren"]

    tasks = list(dict.fromkeys(tasks))
    return {"risk":risk,"reasons":reasons,"tasks":tasks}
