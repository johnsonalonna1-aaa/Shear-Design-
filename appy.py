import math
import streamlit as st

# -----------------------------------------------------------
# Reinforced Concrete Beam Shear Design App
# Simple ACI-style shear reinforcement calculator
# Units:
#   f'c   = psi
#   b_w   = in
#   d     = in
#   V_u   = kips
#   f_yt  = psi
#   A_v   = in^2
#   phi   = unitless
#
# Equations used:
# 1. Vc = 2*sqrt(f'c)*b_w*d      [lb]
# 2. Vs = Vu/phi - Vc            [lb]
# 3. s  = (A_v*f_yt*d)/Vs        [in]
# -----------------------------------------------------------

st.set_page_config(page_title="Beam Shear Design App", layout="centered")

st.title("Reinforced Concrete Beam Shear Design")
st.subheader("Simple Streamlit App for Shear Reinforcement")

st.write(
  """
This app calculates:

1. **Concrete shear strength** \(V_c\)  
2. **Required shear resisted by stirrups** \(V_s\)  
3. **Required stirrup spacing** \(s\)

using basic ACI-style shear design equations.
"""
)

st.markdown("---")

# -----------------------------
# User Inputs
# -----------------------------
st.header("Input Values")

fc = st.number_input("Concrete compressive strength, f'c (psi)", min_value=1.0, value=4000.0, step=500.0)
bw = st.number_input("Beam web width, b_w (in)", min_value=0.1, value=12.0, step=0.5)
d = st.number_input("Effective depth, d (in)", min_value=0.1, value=20.0, step=0.5)
Vu_kips = st.number_input("Factored shear force, V_u (kips)", min_value=0.0, value=60.0, step=1.0)
fyt = st.number_input("Stirrup yield strength, f_yt (psi)", min_value=1.0, value=60000.0, step=1000.0)
Av = st.number_input("Area of stirrup legs, A_v (in²)", min_value=0.0001, value=0.20, step=0.01, format="%.4f")
phi = st.number_input("Strength reduction factor, phi", min_value=0.01, max_value=1.0, value=0.75, step=0.01)

st.markdown("---")

# -----------------------------
# Calculation Button
# -----------------------------
if st.button("Calculate Shear Design"):
  
  # Convert Vu from kips to lb
  Vu_lb = Vu_kips * 1000.0

# Step 1: Concrete shear strength
Vc_lb = 2.0 * math.sqrt(fc) * bw * d
Vc_kips = Vc_lb / 1000.0

# Step 2: Required shear resisted by stirrups
Vs_required_lb = (Vu_lb / phi) - Vc_lb
Vs_required_kips = Vs_required_lb / 1000.0

st.header("Step-by-Step Results")

st.write("### Step 1: Concrete Shear Strength, Vc")
st.latex(r"V_c = 2\sqrt{f'_c}\,b_w d")
st.write(
  f"Vc = 2 × √({fc:.2f}) × ({bw:.2f}) × ({d:.2f}) = **{Vc_lb:,.2f} lb** = **{Vc_kips:,.2f} kips**"
)

st.write("### Step 2: Required Stirrup Shear, Vs")
st.latex(r"V_s = \frac{V_u}{\phi} - V_c")
st.write(
  f"Vs = ({Vu_lb:,.2f} / {phi:.2f}) - {Vc_lb:,.2f} = **{Vs_required_lb:,.2f} lb** = **{Vs_required_kips:,.2f} kips**"
)

# Handle case where concrete alone is enough
if Vs_required_lb <= 0:
  st.success("Concrete alone provides enough shear strength for this simplified check.")
st.write(
  "Since **Vs ≤ 0**, no additional stirrup shear is required by this basic equation."
)
st.info(
  "In real beam design, you would still check minimum shear reinforcement and maximum stirrup spacing requirements from ACI."
)

else:
  # Step 3: Stirrup spacing
  s_in = (Av * fyt * d) / Vs_required_lb

st.write("### Step 3: Required Stirrup Spacing, s")
st.latex(r"s = \frac{A_v f_{yt} d}{V_s}")
st.write(
  f"s = [({Av:.4f}) × ({fyt:,.2f}) × ({d:.2f})] / ({Vs_required_lb:,.2f})"
)
st.write(f"Required stirrup spacing = **{s_in:.2f} in**")

st.markdown("---")
st.subheader("Final Answers")
st.write(f"**Concrete shear strength, Vc = {Vc_kips:,.2f} kips**")
st.write(f"**Required stirrup shear, Vs = {Vs_required_kips:,.2f} kips**")
st.write(f"**Required stirrup spacing, s = {s_in:.2f} in**")

st.warning(
  "This app gives the required spacing from the basic shear equation only. "
  "For a full ACI design, also check maximum spacing limits, minimum shear reinforcement, "
  "and any section-specific code limits."
)

st.markdown("---")
st.caption("Based on basic ACI-style beam shear design equations from class shear design material. :contentReference[oaicite:1]{index=1}")