---
layout: post
title: Scroll to top button with no jQuery
tags:
    - scroll
    - top
    - jquery
    - button
typora-root-url: ../..
---

Dynamic scroll to top buttons have become quite common amongst a lot of webpages now, but most guides online require the use of `jQuery` to achieve the functionality of smooth scrolling plus fade in/out. In modern browsers however, you can get much the same effect without the additional `~30kb+` library overhead if you are already using a separate framework.

### Create the button

First step is to create an element representing the actual button. This takes the form of a very simple `div` element (upon which dynamic styles will be attached) and a nested `img` pointing to whatever arrow etc you need. The button element can be as complex as you need as long as you wrap in a single `div` like below. The scroll to top button for this site is a simple `45x45px` arrow image which works well.

```html
<div id="topcontrol" title="Scroll to Top">
    <img src="/images/arrow.png" />
</div>
```

### Add styling

Without any styling, the image above will just appear at the bottom of your page. We need to add some `CSS` to ensure that the button always appears in the same position on the bottom right hand corner of the screen regardless of the current scroll position:

```scss
#topcontrol {
    @media (max-width: 38rem) {
        display: none;
    }

    position: fixed;
    bottom: 10px;
    right: 20px;
    opacity: 0;
    cursor: pointer;
}
```

The above `SCSS` selector (which can be translated to standard `CSS` as well), positions the element in a fixed position on the bottom right corner of the screen, sets the opacity to zero (to hide by default) and ensures that your cursor becomes a pointer when hovering over the button as you would expect.

### JavaScript Handler

Finally, to get the desired behaviour when the button is clicked, a small JavaScript segment is needed. The below snippet uses the `scrollTo` function on `window` to scroll the page to the top whenever the button is clicked. The new `smooth` behaviour controls the animated effect.

Because the button is hidden by default due to `opacity: 0` above, we also need to add an event handler to be called whenever the page is scrolled. If the current position is above a default threshold (100 in this case), the scroll to top button becomes visible and vice versa.

```html
<script>
    (function (document) {
        const topbutton = document.getElementById("topcontrol");
        topbutton.onclick = function (e) {
            window.scrollTo({ top: 0, behavior: "smooth" });
        };

        window.onscroll = function () {
            if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
                topbutton.style.opacity = "1";
            } else {
                topbutton.style.opacity = "0";
            }
        };
    })(document);
</script>
```

### Fade in/out

The above code will get all the behaviour we need, but the button will jump in and out of the page depending on the page position. To make it a little less jarring, some fade in/out can be added in. This is very similar to the `el.fadeIn()` methods you can find in jQuery. Because we are controlling the visibility solely based on opacity, we can make use of CSS transitions to animate the change across a number of milliseconds. Adding the below to the CSS selector above is a simple way to replicate the effect:

```scss
-webkit-transition: opacity 400ms ease-in-out;
-moz-transition: opacity 400ms ease-in-out;
-o-transition: opacity 400ms ease-in-out;
transition: opacity 400ms ease-in-out;
```
