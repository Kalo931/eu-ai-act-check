def assess(**k):
    risk = "Grün"; reasons=[]; tasks=[]
    if not k["is_ai"]:
        return {"risk":"Grün","reasons":["Kein KI-System i.S.d. EU AI Act"],"tasks":["Best Practices prüfen"]}

    if k["biometric_remote"] or k["auto_scoring"] or k["critical_infra"]:
        risk="Rot"; reasons.append("hochkritischer Anwendungsfall")
        tasks += ["Risikobewertung/DPIA durchführen","Rechtsprüfung einholen","Techn.-org. Maßnahmen nachschärfen"]

    if ("Gesundheit" in k["sensitive"]) or ("Kinder/Jugendliche" in k["sensitive"]) or ("Personenbezogen" in k["sensitive"] and not k["logging"]):
        if risk!="Rot": risk="Gelb"
        reasons.append("sensible/personenbezogene Daten ohne ausreichende Kontrollen")
        tasks += ["Protokollierung aktivieren","Datenminimierung/DPIA prüfen"]

    if not k["transparency"]:
        if risk!="Rot": risk="Gelb"
        reasons.append("fehlender Transparenzhinweis")
        tasks.append("Nutzer klar informieren: 'Dieses Feature nutzt KI.'")

    if not k["human_oversight"]:
        if risk!="Rot": risk="Gelb"
        reasons.append("fehlende menschliche Aufsicht")
        tasks.append("Verantwortliche Rolle/Prozess definieren")

    if k["use_case"] in ["Bildung","HR/Bewerbung"] and not k["genai_label"]:
        if risk!="Rot": risk="Gelb"
        reasons.append("GenAI-Inhalte ohne Kennzeichnung")
        tasks.append("Kennzeichnung/Labeling einführen")

    if not tasks:
        tasks = ["Transparenzhinweis aktuell halten","Protokolle regelmäßig prüfen","Verantwortlichkeiten dokumentieren"]

    tasks = list(dict.fromkeys(tasks))
    return {"risk":risk,"reasons":reasons,"tasks":tasks}
