using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;


[RequireComponent(typeof(Rigidbody))]
public class CarAgent : Agent
{
   [Header("Transforms & Layer")]
   public Transform roadCenterTransform;       // center of the corridor
   public LayerMask wallLayer;


   [Header("Physics Parameters")]
   public float maxMotorForce = 1500f;         // forward force
   public float maxSteerAngle = 20f;           // steering angle for smooth turns
   public float rayDistance = 10f;             // distance for wall raycasts
   public float[] rayAngles = new float[] { -60f, -30f, -15f, 0f, 15f, 30f, 60f };


   [Header("Road Limits")]
   public float roadMinZ = -19f;                 // start of corridor
   public float roadMaxZ = 18f;                // end of corridor


   private Rigidbody rb;
   private Vector3 startPos;
   private Quaternion startRot;


   void Start()
   {
       rb = GetComponent<Rigidbody>();
       startPos = transform.position;
       startRot = transform.rotation;


       // smooth physics
       rb.linearDamping = 0.1f;
       rb.angularDamping = 0.3f;
   }


   public override void OnEpisodeBegin()
   {
       // reset position and orientation with slight randomization
       transform.position = startPos + new Vector3(Random.Range(-0.3f, 0.3f), 0f, 0f);
       transform.rotation = startRot * Quaternion.Euler(0f, Random.Range(-5f, 5f), 0f);
       rb.linearVelocity = Vector3.zero;
       rb.angularVelocity = Vector3.zero;
   }


   public override void CollectObservations(VectorSensor sensor)
   {
       // Raycasts to detect walls
       foreach (var angle in rayAngles)
       {
           Vector3 dir = Quaternion.Euler(0f, angle, 0f) * transform.forward;
           if (Physics.Raycast(transform.position + Vector3.up * 0.2f, dir, out RaycastHit hit, rayDistance, wallLayer))
               sensor.AddObservation(hit.distance / rayDistance);
           else
               sensor.AddObservation(1f); // no wall within range
       }


       // lateral offset from center
       float offsetX = roadCenterTransform != null ? transform.position.x - roadCenterTransform.position.x : 0f;
       sensor.AddObservation(offsetX / 5f);


       // forward speed normalized
       float forwardSpeed = Vector3.Dot(rb.linearVelocity, transform.forward);
       sensor.AddObservation(Mathf.Clamp(forwardSpeed / 10f, -1f, 1f));
   }


   public override void OnActionReceived(ActionBuffers actions)
   {
       float steer = Mathf.Clamp(actions.ContinuousActions[0], -1f, 1f);
       float throttle = Mathf.Clamp(actions.ContinuousActions[1], 0f, 1f); // only forward


       // Forward force
       rb.AddForce(transform.forward * throttle * maxMotorForce * Time.fixedDeltaTime, ForceMode.Acceleration);


       // Smooth steering torque
       float steerAngle = steer * maxSteerAngle;
       rb.AddTorque(Vector3.up * steerAngle * 5f * Time.fixedDeltaTime, ForceMode.VelocityChange);


       // --- Reward shaping ---
       float forwardVel = Vector3.Dot(rb.linearVelocity, transform.forward);


       // Reward for forward motion
       if (forwardVel > 0f)
           AddReward(forwardVel * 0.002f * Time.fixedDeltaTime);
       else
           AddReward(-Mathf.Abs(forwardVel) * 0.001f * Time.fixedDeltaTime); // penalty for backward motion


       // Penalty for lateral drift
       float lateralOffset = Mathf.Abs(transform.position.x - roadCenterTransform.position.x);
       AddReward(-lateralOffset * 0.01f * Time.fixedDeltaTime);


       // Penalty for too much rotation (spinning)
       AddReward(-Mathf.Abs(rb.angularVelocity.y) * 0.001f * Time.fixedDeltaTime);


       // --- Corridor Z boundaries ---
       float zPos = transform.position.z;
       if (zPos < roadMinZ || zPos > roadMaxZ)
       {
           AddReward(-1f);   // big penalty
           EndEpisode();     // reset episode
       }


       // Optional: small penalty for being near the back
       if (zPos < roadMinZ + 2f)
           AddReward(-0.01f * Time.fixedDeltaTime);
   }


   public override void Heuristic(in ActionBuffers actionsOut)
   {
       var cont = actionsOut.ContinuousActions;
       cont[0] = Input.GetAxis("Horizontal"); // steering
       cont[1] = Input.GetAxis("Vertical");   // throttle
   }


   void OnCollisionEnter(Collision collision)
   {
       if (collision.gameObject.CompareTag("Wall"))
       {
           AddReward(-1f);  // collision penalty
           EndEpisode();
       }
   }
}
