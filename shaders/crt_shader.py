import struct
import pygame
import moderngl
import os

class Shader:
    def __init__(self, game):
        self.game = game
        self.ctx = moderngl.create_context()
        self.load_shaders()
        self.texture_coords = [
            0, 1,  1, 1,
            0, 0,  1, 0
        ]
        self.world_coords = [
            -1, -1,  1, -1,
            -1,  1,  1,  1
        ]
        self.render_indices = [
            0, 1, 2,
            1, 2, 3
        ]
        self.program = self.ctx.program(
            vertex_shader=open(self.vertex_shader_path).read(),
            fragment_shader=open(self.fragment_shader_path).read()
        )
        self.screen_texture = self.ctx.texture(
            game.GAME_LOGIC_SIZE, 3,
            pygame.image.tostring(game.game_canvas, "RGB", 1)
        )
        self.vbo = self.ctx.buffer(struct.pack('8f', *self.world_coords))
        self.uvmap = self.ctx.buffer(struct.pack('8f', *self.texture_coords))
        self.ibo = self.ctx.buffer(struct.pack('6i', *self.render_indices))
        self.vao_content = [
            (self.vbo, '2f', 'vert'),
            (self.uvmap, '2f', 'in_text')
        ]
        self.vao = self.ctx.vertex_array(self.program, self.vao_content, self.ibo)

    def load_shaders(self):
        base_path = os.path.dirname(__file__)
        self.vertex_shader_path = os.path.join(base_path, 'vertex_shader.glsl')
        self.fragment_shader_path = os.path.join(base_path, 'fragment_shader.glsl')

    def update_texture(self):
        self.screen_texture.write(pygame.image.tostring(self.game.game_canvas, "RGB", 1))

    def render(self):
        self.update_texture()
        self.screen_texture.use()
        self.vao.render()

    def release(self):
        self.vbo.release()
        self.uvmap.release()
        self.ibo.release()
        self.screen_texture.release()
        self.program.release()
        self.vao.release()