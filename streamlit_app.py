# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app.

st.markdown(
    """
    <h1 style='text-align:center;'>
        <img src="https://emojiapi.dev/api/v1/1f964/64.png" width="45">Customize Your Smoothie!<img src="https://emojiapi.dev/api/v1/1f964/64.png" width="45">
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("""Choose the fruits you want in your custome Smoothie! """)

name_on_order=st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be: ',name_on_order)
# Add values from table fruit_options
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
   my_dataframe,max_selections=5
)
if ingredients_list:
    ingredients_string=''#str(ingredient_list)
    for fruit_choosen in ingredients_list:
        ingredients_string+=fruit_choosen+' ' 
    #st.write("String ", ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    #st.write(my_insert_stmt) 
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is Ordered', icon="✅")
