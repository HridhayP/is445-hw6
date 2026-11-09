import streamlit as st
import pandas as pd
import altair as alt

alt.data_transformers.disable_max_rows()

st.set_page_config(page_title="IS 445 HW6", layout="wide")

URL = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/building_inventory.csv"

@st.cache_data
def load():
    df = pd.read_csv(URL)
    df = df[(df["Year Constructed"] > 0) & (df["Square Footage"] > 0)]
    return df

df = load()

st.title("Illinois State Building Inventory")
st.text("Hridhay Prabahar | IS 445 HW6")

# ---------- Viz 1: interactive (dropdown filter + brush-linked bars) ----------
st.header("1. Square footage over time by agency")

agencies = df["Agency Name"].value_counts().head(10).index.tolist()
top = df[df["Agency Name"].isin(agencies)]

agency_dd = alt.selection_point(
    fields=["Agency Name"],
    bind=alt.binding_select(options=[None] + agencies, labels=["All"] + agencies, name="Agency: "),
)
brush = alt.selection_interval(encodings=["x"])

scatter = (
    alt.Chart(top)
    .mark_circle(opacity=0.6)
    .encode(
        x=alt.X("Year Constructed:Q", scale=alt.Scale(zero=False)),
        y=alt.Y("Square Footage:Q", scale=alt.Scale(type="log")),
        color=alt.condition(brush, "Agency Name:N", alt.value("lightgray"), legend=None),
        tooltip=["Location Name", "Agency Name", "Year Constructed", "Square Footage"],
    )
    .add_params(agency_dd, brush)
    .transform_filter(agency_dd)
    .properties(width=650, height=350)
)

bars = (
    alt.Chart(top)
    .mark_bar()
    .encode(
        y=alt.Y("Agency Name:N", sort="-x"),
        x=alt.X("sum(Square Footage):Q", title="Total Square Footage"),
        color="Agency Name:N",
    )
    .transform_filter(agency_dd)
    .transform_filter(brush)
    .properties(width=650, height=250)
)

st.altair_chart(scatter & bars, use_container_width=False)

st.write("""
WRITE-UP 1: [what this viz highlights; why log scale for sq ft; why color = agency;
how the dropdown + brush interaction works; what you'd change with more time]
""")

# ---------- Viz 2: buildings constructed per decade by status ----------
st.header("2. Buildings constructed per decade")

df2 = df.assign(Decade=(df["Year Constructed"] // 10) * 10)

decade_chart = (
    alt.Chart(df2)
    .mark_bar()
    .encode(
        x=alt.X("Decade:O"),
        y=alt.Y("count():Q", title="Number of Buildings"),
        color=alt.Color("Bldg Status:N"),
        tooltip=["Decade", "Bldg Status", "count()"],
    )
    .properties(width=800, height=350)
)

st.altair_chart(decade_chart, use_container_width=False)

st.write("""
WRITE-UP 2: [what this viz highlights; why binned by decade (ordinal x); why stacked
by status; what you'd change with more time]
""")
