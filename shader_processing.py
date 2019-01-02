#!/usr/local/bin python
import shader_generator as sg

SAVE_PATH = "FragmentShader.glsl"

def makeNewShader(filename):
    codeGenerator = sg.Generator()
    codeGenerator.init()
    codeGenerator.expandToEnd()
    codeGenerator.extend()
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
    f = open(filename,"w")
    f.write(fragment_shader_code)
    f.close()
    return

def main():
    makeNewShader(SAVE_PATH)
    return

if __name__ == "__main__":
    main()