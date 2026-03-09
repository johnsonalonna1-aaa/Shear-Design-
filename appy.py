import math
import streamlit as st

# -----------------------------------------------------------
# Reinforced Concrete Beam Shear Design App
# Simple ACI-style shear reinforcement calculator
#
# Units:
# f'c    = psi
# lambda = unitless
# b_w    = in
# d      = in
# V_u    = kips
# f_yt   = psi
# A_v    = in^2
# phi    = unitless
#
# Equations used:
# 1. Vc = 2 * lambda * sqrt(f'c) * b_w * d   [lb]
# 2. Vs = Vu / phi - Vc                       [lb]
# 3. s  = (A_v * f_yt * d) / Vs               [in]
# -----------------------------------------------------------

st.set_page_config(page_title="Beam Shear Design App", layout="centered")

st.title("Reinforced Concrete Beam Shear Design")
st.subheader("ACI-Style Shear Reinforcement Calculator")

st.write("""
This app calculates:

1. Concrete shear strength, Vc  
2. Required shear resisted by stirrups, Vs  
3. Required stirrup spacing, s
""")

st.markdown("---")

st.header("Input Values")

fc = st.number_input("Concrete compressive strength, f'c (psi)", min_value=1.0, value=4000.0, step=500.0)
lam = st.number_input("Lambda, λ (unitless)", min_value=0.1, max_value=1.0, value=1.0, step=0.05)
bw = st.number_input("Beam web width, b_w (in)", min_value=0.1, value=12.0, step=0.5)
d = st.number_input("Effective depth, d (in)", min_value=0.1, value=20.0, step=0.5)
Vu_kips = st.number_input("Factored shear force, V_u (kips)", min_value=0.0, value=60.0, step=1.0)
fyt = st.number_input("Stirrup yield strength, f_yt (psi)", min_value=1.0, value=60000.0, step=1000.0)
Av = st.number_input("Area of stirrup legs, A_v (in^2)", min_value=0.0001, value=0.20, step=0.01, format="%.4f")
phi = st.number_input("Strength reduction factor, phi", min_value=0.01, max_value=1.0, value=0.75, step=0.01)

st.markdown("---")

if st.button("Calculate Shear Design"):

    # Convert Vu from kips to lb
    Vu_lb = Vu_kips * 1000.0

    # Step 1: Concrete shear strength
    Vc_lb = 2.0 * lam * math.sqrt(fc) * bw * d
    Vc_kips = Vc_lb / 1000.0

    # Step 2: Required stirrup shear
    Vs_lb = (Vu_lb / phi) - Vc_lb
    Vs_kips = Vs_lb / 1000.0

    st.header("Step-by-Step Results")

    st.write("### Step 1: Concrete Shear Strength, Vc")
    st.latex(r"V_c = 2\lambda\sqrt{f'_c}\,b_w d")
    st.write(
        f"Vc = 2 × {lam:.2f} × √({fc:.2f}) × ({bw:.2f}) × ({d:.2f}) = "
        f"{Vc_lb:,.2f} lb = {Vc_kips:,.2f} kips"
    )

    st.write("### Step 2: Required Shear Carried by Stirrups, Vs")
    st.latex(r"V_s = \frac{V_u}{\phi} - V_c")
    st.write(
        f"Vs = ({Vu_lb:,.2f} / {phi:.2f}) - {Vc_lb:,.2f} = "
        f"{Vs_lb:,.2f} lb = {Vs_kips:,.2f} kips"
    )

    if Vs_lb <= 0:
        st.success("Concrete alone provides enough shear strength for this simplified check.")
        st.write("Since Vs ≤ 0, no additional stirrup shear is required by this equation.")
        st.info("For full ACI design, still check minimum shear reinforcement and maximum stirrup spacing.")
    else:
        # Step 3: Stirrup spacing
        s_in = (Av * fyt * d) / Vs_lb

        st.write("### Step 3: Required Stirrup Spacing, s")
        st.latex(r"s = \frac{A_v f_{yt} d}{V_s}")
        st.write(
            f"s = [({Av:.4f}) × ({fyt:,.2f}) × ({d:.2f})] / ({Vs_lb:,.2f})"
        )
        st.write(f"Required stirrup spacing = {s_in:.2f} in")

        st.markdown("---")
        st.subheader("Final Answers")
        st.write(f"Concrete shear strength, Vc = {Vc_kips:,.2f} kips")
        st.write(f"Required stirrup shear, Vs = {Vs_kips:,.2f} kips")
        st.write(f"Required stirrup spacing, s = {s_in:.2f} in")

        st.warning(
            "This is a simplified shear design calculation. "
            "For full ACI design, also check maximum spacing limits, minimum shear reinforcement, "
            "and any other applicable code requirements."
        )

st.markdown("---")
st.caption("Based on the uploaded beam shear analysis and design procedure. :contentReference[oaicite:1]{index=1}")
