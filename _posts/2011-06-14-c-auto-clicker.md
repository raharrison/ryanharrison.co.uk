---
layout: post
title: 'C# – Auto Clicker'
tags:
  - 'c#'
---
I recently got a link to a Facebook app which challenges you to how many times you can click a button in 30 seconds. After a couple of tries I got to around 180, yet I thought that I must be able to do better by making the computer click for me.

After a bit of research I came across two functions from MSDN named `SendInput` and `mouse_event`, both of which are provided in the Win32 API, and allow you to programatically simulate both mouse clicks and keyboard input. Thus I thought it was a great opportunity to try out C#'s p/invoke feature which allows the programmer to 'import' unmanaged functions from DLL libraries and use them in a C# application.

In this example I will only be using the `mouse_event` function, however an implementation of `SendInput` is included in the sources files, which are available for download at the bottom of this post.

The MSDN page of the `mouse_event` function gives us some good information on how to implement the function, including a function header and a rundown on each of the parameters. They give the `mouse_event` function the following header –

{% highlight cpp %}  
VOID WINAPI mouse_event(  
  __in DWORD dwFlags,  
  __in DWORD dx,  
  __in DWORD dy,  
  __in DWORD dwData,  
  __in ULONG_PTR dwExtraInfo  
);  
{% endhighlight %}

Which can then be imported for use in our C# application using using the DLLImport attribute and the `extern` keyword (which simply indicates that the method is implemented externally) –

{% highlight csharp %}  
[DllImport("user32.dll")]  
public static extern void mouse_event(int dwFlags, int dx, int dy, int dwData, int dwExtraInfo);  
{% endhighlight %}

We can now call this unmanaged function as we would any other method already in our project. However to make good use of them, we need to find out a bit more information on each of the parameters. 

They can be summed up as follows –

  * **dwFlags** – In our case this parameter specifies which mouse button we would like to press depending on the integer value we pass
  * **dx** – The relative mouse position along the x-axis
  * **dy** – The relative mouse position along the y-axis
  * **dwData** – Contains how much we would like to move the mouse wheel and in which direction
  * **dwExtraInfo** – Contains extra information on the function call (not needed in our case)

In the case of this example we only have a need for the dwFlags parameter as we can easily set the cursor position using C# –

{% highlight csharp %}  
Cursor.Position.X = ...
Cursor.Position.Y = ...
{% endhighlight %}

Before we finally call this method, it is a good idea to declare some constants, each describing which mouse button we would like to press. Details can again be found on the relevant MSDN page –

{% highlight csharp %}  
public const int MOUSEEVENTF_LEFTDOWN = 0x0002;  
public const int MOUSEEVENTF_LEFTUP = 0x0004;  
public const int MOUSEEVENTF_RIGHTDOWN = 0x0008;  
public const int MOUSEEVENTF_RIGHTUP = 0x0010;  
public const int MOUSEEVENTF_MIDDLEDOWN = 0x0020;  
public const int MOUSEEVENTF_MIDDLEUP = 0x0040;  
{% endhighlight %}

Finally we can now call the function, which will be wrapped into two methods –

{% highlight csharp %}

private void ClickLeftMouseButtonMouseEvent()  
{  
  //Send a left click down followed by a left click up to simulate a  
  //full left click  
  mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);  
  mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);  
}

private void ClickRightMouseButtonMouseEvent()  
{  
  //Send a left click down followed by a right click up to simulate a  
  //full right click  
  mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0);  
  mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0);  
}  
{% endhighlight %}

As you can see we actually need to call the function twice, once for the mouse down action, and again for the mouse up action, to simulate a full mouse click. In this example we only use the `dwFlags` parameter and pass zero for the rest as we have no need for them.

So we now have two methods that we can use to simulate a mouse click, yet no way of letting the user determine where to click, how many times to click, and what mouse button to click – the perfect chance to create a C# Windows Forms Application (a.ka. GUI) to make our program a little more presentable.

In my program, I have created a simple User Interface containing a list view, a few buttons, and a couple of textboxes, which will allow the user to specify a queue of points to click in sequence, as well as the ability to insert additional information for each click (button to press, time in between, etc).

![Screenshot of the final Auto Clicker programe]({{ site.url }}/images/2011/Auto_Clicker.jpg){: .center-image width="527" height="276"}

[1]: http://ryanharrison.co.uk/apps/autoclicker/Auto_Clicker.zip
[2]: http://apps.facebook.com/myclickchallenge/

<!--more-->

The meat of the application happens in two methods. The first is the `StartClickingButton_Click` event handler, where a new thread is created to handle the mouse clicks so that the main form does not become completely unresponsive when the program is clicking every couple of milliseconds.

{% highlight csharp %}  
private void StartClickingButton_Click(object sender, EventArgs e)  
{  
  if (IsValidNumericalInput(NumRepeatsTextBox.Text))  
  {  
    int iterations = Convert.ToInt32(NumRepeatsTextBox.Text);  
    List<Point> points = new List<Point>();  
    List<string> clickType = new List<string>();  
    List<int> times = new List<int>();

    foreach (ListViewItem item in PositionsListView.Items)  
    {  
      //Add data in queued clicks to corresponding List collection  
      int x = Convert.ToInt32(item.Text); //x coordinate  
      int y = Convert.ToInt32(item.SubItems[1].Text); //y coordinate  
      clickType.Add(item.SubItems[2].Text); //click type  
      times.Add(Convert.ToInt32(item.SubItems[3].Text)); //sleep time

      points.Add(new Point(x, y));  
    }  
    try  
    {  
      //Create a ClickHelper passing Lists of click information  
      ClickThreadHelper helper = new ClickThreadHelper() { Points = points, ClickType = clickType, Iterations = iterations, Times = times };  
      //Create the thread passing the Run method  
      ClickThread = new Thread(new ThreadStart(helper.Run));  
      //Start the thread, thus starting the clicks  
      ClickThread.Start();  
    }  
    catch (Exception exc)  
    {  
      MessageBox.Show(exc.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);  
    }  
  }  
  else  
  {  
    MessageBox.Show("Number of repeats is not a valid positive integer", "Invalid Input", MessageBoxButtons.OK, MessageBoxIcon.Error);  
  }  
}  
{% endhighlight %}

In this method a few `List` collections are made to to store each portion of data about each click in the queue in a parallel manner. The corresponding information is added to each collection before they are passed into a new `ClickThreadHelper` object which will handle the mouse clicking. Next, a new thread is created and the `Run` method inside the `ClickThreadHelper` object is assigned to it. Finally, the thread is started, leaving all the work to `Run` method –

{% highlight csharp %}  
public void Run()  
{  
  try  
  {  
    int i = 1;

    while (i <= Iterations) 
    { 
      //Iterate through all queued clicks 
      for (int j = 0; j <= Points.Count - 1; j++) 
      { 
        //Set cursor position before clicking
        SetCursorPosition(Points[j]); 
        if (ClickType[j].Equals("R")) 
        { 
          ClickRightMouseButtonSendInput(); 
        } 
        else 
        {
          ClickLeftMouseButtonSendInput(); 
        } 
        Thread.Sleep(Times[j]); 
      }
      i++; 
    } 
  } 
  catch (Exception exc) 
  { 
    MessageBox.Show(exc.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error); 
  } 
} 
{% endhighlight %} 

This method is the only place where the two `imported` functions are called, and simply iterates over each of the collections already passed by the `StartClickingButton_Click` event handler. In each case the current position of the cursor is changed before the method decides on which mouse button to press. Finally the Thread is 'put to sleep' by the `.Sleep()` method of the `Thread` class by the allotted time given by the user - which results in a pause between each queued click. The rest of the program mainly consists of error checking user input, along with allowing the ability to stop the thread at any time and use keyboard shortcuts to set cursor coordinates. 

In my short tests I was able to accomplish 368,521 clicks on the same Facebook app, although it should be noted that it is is possible to gain much higher scores when the timer on the app sometimes freezes completely when clicking every few milliseconds In this program, only the left and right mouse buttons can be clicked, however the middle mouse button and mouse wheel can be manipulated much in the same manner by changing the constants used in the functions. 

Full commented source code along with an executable is available for download [HERE][1]. This includes example code on how to use the `SendInput` function, which requires the use of two small custom structs that essentially provide much of the same information as before.

Hope you enjoyed.

The Facebook app can be found [HERE][2]

MSDN links to the Win32 functions –

mouse_event = <http://msdn.microsoft.com/en-us/library/ms646260>  
SendInput = <http://msdn.microsoft.com/en-us/library/ms646310(v=vs.85).aspx>  

Pages on the two custom structures for the SendInput function

  * <http://msdn.microsoft.com/en-us/library/ms646270(v=vs.85).aspx>  
  * <http://msdn.microsoft.com/en-us/library/ms646273(v=vs.85).aspx>
