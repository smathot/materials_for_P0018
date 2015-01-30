## Processing of pupil and eye-position signal

All signals were locked to the moment that the eyes crossed the vertical (for horizontal saccades) or horizontal (for vertical saccades) meridian (from now on: mid-saccade point). Mean pupil size from 105 to 95 ms before the mid-saccade point was takes as baseline, and all pupil size measures are reported relative to this baseline [cf. @Mathôt2013Plos]. Pupil size is based on area (i.e. not diameter). We analyzed pupil size from 300 ms before the mid-saccade point until 1200 ms after. Pupil size during blinks was reconstructed using cubic-spline interpolation [@Mathôt2013Reconstruct]. Eye position was smoothed using an 11 ms Hanning window.

## Trial-exclusion criteria

Trials were discarded when any of the following criteria was met: Saccade latency was below 0 ms (i.e. anticipation) or above 2000 ms; Peak saccade velocity could not be determined or was unrealistically high (> 1000 °/s; usually due to data loss); The eyes deviated more than 3.3° from the fixation dot before the saccade (excluding a 200 ms around the mid-saccade point). The eyes deviated more than 3.3° from the saccade target after the saccade (again excluding a 200 ms around the mid-saccade point). In total, 4001 trials (83.3%) remained for further analysis.

## Position artifacts in pupil size

In video-based eye trackers, changes in eye position cause artifactual changes in pupil size. This is due to factors such as the angle from which the camera records the eye, which changes as the eyes move. A common way to correct for position artifacts is to determine a linear regression that predicts (baseline) pupil size from horizontal (*X*) and vertical (*Y*) eye position. The *X* and *Y* slopes can then be used to 'regress out' eye position from pupil size [e.g. @Brisson2013Errors].

Clearly, this is applicable to our study as well. However, to our surprise, when we tried to eliminate position artifacts with linear regression, the apparently artifactual differences in pupil size between the four saccade directions increased. On closer inspection, it appeared that eye position had a real effect on pupil size. Correcting for this real effect as if it were artifactual distorted pupil-size measurements even further. Therefore, we decided not to correct our pupil-size measurements for position artifacts.

## Statistical analyses

Unless otherwise specified, we used linear mixed-effects models (LME) with by-participant random intercept and by-participant random slopes for all predictors. Identical analyses were conducted separately for each 1 ms sample. We did not estimate *p*-values, but considered effects reliable if they correspond to *t* > 2 for at least 200 consecutive 1 ms samples [cf. Mathôt2013Plos]. However, we emphasize effect sizes and overall patterns.
