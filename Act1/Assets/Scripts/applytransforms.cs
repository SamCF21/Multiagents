/*
Use transformation position matrices to modify the vertices of a mesh

*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class applytransforms : MonoBehaviour
{
    // Variables to store the transformation matrices
    [SerializeField] Vector3 displacement;
    [SerializeField] AXIS rotationAxis;
    [SerializeField] float angle;
    // Variables to store the mesh data
    Mesh mesh;
    Vector3[] vertices;
    Vector3[] newVertices;
    // Start is called before the first frame update
    void Start()
    {
        // Get the mesh component
        mesh= GetComponentInChildren<MeshFilter>().mesh;
        // Allocate memory for the vertices
        vertices = mesh.vertices;
        // Create a new array to store the new vertices
        newVertices = new Vector3[vertices.Length];
        // Copy the vertices to the new array
        for (int i=0; i<vertices.Length; i++){
            newVertices[i] = vertices[i];

        }

        DoTransform();
    }

    // Update is called once per frame
    void Update()
    {
        DoTransform();
    }

    void DoTransform(){
        Matrix4x4 move = HW_Transforms.TranslationMat(displacement.x * Time.time, displacement.y * Time.time, displacement.z * Time.time);

        Matrix4x4 moveOrigin = HW_Transforms.TranslationMat(-displacement.x, -displacement.y, -displacement.z);

        Matrix4x4 moveObject = HW_Transforms.TranslationMat(displacement.x, displacement.y, displacement.z);

        Matrix4x4 rotate = HW_Transforms.RotateMat(angle * Time.time, rotationAxis); //time delta time, para que se normalice la velocidad

        //Matrix4x4 composite = move * rotate;
        Matrix4x4 composite = move * rotate;

        for (int i=0; i<newVertices.Length; i++){
            Vector4 temp = new Vector4(vertices[i].x, vertices[i].y, vertices[i].z, 1);

            newVertices[i] = composite * temp;

        
        mesh.vertices = newVertices;
        mesh.RecalculateNormals();
        }
    }
}
