#!/usr/local/bin python
import sys
import time
import shader_generator as sg

GLSL_SANDBOX = True

def test():
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
    if GLSL_SANDBOX:
        fragment_shader_code = """
        #ifdef GL_ES
        precision mediump float;
        #endif
        """ + fragment_shader_code
    fragment_shader_code += textObj["line"]
    fragment_shader_code += "}"
    print(fragment_shader_code)

def main(argv):
    test()
    return

if __name__ == "__main__":
    main(sys.argv)
