from core.position import Position
import pygame

class Entity:
    def __init__(self, position: Position):
        self.position = position
        self.children = []

    def move(self, dx: int, dy: int):
        self.position.x += dx
        self.position.y += dy

    def add_child(self, child_entity):
        if child_entity not in self.children:
            self.children.append(child_entity)

    def remove_child(self, child_entity):
        if child_entity in self.children:
            self.children.remove(child_entity)

    def set_position(self, new_position: Position):
        dx = new_position.x - self.position.x
        dy = new_position.y - self.position.y
        self.move(dx, dy)
