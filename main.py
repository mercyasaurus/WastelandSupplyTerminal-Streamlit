import streamlit as st
from recipelist import recipes

st.set_page_config(
    page_title="Wasteland Supply Terminal",
    page_icon="🟢",
    layout="centered",
)

#ST DESIGN ASPECT#

st.markdown("""
<style>
/* Main page background */
.stApp {
    background-color: #0b0f0b;
    color: #7CFF7C;
}

/* General text */
html, body, [class*="css"]  {
    color: #7CFF7C;
    font-family: monospace;
}

/* Headers */
h1, h2, h3 {
    color: #99ff99 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Text input boxes */
.stTextInput input {
    background-color: #111711;
    color: #7CFF7C;
    border: 1px solid #2f5f2f;
    border-radius: 0px;
}

/* Number input */
.stNumberInput input {
    background-color: #111711;
    color: #7CFF7C;
    border: 1px solid #2f5f2f;
    border-radius: 0px;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #111711 !important;
    color: #7CFF7C !important;
    border: 1px solid #2f5f2f !important;
    border-radius: 0px !important;
}

/* Buttons */
.stButton > button {
    background-color: #111711;
    color: #7CFF7C;
    border: 1px solid #2f5f2f;
    border-radius: 0px;
    font-family: monospace;
}

.stButton > button:hover {
    background-color: #1a241a;
    border-color: #7CFF7C;
    color: #b7ffb7;
}

/* Alerts */
.stAlert {
    background-color: #111711;
    color: #7CFF7C;
    border: 1px solid #2f5f2f;
}

/* Divider */
hr {
    border-color: #2f5f2f;
}
</style>
""", unsafe_allow_html=True)

#END OF DESIGN





validCats = ["food", "chems", "drinks", "alcohol", "big bloom", "misc", "more food", "more drinks"]

# ---- HEADER ----
st.title("ROB-TEC INDUSTRIES")
st.subheader("Wasteland Supply Terminal")
st.write("Fallout 76 Crafting Helper")

st.divider()

mode = st.radio(
    "Choose Mode:",
    ["Crafting Calculator", "Recipe Directory"]
)

# ---- RECIPE DIRECTORY ----
if mode == "Recipe Directory":

    st.subheader("Recipe Directory")

    category = st.selectbox(
        "Select a category",
        ["all"] + validCats
    )

    st.divider()

    if category == "all":
        for recipe in recipes:
            st.write(recipe.title())
    else:
        for recipe in recipes:
            if recipes[recipe]["category"] == category:
                st.write(recipe.title())

# ---- CALCULATOR ----
else:

    st.subheader("Crafting Calculator")

    recipe_input = st.text_input(
        "Enter recipes (comma separated)",
        placeholder="e.g. gigablossom, brain bombs"
    )

    if recipe_input:

        separateRecipes = [r.strip() for r in recipe_input.lower().split(",") if r.strip() != ""]
        uniqueRecipes = []

        for r in separateRecipes:
            if r not in uniqueRecipes:
                uniqueRecipes.append(r)

        invalidRecipes = [r for r in uniqueRecipes if r not in recipes]
        validRecipes = [r for r in uniqueRecipes if r in recipes]

        # ---- INVALID ----
        if invalidRecipes:
            st.warning("Invalid recipes will be skipped:")
            for r in invalidRecipes:
                st.write(r.title())

        # ---- VALID ----
        if validRecipes:
            st.success("Valid recipes selected:")
            for r in validRecipes:
                st.write(r.title())

        quantities = {}

        for recipe in validRecipes:
            quantities[recipe] = st.number_input(
                f"How many {recipe.title()}?",
                min_value=0,
                step=1,
                key=recipe
            )

        if st.button("Calculate Grocery List"):

            shoppingList = {}

            for recipe in validRecipes:
                quantityRecipes = quantities[recipe]

                recipeData = recipes.get(recipe)
                ingredients = recipeData.get("ingredients")

                for ingredient, amount in ingredients.items():
                    totalNeeded = amount * quantityRecipes

                    if ingredient in shoppingList:
                        shoppingList[ingredient] += totalNeeded
                    else:
                        shoppingList[ingredient] = totalNeeded

            st.divider()
            st.subheader("Final Grocery List")

            for ingredient, amount in shoppingList.items():
                st.write(f"{ingredient}: {amount}")
