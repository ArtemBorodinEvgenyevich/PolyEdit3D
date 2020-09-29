//fragment
#version 420 core

in vec3 fragColor;
out vec4 FragColor;

vec4 dotColor;

void main()
{
    vec2 circCoord = 2.0 * gl_PointCoord - 1.0;
    if (dot(circCoord, circCoord) > 1.0)
    {
        discard;
    } else
    {
        dotColor = vec4(fragColor, 1.0);
    }
    FragColor = dotColor;
}
