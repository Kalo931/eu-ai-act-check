def assess(**k):
    """
    Einfache Ampellogik für eine Erstorientierung zum EU AI Act.
    Rückgabeformat:
      {
        "risk": "Grün" | "Gelb" | "Rot",
        "reasons": [Liste mit Begründungen],
        "tasks": [Liste mit To-dos]
      }
    """
    risk = "Grün"
    reasons = []
    tasks = []

    # Kein KI-System -> Grün mit Basis-Aufgaben
    if not k.get("is_ai"):
        return {
            "risk": "Grün",
            "reasons": ["Kein KI-System i.S.d. EU AI Act"],
            "tasks": [
                "Best Practices prüfen",
                "Transparenzhinweis erwägen, falls unklarer KI-Bezug"
            ],
        }

    # Hochkritische Trigger (rot)
    if k.get("biometric_remote") or k.get("auto_scoring") or k.get("critical_infra"):
        risk = "Rot"
        reasons.append("Hochkritischer Anwendungsfall (Biometrie/Scoring/Kritische Infrastruktur)")
        tasks += [
            "Formelle Risikobewertung/DPIA durchführen",
            "Rechtsprüfung einholen",
            "Technische & organisatorische Maßnahmen nachschärfen",
            "Rollout ggf. gestuft mit Gate-Reviews planen"
        ]

    # Sensible/personenbezogene Daten ohne ausreichende Kontrollen -> mind. Gelb
    sensitive = set(k.get("sensitive", []))
    if (
        ("Gesundheit" in sensitive)
        or ("Kinder/Jugendliche" in sensitive)
        or ("Personenbezogen" in sensitive and not k.get("logging"))
    ):
        if risk != "Rot":
            risk = "Gelb"
        reasons.append("Sensible/personenbezogene Daten – Kontrollen prüfen/erweitern")
        tasks += [
            "Protokollierung aktivieren/prüfen (Events, Aufbewahrung)",
            "Datenminimierung & Rechtsgrundlage dokumentieren",
            "DPIA/DSFA prüfen (insb. bei Kindern/gesundheitlichen Daten)"
        ]

    # Transparenz
    if not k.get("transparency"):
        if risk != "Rot":
            risk = "Gelb"
        reasons.append("Fehlender Transparenzhinweis für Nutzer")
        tasks.append("Klarer Hinweis: 'Dieses Feature nutzt KI' (Ort & Wortlaut festlegen)")

    # Menschliche Aufsicht
    if not k.get("human_oversight"):
        if risk != "Rot":
            risk = "Gelb"
        reasons.append("Menschliche Aufsicht nicht geregelt")
        tasks.append("Verantwortliche Rolle & Eskalationspfad definieren")

    # Kennzeichnung generativer Inhalte (insb. Bildung/HR)
    if k.get("use_case") in ["Bildung", "HR/Bewerbung"] and not k.get("genai_label"):
        if risk != "Rot":
            risk = "Gelb"
        reasons.append("Generative KI-Inhalte ohne Kennzeichnung")
        tasks.append("Kennzeichnung/Labeling für KI-generierte Inhalte einführen")

    # Default-Aufgaben, falls nichts gesetzt wurde
    if not tasks:
        tasks = [
            "Transparenzhinweis aktuell halten",
            "Protokolle regelmäßig prüfen",
            "Verantwortlichkeiten dokumentieren"
        ]

    # Doppelte To-dos entfernen (Reihenfolge behalten)
    tasks = list(dict.fromkeys(tasks))

    return {"risk": risk, "reasons": reasons, "tasks": tasks}
