# Computer Graphics Final Project: Ela Gulsen

## Implemented Features
 * partial Gouraud shading
 * light command - can be used multiple times
 * vary to move lights
 * mesh command

## Usage of new features
 * vary: vary NAME STARTING_FRAME ENDING_FRAME LOCATION_OF_X LOCATION_OF_Y LOCATION_OF_Z R_VALUE G_VALUE B_VALUE
  - ex. vary sun 0 49 0 1 0 150 150 150
 * light: light LOCATION_OF_X LOCATION_OF_Y LOCATION_OF_Z R_VALUE G_VALUE B_VALUE
 * mesh: mesh OPTIONAL_CONSTANT :FILE_STEM 
 * gouraud shading: shading gouraud
  - note: the form of gouraud shading I implemented is a gradient by scanline, not by individual pixel in the scanline.
  - gouraud shading was not used in my image example (wavy_fruit_bowl.mdl) because of added time cost and for aesthetic purposes
