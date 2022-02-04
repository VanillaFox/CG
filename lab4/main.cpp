#include <iostream>
#include <cmath>
#include <map>

#define GLEW_STATIC
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include "glm/glm/glm.hpp"
#include "glm/glm/gtc/matrix_transform.hpp"
#include "glm/glm/gtc/type_ptr.hpp"

#include "shaders.h"
#include "object.h"
#include "matrix.h"
#include "generators.h"

const std::string FRAME_FLAG = "-wframe";
const std::string SCALE_FLAG = "-scale";
const std::string YSTEP_FLAG = "-ystep";
const std::string RCOUNT_FLAG = "-rcount";
const std::string PCOUNT_FLAG = "-pcount";
const std::string GENERATE_FLAG = "-generate";

const std::string HEMISPHERE = "hemisphere";
const std::string HORSESHOE = "horseshoe";


std::map<std::string, std::vector<float>> materials{
    {"plastic", {0.9, 0.5, 0.6, 0.3}},
    {"gold", {1.0, 0.9, 0.2, 2.0}},
    {"copper", {0.8, 0.3, 0.2, 2.0}}
};


bool CheckFlags(std::string flag, bool& frameFlag, bool& genFlag,std::string& modelName, float& scale, float& ystep, int& ringCount, int& pointCount, std::string flagValue = "0"){
    bool answer = false;
    if(flag==SCALE_FLAG){
        if(stof(flagValue)>0){
            scale = stof(flagValue);
            answer = true;
        }
    }
    if(flag==YSTEP_FLAG){
        if(stof(flagValue)>0){
            ystep = stof(flagValue);
            answer = true;
        }
    }
    if(flag==RCOUNT_FLAG){
        if(stoi(flagValue)>2){
            ringCount = stoi(flagValue);
            answer = true;
        }
    }
    if(flag==PCOUNT_FLAG){
        if(stoi(flagValue)>2){
            pointCount = stoi(flagValue);
            answer = true;
        }
    }
    if(flag==GENERATE_FLAG){
        if(flagValue==HEMISPHERE){
            modelName = HEMISPHERE;
        }
        else if(flagValue==HORSESHOE){
            modelName = HORSESHOE;
        }
        else{
            return answer;
        }
        genFlag = true;
        answer = true;
    }
    if(flag==FRAME_FLAG){
        frameFlag = true;
        answer = true;
    }
    return answer;
}

int main(int argc, char *argv[]){
    if(argc < 3){
        perror("Usage: ./result <material> <model name> <flags> ");
        exit(-1);
    }
    std::string materialName = argv[1];
    std::vector<float> data = materials[materialName];
    if(data.empty()){
        std::cout << "There is no such material";
        return 0;
    }
    
    std::string flag, flagValue, modelName = argv[2];
    int flagIndx = 3;
    if(modelName[0]=='-'){
        flagIndx--;
    }
    bool frameFlag = false, genFlag = false;
    float scale = 1.0, stepOfY = 0.1;
    int ringCount = 15, pointsCount = 9;
    for(int i = flagIndx; i < argc; i++){
        flag = argv[i];
        if(flag==FRAME_FLAG){
            CheckFlags(flag, frameFlag, genFlag, modelName, scale, stepOfY, ringCount, pointsCount);
        }
        else{
            if(argc==i+1){
                perror("Enter a value for the flag");
                exit(-1);
            }
            i++;
            flagValue = argv[i];
            if(!CheckFlags(flag, frameFlag, genFlag, modelName, scale, stepOfY, ringCount, pointsCount, flagValue)){
                std::cout << "Incorrect use of flag: " + flag + "\n";
                exit(-1);
            }
        }
    }

    if(genFlag){
        if(modelName==HEMISPHERE)
            GenHemisphere(stepOfY, pointsCount);
        else
            GenHourseshoe(ringCount, pointsCount);
        modelName = "figures/" + modelName + ".obj";
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
    Object object(modelName);
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
    if(frameFlag){
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    }
    glEnable(GL_DEPTH_TEST);
    while(!glfwWindowShouldClose(window)){
        glfwPollEvents();
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		shader.Use();
		GLfloat timeValue = glfwGetTime();
        object.SetrotX(timeValue*20);
        object.SetrotY(timeValue*15);
        object.SetscaleX(scale);
        object.SetscaleY(scale);
        object.SetscaleZ(scale);
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