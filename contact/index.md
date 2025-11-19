---
title: Contact
nav:
  order: 5
  tooltip: Email, address, and location
---

# <i class="fas fa-envelope"></i>Contact


Our group is part of the [Faculty of Science and Engineering](https://www.fsg.ulaval.ca/en) at the Université Laval (https://www.ulaval.ca/). We located in Québec City, Québec, Canada. 

Québec City is a one of the most oldest and most beautiful cities in North America, full of cultural events, fine dining but yet close to several hiking trails and farms.   

{%
  include link.html
  type="email"
  icon=""
  text=""
  tooltip=""
  link="gabriel.reno@gmail.com"
  style="button"
%}
{%
  include link.html
  type="address"
  icon=""
  text="Google Maps"
  tooltip="Our location on Google Maps for easy navigation"
  link="https://maps.app.goo.gl/HWSiKXRUnsgwaXhUA"
  style="button"
%}

{:.center}

{% include section.html %}


{% capture col1 %}
{%
  include figure.html
  image="images/frontenac.jpg"
  caption="The Chateau Frontenac (picture by Wikicommons)"
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/jacques_cartier.jpg"
  caption="The Jacques Cartier National Park, 670 km2 (260 mi2), (picture by Wikicommons)"
%}
{%
  include figure.html
  image="images/ulaval.jpg"
  caption="The Université Laval campus"
%}


{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}
