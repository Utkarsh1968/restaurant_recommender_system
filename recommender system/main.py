import streamlit as st
import pandas as pd
import pickle

new_df = pickle.load(open('new_df.pkl','rb'))
new_df = pd.DataFrame(new_df)

similarity_matrix = pickle.load(open('similarity_matrix.pkl','rb'))

lis = []
for i in new_df['Cuisines']:
    for j in i:
        lis.append(j)

uniq = list(set(lis))   
light = pd.DataFrame(uniq,columns=['cuisine'])

def get_recommendations(city, cuisines, top_n=5):
    # Filter restaurants based on the provided city and cuisine
    filtered_restaurants = new_df[(new_df['City'] == city) & (new_df['Cuisines'].apply(lambda x: any(cuisine in x for cuisine in cuisines)))]

    if filtered_restaurants.empty:
        return pd.DataFrame(columns=['Restaurant Name'])

    
    filtered_indices = filtered_restaurants.index
    filtered_similarity = similarity_matrix[filtered_indices]

  
    similarity_scores = filtered_similarity.mean(axis=0)
    top_indices = similarity_scores.argsort()[-min(top_n, len(filtered_indices)):][::-1]

    return new_df.iloc[top_indices]['Restaurant Name']

st.title('Restaurant recommender System')

selected_city = st.selectbox('Select City',new_df['City'].unique())

selected_cuisine = st.multiselect('select Cuisines',light['cuisine'] )

if st.button('Get Recommendations'):
        if not selected_cuisine:
            st.warning("Please select at least one cuisine.")
        else:
            recommendations = get_recommendations(selected_city,selected_cuisine)
            if recommendations.empty:
                st.write("No recommendations found.")
            else:
                st.write("Recommended Restaurants:")
                for restaurant in recommendations:
                    st.write(restaurant)

