#version 330

in vec2 UV;

uniform vec2 TILE;
uniform vec2 SCREEN;

uniform sampler2D tilebank;
uniform sampler2D map;

void main()
{
  vec3 coordTex = texture(map, UV).rgb;
  int id = int(coordTex.r * 255.0) + int(coordTex.g * 255.0) + int(coordTex.b * 255.0);
  //float id = (coordTex.r) + (coordTex.g) + (coordTex.b);

  if (id==0.0) {
    gl_FragColor = vec4(1.0, 0.0, 1.0, 1.0);
  }
  else {
    // float x = (SCREEN.x / TILE.x) / SCREEN.x;
    // float y = (SCREEN.y / TILE.y) / SCREEN.y;
    //
    // float offsetX = UV.x - (round(UV.x / TILE.x) * TILE.x);
    // float offsetY = UV.y - (round(UV.y / TILE.y) * TILE.y);
    //
    // gl_FragColor = texture(tilebank, vec2(x * id + offsetX, y + offsetY));

    // float xx = (TILE.x/SCREEN.x * id);
    // float yy = 0.0;
    //
    // vec2 UVr = UV * SCREEN;
    //
    // float offsetX = UVr.x - (round(UVr.x / TILE.x) * TILE.x);
    // float offsetY = UVr.y - (round(UVr.y / TILE.y) * TILE.y);
    //
    // //offsetX /= SCREEN.x;
    // //offsetY /= SCREEN.y;
    //
    // gl_FragColor = vec4(texture(tilebank, vec2(xx, yy)).rgba);

    float xx = ((SCREEN.x/4.0) * id) / SCREEN.x;
    float yy = 0.0;

    // vec2 UVo = vec2(((round((UV.x * SCREEN.x) / TILE.x)) * TILE.x) / SCREEN.x,
    //                 ((round((UV.y * SCREEN.y) / TILE.y)) * TILE.y) / SCREEN.y);
    //
    // vec2 offset = vec2((UV.x - UVo.x) / ((fac / (SCREEN.x/4.0))+1.0),
    //                    (UV.y - UVo.y) / ((fac / (SCREEN.x/4.0))+1.0));

    vec2 offset = vec2(mod((gl_FragCoord.x / SCREEN.x), (TILE.x / SCREEN.x)),
                       mod((gl_FragCoord.y / SCREEN.y), (TILE.y / SCREEN.y)));

    gl_FragColor = texture(tilebank, vec2(xx + offset.x, yy + offset.y));

    // float xx = (TILE.x/SCREEN.x * id);
    // float yy = 0.0;
    //
    // vec2 UVr = vec2(UV.x * SCREEN.x, UV.y * SCREEN.y);
    // float offsetX = UVr.x - (roundEven(UVr.x / TILE.x) * TILE.x);
    // float offsetY = UVr.y - (roundEven(UVr.y / TILE.y) * TILE.y);
    // offsetX /= SCREEN.x;
    // offsetY /= SCREEN.y;
    //
    // gl_FragColor = texture(tilebank, vec2(xx + offsetX, yy + offsetY));
  }
}
