#version 330 core

out vec4 fragColor;

smooth in vec2 f_TexCoord;

vec4 gridColor;

void main()
{
    if(fract(f_TexCoord.x / 0.0005f) < 0.025f || fract(f_TexCoord.y / 0.0005f) < 0.025f)
        gridColor = vec4(0.75, 0.75, 0.75, 1.0);
    else
        gridColor = vec4(0);
    // Check for alpha transparency
    if(gridColor.a != 1)
        discard;

    fragColor = gridColor;
}
