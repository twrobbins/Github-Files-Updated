# File: Final_Project.py
# Name: Timothy Robbins
# Date: 8/10/19
# Course: DSC510 - Introduction to Programming
# Desc:  The program prompts the user for their city or zip code and requests weather forecast data from
# OpenWeatherMap. The program displays the weather information in a READABLE format to the user.
# The Python Application asks the user for their zip code or city.
# The zip code or city name is used to obtain weather forecast data from OpenWeatherMap.
# The weather forecast is displayed in a readable format to the user.
# Functions are used including a main function.
# The user can run the program multiple times to allow them to look up weather conditions for multiple locations.
# The user input is validated. If valid data isn’t presented the user is notified.
# The Requests library is used to request data from the webservice.
# Try blocks are used to ensure that the request was successful. If the connection was not successful a message is
# displayed to the user.
# Python 3 is used.
# Try blocks are used to to establish connections to the webservice.  A message is printed for uhe user indicating
# whether or not the connection was successful.

def retrieveWeatherByCity(): # use city name to obtain weather forecast data from OpenWeatherMap.
    import requests  # import requests library to connect to api
    key = '&APPID=6c755077b1a5bc3ed49e2879eb5bd4c5'  # api key used to connect to api
    api = 'http://api.openweathermap.org/data/2.5/weather?q='  # url for api
    while True:  # repeat loop until user enters valid input
        city = input('Please enter the US city name: ')
        if city.isalpha():  # if the city name is alphabetic
            lookup = api + city + ',US&units=imperial' + key  # combine elements to create lookup
            print('Retrieving: ', lookup)
            try:  # use try block in case error generated when connecting to api
                r = requests.get(lookup)  # attempt to connect to api
            except:  # if error when connecting to ap[
                print('Connection was not successful.')
                continue  # repeat loop until connection successful
            else:
                print('Connection was successful.')  # if api connection successful
                import json  # import json library
                js = r.json()  # create variable to read in json data
                try:  # use try in case city name is not valid
                    print('Current Weather Conditions for', js['name'])
                except:  # except clause in case city is invalid
                    print('US city not found.')
                    continue  # repeat loop until user input is valid
                else:  # if city name found
                    return r  # return results of to the main function
                    break  # exit loop
        else:  # if customer enters numeric characters
            print('Please enter alphabetic characters only.')
            continue  # return to beginning of loop until user input is valid

def retrieveWeatherByZip():  # use zip code to obtain weather forecast data from OpenWeatherMap.
    import requests  # import requests library to connect to api
    key = '&APPID=6c755077b1a5bc3ed49e2879eb5bd4c5'  # api key used to connect to api
    api = 'http://api.openweathermap.org/data/2.5/weather?q='  # url for api
    while True:  # repeat loop until valid user input
        zip = input('Please enter the US zip code: ')
        if zip.isnumeric():  # if user inputs numeric value (i.e. potential zip code)
            lookup = api + zip + ',US&units=imperial' + key  # combine elements to create lookup
            print('Retrieving: ', lookup)
            try:  # use try in case error when connecting
                r = requests.get(lookup)
            except:  # inform user if connectin was not successful
                print('Connection was not successful.')
                continue  # return to beginning of loop
            else:
                print('Connection was successful.')  # if try request successful
                import json  # import json library
                js = r.json()  # create variable to read in json data
                try:  # use try in case zip code is not found
                    print('Current Weather Conditions for', js['name'])
                except:  # print message if zip code not found
                    print('US zip code not found.')
                    continue  # return to beginning of loop
                else:  # if zip code is found
                    return r  # return results to main function
                    break  # exit loop
        else:  # if user enters alphabetic characters (i.e. not valid for zip code)
            print('Please enter numeric characters only.')
            continue  # return to beginning of loop

def parseWeather(r):  # print the results to the user in readable format
    import json  # import json library
    js = r.json()  # create variable for json data
    print('Current Temp: {:.2f} degrees'.format(js['main']['temp']))  # format float to two decimal places
    print('High Temp: {:.2f} degrees'.format(js['main']['temp_max']))  # format float to two decimal places
    print('Low Temp: {:.2f} degrees'.format(js['main']['temp_min']))  # format float to two decimal places
    print('Pressure: {}hPa'.format(js['main']['pressure']))  # format the pressure line to show 'hPA' without spaces
    print('Humidity: {}%'.format(js['main']['humidity']))  # format the humidity line to show percentage without spaces
    print('Cloud Cover: {}'.format(js['weather'][0]['description']).title())  # capitalize first letter of each word

def main():
    while True:  # outer loop used to encompass the initial choice as well as the input for another choice
        while True:  # loop to validate user input
            choice = input('Would you like to lookup weather data by US city or zip code?  Enter 1 for city; 2 for zip: ')
            try:  # use try in case an error comes up
                if int(choice) == 1:
                    r = retrieveWeatherByCity()  # call retrieveWeatherByCity function
                    break  # exit loop after calling function
                elif int(choice) == 2:
                    r = retrieveWeatherByZip()  # call retrieveWeatherByZip function
                    break  # exit loop after calling function
                else:  # print error message if user does not select 1 or 2
                    print('Invalid selection!  Please enter "1" or "2"')
                    continue  # return to beginning of loop
            except:  # use except clause in case user input causes error
                print('Invalid selection! Please enter a numeric value.')
                continue  # return to beginning of loop
        parseWeather(r)  # call parseWeather function
        while True:  # loop to validate user input for another lookup
            another = input('Would you like to perform another weather lookup? (Y/N) ')
            try:  # try used in case user input causes error
                if another.lower() == 'y' or another.lower() == 'n':
                    break  # if user input is valid exit the inner loop
                else:  # print error message if invalid input
                    print('Invalid selection!  Please enter "Y" or "N"')
                    continue  # return to beginning of loop
            except:  # use except clause in case user input causes error
                print('Invalid selection! Please enter an alphabetic character.')
                continue  # return to beginning of loop
        if another.lower() == 'y':  # if user input is y
            continue  # repeat outer loop
        elif another.lower() == 'n':  # if user input is n, exit loop
            break  # exit outer loop

if __name__ == '__main__':
    main()  # call the main function




