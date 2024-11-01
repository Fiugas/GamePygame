import struct, pygame, moderngl, os

class Shader:
    def __init__(self, game):
        self.game = game
        self.load_shaders()
        self.ctx = moderngl.create_context()
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
            vertex_shader = open(self.vertex_shader_path).read(),
            fragment_shader = open(self.fragment_shader_path).read()
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
        self.program['ScreenResolution'] = game.GAME_LOGIC_SIZE

    def render(self):
        self.ctx.viewport = (0, 0, *self.game.SCREEN_SIZE)
        self.texture_data = self.game.game_canvas.get_view('1')
        self.screen_texture.write(self.texture_data)
        self.ctx.clear(14/255,40/255,66/255)
        self.screen_texture.use()
        self.vao.render()

    def load_shaders(self):
        self.shader_dir = os.path.join('shaders')
        self.vertex_shader_path = os.path.join(self.shader_dir, 'vertex_shader.glsl')
        self.fragment_shader_path = os.path.join(self.shader_dir, 'fragment_shader.glsl')