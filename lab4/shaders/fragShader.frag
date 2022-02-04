#version 330 core
out vec4 color;
in vec3 Normals;
in vec3 pointPos;
uniform vec3 ourColor;
uniform vec3 viewPos;
uniform vec3 lightPos;
uniform vec3 lightColor;
uniform float reflectionIntensity;

void main(){
    vec3 lightVec = normalize(lightPos-pointPos);
    float difLight = max(dot(Normals, lightVec), 0.0);
    vec3 viewVec = normalize(viewPos-pointPos);
    vec3 reflectVec = reflect(-lightVec, Normals);
    float refl = pow(max(dot(viewVec, reflectVec), 0.0), 8);
    vec3 resRefl = reflectionIntensity * refl * lightColor;
    vec3 res = (difLight*lightColor + resRefl)*ourColor;
    color = vec4(res, 1.0f);
}