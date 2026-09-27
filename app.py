import streamlit as st
import requests

st.set_page_config(page_title="DBAASP AMP Search", page_icon="🧬")

st.title("AMP Sequence Search")
st.caption("Antimicrobial peptide sequences from DBAASP, by target organism. Live from dbaasp.org.")


@st.cache_data(show_spinner=False)
def find_amps(organism):
    seqs, offset = [], 0
    while True:
        r = requests.get("https://dbaasp.org/peptides",
                         params={"targetSpecies.value": organism,
                                 "limit": 200, "offset": offset},
                         headers={"Accept": "application/json"}, timeout=30)
        r.raise_for_status()
        data = r.json()
        batch = data.get("data") or []
        if not batch:
            break
        for p in batch:
            if p.get("sequence"):
                seqs.append(p["sequence"])
            for m in p.get("monomers") or []:
                if isinstance(m, dict) and m.get("sequence"):
                    seqs.append(m["sequence"])
        offset += 200
        if offset >= data.get("totalCount", 0):
            break
    return sorted(set(seqs))


organism = st.text_input("Target organism", placeholder="Escherichia coli")

st.caption("Try: Staphylococcus aureus · Candida albicans · Pasteurella multocida · "
           "Pseudomonas aeruginosa PAO1")

if organism.strip():
    try:
        with st.spinner(f"Searching DBAASP for {organism}..."):
            results = find_amps(organism.strip())
    except requests.RequestException as e:
        st.error(f"Couldn't reach DBAASP: {e}")
    else:
        if not results:
            st.warning("No sequences found. Check the spelling, or try a broader name "
                       "(species without the strain).")
        elif len(results) > 5000:
            st.error("That returned the entire database — the filter didn't match. "
                     "Check the organism name.")
        else:
            st.success(f"{len(results):,} unique sequences")

            fasta = "\n".join(f">DBAASP_{i+1}\n{s}" for i, s in enumerate(results))
            c1, c2 = st.columns(2)
            c1.download_button("Download .txt", "\n".join(results),
                               f"{organism.replace(' ', '_')}_amps.txt")
            c2.download_button("Download FASTA", fasta,
                               f"{organism.replace(' ', '_')}_amps.fasta")

            st.dataframe({"Sequence": results, "Length": [len(s) for s in results]},
                         use_container_width=True, height=500)
