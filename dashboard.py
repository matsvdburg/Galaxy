# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import numpy as np

# Inlezen van opgeschoonde bestanden en maak er een DataFrame van
df = pd.read_excel('final_data.xlsx')

# Sorteer de kolommen op basis van 'discoveryPeriod'
df = df.sort_values(by=['discoveryPeriod'])

# Maak filter optie
st.sidebar.header ("please filter here:")

# Eerste filter is op basis van 'discoveryPeriod'
discoveryPeriod = st.sidebar.multiselect(
    "Select discovery period:",
    options=df["discoveryPeriod"].unique(),
    default=df["discoveryPeriod"].unique()
    )

# Tweede filter is op basis van 'bodyType'
bodyType = st.sidebar.multiselect(
    "Select body:",
    options=df["bodyType"].unique(),
    default=df["bodyType"].unique()
    )

# Plaats de waarden in een nieuwe selectie (df_selection)
df_selection = df.query(
    "discoveryPeriod == @discoveryPeriod & bodyType == @bodyType"
    )

# Titel en ondertitel van dashboard
st.title(":milky_way: SOLAR SYSTEM DASHBOARD")
st.markdown("A journey through the discovery of extraterrestrial bodies in our solar system. Authored by Mats van der Burg as part of the module 'Data Playground' for the minor Big Data for Smart Media & Business at Utrecht University of Applied Sciences. ")

st.markdown ("""___""")

st.markdown("Discovering space is something that arouses interest among many people, but the problem is that providing clear insight into this space data actually happens little. This dashboard is built with the ideal that you learn more about space exploration in a clear way. With that being said, step into this: :rocket: rocket and let's go on an adventure through our solar system together! ")

st.markdown ("""___""")

# Optie om ruwe data in te zien
if st.checkbox ('Raw data'):
    st.subheader('Raw data')
    st.dataframe(df_selection) 

st.markdown ("""___""")

# Afbeelding van heelal
image = Image.open('space.png')
st.image(image)

# Tel het aantal 'englishName' van de df_selection
total_bodies = df_selection['englishName'].count()

# Stel twee centrale kolommen op
middle_column, right_column = st.columns(2)

with middle_column:
    st.subheader(":telescope: Earliest discovery year :")
    try:     # Try & Except opgesteld om te voorkomen dat er bij een leeg filter een foutmelding optreed.
        early_disc = int(df_selection["discoveryYear"].min())
        st.subheader(f"{early_disc:,} ")
    except ValueError:
        st.subheader(np.nan)

with right_column:
    st.subheader(":earth_africa: Total amount of bodies:")
    st.subheader(f"{total_bodies:,} ")
    
st.markdown ("""___""")

st.title("Discoveries") 

st.markdown("410 years ago, Galileo Galilei discovered the moons of the planet Jupiter with a telescope that he developed himself (Uri, 2020). Observing space has continued through the ages and has led to new insights about humanity, the origin of our existence and has also contributed to a changing perspective on life. The graph below clearly shows that there has been a significant increase in discoveries of extraterrestrial objects over time.")

# Opstellen variabele met groupby selection
amount_disc_group = (
    df_selection.groupby(by=["discoveryPeriod"]).count()[["Amount of discoveries"]].sort_values(by="Amount of discoveries")
    )

# Opstellen barchart van englishName en de hoevelheid discoveries
amount_disc = px.bar(
    amount_disc_group,
    y="Amount of discoveries",
    title="<b>Amount of discoveries through time<b>"
    )

# Plot chart in Streamlit
st.plotly_chart(amount_disc)

middle_column, right_column = st.columns(2)

with middle_column:
    st.subheader(":date: Year most discoveries :")
    try:
        disc_year = int(df_selection['discoveryYear'].value_counts().idxmax())
        st.subheader(disc_year)
    except ValueError:
        st.subheader(np.nan)

with right_column:
    st.subheader(":male-scientist: Person most discoveries:")
    try:
        disc_by = df_selection['discoveredBy'].value_counts().idxmax()
        st.subheader(disc_by)
    except ValueError:
        st.subheader(np.nan)

st.markdown ("""___""")

# Subsectie met nieuwe titel
st.title("Distance to the sun")

# Tekst met uitleg over aphelion and perihelion
st.markdown('Aphelion and perihelion are used to quantify the distance between the sun and a particular object. The orbits of objects around the sun are never completely round and symmetrical. The distance from the sun can therefore differ at different periods. Aphelion is described here as the point of the orbit where the body is furthest from the sun. The perihelion is the opposite, describing the point where the body is closest to the sun (Britannica, n.d.).')

# Plaatsen van een afbeelding
image = Image.open('aphelion.png')
st.image(image)

# Set de index van de kolommen naar die van 'englishName' om te zorgen voor correcte x-as in grafieken
df_selection = df_selection.set_index('englishName')

# Koppel variabele 'perihelion' aan de tien grootste van de kolom
perihelion = df_selection['perihelion'].nlargest(10)

# Opstellen van barchart
perihelion_chart = px.bar(
    perihelion,
    y="perihelion",
    x=perihelion.index,
    title="<b>Top 10 bodies with highest perihelion (in km)<b>"
    )

# Tonen van barchart
st.plotly_chart(perihelion_chart)

# Koppel variabele 'aphelion'aan de tien grootste van de kolom
aphelion = df_selection['aphelion'].nlargest(10)

# Opstellen van barchart
aphelion_chart = px.bar(
    aphelion,
    y="aphelion",
    x=aphelion.index,
    title="<b>Top 10 bodies with highest aphelion (in km)<b>"
    )

# Tonen van barchart
st.plotly_chart(aphelion_chart)

st.markdown ("""___""")

# Quote
st.markdown("“Space is for everybody. It’s not just for a few people in science or math, or for a select group of astronauts. That’s our new frontier out there, and it’s everybody’s business to know about space.”")
st.markdown("     - Christa McAuliffe, teacher and astronaut (1948 - 1986)")

st.markdown ("""___""")

# Titel van nieuwe sectie
st.title("Relative amount of bodies")
st.markdown("The solar system consists of a great diversity of different bodies. These are things like planets, asteroids, moons, comets, dwarf planets and stars. But to what extent are these bodies distributed in the solar system in relation to each other? That question is covered in the pie chart below!")

# Opstellen van nieuwe pie chart
fig = px.pie(df_selection, values='Amount of discoveries', names='bodyType')

# Tonen van chart in dashboard
st.plotly_chart(fig)

st.markdown ("""___""")

# Titel van nieuwe sectie
st.title("Gravitational forces")

st.markdown("In essence, gravity is the force that makes objects pull together. The moon has much less gravity than the earth. Jupiter in contrast has the highest gravity of any planet in the solar system, on Jupiter you would weigh about 2.5 times as much as on Earth! (Eternach, n.d.)")
# Koppel de variabele 'highest_gravity' aan de maximale waarde van de 'gravity' kolom
highest_gravity = df_selection['gravity'].max()

# Opstellen van de kolommen
middle_column, right_column = st.columns(2)

with middle_column:
    st.subheader(":earth_africa: Gravity of Earth :")
    st.subheader("9,81 m/s²")
with right_column:
    st.subheader(":milky_way: Highest gravity:")
    st.subheader(f"{highest_gravity:,} m/s²")

st.markdown ("""___""")

# Titel van nieuwe sectie
st.title("Relative size and temperature")

# Koppel de 8 grootste lichamen aan 'meanCircum'
meanCircum = df_selection['Circumference'].nlargest(8)

# Stel barchart op
meanCircum_chart = px.bar(
    meanCircum,
    y="Circumference",
    x=meanCircum.index,
    title="<b>Largest extraterrestrial objects (circumference in km)<b>"
    )

# Toon barchart
st.plotly_chart(meanCircum_chart)

# koppel maximale avgTemp aan max_avgtemp
max_avgtemp = (df_selection["avgTemp"].max())

# Stel kolommen op
middle_column, right_column = st.columns(2)

with middle_column:
    st.subheader(":straight_ruler: Highest circumference :")
    try: # Constructie om te voorkomen dat programma error geeft bij geen value
        early_disc = int(df_selection["Circumference"].max())
        st.subheader(f"{early_disc:,} km")
    except ValueError:
        st.subheader(np.nan)
with right_column:
    st.subheader(":thermometer: Max average temperature:")
    st.subheader(f"{max_avgtemp:,} K")

st.markdown ("""___""")

st.title(":balloon: Congratulations")

st.markdown("You made it to the end of this interactive dashboard! Hopefully you have seen and learned many new things about our solar system. We've looked at gravitational forces, the discoveries over the years, temperatures, distances and basically everything to do with space. Hopefully this new knowledge has given you a broader perspective on discoveries and the beauty of space itself!")
st.markdown ("""___""")

# Titel laatste sectie
st.title(":book: Sources")

st.markdown("Uri, J. (2020, January 9). 410 Years Ago: Galileo Discovers Jupiter’s Moons. NASA. Retrieved 26 March 2022, from https://www.nasa.gov/feature/410-years-ago-galileo-discovers-jupiter-s-moons/")
st.markdown("Britannica. (n.d.). aphelion | Definition & Facts. Encyclopedia Britannica. Retrieved 28 March 2022, from https://www.britannica.com/science/aphelion")
st.markdown("Echternach, E. (n.d.). Natuurkunde.nl - Zwaartekracht. Stichting natuurkunde.nl. Retrieved 30 March 2022, from https://www.natuurkunde.nl/artikelen/684/zwaartekracht")