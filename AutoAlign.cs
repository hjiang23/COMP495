using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AutoAlign : MonoBehaviour
{
    
    //Drag and drop the camera pointing at the floor here
    // public GameObject floorCam ;

    //Drag and Drop a object in the scene to act as origin
    public GameObject cube;
    //public GameObject model;
    
    //Camera component from the floorcam
    public Camera camC; 
    public Camera camC2;

    public GameObject OVRCameraRig;

    // List of Polygons Hit Normals to be used to get an average
    private List<Vector3> polygonNormals = new List<Vector3>(); 

    void Start()
    {      
        float scalingFactor = AutoScale();
        print("Scaling factor: " + scalingFactor);
        //get component
        //camC = floorCam.GetComponent<Camera>(); 

        //print(camC.transform.position);
        // Shoot a bunch of rays from the camera and record the hit normals
        ShootRays(); 

        //define average of hit normals
        var _normal_average = Vector3.zero; 

        //Add normals
        foreach (Vector3 vec in polygonNormals)
        {
            _normal_average += vec; 
        }

        //calculate normal average
        _normal_average  = _normal_average / polygonNormals.Count;  

        // final raycast to set change origin and rotate the mesh
        RaycastHit hit; 
        // Vector3 fwd = floorCam.transform.TransformDirection(Vector3.forward); //forward dorection AKA the direction the camera is looking to
        // if (Physics.Raycast(floorCam.transform.position, fwd, out hit, Mathf.Infinity))
        Vector3 fwd = camC.transform.TransformDirection(Vector3.forward); //forward dorection AKA the direction the camera is looking to
        if (Physics.Raycast(camC.transform.position, fwd, out hit, Mathf.Infinity))
        {
            
            cube.transform.position = hit.point; //move object to where the raycast hit
            cube.transform.rotation = Quaternion.FromToRotation(cube.transform.up, _normal_average) * cube.transform.rotation; //rotate objext so its facing the normal we calculated above
            //cube.transform.localScale = new Vector3(scalingFactor, scalingFactor, scalingFactor);
            this.transform.SetParent(cube.transform); //set oject as origin by making it the root parent
            OVRCameraRig.transform.SetParent(cube.transform);
            cube.transform.rotation = Quaternion.FromToRotation(_normal_average, Vector3.up) * cube.transform.rotation; //inverse the rotation back to up from the normal so the whole mesh rotates
            cube.transform.position = Vector3.zero; //put the whole mesh at position 0,0,0
            cube.transform.localScale = new Vector3(scalingFactor, scalingFactor, scalingFactor);

        }

    }

    // Update is called once per frame
    void Update()
    {
        //Draw Rays every frame
        ShootRays(); 

        //AutoScale();
        
    }


    void ShootRays()
    {
        //The camera viewport is normalized from 0->1 on a XY plane we are only interested in part of the mesh in the center
        //so we loop from 0.4-0.6 in the center of the camera viewport and shoot rays
        for(float y = 0.4f; y < 0.6f; y+= 0.02f)
        {
            for(float x = 0.4f; x < 0.6f; x+= 0.02f)
            {   
                //Define the ray position 
                Ray ray = camC.ViewportPointToRay(new Vector3(x, y, 0));
                RaycastHit hit;
                //do the raycast hit
                if (Physics.Raycast(ray, out hit))
                {   
                    //record the hit normals
                    polygonNormals.Add(hit.normal); 

                    //draw the hit normals
                    //Debug.DrawRay(hit.point, hit.normal * 2000, Color.blue);
                }

            }
        } 
    }

    float AutoScale()
    {
        Vector3 pos1 = new Vector3();
        Vector3 pos2 = new Vector3();
        Debug.DrawRay(camC.transform.position, camC.transform.forward * 2000, Color.green);
        Ray ray = camC.ViewportPointToRay(new Vector3(0.5f, 0.5f, 0));
        RaycastHit hit;
        if (Physics.Raycast(ray, out hit))
        {   
            pos1 = hit.point;
            print(hit.point);
        }
        
        Debug.DrawRay(camC2.transform.position, camC2.transform.forward * 2000, Color.green);
        Ray ray2 = camC2.ViewportPointToRay(new Vector3(0.5f, 0.5f, 0));
        RaycastHit hit2;
        if (Physics.Raycast(ray2, out hit2))
        {   
            pos2 = hit2.point;
            print(hit2.point);
        }
        
        float dist = Vector3.Distance(pos1, pos2);
        print("Distance to other: " + dist);
                
        return 0.3048f/dist;
    }

}

