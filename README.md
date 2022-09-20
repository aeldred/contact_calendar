# Customer Engagement Calendar
A simple Python/Flask application to display the best contact method to engage a customer based on 
the weather in a 5-day forecast.

## The Problem

Welcome! You are a brand new developer starting out at Acme Software Incorporated! You have just 
completed your first week, including some excellent onboarding to learn about the history of the
company, the current technology, and the future roadmap for the platform.

You have a basic understanding of Acme's business, which is to work with smaller, independent 
restaurants to engage with their customers and potential customers to come in for specials, happy
hours, and events. Acme does this through various channels including:
* automated phone calls
* texts
* email
* others
Acme prides itself on the ability to determine both the best message to use to engage food lovers
and when to most effectively engage them.

Now you are ready to get down to business! In talking with your Scrum team and your technical lead, 
you have determined that the first task you are going to take on is to implement a new feature
that determines when to best contact individuals based on the weather. Acme's product team has
determined the following:
* the best time to engage a customer via a text message is when it is sunny and warmer than 75
degrees Fahrenheit
* the best time to engage a customer via email is when it is between 55 and 75 degrees Fahrenheit
* the best time to engage a customer via a phone call is when it is less than 55 degrees or when
it is raining

You will need to build a function that uses the API provided by openweathermap.org. Your function
should determine what outreach method is best for Minneapolis, MN over the next 5 days. The 
forecast will give you data for mulitple points during a given day, you may choose to use that data 
how you wish. 

The function can be run as either a web application or a command line application. If it is a web
application it should display a 5 day calendar with the best outreach method listed for that
date. If it is a command line application it should print out each date and the best outreach method
for that day on a new line.

## Running the application
Note: this Flask app uses a .flaskenv file to set the FLASK_APP environment variable

1. Install the required modules in requirements.txt
`pip install -r requirements.txt`
2. Run the Flask application
`python -m flask run`
3. Once the server starts, it will output a message like `Running on http://127.0.0.1:5000`. Copy
the url provided into a web browser and append '/contact_calendar' to the end of the url
`http://127.0.0.1:5000/contact_calendar/`
4. The city will default to Minneapolis. You can change the city for the forecast by appending 
the `/city/state` to the url
`http://127.0.0.1:5000/contact_calendar/savage/mn`
5. Note: If no state is given, the API will return a forecase for some city with that name
