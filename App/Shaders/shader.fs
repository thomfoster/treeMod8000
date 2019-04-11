#version 330 core

// in vec3 gs_out_lightColor;

in GS_OUT {
  vec3 lightColor;
  float diffuseStrength;
} fs_in;

out vec4 outColor;

void main()
{

  float ambientStrength = 0.01;
  float diffuseStrength = fs_in.diffuseStrength;

  vec3 light = (ambientStrength + 3*diffuseStrength) * fs_in.lightColor;
  outColor = vec4(light, 1.0);
}
