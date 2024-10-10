#version 330 core
uniform sampler2D Texture;
uniform vec2 ScreenResolution;

out vec4 color;
in vec2 v_text;

// Pseudo-random number generator
float rand(vec2 co) {
    return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec2 uv = v_text;
    uv = uv * 2.0 - 1.0;

    // Warp the edges of the screen to simulate a CRT screen
    float radialDist = length(uv);
    float curvature = 30.0; // Control the amount of curvature. Higher values = less curvature
    float offset = 0.5 / curvature * radialDist * radialDist;
    vec2 warpedUV = uv * (1.0 + offset);
    warpedUV = (warpedUV + 1.0) / 2.0;

    // If the UV coordinates are out of bounds, set the color to black
    if (warpedUV.x < 0.0 || warpedUV.x > 1.0 || warpedUV.y < 0.0 || warpedUV.y > 1.0) {
        color = vec4(0.0, 0.0, 0.0, 1.0);
    } else {
        vec4 texColor = texture(Texture, warpedUV);

        // Add a scanline effect
        float scanlineWidth = 1000.0; // Control the width of the scanlines
        float scanlineAmount = 0.25; // Control the amount of scanlines
        float scanlineIntensity = 1.0; // Control the intensity of the scanlines
        float scanline = sin(warpedUV.y * scanlineWidth) * scanlineAmount;
        texColor *= (scanlineIntensity - scanline);

        // Add a simple color bleed effect
        float bleed = 0.002; // Control the amount of color bleed
        float r = texture(Texture, warpedUV + vec2(bleed, 0.0)).r;
        float b = texture(Texture, warpedUV - vec2(bleed, 0.0)).b;
        texColor = vec4(r, texColor.g, b, 1.0);

        // Add a vignette effect
        float vignetteWidth = 0.02; // Control the width of the vignette
        float edgeDist = min(min(warpedUV.x, 1.0 - warpedUV.x), min(warpedUV.y, 1.0 - warpedUV.y));
        float vignette = smoothstep(0.0, vignetteWidth, edgeDist);
        texColor *= vignette;

        // Add noise
        float noise = rand(gl_FragCoord.xy / ScreenResolution.xy);
        texColor.rgb += noise * 0.05;

        // Add a phosphor mask effect
        vec3 phosphorMask = vec3(1.0, 1.0, 1.0);
        vec2 pixelPos = gl_FragCoord.xy / ScreenResolution.xy;
        texColor.rgb *= phosphorMask * (0.5 + 0.5 * sin(3.0 * pixelPos.y));

        // Add a ghosting effect
        vec4 ghostColor = texture(Texture, warpedUV + vec2(0.0065, 0.0065));
        texColor = mix(texColor, ghostColor, 0.1);

        color = texColor;
    }
}