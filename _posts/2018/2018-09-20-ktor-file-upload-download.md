---
layout: post
title: Ktor - File Upload and Download
tags:
    - kotlin
    - ktor
    - file
    - upload
    - download
last_modified_at: 2022-10-15
typora-root-url: ../..
---

The ability to perform file uploads and downloads is a staple part of any good web server framework. [Ktor](https://github.com/ktorio/ktor) has support for both operations in just a few lines of code.

## File Upload

File uploads are handled through multipart `POST` requests in standard `HTTP` - normally from `form` submissions where the file selector field would be just one item (another could be the title for example).

To handle this in [Ktor](https://github.com/ktorio/ktor), you can get hold of the multipart data through `receiveMultipart` and then loop over each part as required. In the below example, we are just interested in files (`PartData.FileItem`), although you could also look at the individual `PartData.FormItem` as well (which would be the other form fields in the submission).

A Ktor `FileItem` exposes an `InputStream` via `streamProvider` which can be used to access the raw bytes of the file which has been uploaded. As in the below example, you can then simply create the appropriate file and copy the bytes from one stream (input) to the other (output).

```kotlin
post("/upload") { _ ->
    // retrieve all multipart data (suspending)
    val multipart = call.receiveMultipart()
    multipart.forEachPart { part ->
        // if part is a file (could be form item)
        if(part is PartData.FileItem) {
            // retrieve file name of upload
            val name = part.originalFileName!!
            val file = File("/uploads/$name")

            // use InputStream from part to save file
            part.streamProvider().use { its ->
                // copy the stream to the file with buffering
                file.outputStream().buffered().use {
                    // note that this is blocking
                    its.copyTo(it)
                }
            }
        }
        // make sure to dispose of the part after use to prevent leaks
        part.dispose()
    }
}
```

## File Download

File downloads are very straightforward in `Ktor`. You just have to create a handle to the specified `File` and use the `respondFile` method:

```kotlin
get("/{name}") {
    // get filename from request url
    val filename = call.parameters["name"]!!
    // construct reference to file
    // ideally this would use a different filename
    val file = File("/uploads/$filename")
    if(file.exists()) {
        call.respondFile(file)
    }
    else call.respond(HttpStatusCode.NotFound)
}
```

By default, if called from the browser, this will cause the file to be viewed `inline`. If you instead want to prompt the browser to download the file, you can include the `Content-Disposition` header:

```kotlin
call.response.header("Content-Disposition", "attachment; filename=\"${file.name}\"")
```

This is also helpful if you save the uploaded file with a different name (which is advisable), as you can override the filename with the original when it gets downloaded by users.

[More information about the `Content-Disposition` header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition)
