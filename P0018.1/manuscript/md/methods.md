## Materials and availability

Participant data, the experimental script, and analysis scripts are available from <https://github.com/smathot/materials_for_P0018>. On-line materials include easy-to-use demonstration software that allows anyone with a sufficiently fast display to experience intrasaccadic perception.

## Participants

Ten naive observers (age range: 18-21 y; 3 men) participated in the experiment. Participants reported normal uncorrected vision. Participants provided written informed consent prior to the experiment, and received €20 for their participation. The experiment was conducted with approval of the *Comité d'éthique de l'Université d'Aix-Marseille* (Ref.: 2014-12-03-09).

## Software and apparatus

Eye position and pupil size were recorded monocularly with an EyeLink 1000 (SR Research, Mississauga, ON, Canada), a video-based eye tracker sampling at 1000 Hz. Stimuli were presented on a gamma-calibrated 21" ViewSonic p227f CRT monitor (1024x768, 150 Hz). Testing took take place in a dimly lit room. The experiment was implemented with OpenSesame [@MathôtSchreij2012] using the PsychoPy back-end [@Peirce2007] for display control and PyGaze [@Dalmaijer2014] for eye tracking.

## General stimuli and procedure

At the beginning of each session, a nine-point eye-tracker calibration was performed. Before each trial, a small dot was presented 8.5° left of, right of, above, or below the display center. When a stable fixation was detected, a one-point recalibration (drift correction) was performed. Next, the trial started with the presentation of a green fixation dot (36.8 cd/m²) at the same location as the drift-correction stimulus. At the same time, another green dot (the saccade target) was presented at the location opposite from the fixation dot (%FigMethods). After 1 s, an auditory cue (a 100 ms, 440 Hz sine wave) instructed the participant to make a saccade from the initial fixation dot to the saccade target. The trial ended 3 s after the onset of the auditory cue. Participants were instructed not to move their eyes before the cue, and to fixate on the saccade target until the end of the trial. In total, the experiment lasted about 2.5 hours. For some participants, data collection was spread across two days, in which case peak saccade velocities (as described below) were determined again on the second day.

%--
figure:
 id: FigMethods
 source: FigMethods.svg
 caption: |
  Participants initially fixated on a dot presented at the left, right, top, or bottom of the screen. A saccade target was presented at the location opposite from the fixation dot. An auditory cue instructed participants to make a saccadic eye movement to the saccade target.
--%

## Part 1: Peak saccade velocity

In the first part of the experiment, we determined the median peak velocity of saccades for each direction (left, right, down, up) and participant. The background was static and uniformly gray (51.1 cd/m²). Gaze position was sampled on every frame (i.e. every 6.67 ms). Blinks were treated as missing data. On every trial, the maximum of the peaks of the horizontal or vertical velocity profiles for the entire trial was taken as the peak saccade velocity; that is, peak velocity was the highest speed of the eyes at any moment and in any direction. When peak saccade velocity was unrealistic [above 664°/s or below 220°/s, based on a peak velocity of around 400°/s for 17° saccades, see @Baloh1975], the trial was discarded and repeated at a random moment during the remainder of the session. For every saccade direction, peak saccade velocity was based on the median of 40 trials.

## Part 2: Intrasaccadic perception

%--
figure:
 id: FigBistable
 source: FigBistable.svg
 caption: |
  During Part 2 of the experiment (see main text), the background consisted of a sinusoid grating that reversed polarity on every frame. The motion direction in this flickering display is ambiguous. The two opposite motion signals (leftward: red arrow; rightward: green arrow) result from matching the white and black bars across time. When viewed with static eyes, the flickering display appears as a homogeneous gray surface.
--%

In the second part of the experiment, we investigated the effect of intrasaccadic perception on pupil size. The background was a 22.6° x 22.6° full-contrast sinusoid (5.2 cd/m² to 95.1 cd/m²) grating that reversed in polarity on every frame (%FigBistable). During fixation, the background appeared a homogeneous gray surface, because the frame rate (150 Hz) exceeded the flicker fusion threshold (see %FigFusion::a). Furthermore, the display appeared uniformly gray, because the monitor was gamma calibrated: A pixel that alternated between minimum (5.2 cd/m²) and maximum brightness (95.1 cd/m²) had the same mean (fused) luminance as a pixel that was constantly at 50% brightness (50.2 cd/m²). The spatial frequencies of the gratings were set for each participant and saccade direction separately, based on the peak saccade velocities estimated during the first part of the experiment. (Due to a technical issue, for three participants the gratings were set to a default spatial frequency of 0.17 cycles/°. However, this default value was based on pilot testing, and was close to the ideal spatial frequency.) The spatial frequency was such that the maximum distance that the eyes traveled between two frames was equal to half a cycle. The logic behind this is that the flickering background contains ambiguous motion: It can be perceived as moving leftward or rightward with a speed of half a cycle per frame (%FigBistable). Therefore, the peak velocity of the eyes matched the velocity of the motion. As a result, the background approximated a retinotopically stabilized grating when saccade velocity was maximal (%FigFusion::b).

%--
figure:
 id: FigFusion
 source: FigFusion.svg
 caption: |
  a) The background is a rapidly flickering grating that is perceived as uniformly gray during fixation. b) When a saccade is made perpendicular to the grating (Intrasaccadic-Percept condition), the grating is briefly stabilized on the retina, which results in a flash-like intrasaccadic percept. c) When a saccade is made parallel to the grating (No-Percept condition), the grating is not stabilized on the retina, and no intrasaccadic percept arises.
--%

In the Intrasaccadic-Percept condition, the orientation of the grating was perpendicular to the direction of the saccade. Therefore, in this condition, participants should briefly perceive a static grating during the saccade, as described above (%FigFusion::b). In the No-Percept condition, the orientation of the grating was parallel with the direction of the saccade. Therefore, in this condition, no static grating should be perceived, because the saccade did not stabilize the grating on the retina (%FigFusion::c).

## Part 3: Subjective report

At the end of the experiment, participants provided a subjective report of how strongly they had perceived 'something odd' while making saccades. They provided separate ratings for each saccade direction on a 1 - 5 scale. Participants did not report the nature of the percept, i.e. whether they had perceived static or moving gratings.
