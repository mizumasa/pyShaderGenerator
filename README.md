# pyShaderGenerator
Processing Library for generating glsl code


```
import shader_lib

def setup():
    global sd
    size(600, 600, P2D)
    global code
    code = shader_lib.makeNewShader()
    print(code)
    shader_lib.saveShader("data/sample.glsl",code)
    sd = loadShader("sample.glsl")

def keyPressed():
    if key == "s":
        global code
        timeStamp = shader_lib.getTimeStamp()
        shader_lib.saveShader("data/"+timeStamp+".glsl",code)
        save("data/"+timeStamp+".png")

def draw():
    global sd
    sd.set("time", millis() / 1000.0)
    sd.set("resolution", float(width), float(height))  
    shader(sd)
    rect(0, 0, width, height)
```
