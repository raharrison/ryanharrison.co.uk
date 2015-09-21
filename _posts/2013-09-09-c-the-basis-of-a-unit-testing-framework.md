---
layout: post
title: 'C# – The basis of a unit testing framework'
tags:
  - attributes
  - 'c#'
  - reflection
  - testing
---
Cut out all the sugar from pretty much any unit testing framework and you have yourself the situation where the users have marked their test classes to signify that they contain test methods and have marked the test methods themselves to tell the framework to actually run them.

So really on the base level (cutting out assertions and such) you need to somehow figure out which methods in which classes should be run by your tester. In managed languages this becomes a lot simpler through the use of reflection. We can simply ‘reflect’ on each of the classes/methods and decide if they should be run or not.

Here is some short C# code that demonstrates this idea through attributes and reflection. Classes which contain test methods are marked with the `TestClass` attribute and the test methods themselves which will be run later on are marked with the `TestMethod` attribute. The code uses `LINQ` to first get all the types in the currently executing assembly which include the `TestClass` attribute. Then all the methods are found in each of those classes which are marked with the `TestMethod` attribute. Finally each of those test methods are invoked using a new instance of the test class itself. The code is all commented so it should all be self-explanatory.

This simple idea can then be added onto in a load of different ways. For example some methods are expected to throw certain exceptions. The `TestMethod` attribute could therefore be modified to allow that exception through. The unit tester itself could then be adapted to catch that exception and still pass.

{% highlight csharp %}  
using System;  
using System.Collections.Generic;  
using System.Linq;  
using System.Reflection;

namespace UnitTester  
{  
    // Attribute to mark that a class contains tests that should be run  
    [AttributeUsage(AttributeTargets.Class)]  
    internal class TestClassAttribute : Attribute  
    {  
    }

    // Attribute to mark that a method is a test and so should be run  
    [AttributeUsage(AttributeTargets.Method)]  
    internal class TestMethodAttribute : Attribute  
    {  
    }

    // Class does not have TestClassAttribute so will ignored  
    internal class TestSuiteOne  
    {  
        // Method has TestMethod attribute but resides in a class without TestClass so will be ignored  
        [TestMethod]  
        public void DoTestOne()  
        {  
            Console.WriteLine("Doing test one in TestSuiteOne");  
        }  
    }

    // Class does have TestClassAttribute so will not be ignored  
    [TestClass]  
    internal class TestSuiteTwo  
    {  
        // Helper method does not have TestMethod attribute so will be ignored by the tester  
        // However will be run once indirectly through DoTestOne()  
        private void Helper()  
        {  
            Console.WriteLine("Helping to run the tests in TestSuiteTwo");  
        }

        // Method has TestMethod attribute so will be run by the tester  
        [TestMethod]  
        public void DoTestOne()  
        {  
            Console.WriteLine("Doing test one in TestSuiteTwo");  
            Helper();  
        }

        // Method has TestMethod attribute so will be run by the tester  
        [TestMethod]  
        public void DoTestTwo()  
        {  
            Console.WriteLine("Doing test two in TestSuiteTwo");  
        }  
    }

    internal class Program  
    {  
        public static void Main()  
        {  
            // Get access to all the types in the executing assembly  
            Assembly assembly = Assembly.GetExecutingAssembly();

            // Get all the types whose custom attributes includes TestClassAttribute  
            IEnumerable<Type> testClasses =  
            assembly.GetTypes().Where(t => t.GetCustomAttributes(false).Any(a => a is TestClassAttribute));

            foreach (Type testClass in testClasses)  
            {  
                Console.WriteLine("Running tests in TestClass: " + testClass.Name);

                // Get all the methods from the testclass whose custom attributes includes TestMethodAttribute  
                IEnumerable<MethodInfo> testMethods =  
                testClass.GetMethods().Where(m => m.GetCustomAttributes(false).Any(a => a is TestMethodAttribute));

                // Create an instance of the test class so we can run the test methods from it  
                object testClassInstance = Activator.CreateInstance(testClass);  
                foreach (MethodInfo testMethod in testMethods)  
                {  
                    // Run each of the test methods using the instance of the testclass  
                    testMethod.Invoke(testClassInstance, null);  
                }  
            }  
        }  
    }  
}  
{% endhighlight %}