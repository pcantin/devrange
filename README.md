# devrange

As part of a personal research project, I need to create a simulated group of web developers, each one with a random unique skill set constrained by the actual probability of having those skills. To calculate this probability, one of the pieces of information needed was the ‘shape’ of the developers or how many types of technologies they knew. As I was looking for usable data I figured I could simply extract this information from the Stackoverflow annual survey. By the way, thanks to Stackoverflow for this [open data](https://insights.stackoverflow.com/survey).

In the 2021 survey, I only used the answers from the 58,153 participants who identified as “I am a developer by profession”. Using the survey questionnaire, I created a classification for front-end developers and 6 classifications for back-end developers; Javascript, Java, C#, Python, PHP, and Ruby. With this, the shape of the web developer could be described by any combination between the front-end skill and the 6 back-end skills

This program reads in data from the Stackoverflow 2021 survey and can:
* Generate a JSON file with the developers Web "Shape" 
* Generate graphs with the shape data
* Convert the shape data from total-number-of-developers to percentages

*Note: to change program behavior, see the main() function*

To run this code, you must:
1. Download the [Stackoverflow Data Zip](https://info.stackoverflowsolutions.com/rs/719-EMH-566/images/stack-overflow-developer-survey-2021.zip) from the 2021 Stackoverflow survey
2. Extract the **survey_results_public.csv** file and place it the the root of this program's directory
3. run SORange.py

