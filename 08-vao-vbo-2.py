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
layout(location=0) in vec3 position;
layout(location=1) in vec3 color;

out vec3 newColor;
void main()
{
    gl_Position = vec4(position, 1.0);
    newColor = color;
}
"""

fragment_shader_source = """
#version 430 core
in vec3 newColor;

out vec4 fragColor;
void main()
{
    fragColor = vec4(newColor, 1.0);
}
"""

vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
shader = shaders.compileProgram(vertex_shader, fragment_shader)

# -1에서 1사이의 랜덤한 정점 좌표 생성
vertices = np.random.uniform(-1.0, 1.0, (6, 3)).astype(np.float32)
# 0에서 1사이의 랜덤한 색상 생성
colors = np.random.uniform(0.0, 1.0, (6, 3)).astype(np.float32)

# 두 배열을 하나의 배열로 합침
interleaved_data = np.concatenate((vertices, colors))

# VBO 생성
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, interleaved_data.nbytes, interleaved_data, GL_STATIC_DRAW)

# enable vertex attributes
position_location = glGetAttribLocation(shader, "position")
glVertexAttribPointer(position_location, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
glEnableVertexAttribArray(position_location)

color_location = glGetAttribLocation(shader, "color")
glVertexAttribPointer(color_location, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(3 * 4))
glEnableVertexAttribArray(color_location)

# 렌더링 루프
while not glfw.window_should_close(window):
    # 화면 지우기
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader)
    glDrawArrays(GL_TRIANGLES, 0, len(vertices))

    # 버퍼 스왑 및 이벤트 처리
    glfw.swap_buffers(window)
    glfw.poll_events()

# 자원 해제
glDeleteBuffers(1, [vbo])
glfw.terminate()
