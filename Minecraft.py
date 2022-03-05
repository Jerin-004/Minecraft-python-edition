import pickle
from numpy import *
from numpy import floor
from perlin_noise import PerlinNoise
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina(vsync=False)
player = FirstPersonController()

Entity.default_shader = lit_with_shadows_shader
grass_texture = load_texture('assets/grass_block_1.png')
stone_texture = load_texture('assets/stone_block_1.png')
oak_wood_texture = load_texture('assets/oak_log_block_1')
oak_plank_texture = load_texture("assets/oak_plank.png")
dirt_texture = load_texture('assets/dirt_block_1.png')
sky_texture = load_texture('assets/skybox_2.png')
arm_texture = load_texture('assets/arm_texture_1.png')
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)
Minecraft_music = Audio("assets/Minecraft_music", loop=True, autoplay=False, auto_destroy=False)
block_pick = 5

window.title = 'Minecraft python edition'
window.fps_counter.enabled = True
window.exit_button.visible = False
window.fullscreen = True
window.color = color.black

# # Our main character.
# player = FirstPersonController()
# player.cursor.visible = True
# player.gravity = 0.5
# # grav_speed = 0
# # grav_acc = 0.1
# player.x = player.z = 5
# # player.y = 32
# prevZ = player.z
# prevX = player.x
# origin = player.position # Vec3 object? .x .y .z
global voxpos
newlist = []
blocktyp = {}
blocktext = ""
voxpos = []
newdict = {}
rmlist = []

Minecraft_music.play()


def save():
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('terrain_map_1.panda', 'wb') as f:
        # newlist.remove(rmlist)
        # print(newlist)
        # Write game state objects to file.
        pickle.dump(newlist, f)
        # Clear out temporary lists.
        newlist.clear()


def load():
    # global voxpos, newdict
    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    with open('terrain_map_1.panda', 'rb') as f:
        newlist.extend(pickle.load(f))
        print(newlist)
        # # voxpos = list(nd)
        # # voxpos = dict(voxpos)
        # lenOfVoxel = len(voxpos)
        # print(lenOfVoxel)
        #

        for i in newlist:
            newdict.update(i)
            #
            # print(newdict.items())
            #
            # # lenOfnewDict = len(newdict)
        for k, v in newdict.items():
            Voxel(position=k, texture=v)
            # voxel.position(eval(vox))

            # for i in nd:
            #     voxpos = dict(copy(i))
            #
            # print(voxpos)
            # val = list(voxpos.keys())
            # print(val)
            # for i in val:
            #     print(i)
            #     voxel.position = i
            # voxel.combine()

            # print(int(Vec3))


class Voxel(Button):
    global voxel

    def __init__(self, position=(), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5)

    def input(self, key):
        global voxel

        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                if block_pick == 1:
                    voxel = Voxel(position=self.position + mouse.normal, texture=grass_texture)
                    blocktext = texture = grass_texture
                    blocktyp = {voxel.position: blocktext}
                    newlist.append(blocktyp)

                if block_pick == 2:
                    voxel = Voxel(position=self.position + mouse.normal, texture=stone_texture)
                    blocktext = texture = stone_texture
                    blocktyp = {voxel.position: blocktext}
                    newlist.append(blocktyp)

                if block_pick == 3:
                    voxel = Voxel(position=self.position + mouse.normal, texture=oak_wood_texture)
                    blocktext = texture = oak_wood_texture
                    blocktyp = {voxel.position: blocktext}
                    newlist.append(blocktyp)

                if block_pick == 4:
                    voxel = Voxel(position=self.position + mouse.normal, texture=dirt_texture)
                    blocktext = texture = dirt_texture
                    blocktyp = {voxel.position: blocktext}
                    newlist.append(blocktyp)

                if block_pick == 5:
                    voxel = Voxel(position=self.position + mouse.normal, texture=oak_plank_texture)
                    blocktext = texture = oak_plank_texture
                    blocktyp = {voxel.position: blocktext}
                    newlist.append(blocktyp)

            if key == 'left mouse down':
                punch_sound.play()
                # voxel = Voxel(position=self.position)
                destroy(self)
                # rmlist.append(voxel.position)

            if key == 'q' or key == 'escape':
                quit()

            if key == 'p':
                # Create a new entity that combines all our
                # subsets and megasets, which we can
                # place onto a file.

                # First, let's open/create a file in the
                # folder we are working in (working directory)
                # that we can save to.
                save()

            if key == 'l':
                # Open main module directory for correct file.
                load()


load()
voxel = Voxel()


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True)


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6))

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)


# load()

def greenTer():
    noise = PerlinNoise(octaves=2, seed=1001)
    freq = 24
    amp = 5
    terrain_width = 50

    for i in range(terrain_width * terrain_width):
        x = floor((i / terrain_width) + player.x - 0.5 * terrain_width)
        z = floor((i % terrain_width) + player.x - 0.5 * terrain_width)
        y = floor(noise([x / freq, z / freq]) * amp)
        voxel = Voxel(position=(x, y, z))

    # for i in range(terrain_width*terrain_width):
    #     x =  floor(i/terrain_width)
    #     z = floor(i%terrain_width)
    #     y =  floor(noise([x/freq, z/freq]) * amp)
    #     voxel = Voxel(position=(x, y, z))


greenTer()


# load()
def update():
    global block_pick  ## Cheats
    global voxpos
    if held_keys['u' or 'U']:
        player.y += 0.1

    elif held_keys['j' or 'J']:
        player.y -= 0.1

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()

    else:
        hand.passive()

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5


# player = FirstPersonController()
player.gravity = 0.5
player.x = player.z = 5
player.y = 12

sky = Sky()
hand = Hand()

app.run()
