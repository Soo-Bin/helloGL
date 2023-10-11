import glfw
import OpenGL.GL.shaders as shaders
import numpy as np
from OpenGL.GL import *
from PIL import Image

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
layout(location=0) in vec2 position;
layout(location=1) in vec2 in_texcoord;

out vec2 texcoord;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    texcoord = in_texcoord;
}
"""

fragment_shader_source = """
#version 430 core
in vec2 texcoord;

uniform sampler2D tex;

out vec4 fragColor;
void main()
{
    fragColor = texture(tex, texcoord);
}
"""

vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
shader = shaders.compileProgram(vertex_shader, fragment_shader)

# 정점 데이터와 텍스처 좌표 데이터
vertices = np.array([
    0.0, 0.5,  # 정상
    -0.5, -0.5,  # 왼쪽 아래
    0.5, -0.5  # 오른쪽 아래
], dtype=np.float32)

tex = np.array([
    0.5, 1.0,  # 정상
    0.0, 0.0,  # 왼쪽 아래
    1.0, 0.0  # 오른쪽 아래
], dtype=np.float32)

# VBO 생성
vbo_position = glGenBuffers(1)
vbo_tex = glGenBuffers(1)

glBindBuffer(GL_ARRAY_BUFFER, vbo_position)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

glBindBuffer(GL_ARRAY_BUFFER, vbo_tex)
glBufferData(GL_ARRAY_BUFFER, tex.nbytes, tex, GL_STATIC_DRAW)

# enable vertex attributes
glBindBuffer(GL_ARRAY_BUFFER, vbo_position)
position_location = glGetAttribLocation(shader, "position")
glVertexAttribPointer(position_location, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
glEnableVertexAttribArray(position_location)

glBindBuffer(GL_ARRAY_BUFFER, vbo_tex)
color_location = glGetAttribLocation(shader, "in_texcoord")
glVertexAttribPointer(color_location, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
glEnableVertexAttribArray(color_location)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

""" 텍스처 입히기 """
image = Image.open("brick-block.jpg")
width, height = image.size
image = image.tobytes('raw', 'RGBA', 0, -1)

texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

# 렌더링 루프
while not glfw.window_should_close(window):
    # 화면 지우기
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture)
    glUniform1i(glGetUniformLocation(shader, "tex"), 0)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    # 버퍼 스왑 및 이벤트 처리
    glfw.swap_buffers(window)
    glfw.poll_events()

# 자원 해제
glDeleteBuffers(1, [vbo_position])
glDeleteBuffers(1, [vbo_tex])
glfw.terminate()
