import joblib
import folium
import numpy as np
import pandas as pd
import streamlit as st
import streamlit_folium as st_folium


st.set_page_config(
    page_title='How Much Energy Do You Need?',
    page_icon='⚡',
    layout='centered',
)


# Machine Learning Section

st.title('Find Suitable Dimensions For Your Energy Supply System!')
Energy = st.number_input('The amount of energy you need per day in [kWh]:', 0)
WindSpeed = st.number_input('Average wind speed in your location in [m/s]:', 0)
st.write("*If you don't know the Average Wind Speed of your desired location, you can get help from the map below.")

kgH = Energy/33.33
df_pred = pd.DataFrame([[kgH,WindSpeed]])
model = joblib.load('MLmodel.pkl')
prediction = model.predict(df_pred)

kgH2 = np.round(kgH, 1)
SurElc = np.round(prediction, 2)
SurTur = np.round(prediction*100, 1)


if st.button('Find your system dimensions!'):
    col1, col2, col3 = st.columns(3)
    col1.metric('Produced Hydrogen Weight [kg/day]:', kgH2)
    col2.metric('Electrolyzer Active Surface [m^2]:', SurElc)
    col3.metric('Wind Turbune Surface [m^2]:', SurTur)
    col1.write('The weight of hydrogen that must be produced per day to store the amount of energy you want.')
    col2.write('The dimensions of the active surface that should be considered for the electrolyzer, to be able to produce this amount of hydrogen per day.')
    col3.write('The dimensions of the surface swept by the wind turbine, which must be taken into account, in order to provide the necessary energy for the electrolyzer.')

    
# Map Visualization Section

st.header('Global Atlas of Average Wind Speed')
m = folium.Map(location=None, width='100%', height='100%',tiles='OpenStreetMap')
folium.raster_layers.ImageOverlay(
    image= 'WindSpeed.png',
    name='Global Average Wind Speed Atlas',
    bounds=[[-90, -180], [90, 180]],
    pixelated=True,
    opacity=0.6,
    interactive=True,
    cross_origin=False,
    zindex=1,
    overlay=True, 
    control=True, 
    show=True,
).add_to(m)
st_data1 = st_folium.st_folium(m, width='100%')
st.write('The average wind speed data presented in the map above was obtained from the NASA website. You can easily access the data from [this link](https://disc.gsfc.nasa.gov/datasets/FLDAS_NOAH01_C_GL_M_001/summary).')


# Description Section

st.header('Behind The Scenes Of This Project!')
st.markdown("Humans need energy in various forms such as electricity, heating, cooling, cooking, and car fuel. However, energy production faces many challenges, particularly environmental ones like global warming and pollution of air, soil, and water. These challenges lead us to use clean energy sources. The energy sector includes production, transmission, storage, and consumption, making these systems complex. Renewable energies, although useful, are unstable and this instability adds complexity to the systems. This is why the shift towards renewable energy is slow.")
st.markdown("I believe that one solution to these challenges is to simplify energy systems and use selection algorithms. By simplifying the algorithms, even people without specialized knowledge can understand their energy supply system with basic information. Once they know the system's dimensions, they can estimate the costs and switch to using clean energy sources with a clear vision.")
st.markdown("This web application uses a step-by-step algorithm to determine the appropriate dimensions for an energy supply system. By inputting the daily energy requirement and annual average wind speed, the algorithm calculates the necessary dimensions for key components such as the wind turbine for electricity generation and the electrolyzer for hydrogen energy storage. Hydrogen is a versatile energy carrier that can be used as electricity, gas, and even car fuel.")
st.markdown("I am currently working on expanding this program to include other forms of clean energy so that users can have a wider range of options to choose from. This will allow them to select the most suitable system for their energy needs based on their current circumstances. I hope that my efforts can make a small contribution toward improving both society and the environment.")
st.markdown("If you want to know exactly how this algorithm works, you can read my published article titled [Hydrogen mini-Factory for domestic purposes (wind version)](https://www.nature.com/articles/s41598-023-40205-6). With the help of this article, you can get more details to design your energy supply system.")
