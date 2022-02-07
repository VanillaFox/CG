#include <iostream>
#include <cmath>
#include <fstream>
#include <vector>
#define GLEW_STATIC
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include "glm/glm/glm.hpp"
#include "glm/glm/gtc/matrix_transform.hpp"
#include "glm/glm/gtc/type_ptr.hpp"

#include "shaders.h"
#include "object.h"
#include "matrix.h"

const std::string STEP_FLAG = "-step";
const std::string WFRAME_FLAG = "-wframe";
const std::string M_ORDER_FLAG = "-m";
const std::string N_ORDER_FLAG = "-n";

void GenBezier(std::vector<float>& x, std::vector<float>& y, std::vector<float>& z, float step=0.1, int n=3, int m=3){
    std::ofstream file("figures/bezier.obj", std::ofstream::out | std::ofstream::trunc);
    if(!file.is_open()){
        std::cout << "Can't open file\n";
    }
    else{
        std::vector<float> bu, bv;
        int linecount=0, rowcount;
        for(float u = 0; u < 1; u=u+step){
            linecount++;
            rowcount = 0;
            for(float v = 0; v < 1; v=v+step){
                rowcount++;
                bu.clear();
                bv.clear();

                for(int i = 0; i <= n; i++){
                    bu.push_back(std::tgamma(n+1)/(std::tgamma(i+1)*std::tgamma(n-i+1)) * pow(u, i) * pow((1-u), (n-i)));
                    bv.push_back(std::tgamma(m+1)/(std::tgamma(i+1)*std::tgamma(m-i+1)) * pow(v, i) * pow((1-v), (m-i)));
                }
                float uvx = 0, uvy = 0, uvz = 0;
                for(int i = 0, j = 0; i < (n+1), j < (n+1)*(m+1); i++, j=j+4){
                    uvx += x[j]*bu[i]*bv[0] + x[j+1]*bu[i]*bv[1] + x[j+2]*bu[i]*bv[2] + x[j+3]*bu[i]*bv[3];
                    uvy += y[j]*bu[i]*bv[0] + y[j+1]*bu[i]*bv[1] + y[j+2]*bu[i]*bv[2] + y[j+3]*bu[i]*bv[3];
                    uvz += z[j]*bu[i]*bv[0] + z[j+1]*bu[i]*bv[1] + z[j+2]*bu[i]*bv[2] + z[j+3]*bu[i]*bv[3];
                }
                file << "v "<< uvx << " " << uvy << " " << uvz << "\n";
            }
        }
        for(int i = 0; i < linecount-1; i++){
            for(int j = 0; j < rowcount-1; j++){
                file << "f " << j + i*rowcount << " " << j + (i+1)*rowcount << " " << j+1 + (i+1)*rowcount << " " << j+1 + i*rowcount << "\n";
            }
        }
    }
    file.close();
}

bool ParsFlags(std::string flag, bool& wframeFlag, std::string flagValue, float& step, int& n, int& m){
    bool ans = false;
    if(flag==WFRAME_FLAG){
        wframeFlag = true;
        ans = true;
    }
    if(flag==STEP_FLAG){
        step = stof(flagValue);
        ans = true;
    }
    if(flag==M_ORDER_FLAG){
        m = stoi(flagValue);
        ans = true;
    }
    if(flag==N_ORDER_FLAG){
        n = stoi(flagValue);
        ans = true;
    }
    return ans;
}

int main(int argc, char *argv[]){
    std::string flag, flagValue;
    bool wframeFlag = false;
    float step = 0.1;
    int n=3, m=3;

    if(argc > 1){
        for(int i = 1; i < argc; i++){
            flag = argv[i];
            if(flag==STEP_FLAG){
                i++;
                if(i==argc){
                    std::cout << "Incorrect use of the flag: " << flag << "\n";
                    exit(-1);
                }
                else{
                    flagValue = argv[i];
                    ParsFlags(flag, wframeFlag, flagValue, step, n, m);
                }
            }
            else{
                if(!ParsFlags(flag, wframeFlag, flagValue, step, n, m)){
                    std::cout << "Incorrect use of the flag: " << flag << "\n";
                    exit(-1);
                }
            }
        }
    }
    std::ifstream file("figures/coords.txt");
    if(!file.is_open()){
        std::cout << "Can't open file\n";
        return 0;
    }
    std::string xcoord, ycoord, zcoord;
    std::vector<float> x, y, z;
    int count = 0;
    while(file >> xcoord >> ycoord >> zcoord){
        x.push_back(std::stof(xcoord));
        y.push_back(std::stof(ycoord));
        z.push_back(std::stof(zcoord));
        count++;
    }
    if(count < (n+1)*(m+1)){
        std::cout << "Insufficient number of control points: " << (n+1)*(m+1)-count << "\n";
        exit(-1);
    }
    GenBezier(x, y, z, step, n, m);
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
    Object object("figures/bezier.obj");

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
    if(wframeFlag)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    glEnable(GL_DEPTH_TEST);
    while(!glfwWindowShouldClose(window)){
        glfwPollEvents();
        glClearColor(0.7f, 0.8f, 0.5f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		shader.Use();
		GLfloat timeValue = glfwGetTime();
        object.SetrotX(timeValue*30);
        object.SetrotY(timeValue*20);
        object.Setdz(-15);
		glUniform3f(glGetUniformLocation(shader.shaderProgram, "ourColor"), 0.1f, 0.5f, 0.3f);
		glUniform3f(glGetUniformLocation(shader.shaderProgram, "lightPos"), 0.0f, 0.0f, 15.0f);
		glUniform3f(glGetUniformLocation(shader.shaderProgram, "lightColor"), 1.0f, 1.0f, 1.0f);

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