---
title: New Paper - An algorithm for quantifying and characterizing misleading trajectories in ecological processes
tags: 
  - monitoring
  - tool
  - time series
  - publication
author: Easton R. White
member: easton-white
image: https://quantmarineecolab.github.io/images/journal_covers/2021_Bahlai_etal_EcoInformatics.jpg
---

We have a new paper out today that builds on some of my past work on species monitoring.

Bahlai, C.A., White, E.R., Perrone, J.D., Cusser, S. and Whitney, K.S., 2021. [The Broken Window: An algorithm for quantifying and characterizing misleading trajectories in ecological processes](https://doi.org/10.1016/j.ecoinf.2021.101336). Ecological Informatics, p.101336. 
 
Imagine a short time series of three years for chipmunk monitoring on campus. Over those three years, there is a decline in the number of chipmunk observed. Is this concerning? Or is it simply natural variation? 

In the paper, we describe an algorithm to understand when we might be incorrectly characterizing ecological trends. Specifically, we examine long-term time series that we feel accurately capture a long-term pattern. We then artificially break these time series into smaller chunks of time. We evaluate how often these smaller time series present the same pattern as the overall long-term pattern. The image below shows an example of how looking at trends in shorter time series, compared with the overall time series, can lead to different conclusions.

{%
  include feature.html
  image="images/blog_post_images/broken_window.jpg"
%}


