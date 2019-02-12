# Literature Survey

Papers related to CCTV video summarization and the key points to be noted from them.

**1. CRAM: Compact Representation of Action in Movies** [Link](./papers/CRAM.pdf)

* Identifies only events of interest such as running, pick up, opening trunk etc. to generate action-specific summaries
* Clifford Fourier Transform (CFT)

**2. Making a Long Video Short: Dynamic Video Synopsis** [Link](./papers/dynamic_video_synopsis.pdf)

* Activity Detection
    * Input pixel is **labelled as active** if its colour varies from the temoporal median at that same pixel. The median filter reduces noise.

    * **Energy Minimization:** Two factors: Loss in activity and discontinuity across seams.

    Loss in activity: Difference of sums of active pixels in input and output

    Discontinuity across seam: Sum Difference in colours of boundary pixels in spatio-temporal dimensions. (6 dimensions - 4 spatial & 2 temporal)

**3. Webcam Synopsis: Peeking Around the World** [Link](./papers/webcam_synopsis.pdf)

* Uses an object queue to store events

**4. Non Chronological Video Synopsis and Indexing** [Link](./papers/nonchronological_video_synopsis.pdf)

* Videos are indexed and stored. Clicking on an event in the synopsis video shows the event in the original recording.

**5. Clustered synopsis of Surveillance Video** [Link](./papers/clustered_synopsis.pdf)

* Similar events (spatially similar) are clustered together

**6. You Only Look Once: Unified, Real-Time Object Detection** [Link](./papers/you_only_look_once_unified_real-time_object_detection.pdf)

**7. Efficient adaptive density estimation per image pixel for the task of background subtraction** [Link]
(./papers/efficient_adaptive_density_estimation_per_image_pixel_for_the_task_of_background_subtraction.pdf)

**8. Deep Reinforcement Learning for Unsupervised Video Summarization** [Link](./papers/deep_reinforcement_learning_for_unsupervised_video_summarization)


## Other links

[Israel university vision website](http://www.vision.huji.ac.il/video-synopsis/)
