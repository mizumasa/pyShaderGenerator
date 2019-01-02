#!/usr/local/bin python
import shader_generator as sg

SAVE_PATH = "FragmentShader.glsl"

def makeNewShader(iter = 5):
    codeGenerator = sg.Generator()
    codeGenerator.init()
    codeGenerator.expandToEnd()
    for i in range(iter):
        codeGenerator.extend()
    textObj = codeGenerator.getTextObj()
    fragment_shader_code = """
        uniform vec2 resolution;
        uniform float time;
        void main() {
            vec2 uv = -1. + 2. * gl_FragCoord.xy / resolution.xy;
    """
    fragment_shader_code += textObj["line"]
    fragment_shader_code += "}"
    return fragment_shader_code

def saveShader(filename,code):
    f = open(filename,"w")
    f.write(code)
    f.close()
    
def getTimeStamp():
    from datetime import datetime
    buf = datetime.now()
    return buf.strftime("%Y")[2:] + buf.strftime("%m%d_%H%M%S")

def main():
    makeNewShader(SAVE_PATH)
    return

if __name__ == "__main__":
    main()
