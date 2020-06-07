import itertools
import math
import random
import cgp
import numpy as np


class ImageGenerator():
    # must be a 255x255 image for now
    IMAGE_WIDTH = 255 
    IMAGE_HEIGHT = 255

    def __init__(self, population_size, mutation_prob):
        super(ImageGenerator, self).__init__()
        self.population_size = population_size
        self.generation = 0
        self.mutation_prob = mutation_prob
        self.population = []
        self.selected_features = []

    def _generate_images(self, population_size):
        self.population = cgp.create_population(population_size)
        
    def initial_population(self):
        self.generation += 1
        self._generate_images(self.population_size)



    '''
    the following need rework
    Decision tree??
    '''
    '''
    question:
    what is the feature of a photo?
    '''
 
    def next_generation(self, selected_character):
        # select the chosen character
        parents = [a for a, b in zip(self.population, selected_character) if b == 1]
        offspring = []
        if parents:
            for _ in range(self.population_size):
                parenta = random.choice(parents)
                parentb = random.choice(parents)
                child = parenta.cross_over(parentb)
                offspring.append(child.mutate(self.mutation_prob))
            self.population = offspring
        else:
            self._generate_images(self.population_size)
        self.generation += 1



###############################################################

    # decode procedure
    def decode_pop(self, pop_test):

        pixels = np.zeros((self.IMAGE_WIDTH, self.IMAGE_HEIGHT, 3), dtype=np.uint8)
        for y in range(self.IMAGE_WIDTH):
            for x in range(self.IMAGE_HEIGHT):
                r, g, b = pop_test.eval(x, y)
                pixels[x][y] = [r, g, b]
        return pixels
        
            # Image.fromarray(pixels, mode='RGB').show()
