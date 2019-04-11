#version 330 core

layout (lines) in;
layout (triangle_strip, max_vertices = 250) out;

in VS_OUT {
  float radius;
  vec3 lightColor;
} gs_in[];

out GS_OUT {
  vec3 lightColor;
  float diffuseStrength;
} gs_out;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// ----------------------------------------------------------------------------------------
// Helper function for populating the gs out array and emitting points
// ----------------------------------------------------------------------------------------

void EmitPoint(vec4 pos, int end, vec3 norm){
  gl_Position = pos;
  gs_out.lightColor = gs_in[end].lightColor;
  vec3 lightSource = vec3(20, 10.0, -20.0); // Constant position
  vec3 lightRay = normalize(pos.xyz - lightSource); //Constant light source position
  float d = length(pos.xyz - lightSource);
  d = d/length(lightSource); //Normalise so that 0,0,0 has strength 2
  gs_out.diffuseStrength = max(dot(lightRay, norm), 0.0)/(pow(d,10));
  EmitVertex();
}

// ----------------------------------------------------------------------------------------
// Calculate normals and iteratively emit points
// ----------------------------------------------------------------------------------------

void main()
{

  #define PI 3.1415926535897932384626433832795

  int n = 11;
  float r1 = gs_in[0].radius;
  float r2 = gs_in[1].radius;

  vec3 lightSource = vec3(100.0, 10.0, -100.0); //Constant light location

  vec4 p1_4 = gl_in[0].gl_Position;
  vec3 p1 = p1_4.xyz;

  vec4 p2_4 = gl_in[1].gl_Position;
  vec3 p2 = p2_4.xyz;

  vec3 axis = p2 - p1;
  axis = normalize(axis);

  vec3 handle;
  handle = vec3(0.0, 0.0, 1.0);
  if ((axis.x == 0) && (axis.y == 0))
  {
    handle = vec3(1.0, 0.0, 0.0);
  }

  vec3 u = cross(handle,axis);

  u = normalize(u);
  // u = abs(u);
  vec3 v = cross(u, axis);
  v = normalize(v);

  float angle = 2*PI / float(n);

  // ---------------------------------------------------------------------------
  // Emit Sides
  // ---------------------------------------------------------------------------
  for (int i = 0; i < (n+1); i++)
  {

    // Caculate Points
    float alpha = sin(float(i)*angle);
    float beta = cos(float(i)*angle);
    vec4 a = projection * view * model * vec4(p1+(r1*alpha*u)+(r1*beta*v), p1_4.w);
    vec4 b = projection * view * model * vec4(p2+(r2*alpha*u)+(r2*beta*v), p2_4.w);
    alpha = sin(float(i+1)*angle);
    beta  = cos(float(i+1)*angle);
    vec4 c = projection * view * model * vec4(p1+(r1*alpha*u)+(r1*beta*v), p1_4.w);
    vec4 d = projection * view * model * vec4(p2+(r2*alpha*u)+(r2*beta*v), p2_4.w);

    //Calculate Norm
    alpha = sin((float(i)+0.5)*angle);
    beta = cos((float(i)+0.5)*angle);
    vec3 normal = (alpha*u)+(beta*v);
    normal = (model * vec4(normal, p1_4.w)).xyz;
    normal = normalize(normal);

    EmitPoint(a, 0, normal);
    EmitPoint(projection * view * model * p1_4, 0, axis);
    EmitPoint(c, 0, normal);
    EmitPoint(a, 0, normal);
    EmitPoint(b, 1, normal);
    EmitPoint(projection * view * model * p2_4 , 1, axis);
    EmitPoint(d, 1, normal);
    EmitPoint(b, 1, normal);
    EmitPoint(c, 0, normal);
    EmitPoint(d, 1, normal);
  }

  EndPrimitive();
}
