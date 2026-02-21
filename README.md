This is my submission for the DFR Onboarding project. 
![An image showing two graphs. The top graph plots Fuel Open Time against TPS. The bottom graph shows acceleration over time (calculated from roughly taking the derivative of Driven Average Wheel Speed) over time).](newplot(4).png)

The image above was generated using plotly. The data was stored and accessed using pandas.

Before doing making any graphs, I cleaned up the dataframe in two ways. I first searched for columns
which had only one unique value and then deleted those columns, as they would not be useful for
data analysis. Second, I ommitted all rows with incomplete data to ensure that they would not effect
the final plots.

The first plot correlates Fuel Open Time and TPS. I performed a regression to calculate a polynomial
to the third degree to express the relation between Fuel Open Time and TPS. The equation and resulting trendline appear to be ordinary for a car. It specifically reflects normal engine behavior.

The second plot takes the derivative of Driven Average Wheel Speed over time to approximate acceleration. For the purposes of this project, I converted Driven Average Wheel Speed so it could
be interpreted as meters per second. I smoothed the curve for acceleration for better readability. There are three major spikes in acceleration. My research suggests that this is a visualization of a gear shift.