import glfw
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

# Window가 종료되지 않을 때까지 루프
while not glfw.window_should_close(window):
    # 이벤트 메시지를 처리
    glfw.poll_events()

    # 지울 버퍼를 나타내는 마스크의 비트 OR 연산자
    glClear(GL_COLOR_BUFFER_BIT)

    # back Buffer와 front Buffer를 Swap (Double Buffer)
    glfw.swap_buffers(window)

# 사용된 메모리를 삭제
glfw.terminate()
