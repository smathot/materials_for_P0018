## Main result: Intrasaccadic perception induced pupillary constriction

The main result is shown in %FigMainTrace, in which pupil size is plotted over time as a function of condition (Intrasaccadic Percept vs No Percept). The pupil constricted in both conditions, starting about 220 ms after the mid-saccade point, consistent with the latency of the pupillary response [e.g., @Ellis1981]. Crucially, as predicted, this constriction was more pronounced in the Intrasaccadic-Percept Condition than in the No-Percept Condition. Based on an LME with pupil size as dependent measure, and Condition, Saccade Direction (Horizontal, Vertical), and their interaction as fixed effects, the effect of condition was reliable from 606 ms after the mid-saccade point until the end of the analysis period.

%--
figure:
 id: FigMainTrace
 source: FigMainTrace.svg
 caption: |
  Mean pupil normalized pupil size over time, locked to the mid-saccade point. There was a more pronounced constriction in the Intrasaccadic Percept Condition than in the No-Percept Condition. Error bands indicate the standard error. Gray shading indicates a reliable effect of Condition. See main text for a description of the statistical model. 
--%

## Differences between saccade directions

Based on the LME described above, there was a reliable interaction between Condition and Saccade Direction from 726 ms until the end of the analysis period. This interaction indicated that the Condition effect was driven mainly by horizontal saccades. We confirmed this by analyzing each saccade direction separately, based on four separate LMEs with Condition as fixed effect and pupil size as dependent measure (%FigDirectionTrace). There was a large and reliable Condition effect for leftward and rightward saccades (%FigDirectionTrace::a,d). There was also a reliable Condition effect for downward saccades (%FigDirectionTrace::g), but it was much weaker. For upward saccades, there was no reliable effect of condition (see %FigDirectionTrace::j). In addition, there was considerable sample-to-sample variability in the LME estimates (as shown by the jittery error bands in %FigDirectionTrace), suggesting that the data for upward saccades was especially noisy data.

%--
figure:
 id: FigDirectionTrace
 source: FigDirectionTrace.svg
 caption: |
  Pupil-size, eye-position, and eye-velocity traces for each of the four saccade directions. a,d,g,j) Error bands indicate the standard error. Gray shading indicates a reliable effect of condition. See main text for a description of the statistical models. b,e) Horizontal eye position over time. c,f) Horizontal eye velocity over time. h,k) Vertical eye position over time. i,l) Vertical eye velocity over time. b,c,e,f,h,i,k,l) Individual trials are color coded to indicate peak saccade velocity (red: high velocity; blue: low velocity).
--%

Although there are known differences between horizontal and vertical saccades [REF], we had not expected these to interfere with the effect of intrasaccadic perception on pupil size. We therefore conducted several exploratory analyses to better understand these differences.

First, peak velocities are more variable for vertical than horizontal saccades (compare %FigDirectionTrace::c,f,i,l). This was the case for all participants (two-sided paired-samples t-test using per-participant standard deviation of peak velocity as dependent measure: t = 6.42, p = .0001). This variability is important, because the intrasaccadic percept was optimized for a peak velocity of around 400°/s (depending slightly on the participant and saccade direction). Therefore, the intrasaccadic percept may have been less clear for vertical than horizontal saccades. To control for this, we determined the difference between the actual and the optimal peak velocity (from now on: *peak-velocity error*). Next, we selected trials on which peak-velocity error was less than the median peak-velocity error (separately for each participant and saccade start position).

Second, vertical saccades are more curved than horizontal saccades. Therefore, the velocity component that is perpendicular to the saccade direction (i.e. horizontal velocity during vertical saccades and vertical velocity during horizontal saccades; from now on: *orthogonal velocity*) was higher for vertical than horizontal saccades (%FigOrthoVel). This was the case for all participants (two-sided paired-samples t-test using per-participant mean peak orthogonal velocity as dependent measure: t = 10.25, p < .0001). Peak orthogonal velocity during vertical saccades often approached 150°/s. This leads to partial retinal stabilization of the grating, possible resulting in an intrasaccadic percept of a high-speed motion [see also @CastetMasson2000]. Therefore, horizontal movement during vertical saccades may have elicited an intrasaccadic percept in the No-Percept condition. To control for this, we selected trials on which peak orthogonal velocity was less than the median peak orthogonal velocity (seperately for each participant and saccade start position).

%--
figure:
 id: FigOrthoVel
 source: FigOrthoVel.svg
 caption: |
  Eye velocity perpendicular to the saccade direction (orthogonal velocity). a, b) Vertical eye velocity during horizontal saccades. c,d) Horizontal velocity during vertical saccades. Individual trials are color coded to indicate peak orthogonal velocity (red: high velocity; blue: low velocity).
--%

Next, using vertical saccades from this subset of data, we performed the same analysis as before. Based on an LME with Condition as fixed effect and pupil size as dependent measure, we now also observed a reliable Condition effect for vertical saccades (%FigOptimalTrace). Therefore, we believe that the overall Condition effect for vertical saccades was obscured by variability in peak velocity, and pronounced curvature.

%--
figure:
 id: FigOptimalTrace
 source: FigOptimalTrace.svg
 caption: "Analysis of a subset of vertical-saccade trials on which orthogonal velocity was low and peak saccade velocity was close to optimal. Pupil size is plotted over time, locked to the mid-saccade point. There was a more pronounced constriction in the Intrasaccadic Percept Condition than in the No-Percept Condition. Error bands indicate the standard error. Gray shading indicates a reliable effect of Condition. See main text for the selection procedure, and a description of the statistical model."
--%

## Subjective ratings

%FigRatings shows how the participants' subjective ratings of how strongly they had perceived 'something odd' during saccades, separately for each saccade direction. These ratings suggest that all participants experienced a clear intrasaccadic percept. There is a tendency for the intrasaccadic percept to be rated more salient for horizontal than vertical saccades, but there is considerable variability between participants.

%--
figure:
 id: FigRatings
 source: FigRatings.svg
 caption: |
  Participant's ratings of how strongly they had perceived 'something odd' during saccades, separately for each saccade direction. Error bars indicate 95% within-subject confidence intervals [@Cousineau2005]. Dots correspond to single ratings, color coded by participant.
--%
