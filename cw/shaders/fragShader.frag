#version 330 core
out vec4 color;
in vec3 Normals;
in vec3 pointPos;
uniform vec3 ourColor;
uniform vec3 lightPos;
uniform vec3 lightColor;


void main(){
    vec3 lightVec = normalize(lightPos-pointPos);
    float light = max(dot(Normals, lightVec), 0.0);
    vec3 res = light*lightColor*ourColor;
    color = vec4(res, 1.0f);
}