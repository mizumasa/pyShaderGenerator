
        uniform vec2 resolution;
        uniform float time;
        void main() {
            vec2 uv = -1. + 2. * gl_FragCoord.xy / resolution.xy;
    gl_FragColor = clamp( abs( vec4(
     uv.x * 10. - floor(uv.x * 10.) ,
     uv.x * abs( asin( sin( degrees( sin( uv.x * abs( sin( acos( exp( fract( exp2( sqrt( tan( sin( tan( sin( exp2( cos( time * 5.) ) * time) ) * time) * time) ) ) ) ) ) + time) ) - floor(uv.x * abs( sin( acos( exp( fract( exp2( sqrt( tan( sin( tan( sin( exp2( cos( time * 5.) ) * time) ) * time) * time) ) ) ) ) ) + time) )) + time) ) ) ) ) - floor(uv.x * abs( asin( sin( degrees( sin( uv.x * abs( sin( acos( exp( fract( exp2( sqrt( tan( sin( tan( sin( exp2( cos( time * 5.) ) * time) ) * time) * time) ) ) ) ) ) + time) ) - floor(uv.x * abs( sin( acos( exp( fract( exp2( sqrt( tan( sin( tan( sin( exp2( cos( time * 5.) ) * time) ) * time) * time) ) ) ) ) ) + time) )) + time) ) ) ) )) ,
     uv.y + time ,
     1. ) ),0.,1.);}