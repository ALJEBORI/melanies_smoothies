# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col,when_matched
# Write directly to the app.

st.markdown(
    """
    <h1 style='text-align:center;'>
        <img src="https://emojiapi.dev/api/v1/1f964/64.png" width="45">Pending Smoothie Orders<img src="https://emojiapi.dev/api/v1/1f964/64.png" width="45">
    </h1>
    """,
    unsafe_allow_html=True
)

st.write("""Orders that need to be filled """)

# Add values from table orders
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col('ORDER_FILLED')==0).collect()
if my_dataframe:
    #st.dataframe(data=my_dataframe, use_container_width=True)
    # Make data frame editable
    editable_df = st.data_editor(my_dataframe)
    # Saving changes
    submitted=st.button('Submit')
    if submitted:
        #session.sql(my_insert_stmt).collect()
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        try:
            
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
            st.success("Order(s) Updated", icon='👍')
        except:
            st.write('Something want wrong.') 

else:
    st.success('There are no pending orders right now',icon='👍')
    
   
