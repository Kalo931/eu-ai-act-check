if st.button("Prüfen"):
    result = assess(
        is_ai=(is_ai == "Ja"),
        use_case=use_case,
        sensitive=sensitive,
        biometric_remote=biometric_remote,
        auto_scoring=auto_scoring,
        critical_infra=critical_infra,
        transparency=transparency,
        human_oversight=human_oversight,
        logging=logging,
        genai_label=genai_label
    )

    # ---------- Ampelsystem ----------
    risk = result["risk"]

    if risk.lower().startswith("niedrig"):
        st.markdown("## 🟢 Niedriges Risiko")
        st.info("Das System ist weitgehend unkritisch. Behalten Sie jedoch gesetzliche Änderungen im Blick.")
    elif risk.lower().startswith("mittel"):
        st.markdown("## 🟡 Mittleres Risiko")
        st.warning("Es bestehen einige Anforderungen. Bitte prüfen Sie die Pflichten nach EU AI Act genauer.")
    else:
        st.markdown("## 🔴 Hohes Risiko")
        st.error("Das System fällt in eine hohe Risikoklasse. Unbedingt rechtliche Beratung und Maßnahmen erforderlich!")

    # ---------- Details ----------
    st.write("**Begründung:**", "; ".join(result["reasons"]) or "Kontrollen wirken ausreichend.")
    st.write("**Nächste Schritte:**")
    for t in result["tasks"]:
        st.write("•", t)

    # ---------- PDF-Export ----------
    pdf = create_report(result)
    st.download_button(
        "📄 Ergebnis als PDF herunterladen",
        data=pdf,
        file_name="EU_AI_Act_QuickCheck.pdf",
        mime="application/pdf"
    )

    # ---------- Legende ----------
    st.divider()
    st.markdown("""
    ### Ampel-Legende
    - 🟢 **Grün**: Niedriges Risiko – keine oder wenige Vorgaben  
    - 🟡 **Gelb**: Mittleres Risiko – Anforderungen prüfen und ggf. nachrüsten  
    - 🔴 **Rot**: Hohes Risiko – strenge Vorgaben, rechtliche Beratung nötig  
    """)

