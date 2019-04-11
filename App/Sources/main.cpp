// Local Headers
// why is this being run in main.cpp directory
// but shader and data import being run in builid directory
#include "../Headers/glitter.hpp"
#include "../Headers/shaderTools.h"

// System Headers
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

// Standard Headers
#include <cstdio>
#include <cstdlib>
#include <iostream>

void framebuffer_size_callback(GLFWwindow* window, int width, int height);
void processInput(GLFWwindow *window);

//Settings
const unsigned int SCR_WIDTH = 800;
const unsigned int SCR_HEIGHT = 600;

glm::vec3 rotationAxis = glm::vec3(0.0f, 1.0f, 0.0f);

int main() {

    // ----------------------------------------------------------------------------------------------
    // SET UP GL CONTEXT
    // ----------------------------------------------------------------------------------------------

    // Load GLFW and Create a Window //
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // We want new functionality
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);
    GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "Thom's Window", nullptr, nullptr); // Windowed
    // GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGL", glfwGetPrimaryMonitor(), nullptr);

    // Check for Valid Context //
    if (window == nullptr)
    {
        fprintf(stderr, "Failed to Create OpenGL Context");
        return EXIT_FAILURE;
    }

    // Create Context and Load OpenGL Functions
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
    gladLoadGL();
    fprintf(stderr, "OpenGL %s\n", glGetString(GL_VERSION));

    glEnable(GL_DEPTH_TEST);

    // ----------------------------------------------------------------------------------------------
    // BUILD AND COMPILE SHADERS
    // ----------------------------------------------------------------------------------------------

      Shader myShader("../App/Shaders/shader.vs",
                      "../App/Shaders/shader.fs",
                      "../App/Shaders/shader.gs");

    // ---------------------------------------------------------------------------------------------
    // READ IN VERTICES
    // ---------------------------------------------------------------------------------------------

    int num_vertices;

    // Read data into vertices
    std::cout << "About to read_file" << std::endl;
    std::ifstream read_file("../App/Models/data.dat");
    assert(read_file.is_open());

    read_file >> num_vertices;
    float vertices[4*num_vertices];

    std::cout << "Read in length" << std::endl;

    long i = 0;
    while (!read_file.eof())
    {
      read_file >> vertices[i];
      i++;;
    }
    read_file.close();

    // ---------------------------------------------------------------------------------------------
    // CREATE AND POPULATE BUFFERS
    // ---------------------------------------------------------------------------------------------

    // create 2 objects - a vertex buffer and a vertex attribute array
    // Vertex Buffer Objects store the vertices in the GPU

    unsigned int VBO, VAO; //create space for identifiers

    glGenVertexArrays(1, &VAO); //assign identifier
    glGenBuffers(1, &VBO);  //create a buffer and assign it to the id

    glBindVertexArray(VAO); //bind the vertex array at id vao to the current vertex array

    glBindBuffer(GL_ARRAY_BUFFER, VBO); //bind id to the GL_ARRAY_BUFFER target
    glBufferData(GL_ARRAY_BUFFER, 4*num_vertices*sizeof(float), vertices, GL_STATIC_DRAW); //upload data

    //say how to read attributes
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4*sizeof(float), (void*) 0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, 4*sizeof(float), (void*)(3*sizeof(float)));
    glEnableVertexAttribArray(1);

    // ---------------------------------------------------------------------------------------------//
    // ---------------------------------------------------------------------------------------------//
    //                                      // RENDER LOOP //                                       //
    // ---------------------------------------------------------------------------------------------//
    // ---------------------------------------------------------------------------------------------//

    // Move object back into view
    glm::mat4 view = glm::mat4(1.0f);
    view = glm::translate(view, glm::vec3(0.0f, 0.0f, -3.5f));

    // GLFW uses closed event loop. Only deal with events when you need to.
    while(!glfwWindowShouldClose(window))
    {
      processInput(window);

      glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

      myShader.use();

      // ---------------------------------------------------------------------------------------------
      // SET UP PROJECTIONS
      // ---------------------------------------------------------------------------------------------

      // Define project matrix
      glm::mat4 projection = glm::mat4(1.0f);
      projection = glm::perspective(glm::radians(45.0f), (float)SCR_WIDTH/(float)SCR_HEIGHT, 0.1f, 100.0f);
      int projectionLoc = glGetUniformLocation(myShader.ID, "projection");
      glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, glm::value_ptr(projection));

      glm::mat4 model = glm::mat4(1.0f);
      model = glm::translate(model, glm::vec3(0.0f, -0.5f, 0.0f));
      model = glm::rotate(model, glm::radians(25.0f), glm::vec3(1.0f, 0.0f, 0.0f));
      model = glm::rotate(model, glm::radians(-25.0f), glm::vec3(0.0f, 1.0f, 0.0f));

      //For time based rotation
      model = glm::rotate(model, (float)glfwGetTime() * glm::radians(35.0f), rotationAxis);

      // For key press rotation
      //model = glm::rotate(model, glm::radians(0.035f), rotationAxis);

      // //Send matrices to shader
      int modelLoc = glGetUniformLocation(myShader.ID, "model");
      glUniformMatrix4fv(modelLoc, 1, GL_FALSE, &model[0][0]);
      int viewLoc = glGetUniformLocation(myShader.ID, "view");
      glUniformMatrix4fv(viewLoc, 1, GL_FALSE, &view[0][0]);

      // -------------------------------------------------------------
      // DRAWING
      // ----------------------------------------------------------------

      // Bind, DRAW and unbind vertices
      glBindVertexArray(VAO);
      glBindBuffer(GL_ARRAY_BUFFER, VBO);
      glDrawArrays(GL_LINES, 0, num_vertices);
      glBindVertexArray(0);

      glfwSwapBuffers(window);
      glfwPollEvents();

    } //End of render loop

    glfwTerminate();
    return 0;
}

// process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
// ---------------------------------------------------------------------------------------------------------
void processInput(GLFWwindow *window)
{
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);

    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
        rotationAxis = glm::vec3(-1.0f, 0.0f, 0.0f);

    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
        rotationAxis = glm::vec3(0.0f, -1.0f, 0.0f);

    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
        rotationAxis = glm::vec3(1.0f, 0.0f, 0.0f);

    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
        rotationAxis = glm::vec3(0.0f, 1.0f, 0.0f);

    // if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
    //     rotationAxis = glm::vec3(1.0f, 0.0f, 0.0f);
}

// glfw: whenever the window size changed (by OS or user resize) this callback function executes
// ---------------------------------------------------------------------------------------------
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    // make sure the viewport matches the new window dimensions; note that width and
    // height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height);
}
