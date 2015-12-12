---
layout: post
title: 'C# - The Google Weather API'
tags:
  - 'c#'
  - google api
  - weather
---

---
**UPDATE - Google no longer offers a weather API. The url's and code in this post will no longer function correctly**

As you may or may not know Google has announced over the last couple of months that they plan to bring an end to a load of their services, perhaps the biggest being iGoogle.

Unfortunately one of the services they have already brought an end to is their weather API that I made of use of in this post

The code in the post now no longer works as the request URL is met with this error message

`"404. That's an error"`

I hope to post another update soon with examples on how to use alternative API's.
 
---
<br>
<br>
**This API will no longer function correctly as the API from Google is no longer available. The code is kept here for reference**

You can obtain the current and forecast weather conditions in a user specified city with C# through the free weather API provided by Google. The main concept behind the API is to produce a URL, with a specified city, which then corresponds to an `XML` file that includes the weather forecast. Handily C# makes it easy to obtain this `XML` file, parse it, and finally print out the weather on a large variety of cities.

The URL we will be using, and modifying is -

`http://www.google.com/ig/api?weather=YOUR_CITY_NAME`

For example - 

<http://www.google.com/ig/api?weather=London>

will return an `XML` file with the weather for London.

Now in C#, we will start by creating a `Conditions` class that will simply contain a bunch of properties that represent the weather in the city at a point in time - 

{% highlight csharp %}  
class Conditions  
{  
    public string City { get; set; }  
    public string Condition { get; set; }  
    public string TempF { get; set; }  
    public string TempC { get; set; }  
    public string Humidity { get; set; }  
    public string Wind { get; set; }  
    public string Day { get; set; }  
    public string High { get; set; }  
    public string Low { get; set; }  
}  
{% endhighlight %}

Now we will move on to the main `Weather` class that will hold two methods - `GetCurrentConditions`, and `GetForecastConditions`. The `GetCurrentConditions` method will return one `Conditions` object - representing the current day, and the `GetForecastedConditions` method will return a `List` of conditions - one for each day of the forecast. Before we begin, make sure to put the following using statement at the top of the file so that we can use the various classes and methods inside the `System.Xml` namespace - 

{% highlight csharp %}  
using System.Xml;  
{% endhighlight %}

Now we can create the public static `GetCurrentConditions` method that takes one string parameter representing the city - 

{% highlight csharp %}  
public static Conditions GetCurrentConditions(string city)  
{  
    Conditions cond = new Conditions();  
    XmlDocument doc = new XmlDocument();  
    XmlTextReader reader = null;

    try  
    {  
        reader = new XmlTextReader(string.Format("http://www.google.com/ig/api?weather={0}", city));  
        doc.Load(reader);

        if (doc.SelectSingleNode("xml_api_reply/weather/problem_cause") != null)  
        {  
            cond = null;
        }  
        else  
        {  
            cond.City = doc.SelectSingleNode("/xml_api_reply/weather/forecast_information/city").Attributes["data"].InnerText;  
            cond.Condition = doc.SelectSingleNode("/xml_api_reply/weather/current_conditions/condition").Attributes["data"].InnerText;  
            cond.TempC = doc.SelectSingleNode("/xml_api_reply/weather/current_conditions/temp_c").Attributes["data"].InnerText;  
            cond.TempF = doc.SelectSingleNode("/xml_api_reply/weather/current_conditions/temp_f").Attributes["data"].InnerText;  
            cond.Humidity = doc.SelectSingleNode("/xml_api_reply/weather/current_conditions/humidity").Attributes["data"].InnerText;  
            cond.Wind = doc.SelectSingleNode("/xml_api_reply/weather/current_conditions/wind_condition").Attributes["data"].InnerText;  
        }  
    }  
    catch (Exception)  
    {  
        cond = null;
    }  
    finally  
    {  
        if (reader != null)  
            reader.Close();  
    }

    return cond;  
}  
{% endhighlight %}

The first thing we do is create the `Conditions` object, `XMLDocument` object (representing the returned XML file), and the `XMLTextReader` (which will be used to obtain the XML file and put it in our `XMLDocument` object).

Next, we construct the URL, adding the city string to the end of URL, and load the document into our `XMLDocument` object. We then do a check to see if the XML document was successfully downloaded (i.e the city is valid). If not we set the conditions object to null, which can be used as error checking in our implementation later on.

If the document is valid, we set each property of the `Conditions` object to the relevant portion of the XML document. The `SelectSingleNode` method moves to each element of the file and the `data` attribute and `.InnerText` property are used to parse the data from the document into our object. Again, if an exception is thrown, we set the `Conditions` object to null for error checking. Finally, we close the `XMLTextReader` and return the `Conditions` object.

The `GetForecastConditions` method is very similar. The only difference is the `foreach` loop that goes through each forecast in the `forecast_conditions` node, adds the conditions to a new `Conditions` object, and adds it to the `List` which is then returned at the end.

{% highlight csharp %}  
public static List<Conditions> GetForecastConditions(string city)  
{  
    Conditions cond = new Conditions();  
    XmlDocument doc = new XmlDocument();  
    XmlTextReader reader = null;  
    List<Conditions> conditions = new List<Conditions>();

    try  
    {  
        reader = new XmlTextReader(string.Format("http://www.google.com/ig/api?weather={0}", city));  
        doc.Load(reader);

        if (doc.SelectSingleNode("xml_api_reply/weather/problem_cause") != null)  
        {  
            conditions = null;  
        }  
        else  
        {  
            foreach (XmlNode node in doc.SelectNodes("/xml_api_reply/weather/forecast_conditions"))  
            {  
                cond = new Conditions();  
                cond.City = doc.SelectSingleNode("/xml_api_reply/weather/forecast_information/city").Attributes["data"].InnerText;  
                cond.Condition = node.SelectSingleNode("condition").Attributes["data"].InnerText;  
                cond.High = node.SelectSingleNode("high").Attributes["data"].InnerText;  
                cond.Low = node.SelectSingleNode("low").Attributes["data"].InnerText;  
                cond.Day = node.SelectSingleNode("day_of_week").Attributes["data"].InnerText;  
                conditions.Add(cond);  
            }  
        }  
    }  
    catch (Exception)  
    {  
        conditions = null;
    }  
    finally  
    {  
        if (reader != null)  
            reader.Close();  
    }

    return conditions;  
}  
{% endhighlight %}

<!--more-->

Finally, we can use the two new methods in a simple Console application (although it could easily be used in a GUI). In this example we prompt the user for whether or not they want the current or forecast conditions, prompt them for a city to search for, and print the corresponding conditions to the Console. A prompt if also shown if the `Conditions` object is null - meaning that an error occurred.

{% highlight csharp %}  
using System;  
using System.Collections.Generic;  
using System.Linq;  
using System.Text;

namespace Google_Weather  
{  
    public class Program  
    {  
        public static void Main(string[] args)  
        {  
            string city = "";  
            int option = 0;  
            Conditions conditions = null;  
            List<Conditions> foreacast = null;

            PrintMenu();

            while (option != 3)  
            {  
                if (GetInputChoice(out option))  
                {  
                    switch (option)  
                    {  
                        case 1: //Current  
                        {  
                            city = GetCity();  
                            conditions = Weather.GetCurrentConditions(city);  
                            if (conditions != null)  
                            {  
                                PrintCurrentForecast(conditions);  
                            }  
                            else  
                            {  
                                PrintErrorMessage();  
                            }  
                            break;  
                        }  
                        case 2: //Forecast  
                        {  
                            city = GetCity();  
                            foreacast = Weather.GetForecastConditions(city);  
                            if (foreacast != null && foreacast.Count > 1)  
                            {  
                                PrintForecastConditions(foreacast);  
                            }  
                            else  
                            {  
                                PrintErrorMessage();  
                            }  
                            break;  
                        }  
                        case 3:  
                        { 
                            break;
                        }  
                        default:  
                        {  
                            Console.WriteLine("Invalid Choice");  
                            Console.WriteLine();  
                            break;  
                        }  
                    }  
                }  
                else  
                {  
                    Console.WriteLine("Input must be numeric");  
                    Console.WriteLine();  
                }  
            }

        }

        private static void PrintMenu()  
        {  
            Console.WriteLine("1 - Current Conditions");  
            Console.WriteLine("2 - Forecast Conditions");  
            Console.WriteLine("3 - Exit");  
            Console.WriteLine();  
        }

        private static void PrintErrorMessage()  
        {  
            Console.WriteLine("There was an error processing the request.");  
            Console.WriteLine("Please, make sure you are using a valid city, or try again later.");  
            Console.WriteLine();  
        }

        private static bool GetInputChoice(out int op)  
        {  
            Console.WriteLine("Enter an option - ");  
            string input = Console.ReadLine();

            return int.TryParse(input, out op);
        }

        private static string GetCity()  
        {  
            Console.WriteLine();  
            Console.WriteLine("Enter a city - ");  
            return Console.ReadLine();  
        }

        private static void PrintCurrentForecast(Conditions conditions)  
        {  
            Console.WriteLine("CurrentConditions for: " + conditions.City);  
            Console.WriteLine("Conditions: " + conditions.Condition);  
            Console.WriteLine("Temperature (F): " + conditions.TempF);  
            Console.WriteLine("Temperature (C): " + conditions.TempC);  
            Console.WriteLine("Humidity: " + conditions.Humidity);  
            Console.WriteLine("Wind: " + conditions.Wind);  
            Console.WriteLine();  
        }

        private static void PrintForecastConditions(List<Conditions> conditions)  
        {  
            Console.WriteLine("Foreacast Conditions for: " + conditions[0].City);

            foreach (Conditions c in conditions)  
            {  
                Console.WriteLine("Day: " + c.Day);  
                Console.WriteLine("Conditions: " + c.Condition);  
                Console.WriteLine("Temperature (High): " + c.High);  
                Console.WriteLine("Temperature (Low): " + c.Low);  
                Console.WriteLine();  
            }  
        }  
    }  
}  
{% endhighlight %}

This concludes the tutorial on how to use the Google Weather API. If you have any questions, feel free to post a comment below.