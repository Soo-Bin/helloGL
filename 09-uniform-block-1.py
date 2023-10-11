import glfw
import OpenGL.GL.shaders as shaders
import ctypes as c
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
layout(std140) uniform TransformBlock
{
    float scale;
    vec3 translation;
    float rotation[3];
    mat4 projection_matrix;
} transform;

void main()
{
}
"""

fragment_shader_source = """
"""

vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
shader = shaders.compileProgram(vertex_shader, fragment_shader)

# Query the number of active Uniforms:
uniform_block_index = glGetUniformBlockIndex(shader, "TransformBlock")

num_active = GLint()
indices = (GLuint * num_active.value)()
indices_ptr = c.cast(c.addressof(indices), c.POINTER(GLint))
glGetActiveUniformBlockiv(shader, uniform_block_index, GL_UNIFORM_BLOCK_ACTIVE_UNIFORMS, num_active)
glGetActiveUniformBlockiv(shader, uniform_block_index, GL_UNIFORM_BLOCK_ACTIVE_UNIFORM_INDICES, indices_ptr)

# Create objects and pointers for query values:
offsets = (GLint * num_active.value)()
gl_types = (GLuint * num_active.value)()
offsets_ptr = c.cast(c.addressof(offsets), c.POINTER(GLint))
gl_types_ptr = c.cast(c.addressof(gl_types), c.POINTER(GLint))

# Query the indices, offsets, and types uniforms:
glGetActiveUniformsiv(shader, num_active.value, indices, GL_UNIFORM_OFFSET, offsets_ptr)
glGetActiveUniformsiv(shader, num_active.value, indices, GL_UNIFORM_TYPE, gl_types_ptr)

# 두 배열을 합침
combined = list(zip(offsets, gl_types))

# 특정 키를 기준으로 정렬
sorted_combined = sorted(combined, key=lambda x: x[0])  # 첫 번째 요소를 기준으로 정렬

print(sorted_combined)

# 렌더링 루프
while not glfw.window_should_close(window):
    # 화면 지우기
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader)

    # 버퍼 스왑 및 이벤트 처리
    glfw.swap_buffers(window)
    glfw.poll_events()

# 자원 해제
glfw.terminate()
