# 4 - Alcohol sound check

Some distilleries in Brazil praise their product’s quality by the distinct sound it makes when the bottle is hit after being quickly turned upside down. Investigate the phenomenon. Why does the effect not work with alcoholic carbonated drinks? What other liquids will maintain this “damping” effect for longer?

https://www.youtube.com/watch?v=CoSdcy4cfHA

## Repository content

The repository contains executable scripts in the root directory and common code inside the `modules` directory.

-   `audio_analysis.py` analyzes scans an input folder and computes distance evolution graphs for each recording found. It then tries to fit the data to an exponential function and outputs data to `.csv` and `.txt` files.
-   `visualize_distance.py` produces a graph that compares effect and reference spectra and highlights the area between the two, which represents the distance defined as:

    $$
    	d(s_1, s_2) = \int_{log_{10}(f_{min})}^{log_{10}(f_{max})}\left| s_1(u) - s_2(u) \right| du
    $$

    where $u$ is the base 10 logarithm of the frequency $f$.
