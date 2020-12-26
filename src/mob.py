from entity import Entity


class HostileMob(Entity):
    def __init__(self, scene, core):
        super().__init__(scene, core)
        self.player = self.scene.player
        self.speed = 17

    def update(self):
        if self.position.x < self.player.position.x:
            self.velocity.x += self.speed * self.speed_factor
            self.on_wall = False
            if self.on_ground:
                tile = self.scene.map.get_tile(int((self.position.x+self.hitbox.width+(self.scene.tile_width/2))//self.scene.tile_width),
                                               int((self.position.y-self.scene.tile_height/2)//self.scene.tile_height)+1)

                if self.scene.is_block(tile):
                    self.velocity.y = -self.jump_height * self.jump_factor
                    self.on_ground = False

        else:
            self.velocity.x -= self.speed * self.speed_factor
            self.on_wall = False
            if self.on_ground:
                tile = self.scene.map.get_tile(int((self.position.x - (self.scene.tile_width/2))//self.scene.tile_width),
                                               int((self.position.y-self.scene.tile_height/2)//self.scene.tile_height)+1)

                if self.scene.is_block(tile):
                    self.velocity.y = -self.jump_height * self.jump_factor
                    self.on_ground = False

        self.apply_physics()
