# 4 - Alcohol sound check

Some distilleries in Brazil praise their product’s quality by the distinct sound it makes when the bottle is hit after being quickly turned upside down. Investigate the phenomenon. Why does the effect not work with alcoholic carbonated drinks? What other liquids will maintain this “damping” effect for longer?

https://www.youtube.com/watch?v=CoSdcy4cfHA

## Repository content

The repository contains executable scripts in the root directory and common code inside the `modules` directory.

### Data analysis

-   `audio_analysis.py` scans an input folder and computes distance evolution graphs for each recording found. It then tries to fit the data to an exponential function and outputs data to `.csv` and `.txt` files.
-   `final_fit.py` fits height ($h$), duration ($t$), viscosity ($\eta$) and density ($\rho$) data and extracts the parameter $a$ from the following formula:
    $$t(h,\eta,\rho)=a \frac{h\eta}{\rho}$$
-   `fix_data.py` is a script to graphically reject data from a scatter plot. It allows the user to select a rectangle, discard all points contained inside of it and refit the remaining points to the fit function.
-   `refit.py` refits a `.csv` file to the fit function.

### Graphics

-   `make_animation.py` is used to create a `.mp4` animated version of the effect evolution over time.
-   `visualize_distance.py` produces a graph that compares effect and reference spectra and highlights the area between the two, which represents the distance defined as:

    $$d(s_1, s_2) = \int_{log_{10}(f_{min})}^{log_{10}(f_{max})}\left| s_1(u) - s_2(u) \right| du$$

    where $u$ is the base 10 logarithm of the frequency $f$.

## Results

[At this link](https://1drv.ms/p/s!AoC-sN1MqfUZgaBP7PB43X2qe_tCOg?e=OuFpLJ) you can find the Power Point presentation with our conclusions regarding this problem.
