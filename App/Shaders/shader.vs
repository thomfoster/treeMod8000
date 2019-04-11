#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in float r_in;

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
    vs_out.radius = r_in;

    //For funky colours
    // float n = 23324;
    // float gen = 17;
    // float r = mod(gen*(15600*position.y), n)/n;
    // float g = mod(gen*(1000*position.y), n)/n;
    // float b = mod(gen*(1053200*position.y), n)/n;
    // vs_out.lightColor = vec3(r,g,b);

    // For brown
    vs_out.lightColor = vec3(0.8, 0.4, 0.0);
}
