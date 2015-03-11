## Preprocessing of pupil and eye-position signal

All signals were locked to the moment that the eyes crossed the vertical (for horizontal saccades) or horizontal (for vertical saccades) meridian (from now on: mid-saccade point). Mean pupil size from 105 to 95 ms before the mid-saccade point was takes as a baseline, and all pupil size measures are reported in area (i.e. not diameter) relative to this baseline [cf. @Mathôt2013Plos]. We analyzed pupil size from 300 ms before until 1200 ms after the mid-saccade point. Pupil size during blinks was reconstructed using cubic-spline interpolation [@Mathôt2013Reconstruct]. Pupil size was not smoothed. To obtain an acceptable noise level in eye-velocity profiles, eye position was smoothed using an 11 ms Hanning window.

## Trial-exclusion criteria

Trials were discarded when any of the following criteria was met: Saccade latency was below 0 ms (i.e. anticipation) or above 2000 ms; Peak saccade velocity could not be determined or was unrealistically high (> 1000 °/s; usually due to data loss); The eyes deviated more than 3.3° from the fixation dot before the saccade (excluding a 200 ms around the mid-saccade point). The eyes deviated more than 3.3° from the saccade target after the saccade (again excluding a 200 ms around the mid-saccade point). In total, 4001 trials (83.3%) remained for further analysis.

## Position artifacts in pupil size

In video-based eye trackers, changes in eye position cause artifactual changes in measured pupil size. These position artifacts are due to factors such as the angle from which the camera records the eye, which changes as the eyes move. A common way to correct for position artifacts is to determine a linear regression that predicts (baseline) pupil size from horizontal (*X*) and vertical (*Y*) eye position. The *X* and *Y* slopes can then be used to 'regress out' eye position from pupil size [e.g. @Brisson2013Errors].

Clearly, this is applicable our study as well. But when we tried to eliminate position artifacts through linear regression, the apparently artifactual differences in pupil size between the four saccade directions increased, rather than decreased. On closer inspection, it appeared that eye position had both a real and an artifactual effect on pupil size. Correcting for this combined effect as if it were purely artifactual distorted pupil-size measurements even further. Therefore, we decided not to correct our pupil-size measurements for position artifacts, and absolute changes in pupil size that occur while the eyes are moving should be interpreted with caution.

## Statistical analyses

Unless otherwise specified, we used linear mixed-effects models (LME) with by-participant random intercept and by-participant random slopes for all predictors. Identical analyses were conducted separately for each 1 ms sample. We did not estimate *p*-values, but considered effects reliable if they correspond to *t* > 2 for at least 200 consecutive 1 ms samples [cf. @Mathôt2014JVis]. However, we emphasize effect sizes and overall patterns.
