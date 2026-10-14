# Unity ML-Agents Autonomous Car

## Overview

This project contains a Unity ML-Agents `CarAgent` script for training a
simulated car to move forward through a corridor while avoiding walls
and staying near the center of the road.

The agent uses raycasts to sense nearby walls, observes its position and
forward speed, and controls steering and throttle through Unity physics.
A reward system encourages forward movement and discourages drifting,
spinning, collisions, and leaving the corridor.

This README describes the **third version** of `CarAgent` in the
supplied script---the version with seven sensing rays, road-boundary
checks, and additional reward shaping.

## How It Works

Each training episode follows this general loop:

1.  **Observe:** The agent gathers information about nearby walls, its
    lateral offset from the road center, and its forward speed.
2.  **Act:** The ML-Agents policy provides steering and throttle
    actions.
3.  **Apply physics:** The script applies forces and torque to the car's
    `Rigidbody`.
4.  **Receive rewards:** The agent is rewarded for forward progress and
    penalized for undesirable behavior.
5.  **End or continue:** The episode ends if the car collides with an
    object tagged `Wall` or crosses the configured corridor boundaries.
    ML-Agents can then begin another episode.

The script defines the agent's observations, actions, physics control,
and reward logic. **It does not train the neural network by itself.**
Training is normally run using the Unity ML-Agents Python training tools
and a separate training configuration.

## Observations

The third version supplies **9 observations** to the agent:

  ---------------------------------------------------------------------------
  Observation                                  Count Description
  --------------------- ---------------------------- ------------------------
  Wall raycasts                                    7 Distances to walls at
                                                     angles of -60°, -30°,
                                                     -15°, 0°, 15°, 30°, and
                                                     60° relative to the
                                                     car's forward direction.
                                                     Distances are normalized
                                                     by `rayDistance`; a
                                                     value of `1` means no
                                                     wall was detected within
                                                     range.

  Lateral offset                                   1 The car's X-position
                                                     relative to
                                                     `roadCenterTransform`,
                                                     divided by 5.

  Forward speed                                    1 Velocity in the car's
                                                     forward direction,
                                                     normalized by dividing
                                                     by 10 and clamping to
                                                     the range -1 to 1.
  ---------------------------------------------------------------------------

Raycasts use `wallLayer`, so the Unity scene must assign the relevant
wall objects to a layer included in that mask.

## Actions

The agent expects **2 continuous actions**:

  -----------------------------------------------------------------------
  Action                  Range                   Effect
  ----------------------- ----------------------- -----------------------
  Steering                -1 to 1                 Scales the steering
                                                  torque applied around
                                                  the Y axis. Negative
                                                  and positive values
                                                  turn in opposite
                                                  directions.

  Throttle                0 to 1                  Applies forward force.
                                                  This version does not
                                                  command reverse
                                                  throttle.
  -----------------------------------------------------------------------

The script applies these actions through the car's `Rigidbody`. The
exact handling depends on the Rigidbody configuration, physics settings,
and the force/torque values.

## Reward System

The reward shaping is designed to encourage forward travel through the
corridor.

  -----------------------------------------------------------------------
  Behavior                            Reward or penalty
  ----------------------------------- -----------------------------------
  Moving forward                      Small positive reward proportional
                                      to forward velocity

  Moving backward                     Small negative reward proportional
                                      to backward velocity

  Moving away from the road center    Negative reward proportional to
                                      absolute lateral offset

  Spinning                            Negative reward proportional to the
                                      magnitude of angular velocity
                                      around the Y axis

  Leaving the corridor                `-1` reward, then end the episode

  Colliding with an object tagged     `-1` reward, then end the episode
  `Wall`                              

  Being close to the corridor's       Additional small penalty
  starting boundary                   
  -----------------------------------------------------------------------

The relevant parameters are defined near the top of the script:

-   `maxMotorForce`: forward force scale.
-   `maxSteerAngle`: steering scale used to calculate torque.
-   `rayDistance`: maximum raycast sensing distance.
-   `rayAngles`: angles used for wall sensing.
-   `roadMinZ` and `roadMaxZ`: allowed corridor range along the Z axis.

Reward values are starting points, not guarantees of successful
learning. They may need tuning after observing training behavior.

## Requirements

-   Unity project with the Unity ML-Agents package installed.
-   A car GameObject with a `Rigidbody`.
-   A road/corridor scene with colliders for the walls.
-   A transform assigned to `roadCenterTransform`.
-   A configured `wallLayer` that includes the wall colliders.
-   Wall objects tagged exactly `Wall` for collision-triggered episode
    termination.
-   A `Behavior Parameters` component configured for the observation and
    action spaces described above.
-   For reinforcement-learning training, the ML-Agents Python training
    tools and a training YAML configuration.

## Unity Setup

1.  Create or open a Unity project and install/configure Unity
    ML-Agents.
2.  Save the third implementation as `CarAgent.cs`. The supplied text
    contains three classes with the same name; **do not paste all three
    versions into one C# file**. Keep only the third `CarAgent` class in
    this script.
3.  Attach `CarAgent` to the car GameObject. Ensure that the same
    GameObject has a `Rigidbody`.
4.  Add a `Behavior Parameters` component to the car. Configure its
    observation size to match the script's nine observations, and
    configure two continuous actions.
5.  Assign the road center transform to `roadCenterTransform` in the
    Inspector.
6.  Set `wallLayer` to include the layer used by the wall colliders. The
    raycast layer mask and the `Wall` tag serve different purposes: the
    layer mask controls sensing, while the tag check controls collision
    penalties.
7.  Set the corridor's Z limits using `roadMinZ` and `roadMaxZ`. These
    values must match the coordinates of your actual scene.
8.  Check the car's Rigidbody settings and test the scene in Play mode
    before training.

### Important scene checks

-   The car's forward direction is expected to be `transform.forward`;
    in this setup, the corridor boundaries are checked along the world Z
    axis.
-   The reward calculation uses `roadCenterTransform.position.x` without
    a null check. Assign this reference before running the scene.
-   Make sure the car starts within the configured Z limits.
-   Verify that walls have colliders and are included in `wallLayer`.
-   Verify that wall objects use the `Wall` tag if collisions should end
    an episode.
-   Tune the force and steering parameters for the scale and physics of
    your scene.

## Training and Use

### Train an agent

1.  Configure the ML-Agents `Behavior Parameters` component and create a
    training YAML configuration for the behavior name and trainer
    settings.
2.  Start training using the ML-Agents Python training workflow
    supported by your installed package version.
3.  Run the Unity scene with the agent and monitor training metrics and
    driving behavior.
4.  Save/export the trained model according to the ML-Agents workflow,
    then assign the resulting model to the agent's behavior
    configuration for inference.

The exact command, package versions, and YAML settings are not included
in the supplied script, so they must be provided for your
Unity/ML-Agents installation. The C# file alone is not a complete,
ready-to-train project.

### Test with keyboard input (optional)

The script's `Heuristic()` method maps Unity's `Horizontal` and
`Vertical` input axes to steering and throttle. This can be used for
manual testing when the behavior is configured to use heuristic actions.
It depends on the project's Unity input settings; it is not the trained
policy.

## Limitations and Notes

-   This script is a starting point for a corridor-driving experiment,
    not a complete autonomous-driving system.
-   It detects walls only through the configured raycasts and layer
    mask; it does not identify object types or plan routes.
-   It rewards forward motion and staying centered, but it does not
    explicitly reward reaching the corridor's end.
-   The fixed Z boundaries assume a corridor aligned with the world's Z
    axis.
-   Training quality depends on the scene, trainer configuration, reward
    balance, physics settings, and training duration.
-   The supplied source contains multiple iterations of `CarAgent`. Keep
    the desired implementation separate to avoid duplicate class
    definitions.

## Potential Extensions

-   Add a positive terminal reward for reaching the end of the corridor.
-   Add randomized obstacle placement or corridor layouts to improve
    generalization.
-   Visualize raycasts in the Unity Scene view for debugging.
-   Tune rewards to balance progress, collision avoidance, and center
    tracking.
-   Add evaluation scenes to test the trained policy on layouts not used
    during training.

## Project Status

This README documents the third `CarAgent` implementation from the
supplied source. It does not imply that a trained model, Unity scene,
trainer configuration, or other project assets are included.
