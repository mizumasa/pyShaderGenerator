#!/usr/local/bin python
import sys
import time
import shader_generator as sg

def test():
    codeGenerator = sg.Generator()
    codeGenerator.init()
    codeGenerator.expandToEnd()
    codeGenerator.extend()
    codeGenerator.extend()
    textObj = codeGenerator.getTextObj()
    fragment_shader_code = """
        uniform float texture_width;
        uniform float texture_height;
        uniform float texture_posx;
        uniform float texture_posy;
        uniform float time;

        void main() {
            vec2 resolution = vec2( texture_width , texture_height);
            vec2 point0 = vec2( texture_posx , texture_posy);
            vec2 uv = -1. + 2. * (gl_FragCoord.xy - point0) / resolution.xy;
    """
    fragment_shader_code += textObj["line"]
    fragment_shader_code += "}"
    print(fragment_shader_code)


def main(argv):
    test()
    return

if __name__ == "__main__":
    print(sys.argv)
    main(sys.argv)