#include <iostream>
#include <cmath>
#include <map>
#include <fstream>
#define GLEW_STATIC
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include "../glm/glm/glm.hpp"
#include "../glm/glm/gtc/matrix_transform.hpp"
#include "../glm/glm/gtc/type_ptr.hpp"

#include "shaders.h"
#include "object.h"
#include "matrix.h"

void GenHemisphere(float stepY = 0.05, int countPoints = 16, int r = 2){
    std::ofstream file("tests/hemisphere.obj", std::ofstream::out | std::ofstream::trunc);
    if(!file.is_open()){
        std::cout << "Can't open file\n";
    }
    else{
        float stepDgr = (float)360/countPoints;
        float x, y, z;
        int count = 0;
        for(y = 0; y < 2; y=y+stepY){
            count++;
            float alpha = asin((double)y/r);
            float firstx = r * cos(alpha);
            for(float dgr = 0; dgr < 360; dgr=dgr+stepDgr){
                x = firstx*cos(M_PI/180 * dgr);
                z = firstx*sin(M_PI/180 * dgr);
                file << "v " << x << " " << y << " " << z << "\n";
            }
        }
        file << "v 0 2 0\n";
        for(int i = 0; i < count-1; i++){
            for(int j = 0; j < countPoints; j++){
                file << "f " << j + i*countPoints << " " <<  j+(i+1)*countPoints << " " << (j+1)%countPoints + (i+1)*countPoints << " " << (j+1)%countPoints + i*countPoints << "\n";
            }
        }
        file << "f";
        for(int i = 0; i < countPoints; i++){
            file << " " << i;
        }
        file << "\n";
        for(int i = 0; i < countPoints; i++){
            file << "f " << countPoints*(count-1) + i << " " <<  countPoints*count << " " << countPoints*(count-1) + (i+1)%countPoints << "\n";
        }
    }
    file.close();
}

void GenHourseshoe(int ring=15, int points=9, int R=5, int r=2){
    std::ofstream file("figures/horseshoe.obj", std::ofstream::out | std::ofstream::trunc);
    if(!file.is_open()){
        std::cout << "Can't open file\n";
    }
    else{
        float stepI = (float)200/ring;
        float stepJ = (float)360/points;
        float x, y, z;
        for(float i = 90, countR = 0; i < 290, countR < ring; i=i+stepI, countR++){
            for(float j = 0, countP = 0; j < 360.0f, countP < points; j=j+stepJ, countP++){
                x = (R+r*cos(M_PI/180 * j)) * sin(M_PI/180 * i);
                y = (R+r*cos(M_PI/180 * j)) * cos(M_PI/180 * i);
                z = r * sin(M_PI/180 * j);
                file << "v " << x << " " << y << " " << z << "\n";
            }
        }
        for(int i = 0; i < ring-1; i++){
            for(int j = 0; j < points; j++){
                file << "f " << j+i*points << " " << j+(i+1)*points<< " " << (j+1)%points + (i+1)*points<< " " << (j+1)%points + i*points << "\n";
            }
        }
        file << "f";
        for(int i = 0; i < points; i++){
            file << " " << i;
        }
        file << "\nf";
        for(int i = points-1; i >= 0; i--){
            file << " " << i+(ring-1)*points;
        }
        file << "\n";
    }
    file.close();
}

std::map<std::string, std::vector<float>> materials{
    {"plastic", {0.9, 0.5, 0.6, 0.3}},
    {"gold", {1.0, 0.9, 0.2, 3.0}},
    {"cooper", {0.8, 0.3, 0.2, 4.0}}
};


int main(int argc, char *argv[]){
    if(argc < 2){
        perror("Usage: ./main <material> <count of rings> <points in ring>");
        //perror("Usage: ./main <material> <step of Y> <points in circle>");
        exit(-1);
    }
    std::string materialName = argv[1];
    int ringCount = 15, pointsCount = 9; 
    // float stepOfY = 0.1;
    // int pointsCount = 16; 
    if(argc > 3){
        ringCount = atoi(argv[2]);
        pointsCount = atoi(argv[3]);
        // stepOfY = atof(argv[2]);
        //pointsCount = atoi(argv[3]);
    }
    GenHourseshoe(ringCount, pointsCount);
    // GenHemisphere(stepOfY, pointsCount);

    std::vector<float> data = materials[materialName];
    if(data.empty()){
        std::cout << "There is no such material\n";
        return 0;
    }
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    GLFWwindow* window = glfwCreateWindow(700, 700, "Start", NULL, NULL);
	if(window == NULL){
		fprintf(stderr, "Невозможно открыть окно GLFW. Если у вас Intel GPU, то он не поддерживает версию 3.3. Попробуйте версию уроков для OpenGL 2.1.n");
		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);
	glewExperimental=true;
	if(glewInit()!=GLEW_OK){
		fprintf(stderr, "Невозможно инициализировать GLEWn");
		return -1;
	}
    int width, height;
    glfwGetFramebufferSize(window, &width, &height);  
    glViewport(0, 0, width, height);
    Object object("figures/horseshoe.obj");

	Shader shader;
    GLuint VBO, VAO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glBindVertexArray(VAO);    
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, object.getVAndN().size()*sizeof(float), &object.getVAndN().front(), GL_STATIC_DRAW);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), (GLvoid*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), (GLvoid*)(3*sizeof(GLfloat)));

    glEnableVertexAttribArray(1);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);
    // glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    glEnable(GL_DEPTH_TEST);
    while(!glfwWindowShouldClose(window)){
        glfwPollEvents();
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		shader.Use();
		GLfloat timeValue = glfwGetTime();
        object.SetrotX(timeValue*20);
        // object.SetrotY(timeValue*15);
        // object.SetscaleX(std::abs(cos(timeValue)));
        // object.SetscaleX(15);
        // object.SetscaleY(15);
        // object.SetscaleZ(15);


        object.Setdz(-15);
		glUniform3f(glGetUniformLocation(shader.shaderProgram, "ourColor"), data[0], data[1], data[2]);
		glUniform3f(glGetUniformLocation(shader.shaderProgram, "lightPos"), 0.0f, 0.0f, 15.0f);
		glUniform3f(glGetUniformLocation(shader.shaderProgram, "lightColor"), 1.0f, 1.0f, 1.0f);
		glUniform3f(glGetUniformLocation(shader.shaderProgram, "viewPos"), 0.0f, 0.0f, 0.0f);
		glUniform1f(glGetUniformLocation(shader.shaderProgram, "reflectionIntensity"), data[3]);

        GLuint matLoc = glGetUniformLocation(shader.shaderProgram, "transform");
        glUniformMatrix4fv(matLoc, 1, GL_FALSE, glm::value_ptr(mtx::ModelMatrix(object)));
        matLoc = glGetUniformLocation(shader.shaderProgram, "projection");
        glUniformMatrix4fv(matLoc, 1, GL_FALSE, glm::value_ptr(mtx::ProjectMatrix()));

        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, object.getAllVerteces().size()/3);

        glBindVertexArray(0);
        glfwSwapBuffers(window);
    }

    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glfwTerminate();
    return 0;
}