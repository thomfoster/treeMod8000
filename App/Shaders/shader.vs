#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in float r_in;
layout (location = 2) in float leaf;

out VS_OUT {
  float radius;
  vec3  lightColor;
} vs_out;


uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
  gl_Position = vec4(position, 1.0);
  if(leaf == 0.0){
    vs_out.radius = r_in;
    vs_out.lightColor = vec3(0.8, 0.4, 0.0);
  }
  else{
    vs_out.radius = 0*r_in;
    vs_out.lightColor = vec3(0.1, 0.4, 0.1);
  };
}
