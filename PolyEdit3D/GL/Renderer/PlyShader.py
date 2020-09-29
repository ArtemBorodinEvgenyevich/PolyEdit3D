from OpenGL import GL as gl
from OpenGL.GL.shaders import compileShader, compileProgram


class PlyShader:
    def __init__(self, *filepaths: str):
        self.__mRendererID = self.__compile(filepaths)

    def bind(self):
        gl.glUseProgram(self.__mRendererID)

    def unbind(self):
        gl.glUseProgram(0)

    def setUniformMatrix4fv(self, name: str, *values: float, normalize: bool=gl.GL_FALSE):
        gl.glUniformMatrix4fv(self.__getUniformLocation(name), 1, normalize, *values)

    def deleteShader(self):
        gl.glDeleteProgram(self.__mRendererID)

    # TODO: Determine Uniform value due to its type
    #def setValue(self):
    #    pass

    def __getUniformLocation(self, name: str):
        location = gl.glGetUniformLocation(self.__mRendererID, name)
        if location == -1:
            raise RuntimeWarning(f"Uniform {name} does not exist!")
        return location

    # FIXME: Hardcode shader type checks
    def __compile(self, filepaths):
        for path in filepaths:
            with open(path, "r") as source:
                shader_type = source.readline().strip()
                if "//fragment" == shader_type:
                    fragment = compileShader(source.read(), gl.GL_FRAGMENT_SHADER)
                if "//vertex" == shader_type:
                    vertex = compileShader(source.read(), gl.GL_VERTEX_SHADER)
        return compileProgram(fragment, vertex)
