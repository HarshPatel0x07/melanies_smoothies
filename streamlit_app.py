# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Custumize Your Smoothie :cup_with_straw:")
nameonord = st.text_input("Name on Smoothie")
st.write("The Name on your Smoothie will be", nameonord)
st.write(
    """Chose Fruits you want in your Smoothie
    """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

INGREDIENTS_LIST = st.multiselect(
    "Chose upto 5 Fruit:"
    ,my_dataframe
    ,max_selections =5)

if INGREDIENTS_LIST:
    INGREDIENTS_STRING = ''

    for chosen in INGREDIENTS_LIST:
        INGREDIENTS_STRING += chosen + ' '

    #st.write(INGREDIENTS_STRING)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients,name_on_order) values ('""" + INGREDIENTS_STRING + """','""" + nameonord + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
