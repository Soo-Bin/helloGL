import glfw
import OpenGL.GL.shaders as shaders
import math

import glm
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

uniform mat4 mat_mv;
uniform mat4 mat_proj;

out vec4 newColor;
void main()
{
    gl_Position = mat_proj * mat_mv * vec4(position, 1.0);
    newColor = vec4(color, 1.0);
}
"""

fragment_shader_source = """
#version 430 core
in vec4 newColor;

out vec4 fragColor;
void main()
{
    fragColor = newColor;
}
"""

vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
shader = shaders.compileProgram(vertex_shader, fragment_shader)

vertices = np.array([
    -0.125, -0.125, -0.125,
    0.125, -0.125, -0.125,
    0.125, 0.125, -0.125,
    -0.125, 0.125, -0.125,
    -0.125, -0.125, 0.125,
    0.125, -0.125, 0.125,
    0.125, 0.125, 0.125,
    -0.125, 0.125, 0.125
], dtype=np.float32)

# 3개씩 자르기
vertices = vertices.reshape(-1, 3)

colors = np.array([
    0.0, 1.0, 1.0,
    1.0, 0.0, 0.0,
    1.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 0.0, 1.0,
    1.0, 0.0, 1.0,
    1.0, 1.0, 1.0,
    0.0, 1.0, 1.0,
], dtype=np.float32)

# 3개씩 자르기
colors = colors.reshape(-1, 3)

indices = np.array([
    0, 1, 3, 3, 1, 2,
    0, 1, 4, 4, 5, 1,
    1, 2, 5, 5, 6, 2,
    2, 3, 6, 6, 7, 3,
    3, 7, 4, 4, 3, 0,
    4, 5, 7, 7, 6, 5,
], dtype=np.uint32)

# 3개씩 자르기
indices = indices.reshape(-1, 3)

# VAO 생성
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# VBO 생성 및 데이터 업로드
vbo_position = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_position)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# enable vertex attributes
glBindBuffer(GL_ARRAY_BUFFER, vbo_position)
position_location = glGetAttribLocation(shader, "position")
glVertexAttribPointer(position_location, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
glEnableVertexAttribArray(position_location)

vbo_color = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo_color)
glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)

glBindBuffer(GL_ARRAY_BUFFER, vbo_color)
color_location = glGetAttribLocation(shader, "color")
glVertexAttribPointer(color_location, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
glEnableVertexAttribArray(color_location)

ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

# 렌더링 루프
while not glfw.window_should_close(window):
    # 화면 지우기
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glUseProgram(shader)

    mat_proj = glm.perspective(50.0, 1.0, 0.1, 1000.0)

    for i in range(6):
        f = i + glfw.get_time() * math.pi * 0.1
        mat_mv = glm.translate(glm.vec3(0.0, 0.0, -4.0)) * \
                 glm.translate(glm.vec3(math.sin(2.1 * f) * 0.5, math.cos(1.7 * f) * 0.5,
                                        math.sin(1.3 * f) * math.cos(1.5 * f) * 2.0)) * \
                 glm.rotate(glfw.get_time(), glm.vec3(0.0, 1.0, 0.0)) * \
                 glm.rotate(glfw.get_time(), glm.vec3(1.0, 0.0, 0.0))

        # VBO 활성화 및 vertex 데이터 설정
        mv_location = glGetUniformLocation(shader, "mat_mv")
        glUniformMatrix4fv(mv_location, 1, GL_FALSE, glm.value_ptr(mat_mv))

        proj_location = glGetUniformLocation(shader, "mat_proj")
        glUniformMatrix4fv(proj_location, 1, GL_FALSE, glm.value_ptr(mat_proj))

        glBindVertexArray(vao)
        glDrawElements(GL_TRIANGLES, indices.size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)

    # 버퍼 스왑 및 이벤트 처리
    glfw.swap_buffers(window)
    glfw.poll_events()

# 자원 해제
glDeleteBuffers(1, [vbo_position])
glDeleteBuffers(1, [vbo_color])
glDeleteBuffers(1, [ebo])
glfw.terminate()
