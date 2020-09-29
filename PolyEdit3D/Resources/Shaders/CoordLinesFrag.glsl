//fragment
#version 420 core

in vec3 fragColor;
out vec4 FragColor;

vec4 dotColor;

void main()
{
    FragColor = vec4(fragColor, 1.0);
}
