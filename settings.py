import pygame as pg

class Values:
    WIND_SIZE = (800, 600)
    clock = pg.time.Clock()
    delta_time = clock.tick(60) * 0.001