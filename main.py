import streamlit as st
from recipelist import recipes

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
