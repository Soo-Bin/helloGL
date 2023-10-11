import glfw
import OpenGL.GL.shaders as shaders
import numpy as np
from OpenGL.GL import *

# glfw 초기화
if not glfw.init():
    print("glfw init failed")
    exit()

# Window의 크기를 설정 및 생성한 Window 반환
window = glfw.create_window(400, 400, "OpenGL Tutorial", None, None)

if not window:
    print("create window failed")
    glfw.terminate()
    exit()

# window라는 이름의 Window를 현재 스레드의 주 context로 지정
glfw.make_context_current(window)

vertex_shader_source = """
#version 430 core
in vec3 position;

void main()
{
    gl_Position = vec4(position, 1.0);
}
"""

tess_evaluation_shader_source = """
#version 430 core
layout(triangles) in;

void main()
{
    gl_Position = (gl_TessCoord.x * gl_in[0].gl_Position) +
                  (gl_TessCoord.y * gl_in[1].gl_Position) +
                  (gl_TessCoord.z * gl_in[2].gl_Position);
}
"""

geometry_shader_source = """
#version 430 core
layout(triangles) in;
layout(points, max_vertices=3) out;

void main()
{
    int i;
    
    for (i=0; i<gl_in.length(); i++)
    {
        gl_Position = gl_in[i].gl_Position;
        EmitVertex();
    }
}
"""

fragment_shader_source = """
#version 430 core

out vec4 fragColor;
void main()
{
    fragColor = vec4(1.0);
}
"""

vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
tess_evaluation_shader = shaders.compileShader(tess_evaluation_shader_source, GL_TESS_EVALUATION_SHADER)
geometry_shader = shaders.compileShader(geometry_shader_source, GL_GEOMETRY_SHADER)
fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
shader = shaders.compileProgram(vertex_shader, tess_evaluation_shader, geometry_shader, fragment_shader)

# -1에서 1사이의 랜덤한 정점 좌표 생성
vertices = np.random.uniform(-1.0, 1.0, (3, 3)).astype(np.float32)

# VBO 생성
vbo = glGenBuffers(1)

# enable vertex attributes
position_location = glGetAttribLocation(shader, "position")
glVertexAttribPointer(position_location, 3, GL_FLOAT, GL_FALSE, 0, vertices)
glEnableVertexAttribArray(position_location)

glUseProgram(shader)
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
glPatchParameteri(GL_PATCH_VERTICES, 3)

# 렌더링 루프
while not glfw.window_should_close(window):
    # 화면 지우기
    glClear(GL_COLOR_BUFFER_BIT)

    glPatchParameterfv(GL_PATCH_DEFAULT_OUTER_LEVEL, [4.0, 1.0, 6.0])
    glPatchParameterfv(GL_PATCH_DEFAULT_INNER_LEVEL, [5.0])
    glDrawArrays(GL_PATCHES, 0, len(vertices))

    # 버퍼 스왑 및 이벤트 처리
    glfw.swap_buffers(window)
    glfw.poll_events()

# 자원 해제
glDeleteBuffers(1, [vbo])
glfw.terminate()
