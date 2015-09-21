---
layout: post
title: 'C# – MP3 Tag Renaming'
tags:
  - 'c#'
  - library
---
After a recent migration away from iTunes (thankfully), I realised that a lot of the tags for my music files were pretty messy (thanks iTunes). Particularly the title tags for a few albums consisted of the artist name, a dash, and then the actual title of the song itself. For example `album artist – song title`. This quickly got annoying when scrolling through my library.

It seemed like a good opportunity to play with the [Id3Lib][1] library for C#.

This small C# utility app traverses through a directory structure looking for for all files within with the `.mp3` extension. A new instance of `Mp3File` is then created which allows pretty comprehensive modification of the residing ID3 tags which can be accessed through the `TagHandler` property. In this example a small `Regex` is used to remove the artist from the title and update the file.

{% highlight csharp %}  
using System;  
using System.IO;  
using System.Text.RegularExpressions;  
using Id3Lib.Exceptions;  
using Mp3Lib;

namespace Mp3Renamer  
{  
    class Program  
    {  
        static void Main()  
        {  
            IterateFiles(@"C:\Users\UserName\Music\SomeFolder");

            Console.WriteLine("Done");  
            Console.ReadLine();  
        }

        static void IterateFiles(string path)  
        {  
            var files = Directory.GetFiles(path, "*.mp3″, SearchOption.AllDirectories);  
            var length = files.Length;  
            var count = 0;

            foreach (var file in files)  
            {  
                try  
                {  
                    var mp3 = new Mp3File(file);

                    var title = mp3.TagHandler.Title;  
                    var artist = mp3.TagHandler.Artist;

                    title = Regex.Replace(title, @"^" + artist + @"\s\*-\s\*", "", RegexOptions.IgnoreCase).Trim();

                    mp3.TagHandler.Title = title;

                    mp3.Update();

                    if (count % 100 == 0)  
                        Console.WriteLine("Done " + count + " files of " + length);

                    count++;  
                }  
                catch (InvalidFrameException e)  
                {  
                    Console.WriteLine(e.Message);  
                }  
            }  
        }  
    }  
}  
{% endhighlight %}

This is just one of the many uses of this library which is really easy to get to grips with. The only problem I've had so far is with `'Invalid UTF-8 strings' in some of my files. But I guess that's a problem on my side and not with the library.

[Check out the ID3Lib for C#.][1]

[1]: http://sourceforge.net/projects/csid3lib/